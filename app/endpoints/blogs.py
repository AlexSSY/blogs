from starlette.requests import Request

from app.core.templating import templating


def home_page(request: Request):
    return templating.TemplateResponse(request, 'blogs/home.html', {'hello_world': 'Hello World from Jinja2.'})
