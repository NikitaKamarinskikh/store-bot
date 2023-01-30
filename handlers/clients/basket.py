from typing import List
from re import match
from aiogram import types
from aiogram.dispatcher import FSMContext
from web.basket.models import BasketProducts
from main import dp
from messages_texts import OrdersMessagesText
from db_api import basket as basket_model, transport_companies as transport_companies_model
from keyboards.inline.orders_markups import make_order_markup, make_order_callback, confirm_order_markup, confirm_order_callback
from keyboards.inline.transport_companies import transport_companies_markup, transport_companies_callback
from states.clients.make_order import MakeOrderStates


@dp.message_handler(text=OrdersMessagesText.backet)
async def get_basket_products(message: types.Message, state: FSMContext):
    basket_products = basket_model.get_products_by_client_telegram_id(message.from_user.id)
    if not basket_products:
        await message.answer('Корзина пуста')
        return
    info = _format_basket_products(basket_products)
    await message.answer(
        f'У вас в корзине:\n{info}',
        reply_markup=make_order_markup()
    )


@dp.callback_query_handler(make_order_callback.filter())
async def start_making_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите ФИО на кого оформлять заказ при отправке')
    await MakeOrderStates.get_full_name.set()


@dp.message_handler(state=MakeOrderStates.get_full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    client_full_name = message.text
    await state.update_data(client_full_name=client_full_name)
    await message.answer('Укажите телефон получателя')
    await MakeOrderStates.get_phome_number.set()


@dp.message_handler(state=MakeOrderStates.get_phome_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    transport_companies = transport_companies_model.get_all()
    await state.update_data(phone_number=phone_number)
    await message.answer(
        'Выберите транспортную компанию',
        reply_markup=transport_companies_markup(transport_companies)
    )
    await MakeOrderStates.get_transport_company.set()


@dp.callback_query_handler(transport_companies_callback.filter(), state=MakeOrderStates.get_transport_company)
async def get_transport_company(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    transport_company_id = callback_data.get('id')
    await state.update_data(transport_company_id=transport_company_id)
    await callback.message.answer('Укажите адресс отправителя или центр выдачи')
    await MakeOrderStates.get_delivery_address.set()


@dp.message_handler(state=MakeOrderStates.get_delivery_address)
async def get_delivery_address(message: types.Message, state: FSMContext):
    delivery_address = message.text
    await state.update_data(delivery_address=delivery_address)
    await message.answer('Введите дату, желаемой готовности заказа')
    await MakeOrderStates.get_desired_completion_date.set()


@dp.message_handler(state=MakeOrderStates.get_desired_completion_date)
async def get_desired_completion_date(message: types.Message, state: FSMContext):
    desired_completion_date = message.text
    await state.update_data(desired_completion_date=desired_completion_date)
    await message.answer('Введите дату, последнего срока готовности товара')
    await MakeOrderStates.get_last_completion_date.set()


@dp.message_handler(state=MakeOrderStates.get_last_completion_date)
async def get_last_completion_date(message: types.Message, state: FSMContext):
    last_completion_date = message.text
    await state.update_data(last_completion_date=last_completion_date)
    await _show_order_payload(message, state)
    await MakeOrderStates.confirm_order.set()



async def _show_order_payload(message: types.Message, state: FSMContext) -> None:
    order_data = await _format_order_data(state)
    await message.answer(
        order_data,
        reply_markup=confirm_order_markup()
    )



async def _format_order_data(state: FSMContext) -> str:
    state_data = await state.get_data()
    client_full_name = state_data.get('client_full_name')
    phone_number = state_data.get('phone_number')
    transport_company_id = state_data.get('transport_company_id')
    transport_company = transport_companies_model.get_by_id(transport_company_id)
    delivery_address = state_data.get('delivery_address')
    desired_completion_date = state_data.get('desired_completion_date')
    last_completion_date = state_data.get('last_completion_date')
    return f'ФИО: {client_full_name}\nТел.: {phone_number}\nТранспортная компания: {transport_company}\n'+\
            f'Адрес отправления или центра выдачи: {delivery_address}\n:Желаемая дата готовности: {desired_completion_date}\n'+\
            f'Крайний срок готовности: {last_completion_date}'


def _format_basket_products(basket_products: List[BasketProducts]) -> str:
    products_info = ''
    product_number= 1
    for basket_product in basket_products:
        products_info += f'{product_number}. {basket_product.product.name} {basket_product.product.price}\n'
        additional_products = basket_product.additional_products
        for additional_product in additional_products.all():
            products_info += f'+ {additional_product.name} {additional_product.price}\n'
        product_number += 1
        products_info += '\n'
    return products_info


@dp.callback_query_handler(confirm_order_callback.filter(), state=MakeOrderStates.confirm_order)
async def confirm_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    print(state_data)



# {'client_full_name': 'фыв йцу фыв', 'phone_number': '198278433', 
# 'transport_company_id': '2', 'delivery_address': 'asdas',
# 'desired_completion_date': '123 ltrf,hz', 'last_completion_date': '12ew'}

