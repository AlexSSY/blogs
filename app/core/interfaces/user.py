from typing import Protocol, runtime_checkable


@runtime_checkable
class UserLike(Protocol):
    login: str
    password_hash: str
    is_active: bool
