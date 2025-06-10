from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import json

from src.app.models.task_result import TaskResult


class SQLAlchemyTaskResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task_id: str):
        task = TaskResult(id=task_id, status="queued")
        self.session.add(task)
        await self.session.commit()
        return task

    async def update(self, task_id: str, status: str, result: dict | None = None, error: str | None = None):
        task = await self.session.get(TaskResult, task_id)
        if not task:
            task = TaskResult(id=task_id)
            self.session.add(task)
        task.status = status
        task.result = result
        task.error = error
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get(self, task_id: str) -> TaskResult | None:
        return await self.session.get(TaskResult, task_id)
