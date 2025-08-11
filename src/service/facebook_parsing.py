import asyncio
from datetime import date, datetime
import json

from asyncpg.pgproto.pgproto import timedelta
from loguru import logger
from aiohttp import ClientSession

from src.db.engine import async_session_maker
from src.repository.facebook_ads import insert_facebook_ads_data
from src.service.facebook_api import get_facebook_ads_campaign_stats


async def get_czk_to_usd_rate() -> float:
    """Возвращает текущий курс CZK->USD (сколько USD за 1 CZK) с fallback на несколько источников."""
    providers = [
        ("exchangerate_host_latest", "https://api.exchangerate.host/latest?base=CZK&symbols=USD"),
        ("exchangerate_host_convert", "https://api.exchangerate.host/convert?from=CZK&to=USD"),
        ("open_er_api", "https://open.er-api.com/v6/latest/CZK"),
        ("fawaz_api", "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/czk/usd.json"),
    ]

    async with ClientSession() as session:
        for name, url in providers:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status not in range(200, 300):
                        logger.error(f'[{name}] HTTP {response.status} при получении курса по URL: {url}')
                        continue

                    # Пытаемся распарсить JSON, логируем часть ответа при неудаче
                    try:
                        data = await response.json()
                    except Exception as parse_err:
                        text = await response.text()
                        logger.error(f'[{name}] Ошибка парсинга JSON: {parse_err}; ответ: {text[:200]}')
                        continue

                    # Варианты схем
                    if isinstance(data, dict):
                        # exchangerate.host latest
                        if 'rates' in data and isinstance(data['rates'], dict) and 'USD' in data['rates']:
                            rate = float(data['rates']['USD'])
                            logger.info(f'[{name}] Курс CZK->USD: {rate}')
                            return rate

                        # exchangerate.host convert
                        if 'result' in data:
                            try:
                                rate = float(data['result'])
                                logger.info(f'[{name}] Курс CZK->USD: {rate}')
                                return rate
                            except Exception:
                                pass

                        if 'info' in data and isinstance(data['info'], dict) and 'rate' in data['info']:
                            try:
                                rate = float(data['info']['rate'])
                                logger.info(f'[{name}] Курс CZK->USD: {rate}')
                                return rate
                            except Exception:
                                pass

                        # open.er-api.com
                        if 'rates' in data and isinstance(data['rates'], dict) and 'USD' in data['rates']:
                            try:
                                rate = float(data['rates']['USD'])
                                logger.info(f'[{name}] Курс CZK->USD: {rate}')
                                return rate
                            except Exception:
                                pass

                        # fawazahmed0 currency api
                        if 'usd' in data:
                            try:
                                rate = float(data['usd'])
                                logger.info(f'[{name}] Курс CZK->USD: {rate}')
                                return rate
                            except Exception:
                                pass

                    logger.error(f'[{name}] Не найдены ожидаемые поля в ответе: ключи={list(data.keys()) if isinstance(data, dict) else type(data)}')
            except Exception as e:
                logger.error(f'[{name}] Ошибка при запросе курса CZK->USD: {e}')

    logger.error('Не удалось получить курс CZK->USD ни у одного провайдера, используем 1.0')
    return 1.0


async def facebook_pars():
    last_day = (date.today() - timedelta(days=1)).strftime(format='%Y-%m-%d')
    logger.info(f"Начало парсинга Facebook - {last_day}")
    facebook_ads_data = await get_facebook_ads_campaign_stats(time_range=last_day)
    czk_to_usd = await get_czk_to_usd_rate()
    formated_facebook_ads_data_db = []
    for data in facebook_ads_data:
        date_obj = datetime.strptime(data.get('date_start'), '%Y-%m-%d')
        for action in data.get('actions'):
            if action.get('action_type') == 'link_click':
                clicks = int(action.get('value'))
                break
        else:
            clicks = 0
        spend_czk = float(data.get('spend') or 0)
        spend_usd = float(f"{(spend_czk * czk_to_usd):.2f}")
        formated_date = {
            'date_parsing': date_obj,
            'article': (data.get('campaign_name')).split(' ')[4],
            'reach': int(data.get('reach')),
            'spending': spend_usd,
            'clicks': clicks
        }
        formated_facebook_ads_data_db.append(formated_date)

    try:
        async with async_session_maker() as session:
            await insert_facebook_ads_data(data=formated_facebook_ads_data_db, session=session)
            logger.success("Данные вставлены в бд")

    except Exception as e:
        logger.error(f'Пизда - {e}')


async def main():
    await facebook_pars()

if '__main__' == __name__:

    asyncio.run(main())