import logging

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base

from .settings import settings


engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True
)


# now we see all sqlalchemy queries in debug mode
if settings.app.debug:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


AsyncSessionLocal: AsyncSession = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


Base = declarative_base()
