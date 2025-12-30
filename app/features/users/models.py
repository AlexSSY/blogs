from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Index,
    and_,
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
    foreign,
)

from app.core.database import Base
from app.core.mixins import BaseFieldsMixin


class User(Base, BaseFieldsMixin):
    __tablename__ = 'users'
    
    email: Mapped[str] = mapped_column(String(120))
    hashed_password: Mapped[str]

    @property
    def login(self) -> str:
        return self.email
