from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from messages_texts import GET_BACK_MESSAGE_TEXT, MAIN_MENU_TEXT
from keyboards.default.main_markup import main_markup


@dp.message_handler(text=GET_BACK_MESSAGE_TEXT, state='*')
async def to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        MAIN_MENU_TEXT,
        reply_markup=main_markup
    )




