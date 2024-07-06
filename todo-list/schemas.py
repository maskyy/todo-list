from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ModelDelete(BaseModel):
    id: UUID


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    """Semantically different from UserCreate"""

    password: str


class User(UserBase):
    id: UUID
    created_at: datetime


class TodoListBase(BaseModel):
    name: str


class TodoListCreate(TodoListBase):
    pass


class TodoList(TodoListBase):
    created_at: datetime


class TaskBase(BaseModel):
    name: str
    description: str | None = None
    status: str | None = None


class TaskCreate(TaskBase):
    pass


class Task(BaseModel):
    id: UUID
    todo_list_id: UUID
    created_at: datetime
