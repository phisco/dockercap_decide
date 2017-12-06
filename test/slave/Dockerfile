FROM python:2

RUN apt-get update \
    && apt-get install stress-ng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR .
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./slave.py ./
ENTRYPOINT python slave.py
