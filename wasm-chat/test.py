from wasm_chat import *
from pathlib import Path

import argparse


def main():
    parser = argparse.ArgumentParser(description='Wasm Chat')
    parser.add_argument('model_file', type=str, default='tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf',
                        help='model file to run')
    parser.add_argument('wasm_file', type=str, help='Path to wasm-infer.wasm')
    args = parser.parse_args()


    model_file = args.model_file # "tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf"
    model_alias = "default"
    wasm_file = str(Path(args.wasm_file).resolve()) # "/home/ubuntu/workspace/wasm-llm/wasm-infer/target/wasm32-wasi/release/wasm_infer.wasm"
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