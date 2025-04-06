from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
