import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.blogs import User


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def create_new_user(session: AsyncSession, email: str, hashed_password: str) -> User:
    user = User(email=email, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def hash_password(password: str):
    password_bytes = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


async def verify_password(provided_password, stored_hash):
    provided_password_bytes = provided_password.encode('utf-8')
    stored_hash_bytes = stored_hash.encode('utf-8')
    return bcrypt.checkpw(provided_password_bytes, stored_hash_bytes)
