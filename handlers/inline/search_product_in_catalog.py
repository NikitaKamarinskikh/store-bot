from aiogram import types
from main import dp


@dp.inline_handler(lambda inline_query: True)
async def empty_query(inline_query: types.InlineQuery):
    await inline_query.answer(
        results=[
            types.InlineQueryResultArticle(
                id='unknown',
                title='Введите запрос',
                input_message_content=types.InputTextMessageContent(
                    message_text='Не обязательно жать на кнопку'
                )
            )
        ],
        cache_time=5
    )






