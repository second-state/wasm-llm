import os
import streamlit as st
import sys
import urllib.request
import time
import tempfile
from io import BytesIO

sys.path.append("/home/ubuntu/workspace/langchain/libs/langchain")

from langchain.chat_models.wasm_chat import ChatWasmLocal, PromptTemplateType
from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage
from langchain.document_loaders import (
    DirectoryLoader,
    UnstructuredFileLoader,
    PyPDFLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter


st.set_page_config(layout="wide", page_title="Wasm Chat")


def write_message(user, message):
    with st.chat_message(user):
        st.markdown(message)


def get_model_file(model_name):
    model_file = AVAILABLE_MODELS[model_name]["model_file"]
    if not os.path.exists("models"):
        os.makedirs("models")

    model_path = os.path.join("models", model_file)
    if not os.path.exists(model_path):
        model_url = AVAILABLE_MODELS[model_name]["url"]
        progress_text = f"Downloading {model_file} ..."
        my_bar = st.progress(0, text=progress_text)

        def download_progress(count, block_size, total_size):
            percent_complete = min(count * block_size / total_size, 1.0)
            my_bar.progress(percent_complete, text=progress_text)

        urllib.request.urlretrieve(model_url, model_path, reporthook=download_progress)

    return model_path


if "messages" not in st.session_state:
    st.session_state.messages = []


if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

AVAILABLE_MODELS = {
    "TinyLlama-1.1B-Chat": {
        "model_file": "tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf",
        "prompt_template": PromptTemplateType.ChatML,
        "url": "https://huggingface.co/second-state/TinyLlama-1.1B-Chat-v0.3-GGUF/resolve/main/tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf",
    },
    "Llama-2-13B-Chat": {
        "model_file": "llama-2-13b-chat.Q5_K_M.gguf",
        "prompt_template": PromptTemplateType.Llama2Chat,
        "url": "https://huggingface.co/second-state/Llama-2-13B-Chat-GGUF/resolve/main/llama-2-13b-chat.Q5_K_M.gguf",
    },
    "CodeLlama-13B-Instruct": {
        "model_file": "codellama-13b-instruct.Q4_0.gguf",
        "prompt_template": PromptTemplateType.CodeLlama,
        "url": "https://huggingface.co/second-state/CodeLlama-13B-Instruct-GGUF/resolve/main/codellama-13b-instruct.Q4_0.gguf",
    },
    "Baichuan2-13B-Chat(百川)": {
        "model_file": "Baichuan2-13B-Chat-ggml-model-q4_0.gguf",
        "prompt_template": PromptTemplateType.Baichuan2,
        "url": "https://huggingface.co/second-state/Baichuan2-13B-Chat-GGUF/resolve/main/Baichuan2-13B-Chat-ggml-model-q4_0.gguf",
        "reverse_prompt": "用户:",
    },
}

with st.sidebar:
    st.image("assets/log.png")
    st.subheader("", divider="grey")
    st.write("")
    model_name = st.selectbox("Pick your model", AVAILABLE_MODELS.keys(), index=0)

    if st.button("New Conversation"):
        model_file = get_model_file(model_name)
        prompt_template = AVAILABLE_MODELS[model_name]["prompt_template"]

        if (
            "model_name" not in st.session_state
            or st.session_state.model_name != model_name
        ):
            # clear chat history if the model is changed
            if (
                "model_name" in st.session_state
                and st.session_state.model_name != model_name
                and len(st.session_state.messages) > 0
            ):
                st.session_state.messages = []

            st.session_state.model_name = model_name

            # create ChatWasmLocal instance
            if "reverse_prompt" in AVAILABLE_MODELS[model_name]:
                reverse_prompt = AVAILABLE_MODELS[model_name]["reverse_prompt"]
                st.session_state.wasm_chat = ChatWasmLocal(
                    model_file=model_file,
                    prompt_template=prompt_template,
                    reverse_prompt=reverse_prompt,
                )
            else:
                st.session_state.wasm_chat = ChatWasmLocal(
                    model_file=model_file,
                    prompt_template=prompt_template,
                )

        st.session_state.start_chat = True

    dir_docs = st.text_input("Directory of documents", "./source_documents")
    if st.button("Load Documents"):
        print("[INFO] Creating knowledgebase ...")

if st.session_state.start_chat:
    st.title("💬 Wasmbot")
    st.caption("🚀 A chatbot powered by WasmEdge Runtime")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=("txt", "md", "pdf"),
    )
    if uploaded_file:
        print(f"uploaded_file name: {uploaded_file.name}")
        prefix, suffix = uploaded_file.name.split(".")
        print(f"prefix: {prefix}, suffix: {suffix}")
        bytes = uploaded_file.read()
        pdf_stream = BytesIO(bytes)

        temp = tempfile.NamedTemporaryFile(prefix=prefix + "-", suffix="." + suffix)
        print(f"temp.name: {temp.name}")
        temp.write(bytes)
        print("Created file is:", temp)
        print("Name of the file is:", temp.name)

        loader = UnstructuredFileLoader(temp.name)
        docs = loader.load()
        # print(docs)

        temp.close()

    write_message("assistant", "Hello 👋, how can I help you?")
    # display chat history
    if len(st.session_state.messages) > 0:
        for message in st.session_state.messages:
            if isinstance(message, AIMessage):
                write_message("assistant", message.content)
            elif isinstance(message, HumanMessage):
                write_message("user", message.content)
            elif isinstance(message, SystemMessage):
                write_message("system", message.content)
            else:
                raise ValueError(f"Unknown message type: {type(message)}")

    if prompt := st.chat_input("Input your question"):
        # Display user message in chat message container
        write_message("user", prompt)

        # Add user message to chat history
        user_message = HumanMessage(content=prompt)
        st.session_state.messages.append(user_message)

        with st.chat_message("assistant"):
            # invoke wasm_chat
            ai_message = st.session_state.wasm_chat(st.session_state.messages)

            st.markdown(ai_message.content)

            # Add assistant response to chat history
            st.session_state.messages.append(ai_message)
