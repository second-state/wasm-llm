from langchain.chains import RetrievalQA
from langchain.embeddings import GPT4AllEmbeddings

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models.wasm_chat import ChatWasmLocal, PromptTemplateType

from knowledgebase import MyKnowledgeBase
from knowledgebase import DOCUMENT_SOURCE_DIRECTORY

# model_file = "models/tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf"
# prompt_template = PromptTemplateType.ChatML
model_file = "models/llama-2-13b-chat.Q5_K_M.gguf"
prompt_template = PromptTemplateType.Llama2Chat


def main():
    print("[INFO] Creating LLM ...")
    llm = ChatWasmLocal(
        model_file=model_file,
        prompt_template=prompt_template,
    )

    print("[INFO] Creating knowledgebase ...")
    kb = MyKnowledgeBase(pdf_source_folder_path=DOCUMENT_SOURCE_DIRECTORY)

    print("[INFO] Creating embedder ...")
    embedder = GPT4AllEmbeddings()
    # model_id = "hkunlp/instructor-large"
    # embedder = HuggingFaceEmbeddings(model_name=model_id)

    print("[INFO] Initiating document injection pipeline ...")
    kb.initiate_document_injection_pipeline(embedder)

    retriever = kb.retriever_from_persistant_vector_db(embedder)

    print("[INFO] Initializing qa ...")
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        verbose=True,
    )

    while True:
        query = input("\n\n[Input your query]: ")
        if query == "exit":
            break

        result = qa(query)
        answer, docs = result["result"], result["source_documents"]

        print(f"\n[Answer]\n\n{answer}")

        print("\n\n", "#" * 30, "Sources", "#" * 30)
        for document in docs:
            print("\n[SOURCE] " + document.metadata["source"] + ":\n")
            print(document.page_content)
        print("\n", "#" * 30, "Sources", "#" * 30)


if __name__ == "__main__":
    main()
