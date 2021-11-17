# syntax=docker/dockerfile:1
FROM alpine
RUN apk update && apk add git cmake make g++ python3 py3-pip bash openssl
WORKDIR /opt
RUN git clone https://github.com/LucaFulchir/libRaptorQ.git
WORKDIR libRaptorQ
RUN git submodule init && git submodule update
RUN mkdir build
WORKDIR build
RUN cmake -DCMAKE_BUILD_TYPE=Release ../ && make -j 4 && make install
