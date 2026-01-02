from starlette.requests import Request
from starlette.endpoints import HTTPEndpoint
from pydantic import ValidationError

from app.core.templating import templating
from .forms import SignUpForm


class SignUp(HTTPEndpoint):
    async def get(self, request: Request):
        context = {
            "form": None,
            "form_errors": []
        }

        return templating.TemplateResponse(
            request, "auth/signup.html", context
        )

    async def post(self, request: Request):
        errors = {}

        try:
            signup_form = SignUpForm.from_form_data(request.state.form)
        except ValidationError as e:
            for error in e.errors():
                for loc in error.get("loc"):
                    old = errors.get(loc, [])
                    old.append(error.get("msg"))
                    errors[loc] = old

        context = {
            "form": None,
            "form_errors": errors
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
