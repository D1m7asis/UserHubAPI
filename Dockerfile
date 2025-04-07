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

# Устанавливаем пакет
RUN poetry install --only main --no-interaction --no-ansi
RUN poetry add psycopg2-binary

# Переменная окружения по умолчанию для standalone режима
ENV DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/users_db"

# Создаем скрипт для запуска
RUN echo '#!/bin/sh\n\
alembic upgrade head\n\
uvicorn src.app.asgi:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

# Команда запуска
CMD ["/app/start.sh"]