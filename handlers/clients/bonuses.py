from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from messages_texts import MainMenuMessagesTexts


@dp.message_handler(text=MainMenuMessagesTexts.bonuses)
async def show_bonuses(message: types.Message):
    await message.answer('Bonuses')

