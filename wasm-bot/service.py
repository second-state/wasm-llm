import os
import sys
import time
import urllib.request

import streamlit as st

sys.path.append("/Volumes/Dev/secondstate/me/langchain/libs/langchain")

from langchain_community.chat_models.llama_edge import LlamaEdgeChatService
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

st.set_page_config(layout="wide", page_title="Wasm Chat")

# service_url = os.environ.get("DEFAULT_SERVICE_URL")
# service_url = "https://b008-54-186-154-209.ngrok-free.app"
service_url = "https://f370-50-112-58-64.ngrok-free.app"
if service_url is None:
    raise ValueError("The 'DEFAULT_SERVICE_URL' is not set.")

SERVICE_URL_DEFAULT = "Use default service"
SERVICE_URL_CUSTOM = "Use custom service"
REQUEST_TIMEOUT = 600


def write_message(user, message):
    with st.chat_message(user):
        st.markdown(message)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

with st.sidebar:
    st.image("assets/logo.svg")
    st.subheader("", divider="grey")
    st.write("")

    service_option = st.radio(
        "Select chat service:", [SERVICE_URL_DEFAULT, SERVICE_URL_CUSTOM]
    )

    if service_option == SERVICE_URL_DEFAULT:
        st.session_state.wasm_chat = LlamaEdgeChatService(
            service_url=service_url, request_timeout=REQUEST_TIMEOUT, streaming=True
        )
        st.session_state.start_chat = True
    # base-input
    elif service_option == SERVICE_URL_CUSTOM:
        title = st.text_input(
            "Input service URL,Press Enter to apply.", value="http://localhost:8080"
        )
        if not title:
            st.session_state.start_chat = False
        else:
            st.session_state.wasm_chat = LlamaEdgeChatService(
                service_url=title,
                request_timeout=REQUEST_TIMEOUT,
                streaming=True,
            )
            st.session_state.start_chat = True

    else:
        raise ValueError("Unsupported service option!")


st.title("💬 Wasmbot")
st.caption("🚀 A chatbot powered by LlamaEdge!")
write_message("assistant", "Hello 👋, how can I help you?")

if st.session_state.start_chat:
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

        # * non-streaming mode
        # with st.chat_message("assistant"):
        #     # invoke wasm_chat
        #     ai_message = st.session_state.wasm_chat(st.session_state.messages)
        #     st.markdown(ai_message.content)
        #     # Add assistant response to chat history
        #     st.session_state.messages.append(ai_message)

        # * streaming mode
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in st.session_state.wasm_chat.stream(st.session_state.messages):
                # print(f"[DEBUG] token: {chunk.content}")
                full_response += chunk.content
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            ai_message = AIMessage(content=full_response)
            st.session_state.messages.append(ai_message)
