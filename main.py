from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from database import create_tables, get_db
from models import Visitor

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Створюємо таблиці в базі даних
create_tables()


class VisitorCreate(BaseModel):
    name: str
    email: str
    password: str


@app.get("/register/")
def show_registration_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register/")
def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_visitor = db.query(Visitor).filter(Visitor.email == email).first()
    if db_visitor:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_visitor = Visitor(name=name, email=email, password=password)
    db.add(new_visitor)
    db.commit()
    db.refresh(new_visitor)

    return RedirectResponse(url="/", status_code=303)


@app.get("/login/")
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login/")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_visitor = db.query(Visitor).filter(Visitor.email == email).first()

    if not db_visitor or db_visitor.password != password:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Login successful", "visitor_id": db_visitor.id}


@app.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
