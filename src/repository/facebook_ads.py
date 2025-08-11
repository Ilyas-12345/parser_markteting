from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import FacebookAds


async def insert_facebook_ads_data(data: list, session: AsyncSession):
    stmt = insert(FacebookAds).values(data)
    await session.execute(stmt)
    await session.commit()