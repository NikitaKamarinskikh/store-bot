from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from messages_texts import MainMenuMessagesTexts
from keyboards.default.make_order_markup  import make_order_markup
from states.clients.make_order import MakeOrderStates
from re import match


@dp.message_handler(text=MainMenuMessagesTexts.make_order)
async def start_making_order(message: types.Message):
    await message.answer(
"""
1. Каталог - выбор в каталоге по категориям
2. Оптовый заказ - опишите что нужно и количество единиц
3. Нет в каталоге, но хотите заказать
4. Вернуться в главное меню
5. Посмотреть корзину
""",
    reply_markup=make_order_markup
    )



