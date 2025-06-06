import datetime
import uuid
from functools import wraps

from litestar import Response
from litestar.status_codes import *
from pydantic import ValidationError

from src.app.models.user import UserAction
from src.app.services.rabbitmq import RabbitMQService
from src.app.repositories.task_repository import SQLAlchemyTaskResultRepository


def handle_errors_and_logging(logger):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                logger.info(f"Starting {func.__name__}")
                result = await func(*args, **kwargs)
                return result
            except ValidationError as e:
                logger.warning(f"Validation error in {func.__name__}: {e.errors()}")
                return Response(
                    content={"status": "error", "details": e.errors()},
                    status_code=HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                return Response(
                    content={
                        "status": "error",
                        "message": "Failed to process request",
                    },
                    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return wrapper

    return decorator


class RabbitMQHandler:
    def __init__(self, rabbitmq: RabbitMQService, task_repo):
        self.rabbitmq = rabbitmq
        self.task_repo = task_repo

    async def publish_task(
        self, queue_name: str, action: UserAction, data: dict = None
    ):

        task_id = str(uuid.uuid4())
        message_data = {
            "task_id": task_id,
            "action": action,
            "data": data or {},
            "metadata": {
                "timestamp": datetime.datetime.utcnow().isoformat(),
            },
        }

        await self.rabbitmq.publish(
            queue_name=queue_name,
            message_data=message_data,
        )

        await self.task_repo.create(task_id)

        return {
            "status": "queued",
            "task_id": task_id,
        }
