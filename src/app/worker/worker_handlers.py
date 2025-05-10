from typing import Dict, Any, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.asgi import logger
from src.app.models.user import User
from src.app.repositories.user_repository import SQLAlchemyUserRepository


async def handle_create(session: AsyncSession, data: Dict[str, Any]) -> User:
    """Обработка создания пользователя"""

    user = User(
        name=data["name"],
        surname=data["surname"],
        password=data["password"],
    )

    repo = SQLAlchemyUserRepository(session)
    return await repo.create(user)


async def handle_update(
    session: AsyncSession, user_id: int, data: Dict[str, Any]
) -> User:
    """Обработка обновления пользователя"""
    update_data = {k: v for k, v in data.items() if v is not None}
    logger.info(f"Updating user {user_id} with data: {update_data}")

    repo = SQLAlchemyUserRepository(session)
    user = await repo.get_by_id(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found")

    return await repo.update(user, update_data)

async def handle_delete(session: AsyncSession, user_id: int) -> None:
    """Обработка удаления пользователя"""
    if not user_id:
        raise ValueError("User ID is required for delete")

    repo = SQLAlchemyUserRepository(session)
    return await repo.delete(user_id)


async def handle_read(session: AsyncSession, user_id: int | None) -> List[User]:
    """Обработка удаления пользователя"""
    repo = SQLAlchemyUserRepository(session)

    if not user_id:
        return await repo.get_all()

    return await repo.get_by_id(user_id)
