from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def one_button_markup(button_text: str) ->ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(button_text)],
        ],
        resize_keyboard=True
    )


