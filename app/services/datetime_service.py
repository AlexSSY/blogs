from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.settings import settings


TIME_ZONE = ZoneInfo(settings.app.timezone)


def now() -> datetime:
    return datetime.now(TIME_ZONE)
