# WASM-LLM

## Deploy WasmEdge Runtime and `wasm-infer.wasm`

```bash
curl -sSf https://raw.githubusercontent.com/second-state/wasm-llm/main/deploy.sh | bash
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

Or, use the following command if you want to build `wasm-chat` for test:

```bash
cd wasm-chat
maturin develop
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
