from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from messages_texts import MainMenuMessagesTexts
from config import BasketInfo


def create_main_markup(basket_info: BasketInfo = None) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(MainMenuMessagesTexts.make_order), KeyboardButton(MainMenuMessagesTexts.search_product)],
            [KeyboardButton(MainMenuMessagesTexts.bonuses), KeyboardButton(MainMenuMessagesTexts.info)],
        ],
        resize_keyboard=True
    )
    if basket_info is not None and basket_info.has_products():
        markup.add(
            KeyboardButton(basket_info.as_string())
        )
    return markup




