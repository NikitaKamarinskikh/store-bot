from aiogram import types
from aiogram.dispatcher import FSMContext
from messages_texts import OrdersMessagesText
from states.clients.make_order import WholesaleOrder
from keyboards.default.main_markup import main_markup
from main import dp


@dp.message_handler(text=OrdersMessagesText.wholesale_order)
async def ask_product_description(message: types.Message):
    await message.answer(
        'Напишите что вам нужно и сколько единиц каждой позиции. В зависимости от количества скидка составит от 5 до 20%'
    )
    await WholesaleOrder.get_wholesale_order_info.set()


@dp.message_handler(state=WholesaleOrder.get_wholesale_order_info)
async def get_product_description(message: types.Message, state: FSMContext):
    product_description = message.text
    await state.update_data(product_description=product_description)
    await message.answer('Как вас зовут?')
    await WholesaleOrder.get_full_name.set()


@dp.message_handler(state=WholesaleOrder.get_full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    client_full_name = message.text
    await state.update_data(client_full_name=client_full_name)
    await message.answer('Укажите контактный телефон')
    await WholesaleOrder.get_phone_number.set()


@dp.message_handler(state=WholesaleOrder.get_phone_number)
async def get_phone_number(message: types.Message, state:FSMContext):
    phone_number = message.text
    await state.finish()
    await message.answer(
        'done',
        reply_markup=main_markup
    )

