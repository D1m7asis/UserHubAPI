from litestar import Litestar
from litestar.openapi import OpenAPIConfig

from src.app.migrate import create_tables_if_not_exist
from src.app.logging_config import setup_logging
from src.app.routes.users import UserController

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
    route_handlers=[UserController],
    openapi_config=openapi_config,
    on_startup=[app_startup]
)

if __name__ == "__main__":
    import uvicorn
    import asyncio

    asyncio.run(app_startup())

    uvicorn.run(app, host="127.0.0.1", port=8000)
