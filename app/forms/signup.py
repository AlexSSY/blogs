from wtforms.validators import DataRequired
from wtforms import EmailField, PasswordField

from app.forms.base_form import AppForm


class SignUpForm(AppForm):
    email = EmailField('Email', validators=(DataRequired(), ))
    password = PasswordField('Password', validators=(DataRequired(), ))
    password_confirmation = PasswordField('Password', validators=(DataRequired(), ))
