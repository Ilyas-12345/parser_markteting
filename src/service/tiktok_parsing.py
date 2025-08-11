import asyncio
import json
from datetime import date, datetime

from asyncpg.pgproto.pgproto import timedelta
from loguru import logger

from src.db.engine import async_session_maker
from src.repository.facebook_ads import insert_facebook_ads_data
from src.repository.tiktok_ads import insert_tiktok_ads_data
from src.service.facebook_api import get_facebook_ads_campaign_stats
from src.service.tiktok_api import get_tiktok_ads_campaign_stats


async def tiktok_pars():
    last_day = (date.today() - timedelta(days=1)).strftime(format='%Y-%m-%d')
    start_day = (date.today() - timedelta(days=1)).strftime(format='%Y-%m-%d')
    logger.info(f"Начало парсинга TikTok - {start_day} - {last_day}")
    tiktok_ads_data = await get_tiktok_ads_campaign_stats(start_date=start_day, end_date=last_day)
    tiktok_ads_data_list = tiktok_ads_data.get('list')
    formated_ads_data_db = []
    for data in tiktok_ads_data_list:
        metrics = data.get('metrics')
        formated_date = {
            'date_parsing': date.today(),
            'article': (metrics.get('campaign_name')).split(' ')[4],
            'reach': int(metrics.get('reach')),
            'spending': float(metrics.get('spend')),
            'clicks': int(metrics.get('clicks')),
            'impressions': int(metrics.get('impressions'))
        }
        formated_ads_data_db.append(formated_date)

    try:
        async with async_session_maker() as session:
            await insert_tiktok_ads_data(data=formated_ads_data_db, session=session)
            logger.success("Данные вставлены в бд")

    except Exception as e:
        logger.error(f'Пизда - {e}')


async def main():
    await tiktok_pars()

if '__main__' == __name__:
    asyncio.run(main())