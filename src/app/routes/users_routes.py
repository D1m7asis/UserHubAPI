import logging

from litestar import Controller, get, post, patch, delete, Response
from litestar.status_codes import *

from src.app.models.user import UserAction
from src.app.repositories.base import UserRepository
from src.app.routes.handlers import handle_errors_and_logging, RabbitMQHandler
from src.app.schemas.user import UserCreate, UserUpdate, UserOut
from src.app.services.rabbitmq import RabbitMQService

logger = logging.getLogger("app")


class UserController(Controller):
    @post("/users")
    @handle_errors_and_logging(logger)
    async def create_user(
        self, data: UserCreate, rabbitmq: RabbitMQService
    ) -> Response:
        """Создает нового пользователя через очередь задач"""
        user_data = data.dict()
        result = await RabbitMQHandler(rabbitmq).publish_task(
            queue_name="user_actions",
            action=UserAction.CREATE,
            data=user_data,
        )
        return Response(content=result, status_code=HTTP_202_ACCEPTED)

    @get("/users")
    @handle_errors_and_logging(logger)
    async def get_all_users(self, user_repo: UserRepository) -> Response:
        """Получает список всех пользователей"""
        users = await user_repo.get_all()

        data = [UserOut.model_validate(u) for u in users]
        return Response(content=data, status_code=HTTP_200_OK)

    @get("/users/{user_id:int}")
    @handle_errors_and_logging(logger)
    async def get_user_by_id(self, user_id: int, user_repo: UserRepository) -> Response:
        """Получает определенного пользователя"""
        user = await user_repo.get_by_id(user_id)

        data = UserOut.model_validate(user)
        return Response(content=data, status_code=HTTP_200_OK)

    @patch("/users/{user_id:int}")
    @handle_errors_and_logging(logger)
    async def update_user(
        self,
        user_id: int,
        data: UserUpdate,
        rabbitmq: RabbitMQService,
    ) -> Response:
        """Обновляет информацию о пользователе"""
        user_data = data.dict(exclude_unset=True)
        user_data["user_id"] = user_id

        result = await RabbitMQHandler(rabbitmq).publish_task(
            queue_name="user_actions",
            action=UserAction.UPDATE,
            data=user_data,
        )
        return Response(content=result, status_code=HTTP_202_ACCEPTED)

    @delete("/users/{user_id:int}", status_code=HTTP_200_OK)
    @handle_errors_and_logging(logger)
    async def delete_user(
        self,
        user_id: int,
        rabbitmq: RabbitMQService,
    ) -> Response:
        """Удаляет пользователя"""

        result = await RabbitMQHandler(rabbitmq).publish_task(
            queue_name="user_actions",
            action=UserAction.DELETE,
            data=dict(user_id=user_id),
        )

        return Response(content=result, status_code=HTTP_202_ACCEPTED)
