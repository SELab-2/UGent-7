FROM python:3.11.4-alpine3.18 as requirements

RUN pip install poetry-plugin-export

WORKDIR /code

COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt


FROM python:3.11.4-alpine3.18

RUN apk add --no-cache gettext libintl

WORKDIR /code

COPY --from=requirements /code/requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir
