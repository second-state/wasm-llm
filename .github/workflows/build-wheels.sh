#!/bin/bash
set -ex

# Install Rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"

# Compile wheels
for PYBIN in /opt/python/cp{38,39,310,311,312}*/bin; do
    # rm -rf /io/build/
    "${PYBIN}/pip" install -U maturin==1.4.0 maturin[patchelf]
    "${PYBIN}/pip" list installed
    "${PYBIN}/pip" show maturin
    "${PYBIN}/maturin" build -i "${PYBIN}/python" -r -o dist
    # "${PYBIN}/pip" install -U setuptools setuptools-rust wheel
    # "${PYBIN}/pip" wheel /io/ -w /io/dist/ --no-deps
done

# # Bundle external shared libraries into the wheels
# for whl in dist/*{cp36,cp37,cp38,cp39,cp310}*.whl; do
#     auditwheel repair "$whl" -w /io/dist/
# done

# # Install packages and test
# for PYBIN in /opt/python/cp{36,37,38,39,310}*/bin; do
#     "${PYBIN}/pip" install html-py-ever -f /io/dist/
# done