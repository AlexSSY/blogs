from starlette_wtf import csrf_protect
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.crud import users
from app.core.templating import templating
from app.forms.signup import SignUpForm
from app.core.database import get_session


def home_page(request: Request):
    return templating.TemplateResponse(
        request, "blogs/home.html", {"hello_world": "Hello World from Jinja2."}
    )


@csrf_protect
async def signup_page(request: Request):
    signup_form = await SignUpForm.from_formdata(request)

    if await signup_form.validate_on_submit():
        async with get_session() as session:
            hashed_password = await users.hash_password(signup_form.password.data)
            await users.create_new_user(
                session, signup_form.email.data, hashed_password
            )
        return RedirectResponse(request.url_for("home_page"), status.HTTP_303_SEE_OTHER)

    status_code = (
        status.HTTP_422_UNPROCESSABLE_CONTENT
        if signup_form.errors
        else status.HTTP_200_OK
    )
    return templating.TemplateResponse(
        request, "forms/signup.html", {"form": signup_form}, status_code
    )
