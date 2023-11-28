# WASM-LLM

## Install `WasmEdge`

```bash
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- --plugins wasi_nn-ggml
```

## Build `wasm-chat`

Before building `wasm-chat`, make sure that `maturin` is installed in your environment. If not, install it with the following command:

```bash
pip install maturin
```

Then, build `wasm-chat` for release with the following command:

```bash
cd wasm-chat
maturin build -r
```

If you want to build `wasm-chat` for test, use the following command:

```bash
maturin develop
```

## Build `wasm-llm`

```bash
cd ../wasm-llm
cargo build --release --target wasm32-wasi
```

## Download GGUF model

```bash
cd ../wasm-chat

# TinyLlama-1.1B-Chat-v0.3
curl -LO https://huggingface.co/second-state/TinyLlama-1.1B-Chat-v0.3-GGUF/resolve/main/tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf
```

## Test

```bash
cd wasm-chat

python test.py
```
