from starlette.middleware.base import BaseHTTPMiddleware

from app.core.interfaces.auth import AuthBackend


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dispatch=None, *, auth_backend: AuthBackend):
        super().__init__(app, dispatch)
        self.auth_backend = auth_backend

    async def dispatch(self, request, call_next):
        request.state.user = await self.auth_backend.authenticate(request)
        return await call_next(request)
