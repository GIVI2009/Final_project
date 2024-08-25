from fastapi import FastAPI

from database import create_tables


def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index() -> dict:
    return {"status": "200"}
