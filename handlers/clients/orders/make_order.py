from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from messages_texts import MainMenuMessagesTexts
from keyboards.default.make_order_markup  import make_order_markup
from states.clients.make_order import MakeOrderStates
from re import match
from messages_texts import CATALOG_MESSAGE_TEXT
from db_api import basket


@dp.message_handler(text=MainMenuMessagesTexts.make_order)
async def start_making_order(message: types.Message):
    basket_info = basket.get_info(message.from_user.id)
    await message.answer(
        CATALOG_MESSAGE_TEXT,
        reply_markup=make_order_markup(basket_info.as_string())
    )



