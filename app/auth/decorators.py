from functools import wraps
from starlette.responses import RedirectResponse
from starlette import status

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
