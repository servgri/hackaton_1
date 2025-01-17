from sqlalchemy.ext.asyncio import AsyncSession
from models import User


async def create_user(session: AsyncSession, username: str):
    user = User(username=username)
    session.add(user)
    await session.commit()
