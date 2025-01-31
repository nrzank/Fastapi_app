FROM python:3.11.9-alpine

RUN apk update && apk add --no-cache \
    curl \
    build-base \
    libpq-dev \
    vim \
    && rm -rf /var/cache/apk/*



WORKDIR /Fastapi_app
ENV PYTHONPATH="/Fastapi_app"



COPY app /Fastapi_app/app

COPY main.py ./
COPY .env ./
COPY pyproject.toml poetry.lock ./


RUN pip install --upgrade pip
RUN pip install -v poetry==1.8.3 && poetry config virtualenvs.create false && poetry install --no-root

RUN poetry install --no-root


CMD uvicorn main:app --reload --host "localhost" --port 8000

