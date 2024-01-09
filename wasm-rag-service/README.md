# Wasm-RAG

## Setup

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
