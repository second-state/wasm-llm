import os

import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import datetime
import time
import random

import sys

sys.path.append("/Volumes/Dev/secondstate/me/langchain/libs/langchain")

from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

# from langchain import OpenAI
from streamlit_option_menu import option_menu
from conversations import conversations

st.set_page_config(layout="wide", page_title="Wasm Chat")

default_title = "New Conversation"


def chat_history(user, message):
    with st.chat_message(user):
        st.markdown(message)


if "conversations" not in st.session_state:
    st.session_state.conversations = conversations
conversations = st.session_state.conversations

#  当前选择的对话
if "index" not in st.session_state:
    st.session_state.index = 0

AVAILABLE_MODELS = {
    "TinyLlama-1.1B-Chat": {
        "model_file": "/Volumes/Store/models/gguf/tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf",
        "prompt_template": PromptTemplateType.ChatML,
    },
    "MistralLite-7B": {
        "model_file": "/Volumes/Store/models/gguf/mistrallite.Q5_K_M.gguf",
        "prompt_template": PromptTemplateType.MistralLite,
    },
    "Llama-2-13B-Chat": {
        "model_file": "/Volumes/Store/models/gguf/llama-2-13b-chat.Q5_K_M.gguf",
        "prompt_template": PromptTemplateType.Llama2Chat,
    },
    "CodeLlama-13B-Instruct": {
        "model_file": "/Volumes/Store/models/gguf/codellama-13b-instruct.Q4_0.gguf",
        "prompt_template": PromptTemplateType.CodeLlama,
    },
    "CodeLlama-13B-Instruct": {
        "model_file": "/Volumes/Store/models/gguf/deepseek-llm-7b-chat.Q5_K_M.gguf",
        "prompt_template": PromptTemplateType.CodeLlama,
    },
}

with st.sidebar:
    st.image("assets/log.png")
    st.subheader("", divider="grey")
    st.write("")
    model_name = st.selectbox("Pick your model", AVAILABLE_MODELS.keys(), index=0)
    print(f"[INFO] model_name: {model_name}")

    if st.button("New Conversation"):
        conversations.append({"title": default_title, "messages": []})
        st.session_state.index = len(conversations) - 1

if model_name is None:
    model_name = "TinyLlama-1.1B-Chat"
model = AVAILABLE_MODELS[model_name]
model_file = model["model_file"]
prompt_template = model["prompt_template"]

# * todo: support `reverse_prompt`
wasm_chat = ChatWasm(
    model_file=model_file,
    prompt_template=prompt_template,
)

st.session_state.messages = conversations[st.session_state.index]["messages"]

prompt = st.chat_input("Input your question")

if prompt:
    if conversations[st.session_state.index]["title"] == default_title:
        conversations[st.session_state.index]["title"] = prompt[:12]
    for user, message in st.session_state.messages:
        chat_history(user, message)

    chat_history("user", prompt)
    answer = wasm_chat.predict(prompt)

    st.session_state.messages.append(("user", prompt))
    st.session_state.messages.append(("assistant", answer))
    chat_history("assistant", answer)
