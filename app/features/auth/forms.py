from pydantic import EmailStr, model_validator, field_validator

from app.core.forms import Form


class SignInForm(Form):
    email: EmailStr
    password: str
    remember_me: bool


class SignUpForm(Form):
    email: EmailStr
    password: str
    password_confirmation: str

    @field_validator("password", mode="after")
    @classmethod
    def password_min_length(cls, value):
        if len(value) < 6:
            raise ValueError("Too short")

    @model_validator(mode="after")
    def passwords_must_be_same(self):
        if self.password != self.password_confirmation:
            raise ValueError("Passwords do not match")
