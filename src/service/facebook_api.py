import asyncio
import json

from aiohttp import ClientSession
from loguru import logger

from src.core.config import BASE_URL_FACEBOOK, ID_ADS_ACCOUNT_FLARIO_COSMETICS, ACCESS_TOKEN_FACEBOOK


async def get_facebook_ads_campaign_stats(time_range: str):
    async with ClientSession(base_url=BASE_URL_FACEBOOK) as session:
        url = f'act_{ID_ADS_ACCOUNT_FLARIO_COSMETICS}/insights'
        time_range_param = {"since": time_range, "until": time_range}
        params = {
            'filtering': '[{"field": "campaign.name", "operator": "CONTAIN", "value": "РБ"}, {"field": "campaign.name", "operator": "CONTAIN", "value": "tashe"}]',
            'time_range': f'{time_range_param}',
            'fields': 'spend,campaign_name,reach,actions',
            'access_token': ACCESS_TOKEN_FACEBOOK,
            'level': 'campaign'
        }
        async with session.get(
            url=url,
            params=params
        ) as response:
            if response.status in range(200, 300):
                data = await response.json()
                return data.get('data')
            else:
                logger.error('Ошибка API')


async def main():
    data = await get_facebook_ads_campaign_stats()
    logger.info(json.dumps(data, indent=4,ensure_ascii=False))

if '__main__' == __name__:
    asyncio.run(main())