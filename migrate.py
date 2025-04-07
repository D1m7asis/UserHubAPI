import asyncio

from alembic.config import Config

from alembic import command

alembic_cfg = Config("alembic.ini")


async def run_migrations():
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    asyncio.run(run_migrations())
