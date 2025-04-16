import re
from typing import Optional, Annotated

from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, Field, field_validator, StringConstraints

EXAMPLE_NAME_SURNAME_PASSWORD = {
    "example": {
        "name": "Иван",
        "surname": "Сидоров",
        "password": "NewSecurePass123!"
    }
}

EXAMPLE_ID_NAME_SURNAME = {
    "example": {
        "id": 1,
        "name": "Иван",
        "surname": "Петров"
    }
}

# Конфигурация для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Общие ограничения для строк
NameStr = Annotated[
    str,
    StringConstraints(
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Zа-яА-Я\- ]+$",
        strip_whitespace=True
    )
]
min_password_length: int = 5
max_password_length: int = 40


class UserCreate(BaseModel):
    """Модель для создания пользователя с валидацией"""
    name: NameStr
    surname: NameStr
    password: str = Field(..., min_length=min_password_length, max_length=max_password_length)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Валидация сложности пароля"""
        errors = []
        if not re.search(r"[A-Z]", v):
            errors.append("at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            errors.append("at least one lowercase letter")
        ...

        if errors:
            raise ValueError(f"Password must contain: {', '.join(errors)}")

        return pwd_context.hash(v)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra=EXAMPLE_NAME_SURNAME_PASSWORD
    )


class UserUpdate(BaseModel):
    """Модель для обновления пользователя с валидацией"""
    name: Optional[NameStr] = Field(
        default=None,
        description="Новое имя пользователя"
    )
    surname: Optional[NameStr] = Field(
        default=None,
        description="Новая фамилия пользователя"
    )
    password: Optional[str] = Field(
        default=None,
        min_length=min_password_length,
        max_length=max_password_length,
        description="Новый пароль"
    )

    @field_validator('password')
    @classmethod
    def validate_update_password(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return UserCreate.validate_password(v)
        return None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra=EXAMPLE_NAME_SURNAME_PASSWORD
    )


class UserOut(BaseModel):
    """Модель для вывода данных пользователя (без чувствительных данных)"""
    id: int
    name: str
    surname: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra=EXAMPLE_ID_NAME_SURNAME
    )
