from peewee import *
from playhouse.postgres_ext import DateTimeTZField, PostgresqlExtDatabase

from .config import DATABASE_URI


__all__ = [
    "User",
    "TodoList",
    "Task",
    "create_tables",
]

db = PostgresqlExtDatabase(DATABASE_URI)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = UUIDField(primary_key=True, constraints=[SQL("DEFAULT gen_random_uuid()")])
    login = TextField(unique=True)
    password = TextField()
    created_at = DateTimeTZField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "users"


class TodoList(BaseModel):
    id = UUIDField(primary_key=True, constraints=[SQL("DEFAULT gen_random_uuid()")])
    user_id = ForeignKeyField(User, backref="todo_lists")
    name = TextField()
    created_at = DateTimeTZField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "todo_lists"


class Task(BaseModel):
    id = UUIDField(primary_key=True, constraints=[SQL("DEFAULT gen_random_uuid()")])
    todo_list_id = ForeignKeyField(TodoList, backref="tasks")
    name = TextField()
    description = TextField(null=True)
    status = TextField(null=True)
    created_at = DateTimeTZField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "tasks"


def create_tables():
    try:
        db.connect()
    except Exception as e:
        raise e
    db.create_tables([User, TodoList, Task])
