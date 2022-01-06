# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

USER root


WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install python3-pip ffmpeg libsm6 libxext6 -y

RUN pip install -r ./requirements.txt

COPY . /app/

#RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "http-server.py"]

