FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    pip install --upgrade pip poetry && \
    rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости без пакета
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction --no-ansi

# Копируем исходный код
COPY pyproject.toml poetry.lock alembic.ini ./
COPY alembic ./alembic
COPY src ./src


CMD ["sh", "-c", "python -m uvicorn src.app.asgi:app --host 0.0.0.0 --port ${APP_PORT:-8000}"]
