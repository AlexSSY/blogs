from wtforms.validators import DataRequired
from wtforms import EmailField, PasswordField, BooleanField
from wtforms.widgets import CheckboxInput

from app.forms.base_form import AppForm


class SignInForm(AppForm):
    email = EmailField('Email', validators=(DataRequired(), ))
    password = PasswordField('Password', validators=(DataRequired(), ))
    remember_me = BooleanField('Remember Me', widget=CheckboxInput())

    def invalidate(self):
        error_message = 'Wrong email or password.'
        self.email.errors = [error_message]
        self.password.errors = [error_message]
