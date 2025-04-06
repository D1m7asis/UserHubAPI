from litestar import Litestar
from litestar.openapi import OpenAPIConfig

from src.app.db import create_tables
from src.app.routes.user import UserController

# Конфигурация OpenAPI
openapi_config = OpenAPIConfig(
    title="User API",
    version="1.0.0",
    description="API для управления пользователями",
)

app = Litestar(
    route_handlers=[UserController],
    openapi_config=openapi_config,
    on_startup=[create_tables]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
