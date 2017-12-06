FROM python:3.6

WORKDIR .
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./slave.py ./
EXPOSE 80
ENTRYPOINT python slave.py
