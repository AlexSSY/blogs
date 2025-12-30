from pydantic import BaseModel
from datetime import datetime


class BaseFieldsSchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
