import asyncio
import json
from datetime import date
from math import log

from aiohttp import ClientSession
from loguru import logger

from src.core.config import BASE_URL_TIKTOK, ACCESS_TOKEN_TIKTOK, ADVERTISER_ID_TIKTOK


async def get_tiktok_ads_campaign_stats(start_date: str, end_date: str ,advertiser_id: str = ADVERTISER_ID_TIKTOK,
                                        access_token: str = ACCESS_TOKEN_TIKTOK):
    headers = {
        'Access-Token': access_token
    }
    async with ClientSession(base_url=BASE_URL_TIKTOK,
                             headers=headers,
                             ) as session:
        url = f'open_api/v1.3/report/integrated/get'
        params = {
            'advertiser_id': advertiser_id,
            'report_type': 'BASIC',
            'dimensions': '["campaign_id"]',
            'metrics': '["spend","impressions","reach", "clicks", "campaign_name"]',
            'service_type': 'AUCTION',
            'data_level': 'AUCTION_CAMPAIGN',
            'start_date': start_date,
            'end_date': end_date,
            'filtering': '[{"field_name":"campaign_name","filter_type":"MATCH","filter_value":"РБ"}]'
        }

        async with session.get(
            url=url,
            params=params
        ) as response:
            if response.status in range(200, 300):
                data = await response.json()
                logger.info(json.dumps(data, indent=4,ensure_ascii=False))
                return data.get('data')
            else:
                logger.error('Ошибка API')


async def main():
    data = await get_tiktok_ads_campaign_stats()
    logger.info(json.dumps(data, indent=4,ensure_ascii=False))

if '__main__' == __name__:
    asyncio.run(main())