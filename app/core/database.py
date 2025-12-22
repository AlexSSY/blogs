import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from .settings import settings


engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True
)


# now we see all sqlalchemy queries in debug mode
if settings.app.debug:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session():
    session = AsyncSessionLocal()
    try:
        yield session        
    except SQLAlchemyError:
        await session.rollback()
        raise
    finally:
        await session.close()


Base = declarative_base()
