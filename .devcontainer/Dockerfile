FROM ubuntu:22.04

# 追加パッケージをインストール
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    python3 \
    python3-pip \
    python3-pygame \
    curl \
    unzip \
    fontconfig \
    fonts-dejavu-core \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Amazon Q CLIをインストール
RUN curl --proto '=https' --tlsv1.2 -sSf "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux-musl.zip" -o "/tmp/q.zip" && \
    cd /tmp && \
    unzip q.zip && \
    cd q && \
    ./install.sh --no-confirm --force && \
    cd / && \
    rm -rf /tmp/q && \
    rm -f /tmp/q.zip
