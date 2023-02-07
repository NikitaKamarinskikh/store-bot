from aiogram import types
from main import dp
from commands import GET_TELEGRAM_ID_COMMAND


@dp.message_handler(commands=[GET_TELEGRAM_ID_COMMAND])
async def get_telegram_id(message: types.Message):
    await message.answer(f'Ваш ID в телеграмме: {message.from_user.id}')




