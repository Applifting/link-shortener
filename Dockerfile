FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

COPY . .

LABEL maintainer="Vojtech Janousek" \
      version="1.0"

EXPOSE 8000

ENV PYTHONPATH "${PYTHONPATH}:/app/link_shortener"
CMD ['python', 'link_shortener/server.py']
