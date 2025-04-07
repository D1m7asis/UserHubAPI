import os
from dotenv import load_dotenv

#  Конфиг для деплоя Docker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/users_db")
