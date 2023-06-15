from os import environ


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from leaf.routers import users


MEDIA_FOLDER = environ.get("MEDIA_FOLDER")
MEDIA_BASE_URL = environ.get("MEDIA_BASE_URL")


app = FastAPI(
    title="Leaf",
    description="Let's clean up your neighbourhood together",
    version="0.0.1",
    contact={"name": "Roland Sobczak", "email": "rolandsobczak@icloud.com"},
)
app.include_router(users.router)
app.mount(MEDIA_BASE_URL, StaticFiles(directory=MEDIA_FOLDER), name="media")