from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from leaf.dependencies import get_settings
from leaf.routers import users

settings = get_settings()


app = FastAPI(
    title="Leaf",
    description="Let's clean up your neighbourhood together",
    version="0.0.1",
    contact={
        "name": "Roland Sobczak",
        "email": "rolandsobczak@icloud.com",
    },
)
app.include_router(users.router)
app.mount(
    settings.MEDIA_BASE_URL,
    StaticFiles(directory=settings.MEDIA_FOLDER),
    name="media",
)
