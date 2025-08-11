from sqlalchemy import insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import FacebookAds
from src.models.tiktok_ads import TikTokAds


async def insert_tiktok_ads_data(data: list, session: AsyncSession):
    stmt = insert(TikTokAds).values(data)
    await session.execute(stmt)
    await session.commit()
