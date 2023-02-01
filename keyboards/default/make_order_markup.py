from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from messages_texts import OrdersMessagesText


def make_order_markup(basket_info: str) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(OrdersMessagesText.catalog), KeyboardButton(OrdersMessagesText.product_not_in_catalog)],
            [KeyboardButton(OrdersMessagesText.wholesale_order), KeyboardButton(OrdersMessagesText.back)],
            [KeyboardButton(basket_info)],
        ],
        resize_keyboard=True
    )
    return  markup




