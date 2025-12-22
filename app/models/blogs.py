from sqlalchemy import (
    Integer,
    String
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped
)

from app.core.database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120))
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)


async def create_tables() -> None:
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)
