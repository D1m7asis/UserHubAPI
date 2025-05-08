from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, List

T = TypeVar("T")


class UserRepository(ABC, Generic[T]):
    model: Type[T]

    @abstractmethod
    async def get_all(self) -> List[T]: ...

    @abstractmethod
    async def get_by_id(self, obj_id: int) -> T | None: ...

    @abstractmethod
    async def create(self, obj: T) -> T: ...

    @abstractmethod
    async def update(self, obj: T, update_data: dict) -> T: ...

    @abstractmethod
    async def delete(self, obj: T) -> None: ...
