from .crud import get_user_by_id, get_user_by_email

from app.core.interfaces.user import UserLike
from app.core.database import get_session


class SQLAlchemyUserProvider:
    async def get_by_id(self, user_id: int) -> UserLike | None:
        async with get_session() as session:
            return await get_user_by_id(session, user_id)

    async def get_by_login(self, login: str) -> UserLike | None:
        async with get_session() as session:
            return await get_user_by_email(session, login)
