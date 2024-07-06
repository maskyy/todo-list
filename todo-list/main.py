from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .const import TITLE


app = FastAPI(title=TITLE)


@app.get("/", include_in_schema=False)
async def docs():
    return RedirectResponse("/docs")
