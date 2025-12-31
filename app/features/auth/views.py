from starlette.requests import Request
from pydantic import ValidationError

from app.core.templating import templating
from .forms import SignUpForm


async def sign_up(request: Request):
    signup_form = SignUpForm()
    form_errors = []

    if request.method == "POST":
        form_data = await request.form()
        signup_form = SignUpForm.from_form_data(form_data)

        try:
            signup_form.model_validate()
        except ValidationError as e:
            for error in e.errors():
                print(error)

    context = {
        "form": signup_form,
        "form_errors": form_errors
    }

    return templating.TemplateResponse(
        request, "auth/signup.html", context
    )


async def signup_page(request: Request):
    pass


async def signin_page(request: Request):
    pass


async def signout_page(request: Request):
    pass
