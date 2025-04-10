import asyncio

from alembic.config import Config
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import command
from src.app.db import DATABASE_URL
from src.app.models.user import User

alembic_cfg = Config("alembic.ini")


async def run_migrations():
    await create_tables_if_not_exist()
    command.upgrade(alembic_cfg, "head")


async def create_tables_if_not_exist():
    engine = create_async_engine(DATABASE_URL, echo=True)

    # Проверка подключения к БД
    for attempt in range(10):
        try:
            print(f"Попытка подключения к БД (попытка {attempt + 1})")
            async with engine.begin() as conn:
                await conn.run_sync(lambda conn: None)
            print("Успешное подключение к БД")
            break
        except OperationalError as e:
            print(f"БД ещё не готова: {e}")
            await asyncio.sleep(2)
    else:
        raise RuntimeError("Не удалось подключиться к БД после 10 попыток")

    # Проверка существования таблиц
    async with engine.begin() as conn:
        inspector = await conn.run_sync(lambda conn: inspect(conn))
        existing_tables = await conn.run_sync(lambda conn: inspector.get_table_names())

        required_tables = set(User.metadata.tables.keys())

        if required_tables.issubset(existing_tables):
            print("Все таблицы уже существуют")
            return

        # Создаём только отсутствующие таблицы
        for table_name in required_tables - set(existing_tables):
            table = User.metadata.tables[table_name]
            await conn.run_sync(table.create)
            print(f"Создана таблица: {table_name}")

    print("Все таблицы готовы")
    return


if __name__ == "__main__":
    asyncio.run(run_migrations())
