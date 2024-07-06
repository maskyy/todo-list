from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .const import TITLE
from .database import create_tables
from .routes import users


app = FastAPI(title=TITLE)
create_tables()


@app.get("/", include_in_schema=False)
async def docs():
    return RedirectResponse("/docs")


app.include_router(users.router)
