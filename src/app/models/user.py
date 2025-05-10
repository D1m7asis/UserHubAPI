from enum import Enum

from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True)
    surname = Column(String(255))
    password = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # UTC
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # UTC


class UserAction(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
