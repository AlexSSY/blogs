from starlette.middleware.base import BaseHTTPMiddleware

from app.core.database import get_session
from app.crud import users


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.user = None
        
        user_id = request.session.get("user_id")

        if user_id is not None:
            async with get_session() as session:
                request.state.user = await users.get_user_by_id(session, user_id)

        return await call_next(request)
