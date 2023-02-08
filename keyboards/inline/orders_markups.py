from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from web.transport_companies.models import TransportCompanies
from config import order_points


make_order_callback = CallbackData('make_order')
confirm_order_callback = CallbackData('confirm_order')
update_order_callback = CallbackData('update_order')
update_order_point_callback = CallbackData('update_order_point', 'order_point')


def make_order_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton(
            text='Оформить заказ',
            callback_data=make_order_callback.new(),
        )
    )
    return markup


def confirm_order_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text='Изменить',
            callback_data=update_order_callback.new()
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Верно',
            callback_data=confirm_order_callback.new()
        )
    )
    return markup


def update_order_points_markup() ->  InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for order_point, order_point_name in order_points.items():
        markup.add(
            InlineKeyboardButton(
                text=order_point_name,
                callback_data=update_order_point_callback.new(order_point)
            )
        )
    return markup
