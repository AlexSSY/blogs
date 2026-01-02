import secrets
from functools import wraps
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from starlette.middleware.base import BaseHTTPMiddleware

from .templating import templating


def login_required(endpoint):
    @wraps(endpoint)
    async def wrapper(request, *args, **kwargs):
        if request.state.user is None:
            return RedirectResponse(
                request.url_for("signin_page"),
                status_code=status.HTTP_303_SEE_OTHER,
            )
        return await endpoint(request, *args, **kwargs)
    return wrapper


CSRF_SESSION_KEY = "_csrf_token"
CSRF_FORM_FIELD = "csrf_token"

def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def get_csrf_token(session: dict) -> str:
    token = session.get(CSRF_SESSION_KEY)
    if not token:
        token = generate_csrf_token()
        session[CSRF_SESSION_KEY] = token
    return token


def validate_csrf(request: Request) -> None:
    session = request.session

    session_token = session.get(CSRF_SESSION_KEY)
    if not session_token:
        raise HTTPException(HTTP_403_FORBIDDEN, "CSRF token missing")

    form = request.state.form
    form_token = form.get(CSRF_FORM_FIELD)

    if not form_token or form_token != session_token:
        raise HTTPException(HTTP_403_FORBIDDEN, "Invalid CSRF token")


class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            request.state.form = await request.form()
            validate_csrf(request)

        return await call_next(request)
    

templating.env.globals["csrf_token"] = lambda request: get_csrf_token(request.session)
