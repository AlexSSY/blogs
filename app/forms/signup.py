from wtforms.validators import DataRequired
from wtforms import EmailField, PasswordField, ValidationError

from app.forms.base_form import AppForm
from app.crud import users
from app.core.database import get_session


class SignUpForm(AppForm):
    email = EmailField('Email', validators=(DataRequired(), ))
    password = PasswordField('Password', validators=(DataRequired(), ))
    password_confirmation = PasswordField('Password', validators=(DataRequired(), ))

    async def async_validate_password_confirmation(self, field):
        if field.data != self.password.data:
            raise ValidationError("Passwords do not match")

    async def async_validate_email(form, field):
        async with get_session() as session:
            existing_user = await users.get_user_by_email(session, field.data.strip())
            if existing_user is not None:
                raise ValidationError('Already Exists.')
