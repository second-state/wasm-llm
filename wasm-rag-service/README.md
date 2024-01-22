# Wasm-RAG

## Setup

### Prepare LlamaEdge API server

  The [run-llm.sh](https://github.com/second-state/LlamaEdge/raw/main/run-llm.sh) script provides an interactive way to deploy LlamaEdge API server. Run the following command and follow the prompts to download required assets and start up the LlamaEdge API server:

  ```console
  bash <(curl -sSfL 'https://code.flows.network/webhook/iwYN1SdN3AmPgR5ao5Gt/run-llm.sh')
  ```

  [>> Click to watch Youtube video of Deploying LlamaEdge API Server with run-llm script <<](https://www.youtube.com/watch?v=fu_sM4uSLsI)

### Git clone the repo

  ```console
  git clone https://github.com/second-state/wasm-llm
  cd wasm-bot
  ```

### Install Python packages

```bash
cd wasm-rag-service
pip install -r requirements.txt
```

### Install system dependencies

- Install the following system dependencies if they are not already available on your system. Depending on what document types you're parsing, you may not need all of these.

  - `libmagic-dev` (filetype detection)
  - `poppler-utils` (images and PDFs)
  - `tesseract-ocr` (images and PDFs, install tesseract-lang for additional language support)
  - `libreoffice` (MS Office docs)
  - `pandoc` (EPUBs, RTFs and Open Office docs)


- Install miniconda
  Refer to [Quick command line install](https://docs.conda.io/projects/miniconda/en/latest/#quick-command-line-install) to install miniconda on your local system.

- Create a conda environment

  ```bash
  # create a conda environment named wasm-rag
  conda create -n wasm-rag python=3.11

  # activate the conda environment
  conda activate wasm-rag
  ```

- Install dependencies

```bash
cd wasm-rag-service
pip install -r requirements.txt
```

- Execute wasm-rag app

  - Start the chatbot

    ```console
    streamlit run service.py
    ```

    If the chatbot is started successfully, you will see the following message:

    ```console
    You can now view your Streamlit app in your browser.

    Local URL: http://localhost:8501
    Network URL: http://192.168.0.103:8501
    ```
