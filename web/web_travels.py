from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

import dao

templates = Jinja2Templates(directory="templates")

web_router = APIRouter(
    prefix="",
)


@web_router.get('/')
@web_router.post('/')
def index(request: Request):
    context = {
        'request': request,
        'travels': dao.get_all_travel(20, 0),
        "title": "Main page"}
    return templates.TemplateResponse("index.html", context=context)


@web_router.get('/detailed_search')
def detailed_search(request: Request):
    context = {
        'request': request,

    }
    return templates.TemplateResponse("search_html.html", context=context)
