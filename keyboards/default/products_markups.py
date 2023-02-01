from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from messages_texts import OrdersMessagesText, GET_BACK_MESSAGE_TEXT


def get_product_from_catalog_markup(basket_info: str) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(basket_info)],
            [KeyboardButton(GET_BACK_MESSAGE_TEXT)],
        ],
        resize_keyboard=True
    )
    return markup






