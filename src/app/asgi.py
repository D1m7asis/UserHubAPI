from litestar import Litestar
from litestar.openapi import OpenAPIConfig

from src.app.routes.users import UserController

# Конфигурация OpenAPI
openapi_config = OpenAPIConfig(
    title="User API",
    version="1.0.0",
    description="API для управления пользователями",
)

app = Litestar(
    route_handlers=[UserController],
    openapi_config=openapi_config
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
