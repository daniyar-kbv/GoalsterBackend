FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /goalster
RUN mkdir /goalster/staticfiles
RUN mkdir /goalster/media
WORKDIR /goalster
ADD requirements.txt /goalster/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /goalster/

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y gettext && \
    apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*
