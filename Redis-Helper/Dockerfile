FROM python:latest

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY /src /app/src
COPY requirements.txt /tmp/requirements.txt

WORKDIR /app/src

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

