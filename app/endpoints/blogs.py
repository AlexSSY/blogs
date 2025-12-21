from starlette.requests import Request
from starlette.responses import PlainTextResponse


def home_page(request: Request):
    return PlainTextResponse(
        content="Hello World!"
    )
