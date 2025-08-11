import asyncio
import sys
from loguru import logger

from src.service.facebook_parsing import facebook_pars


async def main():
    await asyncio.gather(facebook_pars())

if __name__ == '__main__':
    logger.remove()  # Полная очистка
    logger.add('marketplace.log',
               level='INFO',
               format="{time:MM-DD HH:mm:ss} | {level} | {message}")
    logger.add(sys.stderr ,
               level='INFO',
               format="{time:MM-DD HH:mm:ss} | {level} | <cyan>{file}:{line}</cyan> | <u><white>{message}</white></u>",
               colorize=True)
    asyncio.run(main())