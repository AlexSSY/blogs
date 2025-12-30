from pydantic import BaseModel

from app.core.schemas import BaseFieldsSchema


class ReadonlyUser(BaseFieldsSchema):
    email: str
