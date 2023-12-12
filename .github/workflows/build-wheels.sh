#!/bin/bash
set -ex

# Install Rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"

# Compile wheels
for PYBIN in /opt/python/cp{38,39,310,311,312}*/bin; do
    # rm -rf /io/build/
    "${PYBIN}/pip" install -U maturin==1.4.0 maturin[patchelf]
    # "${PYBIN}/pip" list installed
    # "${PYBIN}/pip" show maturin
    "${PYBIN}/maturin" build -i "${PYBIN}/python" -r -o dist
    # "${PYBIN}/pip" install -U setuptools setuptools-rust wheel
    # "${PYBIN}/pip" wheel /io/ -w /io/dist/ --no-deps
done

ls -al dist/

# Bundle external shared libraries into the wheels
for whl in dist/*cp{38,39,310,311,312}*.whl; do
    auditwheel repair "$whl" -w dist/
done

ls -al dist/

# PYBIN=(/opt/python/cp38*/bin /opt/python/cp39*/bin)
# WHL=(wasm_chat-*cp38-cp38*.whl wasm_chat-*cp39-cp39*.whl)
# # Get the length of the arrays
# length=${#PYBIN[@]}

# # Iterate over the arrays
# for ((i=0; i<$length; i++)); do
#     "${PYBIN[$i]}/pip" install dist/${WHL[$i]} --force-reinstall
#     "${PYBIN[$i]}/pip" install pytest
#     "${PYBIN[$i]}/pytest" -v -s
# done

/opt/python/cp310*/bin/pip install wasm_chat-*cp310-cp310*.whl --force-reinstall
/opt/python/cp310*/bin/pip install pytest
/opt/python/cp310*/bin/pytest -v -s

# # Install packages and test
# for PYBIN in /opt/python/cp{38,39,310,311,312}*/bin; do
#     "${PYBIN}/pip" install dist/${{ env.PACKAGE_NAME }}-0.1.0-cp38-cp38-*_x86_64.whl --force-reinstall
#     "${PYBIN}/pip" install pytest
#     "${PYBIN}/pytest" -v
# done