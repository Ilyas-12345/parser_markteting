from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from src.core.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DB_URL,
                             echo=False,
                             pool_size=20,
                             max_overflow=10,
                             pool_timeout=30,
                             pool_recycle=3600,
                             pool_pre_ping=True,
                             pool_use_lifo=True
                             )
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session