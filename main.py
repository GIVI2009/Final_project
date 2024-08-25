from datetime import datetime

from fastapi import FastAPI, Path
from pydantic import BaseModel, Field, HttpUrl
from starlette import status

import dao
from database import create_tables


def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index() -> dict:
    return {"status": "200"}


class NewTravel(BaseModel):
    date_start: datetime
    date_end: datetime
    title: str = Field(max_length=100, min_length=2, examples=[""])
    description: str = Field(max_length=100, default="", examples=["Old phone"])
    price: float = Field(ge=0.01, examples=[100.78])
    image: HttpUrl
    hotel_class: int = Field(gt=0, le=5, default=4)
    country: str = Field(default="France")


@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_travel(new_travel: NewTravel) -> NewTravel:
    travel = dao.create_travel(**new_travel.dict())
    return travel


@app.get("/get_all_travel")
def get_all_travel() -> list[NewTravel]:
    travels = dao.get_all_travel(50, 0)
    return travels


@app.get("/travel/{travel_id}")
def get_travel_by_id(travel_id: int) -> NewTravel:
    travel = dao.get_travel_by_id(travel_id)
    return travel


@app.delete("/travel/{travel_id}")
def delete_travel(travel_id: int = Path(gt=0, description="ID of the product")):
    dao.delete_travel(travel_id=travel_id)
    return None
