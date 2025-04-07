from pathlib import Path

from litestar import Controller, Response, MediaType
from litestar import get, post, patch, delete
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_409_CONFLICT, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.sql import func

from src.app.db import SessionLocal
from src.app.models.user import User
from src.app.schemas.user import UserCreate, UserOut, UserUpdate


class UserController(Controller):
    @get("/", media_type=MediaType.HTML, include_in_schema=False)
    async def index(self) -> str:
        """Главная страница с приветственной документацией"""
        template_path = Path(__file__).parent.parent / "templates" / "index.html"

        html_content = template_path.read_text(encoding="utf-8")

        return html_content

    @post("/users")
    async def create_user(self, data: UserCreate) -> Response:
        """
        Создает нового пользователя

        Args:
            data: Данные для создания пользователя (name, surname, password)

        Returns:
            Response: Ответ с результатом операции
                - 201 - пользователь успешно создан
                - 409 - такой пользователь уже существует
                - 500 - ошибка сервера
        """
        async with SessionLocal() as session:
            try:
                user = User(
                    name=data.name,
                    surname=data.surname,
                    password=data.password
                )

                session.add(user)
                await session.commit()
                await session.refresh(user)

                return Response(
                    content={
                        "status": "success",
                        "data": UserOut.model_validate(user)
                    },
                    status_code=HTTP_201_CREATED,
                    headers={"Location": f"/users/{user.id}"}
                )

            except IntegrityError:
                return Response(
                    content={
                        "status": "error",
                        "code": "user_exists",
                        "message": "User with these details already exists"
                    },
                    status_code=HTTP_409_CONFLICT
                )
            except Exception as e:
                return Response(
                    content={
                        "status": "error",
                        "code": "internal_error",
                        "message": "Failed to create user",
                        "details": str(e)
                    },
                    status_code=HTTP_500_INTERNAL_SERVER_ERROR
                )

    @get("/users")
    async def get_users(self) -> Response:
        """
        Получает список всех пользователей

        Returns:
            Response: Ответ со списком пользователей
        """
        try:
            async with SessionLocal() as session:
                async with session.begin():  # безопасный контекст транзакции
                    result = await session.execute(select(User))
                    users = result.scalars().all()

            return Response(
                content={
                    "status": "success",
                    "data": [UserOut.model_validate(user) for user in users]
                },
                status_code=HTTP_200_OK
            )

        except Exception as e:
            return Response(
                content={
                    "status": "error",
                    "code": "internal_error",
                    "message": "Failed to fetch users",
                    "description": str(e)
                },
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @get("/users/{user_id:int}")
    async def get_user(self, user_id: int) -> Response:
        """
        Получает информацию о конкретном пользователе

        Args:
            user_id: ID пользователя

        Returns:
            Response: Ответ с данными пользователя или ошибкой
        """
        async with SessionLocal() as session:
            try:
                user = await session.get(User, user_id)

                if not user:
                    return Response(
                        content={
                            "status": "error",
                            "code": "user_not_found",
                            "message": f"User with ID {user_id} not found"
                        },
                        status_code=HTTP_404_NOT_FOUND
                    )

                return Response(
                    content={
                        "status": "success",
                        "data": UserOut.model_validate(user)
                    },
                    status_code=HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    content={
                        "status": "error",
                        "code": "internal_error",
                        "message": "Failed to fetch user"
                    },
                    status_code=HTTP_500_INTERNAL_SERVER_ERROR
                )

    @patch("/users/{user_id:int}")
    async def update_user(self, user_id: int, data: UserUpdate) -> Response:
        """
        Обновляет информацию о пользователе

        Args:
            user_id: ID пользователя
            data: Данные для обновления

        Returns:
            Response: Ответ с обновленными данными пользователя или ошибкой
        """
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(User)
                    .where(User.id == user_id)
                    .with_for_update()
                )
                user = result.scalars().first()

                if not user:
                    return Response(
                        content={
                            "status": "error",
                            "code": "user_not_found",
                            "message": f"User with ID {user_id} not found"
                        },
                        status_code=HTTP_404_NOT_FOUND
                    )

                # Обновляем только переданные поля
                update_data = data.dict(exclude_unset=True)
                if "password" in update_data:
                    update_data["password"] = update_data["password"]

                for key, value in update_data.items():
                    setattr(user, key, value)

                user.updated_at = func.now()

                await session.commit()
                await session.refresh(user)

                return Response(
                    content={
                        "status": "success",
                        "data": UserOut.model_validate(user)
                    },
                    status_code=HTTP_200_OK
                )
            except Exception as e:
                await session.rollback()
                return Response(
                    content={
                        "status": "error",
                        "code": "internal_error",
                        "message": "Failed to update user"
                    },
                    status_code=HTTP_500_INTERNAL_SERVER_ERROR
                )

    @delete("/users/{user_id:int}", status_code=200)
    async def delete_user(self, user_id: int) -> Response:
        async with SessionLocal() as session:
            try:
                result = await session.execute(select(User).filter_by(id=user_id))
                user = result.scalar_one_or_none()

                if user is not None:
                    await session.delete(user)
                    await session.commit()

                    return Response(status_code=204, content=None)

                return Response(
                    {"status": "error", "message": "User not found"},
                    status_code=404  # Более правильный код статуса для "не найдено"
                )

            except SQLAlchemyError as e:
                await session.rollback()
                return Response(
                    {"status": "error", "message": "Database error occurred while deleting user"},
                    status_code=500
                )
            except Exception as e:
                await session.rollback()
                return Response(
                    {"status": "error", "message": "An unexpected error occurred"},
                    status_code=500
                )
