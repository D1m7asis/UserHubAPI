import json
from pathlib import Path
from litestar import Controller, get, Response, MediaType
from litestar.status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND

from src.app.repositories.task_repository import SQLAlchemyTaskResultRepository


class TaskController(Controller):
    @get("/tasks", media_type=MediaType.HTML, include_in_schema=False)
    async def task_page(self) -> str:
        template_path = Path(__file__).parent.parent / "templates" / "tasks.html"
        return template_path.read_text(encoding="utf-8")

    @get("/tasks/{task_id:str}")
    async def get_task(self, task_id: str, task_repo: SQLAlchemyTaskResultRepository) -> Response:
        task = await task_repo.get(task_id)
        if not task:
            return Response(content={"status": "not_found"}, status_code=HTTP_404_NOT_FOUND)

        data = {"status": task.status}
        if task.result is not None:
            data["result"] = task.result
        if task.error:
            data["error"] = task.error
        return Response(content=data, status_code=HTTP_200_OK)
