from app.crud import users


async def authenticate(session, email: str, password: str):
    user = await users.get_user_by_email(session, email)
    if user is None:
        return None

    if not await users.verify_password(password, user.hashed_password):
        return None

    return user