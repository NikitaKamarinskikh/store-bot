from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from web.transport_companies.models import TransportCompanies


transport_companies_callback = CallbackData('transport_companies', 'transport_company_id')


def transport_companies_markup(transport_companies: List[TransportCompanies]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3)
    for transport_company in transport_companies:
        markup.insert(
            InlineKeyboardButton(
                text=transport_company.name,
                callback_data=transport_companies_callback.new(transport_company.pk)
            )
        )
    return markup


