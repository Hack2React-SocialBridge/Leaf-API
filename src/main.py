from fastapi import FastAPI


app = FastAPI(
    title="Leaf",
    description="Let's clean up your neighbourhood together",
    version="0.0.1",
    contact={"name": "Roland Sobczak", "email": "rolandsobczak@icloud.com"},
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
