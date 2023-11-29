use chat_prompts::chat::{BuildChatPrompt, ChatPrompt};
use endpoints::chat::ChatCompletionRequest;
use pyo3::{exceptions::PyValueError, prelude::*};
use serde::{Deserialize, Serialize};
use std::path::Path;
use thiserror::Error;
use wasmedge_sdk::{
    config::{CommonConfigOptions, ConfigBuilder, HostRegistrationConfigOptions},
    dock::{Param, VmDock},
    plugin::{ExecutionTarget, GraphEncoding, NNPreload, PluginManager},
    Module, VmBuilder,
};

/// A Python module implemented in Rust.
#[pymodule]
fn wasm_chat(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Metadata>()?;
    m.add_class::<WasmChat>()?;
    m.add_class::<PromptTemplateType>()?;
    Ok(())
}

#[pyclass]
#[derive(Debug)]
pub struct WasmChat {
    dock: VmDock,
    template_ty: PromptTemplateType,
}
#[pymethods]
impl WasmChat {
    #[new]
    #[pyo3(signature = (model_file, template_ty, wasm_file=None))]
    pub fn new(
        model_file: String,
        template_ty: PromptTemplateType,
        wasm_file: Option<String>,
    ) -> Result<Self, WasmChatError> {
        let wasm_file = match wasm_file {
            Some(wasm_file) => wasm_file,
            None => {
                if cfg!(target_os = "windows") {
                    "C:\\Program Files\\WasmEdge\\wasm\\wasm_infer.wasm".to_string()
                } else if cfg!(target_os = "macos") || cfg!(target_os = "linux") {
                    format!(
                        "{}/.wasmedge/wasm/wasm_infer.wasm",
                        std::env::var("HOME").unwrap()
                    )
                } else {
                    return Err(WasmChatError::Operation(
                        "Only macOS, Linux and Windows are supported.".to_string(),
                    ));
                }
            }
        };
        let path_wasm_file = Path::new(&wasm_file);

        // load wasinn-pytorch-plugin from the default plugin directory: /usr/local/lib/wasmedge
        PluginManager::load(None).map_err(|e| WasmChatError::Operation(e.to_string()))?;

        // preload named model
        PluginManager::nn_preload(vec![NNPreload::new(
            "default",
            GraphEncoding::GGML,
            ExecutionTarget::AUTO,
            &model_file,
        )]);

        let config = ConfigBuilder::new(CommonConfigOptions::default())
            .with_host_registration_config(HostRegistrationConfigOptions::default().wasi(true))
            .build()
            .map_err(|e| WasmChatError::Operation(e.to_string()))?;
        assert!(config.wasi_enabled());

        // load wasm module from file
        let module = Module::from_file(Some(&config), path_wasm_file)
            .map_err(|e| WasmChatError::Operation(e.to_string()))?;

        // create a Vm
        let mut vm = VmBuilder::new()
            .with_config(config)
            .with_plugin_wasi_nn()
            .build()
            .map_err(|e| WasmChatError::Operation(e.to_string()))?
            .register_module(None, module)
            .map_err(|e| WasmChatError::Operation(e.to_string()))?;

        // init wasi module
        vm.wasi_module_mut()
            .expect("Not found wasi module")
            .initialize(
                Some(vec![path_wasm_file.to_str().unwrap(), model_file.as_ref()]),
                Some(vec!["ENCODING=GGML", "TARGET=AUTO"]),
                None,
            );

        Ok(WasmChat {
            dock: VmDock::new(vm),
            template_ty,
        })
    }

    pub fn init_inference_context(&self, metadata: Metadata) -> Result<(), WasmChatError> {
        // create and init graph instance
        let param_alias = Param::String("default");

        let metadata_s = serde_json::to_string(&metadata).unwrap();
        let param_metadata = Param::String(&metadata_s);
        let init_params = vec![param_alias, param_metadata];

        if let Err(e) = self.dock.run_func("init", init_params) {
            return Err(WasmChatError::Operation(format!("init error: {e:?}")));
        }

        Ok(())
    }

    pub fn generate_prompt_str(&self, data: String) -> Result<String, WasmChatError> {
        let mut chat_request: ChatCompletionRequest =
            serde_json::from_str(&data).map_err(|e| WasmChatError::Operation(e.to_string()))?;

        let template = create_prompt_template(&self.template_ty);

        let prompt = template
            .build(&mut chat_request.messages)
            .map_err(|e| WasmChatError::Operation(e.to_string()))?;

        Ok(prompt)
    }

    pub fn infer(&self, prompt: String) -> Result<String, WasmChatError> {
        let param_prompt = Param::String(prompt.as_ref());
        let infer_params = vec![param_prompt];

        match self
            .dock
            .run_func("infer", infer_params)
            .map_err(|e| WasmChatError::Operation(e.to_string()))?
        {
            Ok(mut res) => {
                let output = res.pop().unwrap().downcast::<String>().unwrap();
                let message = post_process(*output, &self.template_ty);
                return Ok(message);
            }
            Err(e) => {
                return Err(WasmChatError::Operation(format!("infer error: {e:?}")));
            }
        }
    }
}

#[pyclass]
#[derive(Debug, Clone, Default, Deserialize, Serialize)]
pub struct Metadata {
    #[pyo3(get)]
    #[serde(rename = "enable-log")]
    log_enable: bool,
    #[pyo3(get)]
    #[serde(rename = "stream-stdout")]
    stream_stdout: bool,
    #[pyo3(get)]
    #[serde(rename = "ctx-size")]
    ctx_size: u64,
    #[pyo3(get)]
    #[serde(rename = "n-predict")]
    n_predict: u64,
    #[pyo3(get)]
    #[serde(rename = "n-gpu-layers")]
    n_gpu_layers: u64,
    #[pyo3(get)]
    #[serde(rename = "batch-size")]
    batch_size: u64,
    #[pyo3(get)]
    #[serde(skip_serializing_if = "Option::is_none", rename = "reverse-prompt")]
    reverse_prompt: Option<String>,
}
#[pymethods]
impl Metadata {
    #[new]
    #[pyo3(signature = (log_enable=false, stream_stdout=false, ctx_size=4096, n_predict=1024, n_gpu_layers=100, batch_size=4096, reverse_prompt=None))]
    fn new(
        log_enable: bool,
        stream_stdout: bool,
        ctx_size: u64,
        n_predict: u64,
        n_gpu_layers: u64,
        batch_size: u64,
        reverse_prompt: Option<String>,
    ) -> Self {
        Metadata {
            log_enable,
            stream_stdout,
            ctx_size,
            n_predict,
            n_gpu_layers,
            batch_size,
            reverse_prompt,
        }
    }
}

#[derive(Error, Clone, Debug, PartialEq, Eq)]
pub enum WasmChatError {
    // For general operation error
    #[error("{0}")]
    Operation(String),
}
impl From<WasmChatError> for PyErr {
    fn from(err: WasmChatError) -> PyErr {
        PyValueError::new_err(err.to_string())
    }
}

#[pyclass]
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum PromptTemplateType {
    Llama2Chat,
    MistralInstructV01,
    MistralLite,
    OpenChat,
    CodeLlama,
    BelleLlama2Chat,
    VicunaChat,
    ChatML,
    Baichuan2,
    WizardCoder,
    Zephyr,
    IntelNeural,
}

fn create_prompt_template(template_ty: &PromptTemplateType) -> ChatPrompt {
    match template_ty {
        PromptTemplateType::Llama2Chat => {
            ChatPrompt::Llama2ChatPrompt(chat_prompts::chat::llama::Llama2ChatPrompt::default())
        }
        PromptTemplateType::MistralInstructV01 => ChatPrompt::MistralInstructPrompt(
            chat_prompts::chat::mistral::MistralInstructPrompt::default(),
        ),
        PromptTemplateType::MistralLite => {
            ChatPrompt::MistralLitePrompt(chat_prompts::chat::mistral::MistralLitePrompt::default())
        }
        PromptTemplateType::OpenChat => {
            ChatPrompt::OpenChatPrompt(chat_prompts::chat::openchat::OpenChatPrompt::default())
        }
        PromptTemplateType::CodeLlama => ChatPrompt::CodeLlamaInstructPrompt(
            chat_prompts::chat::llama::CodeLlamaInstructPrompt::default(),
        ),
        PromptTemplateType::BelleLlama2Chat => ChatPrompt::BelleLlama2ChatPrompt(
            chat_prompts::chat::belle::BelleLlama2ChatPrompt::default(),
        ),
        PromptTemplateType::VicunaChat => {
            ChatPrompt::VicunaChatPrompt(chat_prompts::chat::vicuna::VicunaChatPrompt::default())
        }
        PromptTemplateType::ChatML => {
            ChatPrompt::ChatMLPrompt(chat_prompts::chat::chatml::ChatMLPrompt::default())
        }
        PromptTemplateType::Baichuan2 => ChatPrompt::Baichuan2ChatPrompt(
            chat_prompts::chat::baichuan::Baichuan2ChatPrompt::default(),
        ),
        PromptTemplateType::WizardCoder => {
            ChatPrompt::WizardCoderPrompt(chat_prompts::chat::wizard::WizardCoderPrompt::default())
        }
        PromptTemplateType::Zephyr => {
            ChatPrompt::ZephyrChatPrompt(chat_prompts::chat::zephyr::ZephyrChatPrompt::default())
        }
        PromptTemplateType::IntelNeural => {
            ChatPrompt::NeuralChatPrompt(chat_prompts::chat::intel::NeuralChatPrompt::default())
        }
    }
}

fn post_process(output: impl AsRef<str>, template_ty: &PromptTemplateType) -> String {
    if *template_ty == PromptTemplateType::Baichuan2 {
        output.as_ref().split('\n').collect::<Vec<_>>()[0]
            .trim()
            .to_owned()
    } else if *template_ty == PromptTemplateType::OpenChat {
        if output.as_ref().contains("<|end_of_turn|>") {
            output
                .as_ref()
                .trim_end_matches("<|end_of_turn|>")
                .trim()
                .to_owned()
        } else {
            output.as_ref().trim().to_owned()
        }
    } else if *template_ty == PromptTemplateType::ChatML {
        if output.as_ref().contains("<|im_end|>") {
            output.as_ref().replace("<|im_end|>", "").trim().to_owned()
        } else {
            output.as_ref().trim().to_owned()
        }
    } else if *template_ty == PromptTemplateType::Zephyr {
        if output.as_ref().contains("</s>") {
            output.as_ref().trim_end_matches("</s>").trim().to_owned()
        } else {
            output.as_ref().trim().to_owned()
        }
    } else {
        output.as_ref().trim().to_owned()
    }
}
