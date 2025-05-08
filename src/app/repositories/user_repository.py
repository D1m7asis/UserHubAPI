from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from typing import List

from src.app.models.user import User
from src.app.repositories.base import UserRepository


class SQLAlchemyUserRepository(UserRepository[User]):
    model = User

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[User]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, obj_id: int) -> User | None:
        return await self.session.get(self.model, obj_id)

    async def create(self, obj: User) -> User:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: User, update_data: dict) -> User:
        for key, value in update_data.items():
            setattr(obj, key, value)
        obj.updated_at = func.now()
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: User) -> None:
        await self.session.delete(obj)
        await self.session.commit()
