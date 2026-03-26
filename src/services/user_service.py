from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models.user_model import User


async def get_or_create_user(session: AsyncSession, email: str, first_name:str = None , last_name:str = None):
    
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    
    if not user:
        user = User(email=email)
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user