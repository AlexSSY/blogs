from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import (
    Integer,
    DateTime,
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
)


from app.core.settings import settings


TIME_ZONE = ZoneInfo(settings.app.timezone)


def now() -> datetime:
    return datetime.now(TIME_ZONE)


class BaseFieldsMixin:
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now,
        onupdate=now,
        nullable=False,
    )
