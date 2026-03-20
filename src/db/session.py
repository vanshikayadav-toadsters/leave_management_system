from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.settings import settings

engine=create_async_engine(settings.DATABASE_URL,echo=TRUE)

async_session= sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session():
    async def async_session() as session:
        yield session