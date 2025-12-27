from typing import Protocol, runtime_checkable
from ..users.models import User


@runtime_checkable
class Authenticable(Protocol):
    def login(self) -> str: ...
    def password_hash(self) -> str: ...
    def is_active(self) -> bool: ...


@runtime_checkable
class AuthBackend(Protocol):
    async def authenticate(self, request) -> User | None:
        raise NotImplementedError


@runtime_checkable
class UserProvider(Protocol):
    async def get_by_id(self, user_id: int) -> Authenticable | None: ...
    async def get_by_login(self, login: str) -> Authenticable | None: ...
