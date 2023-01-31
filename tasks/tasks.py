import aioschedule
from asyncio import sleep

from .check_mailing import check_mailing
from .check_basket import check_basket


async def setup():
    aioschedule.every().minute.do(check_mailing)
    aioschedule.every().minute.do(check_basket)

    while True:
        await aioschedule.run_pending()
        await sleep(1)


