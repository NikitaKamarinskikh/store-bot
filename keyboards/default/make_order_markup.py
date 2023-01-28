from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from messages_texts import OrdersMessagesText



make_order_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(OrdersMessagesText.catalog), KeyboardButton(OrdersMessagesText.product_not_in_catalog)],
        [KeyboardButton(OrdersMessagesText.wholesale_order), KeyboardButton(OrdersMessagesText.back)],
        [KeyboardButton(OrdersMessagesText.backet)],
    ],
    resize_keyboard=True
)




