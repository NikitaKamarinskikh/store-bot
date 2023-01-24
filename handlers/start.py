from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from main import dp

from db_api import clients


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    client = clients.get_by_telegram_id_or_none(message.from_user.id)
    if client is None:
        clients.create(message.from_user.id, message.from_user.username)
        await message.answer('Добро пожаловать ...')
    else:
        await message.answer('Вы уже зарегистрированы в боте')



