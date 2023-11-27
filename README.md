# WASM-LLM

## Build `wasm-chat`

Before building `wasm-chat`, make sure that `maturin` is installed in your environment. If not, install it with the following command:

```bash
pip install maturin
```

Then, build `wasm-chat` with the following command:

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
python test.py --model_file tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf --wasm_file ../wasm-llm/target/wasm32-wasi/release/inference.wasm
```
