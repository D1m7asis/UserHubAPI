from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db import SessionLocal
from src.app.repositories.user_repository import SQLAlchemyUserRepository


async def provide_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def provide_user_repository(session: AsyncSession) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)
