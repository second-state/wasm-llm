# #!/bin/bash
# set -ex

# # Install Rustup
# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# export PATH="$HOME/.cargo/bin:$PATH"

# # Compile wheels
# for PYBIN in /opt/python/cp{38,39,310,311,312}*/bin; do
#     # rm -rf /io/build/
#     "${PYBIN}/pip" install -U maturin==1.4.0 maturin[patchelf]
#     "${PYBIN}/pip" list installed
#     "${PYBIN}/pip" show maturin
#     "${PYBIN}/maturin" build -i "${PYBIN}/python" -r -o dist
#     # "${PYBIN}/pip" install -U setuptools setuptools-rust wheel
#     # "${PYBIN}/pip" wheel /io/ -w /io/dist/ --no-deps
# done

# # # Bundle external shared libraries into the wheels
# # for whl in dist/*{cp36,cp37,cp38,cp39,cp310}*.whl; do
# #     auditwheel repair "$whl" -w /io/dist/
# # done

# # # Install packages and test
# # for PYBIN in /opt/python/cp{36,37,38,39,310}*/bin; do
# #     "${PYBIN}/pip" install html-py-ever -f /io/dist/
# # done


# ===================================================================================

#!/bin/bash
set -ex

# Install Rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"
echo "path: $PATH"

# # Compile wheels
# for PYBIN in /opt/python/cp{38,39,310,311,312}*/bin; do
#     export PYTHON_EXECUTABLE=${PYBIN}/python
#     bash ../../deploy.sh
#     # rm -rf /io/build/
#     "${PYBIN}/pip" install -U maturin==1.4.0 maturin[patchelf]
#     # "${PYBIN}/pip" list installed
#     # "${PYBIN}/pip" show maturin
#     "${PYBIN}/maturin" build -i "${PYBIN}/python" -r -o dist
#     # "${PYBIN}/pip" install -U setuptools setuptools-rust wheel
#     # "${PYBIN}/pip" wheel /io/ -w /io/dist/ --no-deps
# done

current_dir=$(pwd)
echo "Current directory: $current_dir"
echo "home directory: $HOME"

export PYTHON_EXECUTABLE=/opt/python/cp310-cp310/bin/python

# install WasmEdge runtime
bash ../deploy.sh
source $HOME/.bashrc

# display .wasmedge directory
yum install -y tree
tree $HOME/.wasmedge


# install maturin, patchelf and zig
/opt/python/cp310-cp310/bin/pip install -U maturin==1.4.0 maturin[patchelf] ziglang==0.11.0

# check binaries
which zig

# # install zig
# yum install epel-release
# yum install snapd
# systemctl enable --now snapd.socket
# ln -s /var/lib/snapd/snap /snap
# snap install zig --beta --classic

# build wheels
/opt/python/cp310-cp310/bin/maturin build -i /opt/python/cp310-cp310/bin/python -r -o dist --zig


ls -al dist/

# # Bundle external shared libraries into the wheels
# for whl in dist/*cp{38,39,310,311,312}*.whl; do
#     auditwheel repair "$whl" -w dist/
# done

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

/opt/python/cp310-cp310/bin/pip install dist/wasm_chat-0.1.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl --force-reinstall
/opt/python/cp310-cp310/bin/pip install pytest
/opt/python/cp310-cp310/bin/pytest -v -s

# # Install packages and test
# for PYBIN in /opt/python/cp{38,39,310,311,312}*/bin; do
#     "${PYBIN}/pip" install dist/${{ env.PACKAGE_NAME }}-0.1.0-cp38-cp38-*_x86_64.whl --force-reinstall
#     "${PYBIN}/pip" install pytest
#     "${PYBIN}/pytest" -v
# done