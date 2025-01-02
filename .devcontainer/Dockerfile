ARG LIBOQS_BUILD_DEFINES="-DOQS_DIST_BUILD=ON -DBUILD_SHARED_LIBS=ON -DOQS_USE_OPENSSL=OFF"

## FIRST STAGE: get all sources and build the binary content
FROM alpine:3.21 as intermediate
ARG LIBOQS_BUILD_DEFINES
LABEL version="2"
ENV DEBIAN_FRONTEND noninteractive
RUN apk update && apk upgrade
RUN apk add build-base linux-headers cmake ninja git
# Get liboqs and liboqs-python sources
WORKDIR /opt
RUN git clone --depth 1 --branch main https://github.com/open-quantum-safe/liboqs && \
    git clone --depth 1 --branch main https://github.com/open-quantum-safe/liboqs-python.git
# Build liboqs
WORKDIR /opt/liboqs
RUN mkdir build && cd build && cmake -G"Ninja" .. ${LIBOQS_BUILD_DEFINES} && ninja install

## SECOND STAGE: Only create minimal image without build tooling and intermediate build results generated above:
FROM alpine:3.21
RUN apk update && apk upgrade
RUN apk add bash python3 py3-pip
# Only retain the binary contents of liboqs in the final image
COPY --from=intermediate /usr/local /usr/local
# Create a normal user and copy liboqs-python to user directory
#RUN addgroup -g 1000 -S pqb && adduser --uid 1000 -S pqb -G pqb
COPY --from=intermediate /opt/liboqs-python /root/liboqs-python
ENV PYTHONPATH=$PYTHONPATH:/root/liboqs-python
# Enable the user
#USER pqb
# Create venv in user directory
WORKDIR /root
RUN python3 -m venv venv
