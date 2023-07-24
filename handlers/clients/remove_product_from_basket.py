from aiogram import types
from aiogram.dispatcher import FSMContext

from main import dp
from keyboards.inline.orders_markups import remove_product_callback, basket_product_callback, basket_products_markup,\
    make_order_markup
from keyboards.default.main_markup import create_main_markup
from db_api import basket as basket_model
from .basket import format_basket_products


@dp.callback_query_handler(remove_product_callback.filter(), state='*')
async def chose_removal_additional_products(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    products = basket_model.get_products_by_client_telegram_id(callback.from_user.id)
    await callback.message.answer(
        'Выберите товар',
        reply_markup=basket_products_markup(products)
    )


@dp.callback_query_handler(basket_product_callback.filter(), state='*')
async def remove_additional_product(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    basket_product_id = callback_data.get('product_id')
    basket_model.remove(basket_product_id)

    basket_products = basket_model.get_products_by_client_telegram_id(callback.from_user.id)
    
    if not basket_products:
        basket_info = basket_model.get_info(callback.from_user.id)
        await callback.message.answer(
            'Корзина пуста',
            reply_markup=create_main_markup(basket_info)
        )
        await state.finish()
        return

    info = format_basket_products(basket_products)
    basket_info = basket_model.get_info(callback.from_user.id)
    await callback.message.answer(
        'Товар успешно удален'
    )
    
    await callback.message.answer(
        f'У вас в корзине:\n{info}',
        reply_markup=make_order_markup()
    )



