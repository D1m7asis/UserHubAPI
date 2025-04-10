from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    surname: str
    password: str  # Простой пример без хеширования пароля

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    surname: str

    model_config = ConfigDict(from_attributes=True)


class Config:
    orm_mode = True
