from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from messages_texts import MainMenuMessagesTexts



main_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(MainMenuMessagesTexts.make_order), KeyboardButton(MainMenuMessagesTexts.catalog)],
        [KeyboardButton(MainMenuMessagesTexts.bonuses), KeyboardButton(MainMenuMessagesTexts.info)],
    ],
    resize_keyboard=True
)



