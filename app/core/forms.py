from starlette.datastructures import FormData
from pydantic import BaseModel


class Form(BaseModel):
    @classmethod
    def from_form_data(cls, form_data: FormData):
        return cls(dict(form_data))
