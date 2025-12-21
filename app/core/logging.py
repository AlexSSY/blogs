import logging
from app.core.settings import Settings


def config_logger(settings: Settings) -> None:
    filename = "blogs.log" if settings.env == "production" else None

    logging.basicConfig(
        filename=filename,
        level=settings.logging.level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
