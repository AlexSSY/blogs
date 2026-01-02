from starlette.requests import Request

from app.core.templating import templating


async def home_page(request: Request):
    return templating.TemplateResponse(
        request, "blog/home.html"
    )
