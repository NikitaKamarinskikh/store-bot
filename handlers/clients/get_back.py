from aiogram import types
from aiogram.dispatcher import FSMContext

from main import dp
from messages_texts import GET_BACK_MESSAGE_TEXT, MAIN_MENU_TEXT
from keyboards.default.main_markup import create_main_markup
from db_api import basket as basket_model


@dp.message_handler(text=GET_BACK_MESSAGE_TEXT, state='*')
async def to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    basket_info = basket_model.get_info(message.from_user.id)
    await message.answer(
        MAIN_MENU_TEXT,
        reply_markup=create_main_markup(basket_info)
    )




