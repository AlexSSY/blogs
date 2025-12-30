from starlette.requests import Request
from typing import Protocol, runtime_checkable

from .user import UserLike


@runtime_checkable
class AuthBackend(Protocol):
    async def authenticate(self, request: Request) -> UserLike | None:
        ...


@runtime_checkable
class UserProvider(Protocol):
    async def get_by_id(self, user_id: int) -> UserLike | None:
        ...

    async def get_by_login(self, login: str) -> UserLike | None:
        ...
