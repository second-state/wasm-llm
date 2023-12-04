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

# For linux
maturin build -r --compatibility linux

# For mac
maturin build -r
```

If the command is executed successfully, you will get a `wasm_chat` wheel file in the `target/wheels` directory. Use `pip install <wheel file>` to install it.

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

## Chat with `wasm-bot`

- Install dependencies

  `wasm-bot` is a GUI based chat bot. To use it, install the following   dependencies:

  ```bash
  cd wasm-bot

  pip install -r requirements.txt
  ```

  **Notice that `wasm-bot` depends on LangChain with the `wasm-chat` integration.** This version of LangChain is not merged into the main branch yet. You can git clone the specific branch and import it into `wasm-bot` by path.

  ```bash
  git clone -b feat-integrate-wasm-chat --single-branch https://github.com/  apepkuss/langchain.git
  ```

- Run `wasm-bot`

  ```bash
  cd wasm-bot

  # use default port 8501
  streamlit run app.py

  # use custom port, for example, 8080
  streamlit run app.py --server.port 8080
  ```
