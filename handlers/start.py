from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from main import dp


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer("Bot started")



