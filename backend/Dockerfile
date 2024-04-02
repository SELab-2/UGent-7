FROM python:3.11.4

RUN apt update && apt install -y gettext libgettextpo-dev && pip install --upgrade pip && pip install -U poetry
RUN poetry config virtualenvs.create false

WORKDIR /code

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

COPY . .

RUN ./setup.sh
