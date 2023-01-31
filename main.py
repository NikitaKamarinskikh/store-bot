import asyncio
import config
from os import environ
from django import setup
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(dp):
    import filters
    filters.setup(dp)


def setup_django():
    environ.setdefault(
         'DJANGO_SETTINGS_MODULE',
         'web.web.settings',
    )
    environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': 'true'})
    setup()


if __name__ == '__main__':
    setup_django()
    from aiogram import executor
    from handlers import dp
    import tasks

    loop = asyncio.get_event_loop()
    loop.create_task(tasks.tasks.setup())

    executor.start_polling(
        dp,
        on_startup=on_startup
    )

