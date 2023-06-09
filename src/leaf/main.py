from fastapi import FastAPI
from leaf.routers import users


app = FastAPI(
    title="Leaf",
    description="Let's clean up your neighbourhood together",
    version="0.0.1",
    contact={"name": "Roland Sobczak", "email": "rolandsobczak@icloud.com"},
)
app.include_router(users.router)
