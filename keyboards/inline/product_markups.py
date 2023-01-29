from __future__ import annotations
from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from web.products.models import Categories, Subcategories, Products

NEXT_PRODUCT_BUTTON_LABEL = '>>'
PREVIOUS_PRODUCT_BUTTON_LABEL = '<<'

categories_callback = CallbackData('categories', 'id')
subcategories_callback = CallbackData('subcategories', 'id')
chosen_product_callback = CallbackData('chosen_product', 'product_id')
next_product_callback = CallbackData('next_product', 'index')


def categories_markup(categories: List[Categories]) -> InlineKeyboardMarkup:
    return _create_markup(categories, categories_callback)


def subcategories_markup(subcategories: List[Subcategories]) -> InlineKeyboardMarkup:
    return _create_markup(subcategories, subcategories_callback)


def chose_product_markup(product_id: int, current_product_index: int, products_quantity: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text='Добавить в корзину',
            callback_data=chosen_product_callback.new(product_id)
        )
    )
    if current_product_index == 0:
        if products_quantity > 1:
            markup.add(
                InlineKeyboardButton(
                    text=NEXT_PRODUCT_BUTTON_LABEL,
                    callback_data=next_product_callback.new(current_product_index + 1)
                )
            )
    elif current_product_index + 1 == products_quantity:
        markup.add(
               InlineKeyboardButton(
                    text=PREVIOUS_PRODUCT_BUTTON_LABEL,
                    callback_data=next_product_callback.new(current_product_index - 1)
                )
        )
    else:
        markup.add(
            InlineKeyboardButton(
                text=PREVIOUS_PRODUCT_BUTTON_LABEL,
                callback_data=next_product_callback.new(current_product_index - 1)
            )
        )
        markup.insert(
            InlineKeyboardButton(
                text=NEXT_PRODUCT_BUTTON_LABEL,
                callback_data=next_product_callback.new(current_product_index + 1)
            )
        )
        
        
    return markup



def _create_markup(sequence: List[Categories | Subcategories], callback: CallbackData) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3)
    for item in sequence:
        markup.insert(
            InlineKeyboardButton(
                text=item.name,
                callback_data=callback.new(item.pk)
            )
        )
    return markup





