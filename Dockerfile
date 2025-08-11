FROM python:3.12-slim

RUN apt-get update && apt-get install -y cron nano && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /parser/

ENV PYTHONPATH=/parser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./docker_scripts /parser/docker_scripts

COPY ./src /parser/src

COPY ./migration /parser/migration

RUN chmod +x /parser/docker_scripts/*.sh
