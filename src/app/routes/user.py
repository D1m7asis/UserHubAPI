from litestar import Controller, Response, MediaType
from litestar import get, post, put, delete
from litestar.exceptions import NotFoundException
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func

from src.app.db import SessionLocal
from src.app.models.user import User
from src.app.schemas.user import UserCreate, UserOut, UserUpdate
from pathlib import Path


class UserController(Controller):
    @get("/", media_type=MediaType.HTML, include_in_schema=False)
    async def index(self) -> str:
        """Главная страница с документацией API"""
        # Получаем путь к файлу относительно текущего модуля
        template_path = Path(__file__).parent.parent / "templates" / "index.html"

        # Читаем содержимое файла
        html_content = template_path.read_text(encoding="utf-8")

        return html_content

    @post("/users")
    async def create_user(self, data: UserCreate) -> Response:
        """
        Создает нового пользователя

        Args:
            data: Данные для создания пользователя (name, surname, password)

        Returns:
            Response: 201 Created с данными пользователя или ошибка
        """
        async with SessionLocal() as session:
            try:
                user = User(
                    name=data.name,
                    surname=data.surname,
                    password=data.password  # В реальном проекте хешируйте пароль!
                )

                session.add(user)
                await session.commit()
                await session.refresh(user)

                return Response(
                    content=UserOut.model_validate(user),
                    status_code=HTTP_201_CREATED,
                    headers={"Location": f"/users/{user.id}"}
                )

            except IntegrityError as e:
                return Response(
                    content={"error": "User with these details already exists"},
                    status_code=409
                )
            except Exception as e:
                return Response(
                    content={"error": str(e)},
                    status_code=500
                )

    @get("/users")
    async def get_users(self) -> Response:
        async with SessionLocal() as session:
            result = await session.execute(
                select(User).options(selectinload("*"))  # Жадная загрузка
            )
            users = result.scalars().all()

            valid_users = [UserOut.model_validate(user.__dict__) for user in users]

            return Response(content=valid_users)

    @get("/users/{user_id:int}")
    async def get_user(self, user_id: int) -> Response:
        try:
            async with SessionLocal() as session:
                result = await session.execute(select(User).filter_by(id=user_id))
                user = result.scalars().first()
                if user:
                    return Response(UserOut.from_orm(user))
                return Response({"error": "User not found"})
        except Exception as e:
            return Response({"error": f"An error occurred while fetching user: {str(e)}"})

    @put("/users/{user_id:int}")
    async def update_user(
            self,
            user_id: int,
            data: UserUpdate
    ) -> Response:
        async with SessionLocal() as session:
            # 1. Получаем пользователя
            result = await session.execute(
                select(User)
                .where(User.id == user_id)
                .with_for_update()  # Блокировка для избежания race condition
            )
            user = result.scalars().first()

            if not user:
                raise NotFoundException(
                    detail=f"User with ID {user_id} not found",
                    status_code=HTTP_404_NOT_FOUND
                )

            # 2. Обновляем только переданные поля
            if data.name is not None:
                user.name = data.name
            if data.surname is not None:
                user.surname = data.surname
            if data.password is not None:
                user.password = data.password

            # 3. Добавляем метку времени обновления
            user.updated_at = func.now()

            await session.commit()
            await session.refresh(user)

            return Response(UserOut.from_orm(user))

    @delete("/users/{user_id:int}", status_code=200)
    async def delete_user(self, user_id: int) -> Response:
        try:
            async with SessionLocal() as session:
                result = await session.execute(select(User).filter_by(id=user_id))
                user = result.scalars().first()
                if user:
                    await session.delete(user)
                    await session.commit()
                    return Response({"message": "User deleted"})
                return Response({"error": "User not found"})
        except Exception as e:
            return Response({"error": f"An error occurred while deleting user: {str(e)}"})
