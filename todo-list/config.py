DATABASE_URI = "postgresql://todo:todo@localhost/todo"

JWT_SECRET_KEY = "secret"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

try:
    from .local_config import *  # noqa
except ImportError:
    pass
