from __future__ import annotations
from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from web.products.models import Categories, Subcategories


categories_callback = CallbackData('categories', 'id')
subcategories_callback = CallbackData('subcategories', 'id')


def categories_markup(categories: List[Categories]) -> InlineKeyboardMarkup:
    return _create_markup(categories, categories_callback)


def subcategories_markup(subcategories: List[Subcategories]) -> InlineKeyboardMarkup:
    return _create_markup(subcategories, subcategories_callback)


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





