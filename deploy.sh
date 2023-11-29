#!/bin/bash

if [[ $1 == "uninstall" ]]; then
    # Check if the current operating system is macOS, Linux or Windows
    if [[ "$OSTYPE" == "msys" ]]; then
        printf "[-] Removing the directory 'C:\\Program Files\\WasmEdge\\wasm' and all files in it ...\n"
        target_dir="C:\\Program Files\\WasmEdge\\wasm"

    elif [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
        printf "[-] Removing the directory '$HOME/.wasmedge/wasm' and all files in it ...\n"
        target_dir="$HOME/.wasmedge/wasm"

    else
        echo "The OS should be macOS, Linux or Windows"
        exit 1
    fi

    # Check if the directory exists
    if [[ -d "$target_dir" ]]; then
        # Remove the directory and all files in it
        rm -rf "$target_dir"
    fi

    # Uninstall WasmEdge
    printf "\n[-] Uninstalling WasmEdge ...\n\n"
    bash <(curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/uninstall.sh) -q

else

    printf "\nThe installation will deploy 'WasmEdge Runtime' and 'wasm-infer.wasm' in your local environment:\n"

    ########### Step 1: Checking the operating system ###########

    printf "\n[+] Checking the operating system ...\n"

    # Check if the current operating system is macOS, Linux or Windows
    if [[ "$OSTYPE" == "msys" ]]; then
        printf "For Windows, please run 'winget install wasmedge' to install WasmEdge.\n"
    elif [[ "$OSTYPE" != "linux-gnu"* && "$OSTYPE" != "darwin"* ]]; then
        printf "Only macOS, Linux and Windows are supported.\n"
        exit 1
    fi

    printf "\n"

    ########### Step 2: Checking if git and curl are installed ###########

    printf "[+] Checking if 'git' and 'curl' are installed ...\n"

    # Check if git and curl are installed, if not, install them
    for cmd in git curl
    do
        if ! command -v $cmd &> /dev/null
        then
            if [[ "$OSTYPE" == "linux-gnu"* ]]; then
                sudo apt-get install $cmd
            elif [[ "$OSTYPE" == "darwin"* ]]; then
                brew install $cmd
            fi
        fi
    done

    printf "\n"

    ########### Step 3: Installing WasmEdge ###########

    printf "[+] Installing WasmEdge ...\n\n"

    # Run the command to install WasmEdge
    VERSION=0.13.5
    if curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- -v $VERSION --plugins wasi_nn-ggml; then
        source $HOME/.wasmedge/env
        wasmedge_path=$(which wasmedge)
        printf "\n    The WasmEdge Runtime is installed in %s.\n\n" "$wasmedge_path"
    else
        echo "Failed to install WasmEdge"
        exit 1
    fi

    printf "\n"

    ########### Step 4: Downloading the wasm file ###########

    printf "[+] Downloading 'wasm-infer.wasm' ...\n\n"

    wasm_url="https://github.com/second-state/wasm-llm/raw/main/wasm-infer/wasm_infer.wasm"

    if [[ "$OSTYPE" == "msys" ]]; then
        target_dir="C:\\Program Files\\WasmEdge\\wasm"
    elif [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
        target_dir="$HOME/.wasmedge/wasm"
    else
        printf "The OS should be macOS, Linux or Windows\n"
        exit 1
    fi

    # Check if the directory exists
    if [[ ! -d "$target_dir" ]]; then
        # Create the directory if it does not exist
        mkdir -p "$target_dir"
    fi

    # Download the file
    curl -L "$wasm_url" -o "$target_dir/wasm_infer.wasm" -#

    printf "\n"

    printf "* The installation is done! To uninstall WasmEdge Runtime, use the command 'bash deploy.sh uninstall'\n\n"

fi