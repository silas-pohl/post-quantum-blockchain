FROM ubuntu:latest

# Install dependencies
RUN apt-get -y update && \
    apt-get install -y build-essential git cmake libssl-dev python3 python3-venv pip

ENV GITHUB_TAG="main"

# Get and install liboqs
RUN git clone --depth 1 --branch ${GITHUB_TAG} https://github.com/open-quantum-safe/liboqs
RUN cmake -S liboqs -B liboqs/build -DBUILD_SHARED_LIBS=ON && \
    cmake --build liboqs/build --parallel 4 && \
    cmake --build liboqs/build --target install

# Enable a normal user
RUN useradd -m -c "Post Quantum Blockchain" post-quantum-blockchain
USER post-quantum-blockchain
WORKDIR /home/post-quantum-blockchain

# Get and install liboqs-python
RUN git clone --depth 1 --branch ${GITHUB_TAG} https://github.com/open-quantum-safe/liboqs-python.git

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
ENV PYTHONPATH=$PYTHONPATH:/home/post-quantum-blockchain/liboqs-python

RUN python3 -m venv venv
RUN . venv/bin/activate && cd liboqs-python && pip install . && cd $HOME && pip install ecdsa pytest
