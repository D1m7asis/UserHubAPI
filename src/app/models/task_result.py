from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.sql import func

from .user import Base

class TaskResult(Base):
    __tablename__ = 'task_results'

    id = Column(String(36), primary_key=True)
    status = Column(String(50), index=True)
    result = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
