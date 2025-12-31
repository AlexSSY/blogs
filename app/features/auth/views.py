from starlette.requests import Request
from starlette.endpoints import HTTPEndpoint
from pydantic import ValidationError

from app.core.templating import templating
from .forms import SignUpForm


class SignUp(HTTPEndpoint):
    async def get(self, request: Request):
        context = {
            "form": SignUpForm(),
            "form_errors": []
        }

        return templating.TemplateResponse(
            request, "auth/signup.html", context
        )

    async def post(self, request: Request):
        form_data = await request.form()
        signup_form = SignUpForm.from_form_data(form_data)

        try:
            signup_form.model_validate()
        except ValidationError as e:
            for error in e.errors():
                print(error)

        context = {
            "form": SignUpForm(),
            "form_errors": []
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
