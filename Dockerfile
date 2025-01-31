FROM python:3.11-slim

WORKDIR /Fastapi_app

# Копирование pyproject.toml и poetry.lock в рабочую директорию
COPY app/pyproject.toml ./
COPY app/poetry.lock ./

# Установка poetry и зависимостей
RUN pip install poetry==1.8.3 && poetry config virtualenvs.create false && poetry install --no-root

# Копирование папок и файлов проекта
COPY ./app /app/
COPY app/test /test/
COPY app/main.py ./

RUN apt-get update && apt-get install -y vim

# Запуск приложения
CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000
