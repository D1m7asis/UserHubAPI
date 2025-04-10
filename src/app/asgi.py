from litestar import Litestar
from litestar.openapi import OpenAPIConfig

from src.app.logging_config import setup_logging
from src.app.routes.users import UserController

logger = setup_logging()

# Конфигурация OpenAPI
openapi_config = OpenAPIConfig(
    title="UserHubAPI",
    version="1.0.0",
    description="API для управления пользователями",
)


async def log_startup():
    logger.info("Application started")


app = Litestar(
    route_handlers=[UserController],
    openapi_config=openapi_config,
    on_startup=[log_startup]
)

if __name__ == "__main__":
    import uvicorn

    logger = setup_logging()
    log_startup()

    uvicorn.run(app, host="127.0.0.1", port=8000)
