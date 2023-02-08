from aiogram import types
from main import dp
from messages_texts import MainMenuMessagesTexts
from keyboards.inline.inline_mode_markup import switch_inline_query_current_chat_markup


@dp.message_handler(text=MainMenuMessagesTexts.search_product)
async def search_product(message: types.Message):
    await message.answer(
        'Для того чтобы начать поиск нажмите кнопку "поиск" и начинайте вводить то, что ищите.',
        reply_markup=switch_inline_query_current_chat_markup()
    )


