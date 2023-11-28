from wasm_chat import WasmChat, Metadata, PromptTemplateType
from pathlib import Path

import argparse


def main():
    model_file = "tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf"
    wasm_file = str(
        Path("../wasm-infer/target/wasm32-wasi/release/wasm_infer.wasm").resolve()
    )

    # init wasm environment
    wasm_chat = WasmChat(model_file, wasm_file, PromptTemplateType.ChatML)

    metadata = Metadata()
    print(f"log_enable: {metadata.log_enable}")
    print(f"reverse_prompt: {metadata.reverse_prompt}")

    # init inference context
    wasm_chat.init_inference_context(metadata)

    prompt = """<|im_start|>system
        Answer as concisely as possible.<|im_end|>
        <|im_start|>user
        What is the capital of France?<|im_end|>
        <|im_start|>assistant"""

    # run inference
    assistant_message = wasm_chat.infer(
        prompt,
    )
    print(f"[Answer] {assistant_message}")


if __name__ == "__main__":
    main()
