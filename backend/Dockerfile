FROM python:3.11.4-alpine3.18

RUN apk update && apk add --no-cache gettext libintl && pip install -U poetry
RUN poetry config virtualenvs.create false

WORKDIR /code

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

COPY . ./