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
    Ok(())
}

#[pyclass]
#[derive(Debug)]
pub struct WasmChat {
    dock: VmDock,
}
#[pymethods]
impl WasmChat {
    #[new]
    pub fn new(
        model_file: String,
        model_alias: String,
        wasm_file: String,
        dir_mapping: String,
    ) -> Result<Self, WasmChatError> {
        let wasm_file = Path::new(&wasm_file);

        // load wasinn-pytorch-plugin from the default plugin directory: /usr/local/lib/wasmedge
        PluginManager::load(None).map_err(|e| WasmChatError::Operation(e.to_string()))?;

        // preload named model
        PluginManager::nn_preload(vec![NNPreload::new(
            &model_alias,
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
        let module = Module::from_file(Some(&config), wasm_file)
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
                Some(vec![wasm_file.to_str().unwrap(), model_file.as_ref()]),
                Some(vec!["ENCODING=GGML", "TARGET=AUTO"]),
                Some(vec![dir_mapping.as_ref()]),
            );

        Ok(WasmChat {
            dock: VmDock::new(vm),
        })
    }

    pub fn init_inference_context(
        &self,
        model_alias: String,
        metadata: Metadata,
    ) -> Result<(), WasmChatError> {
        // create and init graph instance
        let param_alias = Param::String(&model_alias);

        let metadata_s = serde_json::to_string(&metadata).unwrap();
        let param_metadata = Param::String(&metadata_s);
        let init_params = vec![param_alias, param_metadata];

        if let Err(e) = self.dock.run_func("init", init_params) {
            return Err(WasmChatError::Operation(format!("init error: {e:?}")));
        }

        Ok(())
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
                let message = res.pop().unwrap().downcast::<String>().unwrap();
                return Ok(*message);
            }
            Err(e) => {
                println!("infer error: {:?}", e);
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
