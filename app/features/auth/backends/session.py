from starlette.requests import Request

from ..interfaces import UserLike, UserProvider


class SessionAuthBackend:
    def __init__(self, user_provider: UserProvider):
        self.user_provider = user_provider

    async def authenticate(self, request: Request) -> UserLike | None:
        user_pk = request.session.get("user_pk")

        if user_pk is None:
            return None
        
        return await self.user_provider.get_by_id(user_pk)
