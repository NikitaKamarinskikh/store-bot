from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from messages_texts import GET_BACK_MESSAGE_TEXT



get_back_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(GET_BACK_MESSAGE_TEXT)],
    ],
    resize_keyboard=True
)


