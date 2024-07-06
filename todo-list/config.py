DATABASE_URI = "postgresql://todo:todo@localhost/todo"

try:
    from .local_config import *  # noqa
except ImportError:
    pass
