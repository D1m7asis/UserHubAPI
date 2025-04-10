import logging
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

logger = logging.getLogger("app")


class UserController(Controller):
    @get("/", media_type=MediaType.HTML, include_in_schema=False)
    async def index(self) -> str:
        """Главная страница с приветственной документацией"""
        logger.debug("Accessing index page")
        template_path = Path(__file__).parent.parent / "templates" / "index.html"
        html_content = template_path.read_text(encoding="utf-8")
        return html_content

    @post("/users")
    async def create_user(self, data: UserCreate) -> Response:
        """Создает нового пользователя
        Args:
            data: Данные для создания пользователя (name, surname, password)

        Returns:
            Response: Ответ с результатом операции
                - 201 - пользователь успешно создан
                - 409 - такой пользователь уже существует
                - 500 - ошибка сервера
        """

        logger.info(f"Attempting to create user: {data.name} {data.surname}")

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

                logger.info(f"User created successfully: ID {user.id}")
                return Response(
                    content={
                        "status": "success",
                        "data": UserOut.model_validate(user)
                    },
                    status_code=HTTP_201_CREATED,
                    headers={"Location": f"/users/{user.id}"}
                )

            except IntegrityError:
                logger.warning(f"User already exists: {data.name} {data.surname}")
                return Response(
                    content={
                        "status": "error",
                        "code": "user_exists",
                        "message": "User with these details already exists"
                    },
                    status_code=HTTP_409_CONFLICT
                )
            except Exception as e:
                logger.error(f"Failed to create user: {str(e)}", exc_info=True)
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

        logger.debug("Fetching all users")

        try:
            async with SessionLocal() as session:
                async with session.begin():
                    result = await session.execute(select(User))
                    users = result.scalars().all()

            logger.info(f"Fetched {len(users)} users")
            return Response(
                content={
                    "status": "success",
                    "data": [UserOut.model_validate(user) for user in users]
                },
                status_code=HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Failed to fetch users: {str(e)}", exc_info=True)
            return Response(
                content={
                    "status": "error",
                    "code": "internal_error",
                    "message": "Failed to fetch users"
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

        logger.debug(f"Fetching user with ID: {user_id}")

        async with SessionLocal() as session:
            try:
                user = await session.get(User, user_id)

                if not user:
                    logger.warning(f"User not found: ID {user_id}")
                    return Response(
                        content={
                            "status": "error",
                            "code": "user_not_found",
                            "message": f"User with ID {user_id} not found"
                        },
                        status_code=HTTP_404_NOT_FOUND
                    )

                logger.debug(f"Successfully fetched user ID {user_id}")
                return Response(
                    content={
                        "status": "success",
                        "data": UserOut.model_validate(user)
                    },
                    status_code=HTTP_200_OK
                )
            except Exception as e:
                logger.error(f"Error fetching user ID {user_id}: {str(e)}", exc_info=True)
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

        logger.info(f"Updating user ID {user_id} with data: {data.dict(exclude_unset=True)}")

        async with SessionLocal() as session:
            try:
                user = await session.get(User, user_id)

                if not user:
                    logger.warning(f"User not found for update: ID {user_id}")
                    return Response(
                        content={
                            "status": "error",
                            "code": "user_not_found",
                            "message": f"User with ID {user_id} not found"
                        },
                        status_code=HTTP_404_NOT_FOUND
                    )

                update_data = data.dict(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(user, key, value)
                user.updated_at = func.now()

                await session.commit()
                await session.refresh(user)

                logger.info(f"User ID {user_id} updated successfully")
                return Response(
                    content={
                        "status": "success",
                        "data": UserOut.model_validate(user)
                    },
                    status_code=HTTP_200_OK
                )
            except Exception as e:
                logger.error(f"Failed to update user ID {user_id}: {str(e)}", exc_info=True)
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
        """Удаляет пользователя"""
        logger.info(f"Attempting to delete user ID {user_id}")

        async with SessionLocal() as session:
            try:
                user = await session.get(User, user_id)

                if user is None:
                    logger.warning(f"User not found for deletion: ID {user_id}")
                    return Response(
                        {"status": "error", "message": "User not found"},
                        status_code=404
                    )

                await session.delete(user)
                await session.commit()

                logger.info(f"User ID {user_id} deleted successfully")
                return Response(status_code=204, content=None)

            except SQLAlchemyError as e:
                logger.error(f"Database error deleting user ID {user_id}: {str(e)}", exc_info=True)
                await session.rollback()
                return Response(
                    {"status": "error", "message": "Database error occurred while deleting user"},
                    status_code=500
                )
            except Exception as e:
                logger.error(f"Unexpected error deleting user ID {user_id}: {str(e)}", exc_info=True)
                await session.rollback()
                return Response(
                    {"status": "error", "message": "An unexpected error occurred"},
                    status_code=500
                )
