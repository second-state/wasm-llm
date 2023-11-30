# GGUF Model

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [GGUF Model](#gguf-model)
  - [Llama-2-7B-Chat](#llama-2-7b-chat)
  - [Llama-2-13B-Chat](#llama-2-13b-chat)
  - [CodeLlama-13B-Instruct](#codellama-13b-instruct)
  - [BELLE-Llama2-13B-Chat](#belle-llama2-13b-chat)
  - [Mistral-7B-Instruct-v0.1](#mistral-7b-instruct-v01)
  - [MistralLite-7B](#mistrallite-7b)
  - [OpenChat-3.5](#openchat-35)
  - [Wizard-Vicuna](#wizard-vicuna)
  - [CausalLM-14B](#causallm-14b)
  - [TinyLlama-1.1B-Chat-v0.3](#tinyllama-11b-chat-v03)
  - [Baichuan2-13B-Chat](#baichuan2-13b-chat)
  - [Baichuan2-7B-Chat](#baichuan2-7b-chat)
  - [OpenHermes-2.5-Mistral-7B](#openhermes-25-mistral-7b)
  - [Dolphin-2.2-Yi-34B](#dolphin-22-yi-34b)
  - [Dolphin-2.2-Mistral-7B](#dolphin-22-mistral-7b)
  - [Dolphin-2.2.1-Mistral-7B](#dolphin-221-mistral-7b)
  - [Samantha-1.2-Mistral-7B](#samantha-12-mistral-7b)
  - [Dolphin-2.1-Mistral-7B](#dolphin-21-mistral-7b)
  - [Dolphin-2.0-Mistral-7B](#dolphin-20-mistral-7b)
  - [WizardLM-1.0-Uncensored-CodeLlama-34B](#wizardlm-10-uncensored-codellama-34b)
  - [Samantha-1.11-CodeLlama-34B](#samantha-111-codellama-34b)
  - [Samantha-1.11-7B](#samantha-111-7b)
  - [WizardCoder-Python-7B-V1.0](#wizardcoder-python-7b-v10)
  - [Zephyr-7B-Alpha](#zephyr-7b-alpha)
  - [WizardLM-7B-V1.0-Uncensored](#wizardlm-7b-v10-uncensored)
  - [WizardLM-13B-V1.0-Uncensored](#wizardlm-13b-v10-uncensored)
  - [Orca-2-13B](#orca-2-13b)
  - [Neural-Chat-7B-v3-1](#neural-chat-7b-v3-1)
  - [Yi-34B-Chat](#yi-34b-chat)
  - [Starling-LM-7B-alpha](#starling-lm-7b-alpha)

<!-- /code_chunk_output -->

## Llama-2-7B-Chat

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "llama-2-7b-chat.Q5_K_M.gguf"
chat = ChatWasm(model_file=model_file, prompt_template=PromptTemplateType.Llama2Chat)
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_M.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
e0b99920cf47b94c78d2fb06a1eceb9ed795176dfa3f7feac64629f1b52b997f
```

## Llama-2-13B-Chat

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "llama-2-13b-chat.Q5_K_M.gguf"
chat = ChatWasm(model_file=model_file, prompt_template=PromptTemplateType.Llama2Chat)
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Llama-2-13B-Chat-GGUF/resolve/main/llama-2-13b-chat.Q5_K_M.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
ef36e090240040f97325758c1ad8e23f3801466a8eece3a9eac2d22d942f548a
```

## CodeLlama-13B-Instruct

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "codellama-13b-instruct.Q4_0.gguf"
chat = ChatWasm(model_file=model_file, prompt_template=PromptTemplateType.CodeLlama)
```

Get model:

```bash
curl -LO curl -LO https://huggingface.co/second-state/CodeLlama-13B-Instruct-GGUF/resolve/main/codellama-13b-instruct.Q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
693021fa3a170a348b0a6104ab7d3a8c523331826a944dc0371fecd922df89dd
```

## BELLE-Llama2-13B-Chat

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "BELLE-Llama2-13B-Chat-0.4M-ggml-model-q4_0.gguf"
chat = ChatWasm(model_file=model_file, prompt_template=PromptTemplateType.BelleLlama2Chat)
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/BELLE-Llama2-13B-Chat-0.4M-GGUF/resolve/main/BELLE-Llama2-13B-Chat-0.4M-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
56879e1fd6ee6a138286730e121f2dba1be51b8f7e261514a594dea89ef32fe7
```

## Mistral-7B-Instruct-v0.1

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "mistral-7b-instruct-v0.1.Q5_K_M.gguf"
chat = ChatWasm(model_file=model_file, prompt_template=PromptTemplateType.MistralInstructV01)
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q5_K_M.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
# mistral-7b-instruct-v0.1.Q5_K_M.gguf
c4b062ec7f0f160e848a0e34c4e291b9e39b3fc60df5b201c038e7064dbbdcdc
```

```test
# mistral-7b-instruct-v0.1.Q4_K_M.gguf
14466f9d658bf4a79f96c3f3f22759707c291cac4e62fea625e80c7d32169991
```

## MistralLite-7B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "mistrallite.Q5_K_M.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.MistralLite,
        reverse_prompt="</s>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/MistralLite-7B-GGUF/resolve/main/mistrallite.Q5_K_M.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
d06d149c24eea0446ea7aad596aca396fe7f3302441e9375d5bbd3fd9ba8ebea
```

## OpenChat-3.5

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "openchat_3.5.Q5_K_M.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.OpenChat,
        reverse_prompt="<|end_of_turn|>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/OpenChat-3.5-GGUF/resolve/main/openchat_3.5.Q5_K_M.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
3abf26b0f2ff11394351a23f8d538a1404a2afb69465a6bbaba8836fef51899d
```

## Wizard-Vicuna

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "wizard-vicuna-13b-ggml-model-q8_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.VicunaChat,
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/wizard-vicuna-13B-GGUF/resolve/main/wizard-vicuna-13b-ggml-model-q8_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
681b6571e624fd211ae81308b573f24f0016f6352252ae98241b44983bb7e756
```

## CausalLM-14B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "causallm_14b.Q5_1.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.ChatML,
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/CausalLM-14B-GGUF/resolve/main/causallm_14b.Q5_1.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
8ddb4c04e6f0c06971e9b6723688206bf9a5b8ffc85611cc7843c0e8c8a66c4e
```

## TinyLlama-1.1B-Chat-v0.3

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.ChatML,
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/TinyLlama-1.1B-Chat-v0.3-GGUF/resolve/main/tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
7c255febbf29c97b5d6f57cdf62db2f2bc95c0e541dc72c0ca29786ca0fa5eed
```

## Baichuan2-13B-Chat

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "Baichuan2-13B-Chat-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.Baichuan2,
        reverse_prompt="用户:",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Baichuan2-13B-Chat-GGUF/resolve/main/Baichuan2-13B-Chat-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
789685b86c86af68a1886949015661d3da0a9c959dffaae773afa4fe8cfdb840
```

## Baichuan2-7B-Chat

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "Baichuan2-7B-Chat-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.Baichuan2,
        reverse_prompt="用户:",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Baichuan2-7B-Chat-GGUF/resolve/main/Baichuan2-7B-Chat-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
82deec2b1ed20fa996b45898abfcff699a92e8a6dc8e53e4fd487328ec9181a9
```

## OpenHermes-2.5-Mistral-7B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "openhermes-2.5-mistral-7b.Q5_K_M.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.ChatML,
        reverse_prompt="<|im_end|>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/OpenHermes-2.5-Mistral-7B-GGUF/resolve/main/openhermes-2.5-mistral-7b.Q5_K_M.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
61e9e801d9e60f61a4bf1cad3e29d975ab6866f027bcef51d1550f9cc7d2cca6
```

## Dolphin-2.2-Yi-34B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "dolphin-2.2-yi-34b-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.ChatML,
        reverse_prompt="<|im_end|>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Dolphin-2.2-Yi-34B-GGUF/resolve/main/dolphin-2.2-yi-34b-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
641b644fde162fd7f8e8991ca6873d8b0528b7a027f5d56b8ee005f7171ac002
```

## Dolphin-2.2-Mistral-7B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "dolphin-2.2-mistral-7b-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.ChatML,
        reverse_prompt="<|im_end|>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Dolphin-2.2-Mistral-7B-GGUF/resolve/main/dolphin-2.2-mistral-7b-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
77cf0861b5bc064e222075d0c5b73205d262985fc195aed6d30a7d3bdfefbd6c
```

## Dolphin-2.2.1-Mistral-7B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "dolphin-2.2.1-mistral-7b-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.ChatML,
        reverse_prompt="<|im_end|>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Dolphin-2.2.1-Mistral-7B-GGUF/resolve/main/dolphin-2.2.1-mistral-7b-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
c88edaa19afeb45075d566930571fc1f580329c6d6980f5222f442ee2894234e
```

## Samantha-1.2-Mistral-7B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "samantha-1.2-mistral-7b-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.ChatML,
        reverse_prompt="<|im_end|>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Samantha-1.2-Mistral-7B/resolve/main/samantha-1.2-mistral-7b-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
c29d3e84c626b6631864cf111ed2ce847d74a105f3bd66845863bbd8ea06628e
```

## Dolphin-2.1-Mistral-7B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "dolphin-2.1-mistral-7b-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.ChatML,
        reverse_prompt="<|im_end|>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Dolphin-2.1-Mistral-7B-GGUF/resolve/main/dolphin-2.1-mistral-7b-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
021b2d9eb466e2b2eb522bc6d66906bb94c0dac721d6278e6718a4b6c9ecd731
```

## Dolphin-2.0-Mistral-7B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "dolphin-2.0-mistral-7b-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.ChatML,
        reverse_prompt="<|im_end|>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Dolphin-2.0-Mistral-7B-GGUF/resolve/main/dolphin-2.0-mistral-7b-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
37adbc161e6e98354ab06f6a79eaf30c4eb8dc60fb1226ef2fe8e84a84c5fdd6
```

## WizardLM-1.0-Uncensored-CodeLlama-34B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "WizardLM-1.0-Uncensored-CodeLlama-34b-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.VicunaChat,
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/WizardLM-1.0-Uncensored-CodeLlama-34b/resolve/main/WizardLM-1.0-Uncensored-CodeLlama-34b-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
4f000bba0cd527319fc2dfb4cabf447d8b48c2752dd8bd0c96f070b73cd53524
```

## Samantha-1.11-CodeLlama-34B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "Samantha-1.11-CodeLlama-34b-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.VicunaChat,
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Samantha-1.11-CodeLlama-34B-GGUF/resolve/main/Samantha-1.11-CodeLlama-34b-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
67032c6b1bf358361da1b8162c5feb96dd7e02e5a42526543968caba7b7da47e
```

## Samantha-1.11-7B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "Samantha-1.11-7b-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.VicunaChat,
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Samantha-1.11-7B-GGUF/resolve/main/Samantha-1.11-7b-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
343ea7fadb7f89ec88837604f7a7bc6ec4f5109516e555d8ec0e1e416b06b997
```

## WizardCoder-Python-7B-V1.0

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "WizardCoder-Python-7B-V1.0-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.WizardCoder,
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/WizardCoder-Python-7B-V1.0/resolve/main/WizardCoder-Python-7B-V1.0-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
0398068cb367d45faa3b8ebea1cc75fc7dec1cd323033df68302964e66879fed
```

## Zephyr-7B-Alpha

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "zephyr-7b-alpha.Q5_K_M.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.Zephyr,
        reverse_prompt="</s>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Zephyr-7B-Alpha-GGUF/resolve/main/zephyr-7b-alpha.Q5_K_M.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
2ad371d1aeca1ddf6281ca4ee77aa20ace60df33cab71d3bb681e669001e176e
```

## WizardLM-7B-V1.0-Uncensored

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "wizardlm-7b-v1.0-uncensored.Q5_K_M.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.VicunaChat,
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/WizardLM-7B-V1.0-Uncensored-GGUF/resolve/main/wizardlm-7b-v1.0-uncensored.Q5_K_M.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
3ef0d681351556466b3fae523e7f687e3bf550d7974b3515520b290f3a8443e2
```

## WizardLM-13B-V1.0-Uncensored

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "wizardlm-13b-v1.0-uncensored.Q5_K_M.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.VicunaChat,
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/WizardLM-13B-V1.0-Uncensored-GGUF/resolve/main/wizardlm-13b-v1.0-uncensored.Q5_K_M.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
d5a9bf292e050f6e74b1be87134b02c922f61b0d665633ee4941249e80f36b50
```

## Orca-2-13B

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "Orca-2-13b-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.ChatML,
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Orca-2-13B-GGUF/resolve/main/Orca-2-13b-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
8c9ca393b2d882bd7bd0ba672d52eafa29bb22b2cd740418198c1fa1adb6478b
```

## Neural-Chat-7B-v3-1

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "neural-chat-7b-v3-1-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.IntelNeural,
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Neural-Chat-7B-v3-1-GGUF/resolve/main/neural-chat-7b-v3-1-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
e57b76915fe5f0c0e48c43eb80fc326cb8366cbb13fcf617a477b1f32c0ac163
```

## Yi-34B-Chat

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "Yi-34B-Chat-ggml-model-q4_0.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.ChatML,
        reverse_prompte="<|im_end|>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Yi-34B-Chat-GGUF/resolve/main/Yi-34B-Chat-ggml-model-q4_0.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
d51be2f2543eba49b9a33fd38ef96fafd79302f6d30f4529031154b065e23d56
```

## Starling-LM-7B-alpha

Usage:

```python
from langchain.chat_models.wasm_chat import ChatWasm, PromptTemplateType

model_file = "starling-lm-7b-alpha.Q5_K_M.gguf"
chat = ChatWasm(
        model_file=model_file,
        prompt_template=PromptTemplateType.OpenChat,
        reverse_prompte="<|end_of_turn|>",
    )
```

Get model:

```bash
curl -LO https://huggingface.co/second-state/Starling-LM-7B-alpha-GGUF/resolve/main/starling-lm-7b-alpha.Q5_K_M.gguf
```

To guarantee that the model is downloaded completely, please check its sha256 checksum:

```text
b6144d3a48352f5a40245ab1e89bfc0b17e4d045bf0e78fb512480f34ae92eba
```
