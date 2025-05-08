import logging
from pathlib import Path

from litestar import Controller, get, post, patch, delete, Response, MediaType
from litestar.status_codes import *

from src.app.models.user import User
from src.app.repositories.base import UserRepository
from src.app.schemas.user import UserCreate, UserOut, UserUpdate

logger = logging.getLogger("app")


class UserController(Controller):
    @get("/", media_type=MediaType.HTML, include_in_schema=False)
    async def index(self) -> str:
        """Главная страница с приветственной документацией"""
        logger.debug("Accessing index page")
        template_path = Path(__file__).parent.parent / "templates" / "index.html"

        try:
            html_content = template_path.read_text(encoding="utf-8")
            logger.debug("Index page loaded successfully")
            return html_content
        except Exception as e:
            logger.error(f"Failed to load index page: {e}", exc_info=True)
            raise Exception("Failed to load the index page")

    @post("/users")
    async def create_user(self, data: UserCreate, user_repo: UserRepository) -> Response:
        """Создает нового пользователя

        Returns:
            Response: Ответ с результатом операции
                - 201 - пользователь успешно создан
                - 500 - ошибка сервера
        """
        try:
            logger.info(
                f"Creating user with name {data.name} and surname {data.surname}"
            )

            user = User(name=data.name, surname=data.surname, password=data.password)
            created = await user_repo.create(user)
            logger.info(f"User created successfully: {created.id}")

            return Response(
                content={"status": "success", "data": UserOut.model_validate(created)},
                status_code=HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"Error creating user: {e}", exc_info=True)

            return Response(
                content={"status": "error", "message": "Failed to create user"},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @get("/users")
    async def get_users(self, user_repo: UserRepository) -> Response:
        """
        Получает список всех пользователей

        Returns:
            Response: Ответ с результатом операции
                - 200 - список пользователей
                - 500 - ошибка сервера
        """
        
        try:
            logger.debug("Fetching all users")
            users = await user_repo.get_all()
            logger.debug(f"Found {len(users)} users")

            return Response(
                content={
                    "status": "success",
                    "data": [UserOut.model_validate(u) for u in users],
                },
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error fetching users: {e}", exc_info=True)
            return Response(
                content={"status": "error", "message": "Failed to fetch users"},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @get("/users/{user_id:int}")
    async def get_user(self, user_id: int, user_repo: UserRepository) -> Response:
        """
        Получает информацию о конкретном пользователе

        Returns:
            Response: Ответ с результатом операции
                - 200 - данные пользователя
                - 404 - пользователь не найден
                - 500 - ошибка сервера
        """
        
        try:
            logger.debug(f"Fetching user with ID {user_id}")
            user = await user_repo.get_by_id(user_id)

            if not user:
                logger.warning(f"User not found: ID {user_id}")
                return Response(
                    content={"status": "error", "message": "User not found"},
                    status_code=HTTP_404_NOT_FOUND,
                )

            logger.debug(f"Found user: {user_id}")
            return Response(
                content={"status": "success", "data": UserOut.model_validate(user)},
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {e}", exc_info=True)
            return Response(
                content={"status": "error", "message": "Failed to fetch user"},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @patch("/users/{user_id:int}")
    async def update_user(self, user_id: int, data: UserUpdate, user_repo: UserRepository) -> Response:
        """
        Обновляет информацию о пользователе

        Returns:
            Response: Ответ с результатом операции
                - 200 - измененный пользователь
                - 500 - ошибка сервера
        """
        
        try:
            logger.debug(f"Updating user with ID {user_id}")
            user = await user_repo.get_by_id(user_id)

            if not user:
                logger.warning(f"User not found: ID {user_id}")
                return Response(
                    content={"status": "error", "message": "User not found"},
                    status_code=HTTP_404_NOT_FOUND,
                )

            updated = await user_repo.update(user, data.dict(exclude_unset=True))
            logger.info(f"User {user_id} updated successfully")
            return Response(
                content={"status": "success", "data": UserOut.model_validate(updated)},
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}", exc_info=True)
            return Response(
                content={"status": "error", "message": "Failed to update user"},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @delete("/users/{user_id:int}", status_code=HTTP_200_OK)
    async def delete_user(self, user_id: int, user_repo: UserRepository) -> Response:
        """
        Удаляет пользователя
        
        Returns:
            Response: Ответ с результатом операции
                - 200 - пользователь успешно удален
                - 404 - пользователь не найден
                - 500 - ошибка сервера
        """
        
        try:
            logger.debug(f"Deleting user with ID {user_id}")
            user = await user_repo.get_by_id(user_id)

            if not user:
                logger.warning(f"User not found: ID {user_id}")
                return Response(
                    content={"status": "error", "message": "User not found"},
                    status_code=HTTP_404_NOT_FOUND,
                )

            await user_repo.delete(user)
            logger.info(f"User {user_id} deleted successfully")
            return Response(
                content={"status": "success", "message": "User successfully deleted"},
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}", exc_info=True)
            return Response(
                content={"status": "error", "message": "Failed to delete user"},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )
