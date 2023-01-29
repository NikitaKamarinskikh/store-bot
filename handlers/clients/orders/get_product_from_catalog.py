from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from messages_texts import OrdersMessagesText
from keyboards.inline.product_markups import categories_markup, categories_callback,\
    subcategories_markup, subcategories_callback
from states.clients.make_order import GetProductFromCatalogStates
from db_api import products as products_model


@dp.message_handler(text=OrdersMessagesText.catalog)
async def catalog(message: types.Message):
    categories = products_model.get_all_categories()
    await message.answer(
        'Выберите категорию',
        reply_markup=categories_markup(categories)
    )
    await GetProductFromCatalogStates.get_category.set()


@dp.callback_query_handler(categories_callback.filter(), state=GetProductFromCatalogStates.get_category)
async def get_category(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    category_id = callback_data.get('id')
    await state.update_data(category_id=category_id)
    subcategories = products_model.get_subcategories_by_category_id(category_id)
    await callback.message.answer(
        'Выберите подкатегорию',
        reply_markup=subcategories_markup(subcategories)
    )
    await GetProductFromCatalogStates.get_subcategory.set()


@dp.callback_query_handler(subcategories_callback.filter(), state=GetProductFromCatalogStates.get_subcategory)
async def get_subcategory(callback: types.Message, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    category_id = state_data.get('category_id')
    subcategory_id = callback_data.get('id')
    products = products_model.get_products_by_category_and_subcategory(category_id, subcategory_id)

    for product in products:
        print(product)
        print(product.additional_products.all())






