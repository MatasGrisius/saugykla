# syntax=docker/dockerfile:1
FROM ubuntu:trusty
WORKDIR /opt
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt-get update && apt-get install -y git cmake build-essential python3-pip
RUN git clone https://github.com/LucaFulchir/libRaptorQ.git
WORKDIR libRaptorQ
RUN git submodule init
RUN git submodule update
RUN mkdir build
WORKDIR build
RUN cmake -DCMAKE_BUILD_TYPE=Release ../
RUN make -j 4
RUN make install
WORKDIR /opt
RUN mkdir saugykla
WORKDIR saugykla
COPY . .
