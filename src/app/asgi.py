from litestar import Litestar
from litestar.di import Provide
from litestar.openapi import OpenAPIConfig

from src.app.dependencies import (
    provide_user_repository,
    provide_session,
    get_rabbitmq_service,
)
from src.app.logging_config import setup_logging
from src.app.migrate import create_tables_if_not_exist
from src.app.routes.system_routes import SystemController
from src.app.routes.users_routes import UserController

logger = setup_logging()

# Конфигурация OpenAPI
openapi_config = OpenAPIConfig(
    title="UserHubAPI",
    version="1.0.0",
    description="API для управления пользователями",
)


async def app_startup():
    logger.info("Application started")
    await create_tables_if_not_exist()


app = Litestar(
    route_handlers=[UserController, SystemController],
    openapi_config=openapi_config,
    on_startup=[app_startup],
    dependencies={
        "session": Provide(provide_session, sync_to_thread=False, use_cache=False),
        "user_repo": Provide(provide_user_repository, sync_to_thread=False, use_cache=False),
        "rabbitmq": Provide(get_rabbitmq_service),
    },
)

if __name__ == "__main__":
    import uvicorn
    import asyncio

    asyncio.run(app_startup())

    uvicorn.run(app, host="127.0.0.1", port=8000)
