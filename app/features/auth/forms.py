from pydantic import EmailStr, model_validator

from app.core.forms import Form


class SignInForm(Form):
    email: EmailStr
    password: str
    remember_me: bool


class SignUpForm(Form):
    email: EmailStr
    password: str
    password_confirmation: str

    @model_validator(mode="after")
    def passwords_must_be_same(self):
        if self.password != self.password_confirmation:
            raise ValueError("Passwords do not match")
