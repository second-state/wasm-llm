use once_cell::sync::OnceCell;
use serde::{Deserialize, Serialize};
use std::sync::Mutex;
use wasi_nn::{Error as WasiNnError, Graph, GraphExecutionContext, TensorType};
#[allow(unused_imports)]
use wasmedge_bindgen::*;
use wasmedge_bindgen_macro::*;

static GRAPH: OnceCell<Mutex<MyGraph>> = OnceCell::new();

const DEFAULT_CTX_SIZE: usize = 4096;

#[derive(Debug)]
struct MyGraph {
    _graph: Graph,
    context: GraphExecutionContext,
}
impl MyGraph {
    pub fn new(model_alias: impl AsRef<str>, options: &Metadata) -> Self {
        let graph = wasi_nn::GraphBuilder::new(
            wasi_nn::GraphEncoding::Ggml,
            wasi_nn::ExecutionTarget::AUTO,
        )
        .build_from_cache(model_alias.as_ref())
        .unwrap();

        let mut context = graph.init_execution_context().unwrap();

        let buffer = serde_json::to_vec(options).unwrap();
        context
            .set_input(1, wasi_nn::TensorType::U8, &[1], buffer)
            .unwrap();

        Self {
            _graph: graph,
            context,
        }
    }

    pub fn set_input<T: Sized>(
        &mut self,
        index: usize,
        tensor_type: TensorType,
        dimensions: &[usize],
        data: impl AsRef<[T]>,
    ) -> Result<(), WasiNnError> {
        self.context.set_input(index, tensor_type, dimensions, data)
    }

    pub fn compute(&mut self) -> Result<(), WasiNnError> {
        self.context.compute()
    }

    pub fn get_output<T: Sized>(
        &self,
        index: usize,
        out_buffer: &mut [T],
    ) -> Result<usize, WasiNnError> {
        self.context.get_output(index, out_buffer)
    }
}

#[wasmedge_bindgen]
pub fn init(model_alias: String, options: String) {
    let options: Metadata = serde_json::from_str(&options).unwrap();

    if GRAPH.get().is_none() {
        GRAPH
            .set(Mutex::new(MyGraph::new(&model_alias, &options)))
            .unwrap();
    }
}

#[wasmedge_bindgen]
pub fn infer(prompt: String) -> String {
    let graph = &mut GRAPH.get().unwrap().lock().unwrap();

    let tensor_data = prompt.as_bytes().to_vec();
    graph
        .set_input(0, TensorType::U8, &[1], &tensor_data)
        .unwrap();

    // execute the inference
    graph.compute().unwrap();

    // Retrieve the output.
    let mut output_buffer = vec![0u8; DEFAULT_CTX_SIZE * 6];
    let mut output_size = graph.get_output(0, &mut output_buffer).unwrap();

    String::from_utf8_lossy(&output_buffer[..output_size]).to_string()
}

#[derive(Debug, Default, Deserialize, Serialize)]
struct Metadata {
    #[serde(rename = "enable-log")]
    log_enable: bool,
    #[serde(rename = "ctx-size")]
    ctx_size: u64,
    #[serde(rename = "n-predict")]
    n_predict: u64,
    #[serde(rename = "n-gpu-layers")]
    n_gpu_layers: u64,
    #[serde(rename = "batch-size")]
    batch_size: u64,
    #[serde(skip_serializing_if = "Option::is_none", rename = "reverse-prompt")]
    reverse_prompt: Option<String>,
}
