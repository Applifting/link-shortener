FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

LABEL maintainer="Vojtech Janousek" \
      version="1.0"

EXPOSE 8000

# CMD ['python', 'server.py']
