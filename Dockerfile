FROM ubuntu:20.04
# sql-formatterをインストール
RUN apt-get -y update && \
    apt-get install -y tzdata && \
    apt-get install -y sudo && \
    apt-get install -y npm && \
    npm install -y -g sql-formatter && \
    # lts版のnodejsをインストール(古いとsql-formatterが使えない)
    npm install -y -g n && \
    apt-get install -y curl && \
    n lts && \
    apt purge -y nodejs npm
