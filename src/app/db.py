import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.app.logging_config import setup_sql_logger

setup_sql_logger()

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


def is_docker_container():
    """Определяет, работает ли код в Docker-контейнере"""
    return '.dockerenv' in os.listdir('/')


def get_default_db_host():
    """Определяет хост БД по умолчанию в зависимости от среды выполнения"""
    if is_docker_container():
        return "db"
    elif os.environ.get('RUNNING_IN_DOCKER') == 'true':
        return "db"
    else:
        return "localhost"


# Параметры подключения
DB_HOST = get_default_db_host()
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "users_db")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# Формирование URL подключения
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True  # Проверяем соединение перед использованием
)

# Асинхронная сессия
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)
