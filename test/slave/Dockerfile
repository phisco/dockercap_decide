FROM python:2

WORKDIR .
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./slave.py ./
ENTRYPOINT python slave.py
