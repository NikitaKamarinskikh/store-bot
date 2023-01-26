from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from messages_texts import MainMenuMessagesTexts


@dp.message_handler(text=MainMenuMessagesTexts.catalog)
async def show_catalog(message: types.Message):
    await message.answer('Catalog')

