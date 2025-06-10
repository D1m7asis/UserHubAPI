import os

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db import SessionLocal
from src.app.repositories.user_repository import SQLAlchemyUserRepository
from src.app.repositories.task_repository import SQLAlchemyTaskResultRepository
from src.app.services.rabbitmq import RabbitMQService


async def provide_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def provide_user_repository(session: AsyncSession) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)


async def provide_task_repository(session: AsyncSession) -> SQLAlchemyTaskResultRepository:
    return SQLAlchemyTaskResultRepository(session)


async def get_rabbitmq_service() -> RabbitMQService:
    service = RabbitMQService(os.getenv("RMQ_URL", "amqp://guest:guest@rabbitmq/"))
    await service.connect()
    return service
