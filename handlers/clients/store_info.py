from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from messages_texts import MainMenuMessagesTexts


@dp.message_handler(text=MainMenuMessagesTexts.info)
async def store_info(message: types.Message):
    await message.answer('Store info')

