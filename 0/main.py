
from fastapi import FastAPI

app = FastAPI()


@app.get("/message/")
async def root():
    return {"message": "Hello World"}


@app.get("/")
def index():
    return {"message": "I'm new to this so HELLO World!"}