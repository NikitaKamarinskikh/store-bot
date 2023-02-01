from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from messages_texts import OrdersMessagesText, GET_BACK_MESSAGE_TEXT


get_product_from_catalog_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Корзина')],
        [KeyboardButton(GET_BACK_MESSAGE_TEXT)],
    ],
    resize_keyboard=True
)






