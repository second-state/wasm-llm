from wasm_chat import WasmChat, Metadata, PromptTemplateType
from pathlib import Path

import argparse


def main():
    model_file = "tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf"

    # init wasm environment
    print("\n[INFO] Init wasm environment ...\n")
    wasm_chat = WasmChat(
        model_file,
        PromptTemplateType.ChatML,
    )

    # create a default metadata
    metadata = Metadata()

    # init inference context
    print("[INFO] Init inference context ...\n")
    wasm_chat.init_inference_context(metadata)

    prompt = "<|im_start|>system\nAnswer as concisely as possible.<|im_end|>\n<|im_start|>user\nWhat is the capital of France?<|im_end|>\n<|im_start|>assistant"
    print(f"[INFO] Prompt:\n\n{prompt}\n\n")

    # run inference
    print("[INFO] One-turn conversation ...\n")
    print(f"  (You) What is the capital of France?\n")
    assistant_message = wasm_chat.infer(
        prompt,
    )
    print(f"  (Bot) {assistant_message}\n")


if __name__ == "__main__":
    main()
