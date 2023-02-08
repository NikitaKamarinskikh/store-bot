from typing import List
from re import match
from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from web.basket.models import BasketProducts
from main import dp
from messages_texts import OrdersMessagesText, GET_BACK_MESSAGE_TEXT, MAIN_MENU_TEXT
from db_api import basket as basket_model, transport_companies as transport_companies_model, orders as orders_model
from keyboards.inline.orders_markups import make_order_markup, make_order_callback, confirm_order_markup, confirm_order_callback, update_order_callback,\
    update_order_points_markup, update_order_point_callback
from keyboards.inline.transport_companies import transport_companies_markup, transport_companies_callback
from keyboards.default.get_back_mrkup import get_back_markup
from keyboards.default.main_markup import main_markup
from states.clients.make_order import MakeOrderStates, UpdateOrderStates
from notifications.managers import notify_managers_about_new_order
from config import OrderData


@dp.message_handler(text=GET_BACK_MESSAGE_TEXT,
                    state=[MakeOrderStates.get_recipient_full_name,
                           MakeOrderStates.get_recipient_phone_number,
                           MakeOrderStates.get_transport_company,
                           MakeOrderStates.get_delivery_address,
                           MakeOrderStates.get_desired_completion_date,
                           MakeOrderStates.get_last_completion_date,
                           MakeOrderStates.confirm_order])
async def get_back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'MakeOrderStates:get_recipient_full_name':
        await message.answer(
            MAIN_MENU_TEXT,
            reply_markup=main_markup
        )
        await state.finish()
    elif current_state == 'MakeOrderStates:get_recipient_phone_number':
        await _ask_recipient_full_name(message)
    elif current_state == 'MakeOrderStates:get_transport_company':
        await _ask_recipient_phone_number(message)
    elif current_state == 'MakeOrderStates:get_delivery_address':
        await _ask_transport_company(message)
    elif current_state == 'MakeOrderStates:get_desired_completion_date':
        await _ask_delivery_address(message)
    elif current_state == 'MakeOrderStates:get_last_completion_date':
        await _ask_desired_completion_date(message)
    elif current_state == 'MakeOrderStates:confirm_order':
        await _ask_last_completion_date(message)


@dp.message_handler(regexp='^Корзина.*$', state='*')
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


@dp.callback_query_handler(make_order_callback.filter(), state='*')
async def start_making_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await _ask_recipient_full_name(callback.message)


@dp.message_handler(state=MakeOrderStates.get_recipient_full_name)
async def get_recipient_full_name(message: types.Message, state: FSMContext):
    recipient_full_name = message.text
    await state.update_data(recipient_full_name=recipient_full_name)
    await _ask_recipient_phone_number(message)


@dp.message_handler(state=MakeOrderStates.get_recipient_phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    recipient_phone_number = message.text
    await state.update_data(recipient_phone_number=recipient_phone_number)
    await _ask_transport_company(message)


@dp.callback_query_handler(transport_companies_callback.filter(), state=MakeOrderStates.get_transport_company)
async def get_transport_company(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    transport_company_id = callback_data.get('transport_company_id')
    await state.update_data(transport_company_id=transport_company_id)
    await _ask_delivery_address(callback.message)


@dp.message_handler(state=MakeOrderStates.get_delivery_address)
async def get_delivery_address(message: types.Message, state: FSMContext):
    delivery_address = message.text
    await state.update_data(delivery_address=delivery_address)
    await _ask_desired_completion_date(message)


@dp.message_handler(state=MakeOrderStates.get_desired_completion_date)
async def get_desired_completion_date(message: types.Message, state: FSMContext):
    desired_completion_date = message.text
    await state.update_data(desired_completion_date=desired_completion_date)
    await _ask_last_completion_date(message)


@dp.message_handler(state=MakeOrderStates.get_last_completion_date)
async def get_last_completion_date(message: types.Message, state: FSMContext):
    last_completion_date = message.text
    await state.update_data(last_completion_date=last_completion_date)
    order_data = await _collect_order_data(message.from_user.id, state)
    await _show_order_data(message, order_data)
    await MakeOrderStates.confirm_order.set()


async def _ask_recipient_full_name(message: types.Message) -> None:
    await message.answer(
        'Введите ФИО на кого оформлять заказ при отправке',
        reply_markup=get_back_markup
    )
    await MakeOrderStates.get_recipient_full_name.set()


async def _ask_recipient_phone_number(message: types.Message) -> None:
    await message.answer('Укажите телефон получателя')
    await MakeOrderStates.get_recipient_phone_number.set()


async def _ask_transport_company(message: types.Message) -> None:
    transport_companies = transport_companies_model.get_all()
    await message.answer(
        'Выберите транспортную компанию',
        reply_markup=transport_companies_markup(transport_companies)
    )
    await MakeOrderStates.get_transport_company.set()


async def _ask_delivery_address(message: types.Message) -> None:
    await message.answer('Укажите адресс отправителя или центр выдачи')
    await MakeOrderStates.get_delivery_address.set()


async def _ask_desired_completion_date(message: types.Message) -> None:
    await message.answer('Введите дату, желаемой готовности заказа')
    await MakeOrderStates.get_desired_completion_date.set()


async def _ask_last_completion_date(message: types.Message) -> None:
    await message.answer('Введите дату, последнего срока готовности товара')
    await MakeOrderStates.get_last_completion_date.set()


async def _collect_order_data(client_telegram_id: int, state: FSMContext) -> OrderData:
    state_data = await state.get_data()
    return OrderData(
        client_telegram_id=client_telegram_id,
        recipient_full_name=state_data.get('recipient_full_name'),
        recipient_phone_number=state_data.get('recipient_phone_number'),
        transport_company_id=int(state_data.get('transport_company_id')),
        delivery_address=state_data.get('delivery_address'),
        desired_completion_date=state_data.get('desired_completion_date'),
        last_completion_date=state_data.get('last_completion_date')
    )


async def _show_order_data(message: types.Message, order_data: OrderData) -> None:
    order_data_text = _format_order_data(order_data)
    await message.answer(
        order_data_text,
        reply_markup=confirm_order_markup()
    )


def _format_order_data(order_data: OrderData) -> str:
    client_full_name = order_data.recipient_full_name
    recipient_phone_number = order_data.recipient_phone_number
    transport_company_id = order_data.transport_company_id
    transport_company = transport_companies_model.get_by_id(transport_company_id)
    delivery_address = order_data.delivery_address
    desired_completion_date = order_data.desired_completion_date
    last_completion_date = order_data.last_completion_date
    return f'ФИО: {client_full_name}\nТел.: {recipient_phone_number}\nТранспортная компания: {transport_company}\n'+\
            f'Адрес отправления или центра выдачи: {delivery_address}\nЖелаемая дата готовности: {desired_completion_date}\n'+\
            f'Крайний срок готовности: {last_completion_date}'


def _format_basket_products(basket_products: List[BasketProducts]) -> str:
    products_info = ''
    product_number= 1
    for basket_product in basket_products:
        products_info += f'{product_number} {basket_product.product.name} <i> {basket_product.product_quantity} шт. </i> {basket_product.product.price} руб.\n'
        additional_products = basket_product.additional_products
        for additional_product in additional_products.all():
            products_info += f'+ {additional_product.name} {additional_product.price} руб.\n'
        product_number += 1
        products_info += '\n'
    return products_info


@dp.callback_query_handler(confirm_order_callback.filter(), state=MakeOrderStates.confirm_order)
async def confirm_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    current_basket_info = basket_model.get_info(callback.from_user.id)
    order_data = await _collect_order_data(callback.from_user.id, state)
    basket_products = basket_model.get_products_by_client_telegram_id(callback.from_user.id)
    order_data.products = basket_products
    order_data.amount = current_basket_info.amount_in_rub

    order = orders_model.create(order_data)
    basket_products = basket_model.get_products_by_client_telegram_id(callback.from_user.id)
    order_info = f'Новый заказ\n{_format_basket_products(basket_products)}'
    await notify_managers_about_new_order(order_info)
    basket_model.clear(callback.from_user.id)

    await callback.message.answer(
        f'Ваш заказ {order.pk} оформлен, скоро с вами свяжутся.',
        reply_markup=main_markup
    )
    await state.finish()


@dp.callback_query_handler(update_order_callback.filter(), state=MakeOrderStates.confirm_order)
async def update_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        'Что вы хотите изменить?',
        reply_markup=update_order_points_markup()
    )
    await UpdateOrderStates.get_order_point.set()


@dp.callback_query_handler(update_order_point_callback.filter(), state=UpdateOrderStates.get_order_point)
async def get_order_point(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    order_point = callback_data.get('order_point')
    if order_point == 'receiver_full_name':
        await UpdateOrderStates.update_receiver_full_name.set()
        await callback.message.answer('Введите новые данные')
    elif order_point == 'receiver_phone_number':
        await UpdateOrderStates.update_receiver_phone_number.set()
        await callback.message.answer('Введите новые данные')
    elif order_point == 'transport_company':
        transport_companies = transport_companies_model.get_all()
        await callback.message.answer(
            'Выберите транспортную компанию',
            reply_markup=transport_companies_markup(transport_companies)
        )
        await UpdateOrderStates.update_transport_company.set()
    elif order_point == 'delivery_address':
        await UpdateOrderStates.update_delivery_address.set()
        await callback.message.answer('Введите новые данные')
    elif order_point == 'desired_completion_date':
        await UpdateOrderStates.update_desired_completion_date.set()
        await callback.message.answer('Введите новые данные')
    elif order_point == 'last_completion_date':
        await UpdateOrderStates.update_last_completion_date.set()
        await callback.message.answer('Введите новые данные')


@dp.message_handler(state=UpdateOrderStates.update_receiver_full_name)
async def update_receiver_full_name(message: types.Message, state: FSMContext):
    recipient_full_name = message.text
    await state.update_data(recipient_full_name=recipient_full_name)
    await _reask(message, state)


@dp.message_handler(state=UpdateOrderStates.update_receiver_phone_number)
async def update_receiver_phone_number(message: types.Message, state: FSMContext):
    recipient_phone_number = message.text
    await state.update_data(recipient_phone_number=recipient_phone_number)
    await _reask(message, state)


@dp.callback_query_handler(transport_companies_callback.filter(), state=UpdateOrderStates.update_transport_company)
async def update_transport_company(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    transport_company_id = callback_data.get('transport_company_id')
    await state.update_data(transport_company_id=transport_company_id)
    await _reask(callback.message, state)


@dp.message_handler(state=UpdateOrderStates.update_delivery_address)
async def update_delivery_address(message: types.Message, state: FSMContext):
    delivery_address = message.text
    await state.update_data(delivery_address=delivery_address)
    await _reask(message, state)


@dp.message_handler(state=UpdateOrderStates.update_desired_completion_date)
async def update_desired_completion_date(message: types.Message, state: FSMContext):
    desired_completion_date = message.text
    await state.update_data(desired_completion_date=desired_completion_date)
    await _reask(message, state)



@dp.message_handler(state=UpdateOrderStates.update_last_completion_date)
async def update_last_completion_date(message: types.Message, state: FSMContext):
    last_completion_date = message.text
    await state.update_data(last_completion_date=last_completion_date)
    await _reask(message, state)


async def _reask(message: types.Message, state: FSMContext) -> None:
    order_data = await _collect_order_data(message.from_user.id, state)
    await _show_order_data(message, order_data)
    await MakeOrderStates.confirm_order.set()




