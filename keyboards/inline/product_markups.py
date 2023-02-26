from __future__ import annotations
from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from web.products.models import Categories, Subcategories, Products, AdditionalProducts


NEXT_PRODUCT_BUTTON_LABEL = '>>'
PREVIOUS_PRODUCT_BUTTON_LABEL = '<<'
ADD_PRODUCT_TO_BASKET_BUTTON_TEXT = 'Добавить в корзину'
PRODUCT_INFO_BUTTON_TEXT = 'Подробнее'


categories_callback = CallbackData('categories', 'id')
subcategories_callback = CallbackData('subcategories', 'id')
add_product_to_basket_callback = CallbackData('chosen_product', 'product_id')
next_product_callback = CallbackData('next_product', 'next_product_index')
additional_product_callback = CallbackData('additional_product', 'id', 'product_id')
products_pair_callback = CallbackData('products_pair', 'product_id')
product_info_callback = CallbackData('product_info', 'product_id')


def product_info_markup(product_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text=PRODUCT_INFO_BUTTON_TEXT,
            callback_data=product_info_callback.new(product_id)
        )
    )
    return markup


def categories_markup(categories: List[Categories]) -> InlineKeyboardMarkup:
    return _create_markup(categories, categories_callback)


def subcategories_markup(subcategories: List[Subcategories]) -> InlineKeyboardMarkup:
    return _create_markup(subcategories, subcategories_callback)


def products_pair_markup(products: List[Products]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    for product in products:
        markup.insert(
            InlineKeyboardButton(
                text=product.name,
                callback_data=products_pair_callback.new(product.pk)
            )
        )
    return markup


def add_product_to_basket_markup(product_id: int, additional_products: List[AdditionalProducts],
            chosen_additional_products: List[int] | None) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    for additional_product in additional_products:
        text = additional_product.name
        if chosen_additional_products is not None:
            if additional_product.pk in chosen_additional_products:
                text += ' ✅'
        markup.insert(
            InlineKeyboardButton(
                text=text,
                callback_data=additional_product_callback.new(additional_product.pk, product_id)
            )
        )
    markup.add(
        InlineKeyboardButton(
            text=ADD_PRODUCT_TO_BASKET_BUTTON_TEXT,
            callback_data=add_product_to_basket_callback.new(product_id)
        )
    )
    return markup


def chose_product_markup(product_id: int, current_product_index: int,
                         products_quantity: int,
                         ) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text=PRODUCT_INFO_BUTTON_TEXT,
            callback_data=product_info_callback.new(product_id)
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
    markup = InlineKeyboardMarkup(row_width=2)
    for item in sequence:
        markup.insert(
            InlineKeyboardButton(
                text=item.name,
                callback_data=callback.new(item.pk)
            )
        )
    return markup





