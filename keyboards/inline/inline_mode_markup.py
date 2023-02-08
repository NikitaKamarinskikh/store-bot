from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def switch_inline_query_current_chat_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton(
            text='Поиск',
            switch_inline_query_current_chat=''
        )
    )
    return markup



