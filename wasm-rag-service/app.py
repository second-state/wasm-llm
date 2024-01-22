import os

import streamlit as st
from knowledgebase import DOCUMENT_SOURCE_DIRECTORY, MyKnowledgeBase
from langchain.chains import RetrievalQA
from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage
from langchain_community.chat_models.llama_edge import LlamaEdgeChatService
from langchain_community.embeddings import GPT4AllEmbeddings

st.set_page_config(layout="wide", page_title="Wasm Chat")

DEFAULT_SERVICE_URL = "http://127.0.0.1:8080"
OPTION_SERVICE_URL_DEFAULT = "Use default service"
OPTION_SERVICE_URL_CUSTOM = "Use custom service"
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
        "Select chat service:", [OPTION_SERVICE_URL_DEFAULT, OPTION_SERVICE_URL_CUSTOM]
    )
    if service_option == OPTION_SERVICE_URL_DEFAULT:
        service_url = DEFAULT_SERVICE_URL

    # base-input
    elif service_option == OPTION_SERVICE_URL_CUSTOM:
        service_url = st.text_input(
            "Input service URL:",
            value=DEFAULT_SERVICE_URL,
            help=DEFAULT_SERVICE_URL,
        )

    else:
        raise ValueError("Unsupported service option!")

    if st.button("Connect"):
        if "wasm_chat" not in st.session_state:
            st.session_state.wasm_chat = LlamaEdgeChatService(
                service_url=service_url,
                request_timeout=REQUEST_TIMEOUT,
                # streaming=True,
            )
            st.session_state.start_chat = True

if st.session_state.start_chat:
    st.title("💬 WasmRAG")
    st.caption("🚀 A RAG app driven by LlamaEdge")

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    with st.spinner("Loading documents..."):
        uploaded_files = st.file_uploader(
            "Upload your documents",
            type=("txt", "md", "pdf"),
            accept_multiple_files=True,
        )
        if uploaded_files and len(uploaded_files) > 0:
            num_files = len(st.session_state.uploaded_files)
            for f in uploaded_files:
                if not os.path.exists(DOCUMENT_SOURCE_DIRECTORY):
                    os.makedirs(DOCUMENT_SOURCE_DIRECTORY)
                file_path = os.path.join(DOCUMENT_SOURCE_DIRECTORY, f.name)
                if file_path not in st.session_state.uploaded_files:
                    print(f"[INFO] Saving {f.name}")
                    st.session_state.uploaded_files.append(file_path)
                    with open(
                        os.path.join(DOCUMENT_SOURCE_DIRECTORY, f.name), "wb"
                    ) as out_file:
                        out_file.write(f.read())

            if num_files != len(st.session_state.uploaded_files):
                print("[INFO] Creating knowledgebase ...")
                kb = MyKnowledgeBase(pdf_source_folder_path=DOCUMENT_SOURCE_DIRECTORY)
                if "kb" not in st.session_state:
                    st.session_state.kb = kb

                print("[INFO] Creating embedder ...")
                embedder = GPT4AllEmbeddings()
                if "embedder" not in st.session_state:
                    st.session_state.embedder = embedder

                print("[INFO] Initiating document injection pipeline ...")
                st.session_state.kb.initiate_document_injection_pipeline(
                    st.session_state.embedder
                )

                retriever = st.session_state.kb.retriever_from_persistant_vector_db(
                    st.session_state.embedder
                )
                if "retriever" not in st.session_state:
                    st.session_state.retriever = retriever

                print("[INFO] Initializing qa ...")
                qa = RetrievalQA.from_chain_type(
                    llm=st.session_state.wasm_chat,
                    chain_type="stuff",
                    retriever=st.session_state.retriever,
                    return_source_documents=True,
                    verbose=True,
                )
                st.session_state.qa = qa

    if "qa" in st.session_state:
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
                # * query
                result = st.session_state.qa(prompt)
                ai_message, docs = result["result"], result["source_documents"]
                st.markdown(ai_message)

                # Add assistant response to chat history
                st.session_state.messages.append(AIMessage(content=ai_message))

                print(f"\n[Answer]\n\n{ai_message}")
                print("\n\n", "#" * 30, "Sources", "#" * 30)
                for document in docs:
                    print("\n[SOURCE] " + document.metadata["source"] + ":\n")
                    print(document.page_content)
                print("\n", "#" * 30, "Sources", "#" * 30)

                # # * query in streaming mode
                # for chunk in st.session_state.qa.stream(
                #     {
                #         "query": prompt,
                #     }
                # ):
                #     print(f"[DEBUG] token: {chunk}")
                #     st.markdown(chunk["result"])
