FROM python:3.7-slim

RUN apt-get update
RUN apt-get install -y firejail
RUN apt-get install -y git

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY default.profile /etc/firejail/default.profile

RUN mkdir /skill
WORKDIR /app
COPY * ./

CMD uvicorn run:app --port $PORT --host 0.0.0.0
