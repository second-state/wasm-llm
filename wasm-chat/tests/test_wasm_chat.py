import os
from urllib.request import urlretrieve

from wasm_chat import Metadata, PromptTemplateType, WasmChat


def get_model(url: str) -> str:
    """Download model."""
    local_filename = url.split("/")[-1]

    def download_progress(count: int, block_size: int, total_size: int) -> None:
        percent = count * block_size * 100 // total_size
        print(f"\rDownloading {local_filename}: {percent}%", end="")

    if not os.path.exists(local_filename):
        urlretrieve(url, local_filename, download_progress)

    return local_filename


def remove_downloaded(file: str) -> None:
    """Remove the downloaded assets."""
    if os.path.exists(file):
        os.remove(file)


def test_wasm_chat():
    model_file = get_model(
        "https://huggingface.co/second-state/TinyLlama-1.1B-Chat-v0.3-GGUF/resolve/main/tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf"
    )

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

    assert "Paris" in assistant_message or "Parigi" in assistant_message
