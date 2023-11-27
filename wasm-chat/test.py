from wasm_chat import *

def main():
    model_file = "/Volumes/Dev/secondstate/me/pyo3/wasm-chat/tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf"
    model_alias = "default"
    wasm_file = "/Volumes/Dev/secondstate/me/wasm-llm/target/wasm32-wasi/release/inference.wasm"
    dir_mapping = ".:."

    # init wasm environment
    wasm_chat = WasmChat(model_file, model_alias, wasm_file, dir_mapping)


    metadata = Metadata()
    print(f"log_enable: {metadata.log_enable}")
    print(f"reverse_prompt: {metadata.reverse_prompt}")

    # init inference context
    wasm_chat.init_inference_context(model_alias, metadata)

    prompt = """<|im_start|>system
        Answer as concisely as possible.<|im_end|>
        <|im_start|>user
        What is the capital of France?<|im_end|>
        <|im_start|>assistant"""

    # run inference
    assistant_message = wasm_chat.infer(prompt)
    print(f"[Answer] {assistant_message}")



if __name__ == "__main__":
    main()