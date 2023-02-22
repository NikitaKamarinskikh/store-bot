from aiogram import types
from aiogram.dispatcher import FSMContext
from messages_texts import OrdersMessagesText
from states.clients.make_order import WholesaleOrder
from keyboards.default.main_markup import create_main_markup
from db_api import basket as basket_model
from main import dp
from messages_texts import GET_BACK_MESSAGE_TEXT, MAIN_MENU_TEXT
from notifications.managers import notify_managers_about_wholesale_order


@dp.message_handler(text=GET_BACK_MESSAGE_TEXT,
                    state=[WholesaleOrder.get_wholesale_order_info,
                           WholesaleOrder.get_full_name,
                           WholesaleOrder.get_phone_number,])
async def get_back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'WholesaleOrder:get_wholesale_order_info':
        basket_info = basket_model.get_info(message.from_user.id)
        await message.answer(
            MAIN_MENU_TEXT,
            reply_markup=create_main_markup(basket_info)
        )
        await state.finish()
    elif current_state == 'WholesaleOrder:get_full_name':
        await message.answer(
            'Напишите что вам нужно и сколько единиц каждой позиции. В зависимости от количества скидка составит от 5 до 20%'
        )
        await WholesaleOrder.get_wholesale_order_info.set()
    elif current_state == 'WholesaleOrder:get_phone_number':
        await _ask_full_name(message)


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
    await _ask_full_name(message)


@dp.message_handler(state=WholesaleOrder.get_full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    client_full_name = message.text
    await state.update_data(client_full_name=client_full_name)
    await _ask_phone_number(message)


@dp.message_handler(state=WholesaleOrder.get_phone_number)
async def get_phone_number(message: types.Message, state:FSMContext):
    phone_number = message.text
    state_data = await state.get_data()
    text = f'Новый запрос на оптовый заказ\nОписание: {state_data.get("product_description")}\nФИО: {state_data.get("client_full_name")}\nТелефон: {phone_number}'
    await notify_managers_about_wholesale_order(text)
    baslet_info = basket_model.get_info(message.from_user.id)
    await message.answer(
        'Данные успешно отправлены менеджеру',
        reply_markup=create_main_markup(baslet_info)
    )
    await state.finish()


async def _ask_full_name(message: types.Message) -> None:
    await message.answer('Как вас зовут?')
    await WholesaleOrder.get_full_name.set()


async def _ask_phone_number(message: types.Message) -> None:
    await message.answer('Укажите контактный телефон')
    await WholesaleOrder.get_phone_number.set()

