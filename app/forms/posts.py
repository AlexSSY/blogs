from wtforms.validators import DataRequired
from wtforms import StringField, TextAreaField
from wtforms.widgets import CheckboxInput

from app.forms.base_form import AppForm


class AddPostForm(AppForm):
    title = StringField('Title', validators=(DataRequired(), ))
    body = TextAreaField('Body', validators=(DataRequired(), ))
