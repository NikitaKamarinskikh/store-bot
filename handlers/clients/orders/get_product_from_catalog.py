from typing import List, Tuple
from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp, bot
from messages_texts import OrdersMessagesText
from keyboards.inline.product_markups import categories_markup, categories_callback,\
    subcategories_markup, subcategories_callback
from keyboards.default.products_markups import get_product_from_catalog_markup
from keyboards.default.make_order_markup import make_order_markup
from states.clients.make_order import GetProductFromCatalogStates
from web.products.models import ProductImages
from db_api import products as products_model, basket
from keyboards.inline import product_markups
from states.clients.make_order import GetProductFromCatalogStates
from messages_texts import GET_BACK_MESSAGE_TEXT, CATALOG_MESSAGE_TEXT


@dp.message_handler(text=GET_BACK_MESSAGE_TEXT,
                    state=[GetProductFromCatalogStates.get_category,
                           GetProductFromCatalogStates.get_subcategory,
                           GetProductFromCatalogStates.chose_product])
async def get_back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    state_data = await state.get_data()
    if current_state == 'GetProductFromCatalogStates:get_category':
        await message.answer(
            CATALOG_MESSAGE_TEXT,
            reply_markup=make_order_markup
        )
        await state.finish()
    elif current_state == 'GetProductFromCatalogStates:get_subcategory':
        await _ask_category(message)
    elif current_state == 'GetProductFromCatalogStates:chose_product':
        await _ask_subcategory(message, state)


@dp.message_handler(text=OrdersMessagesText.catalog)
async def catalog(message: types.Message):
    await _ask_category(message)


@dp.callback_query_handler(categories_callback.filter(), state=GetProductFromCatalogStates.get_category)
async def get_category(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    category_id = callback_data.get('id')
    await state.update_data(category_id=category_id)
    await _ask_subcategory(callback.message, state)


@dp.callback_query_handler(subcategories_callback.filter(), state=GetProductFromCatalogStates.get_subcategory)
async def get_subcategory(callback: types.Message, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    category_id = state_data.get('category_id')
    subcategory_id = callback_data.get('id')
    products = products_model.get_products_by_category_and_subcategory(category_id, subcategory_id)

    products_ids_list = [product.pk for product in products]
    await state.update_data(products_ids_list=products_ids_list, additional_products_list=[])
    
    product = products[0]
    markup = product_markups.chose_product_markup(product.pk, 0, product.additional_products.all(),len(products))

    product_images = products_model.get_product_images_by_product_id(product.pk)
    if product_images:
        album = _collect_image_files_to_media_group(product_images)
        images_id = await callback.message.answer_media_group(album)
        await state.update_data(images_id=images_id)
    else:
        await state.update_data(images_id=None)
    r = await callback.message.answer(
        text=f'{product.name}\n{product.description}',
        reply_markup=markup
    )
    await state.update_data(menu_message_id=r.message_id)
    await GetProductFromCatalogStates.chose_product.set()


@dp.callback_query_handler(product_markups.next_product_callback.filter(), state=GetProductFromCatalogStates.chose_product)
async def next_product(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    index = int(callback_data.get('index'))
    state_data = await state.get_data()
    products_ids_list = state_data.get('products_ids_list')
    images_id = state_data.get('images_id')
    next_product_id = products_ids_list[index]
    product = products_model.get_product_by_id(next_product_id)

    markup = product_markups.chose_product_markup(next_product_id, index, product.additional_products.all(), len(products_ids_list))
    product_images = products_model.get_product_images_by_product_id(product.pk)
    if images_id:
        for image_id in images_id:
            await bot.delete_message(
                chat_id=callback.from_user.id,
                message_id=image_id.message_id
            )
        await state.update_data(images_id=None)
    if product_images:
        album = _collect_image_files_to_media_group(product_images)
        images_id = await callback.message.answer_media_group(album)
        menu_message_id = state_data.get('menu_message_id')
        await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=menu_message_id
        )
        r = await callback.message.answer(
            text=f'{product.name}\n{product.description}',
            reply_markup=markup
        )
        await state.update_data(images_id=images_id, menu_message_id=r.message_id)
    else:
        menu_message_id = state_data.get('menu_message_id')
        await bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=menu_message_id,
            text=f'{product.name}\n{product.description}',
            reply_markup=markup
        )


@dp.callback_query_handler(product_markups.additional_product_callback.filter(), state=GetProductFromCatalogStates.chose_product)
async def add_additional_product(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    id = callback_data.get('id')
    product_id = callback_data.get('product_id')
    additional_products_list = state_data.get('additional_products_list')
    additional_products_list.append(
        (int(product_id), int(id))
    )
    await state.update_data(additional_products_list=additional_products_list)



@dp.callback_query_handler(product_markups.add_product_to_basket_callback.filter(), state=GetProductFromCatalogStates.chose_product)
async def add_product_to_basket(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    product_id = callback_data.get('product_id')

    state_data = await state.get_data()
    additional_products_list = state_data.get('additional_products_list')
    additional_products_ids = _get_additional_products_ids_from_chosen_additional_products(additional_products_list, int(product_id))

    basket.add(callback.from_user.id, product_id, additional_products_ids)


def _get_additional_products_ids_from_chosen_additional_products(additional_products: List[Tuple[int, int]], product_id: int) -> List[int]:
    additional_products_ids = list()
    for item in additional_products:
        if item[0] == product_id:
            additional_products_ids.append(item[1])
    return additional_products_ids


def _collect_image_files_to_media_group(product_images: List[ProductImages]) -> types.MediaGroup():
    album = types.MediaGroup()
    for product_image in product_images:
        album.attach_photo(product_image.telegram_id)
    return album


async def _ask_category(message: types.Message) -> None:
    categories = products_model.get_all_categories()
    await message.answer(
        'Выберите категорию',
        reply_markup=get_product_from_catalog_markup
    )
    await message.answer(
        'Список доступных категорий',
        reply_markup=categories_markup(categories)
    )
    await GetProductFromCatalogStates.get_category.set()


async def _ask_subcategory(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    category_id = state_data.get('category_id')
    subcategories = products_model.get_subcategories_by_category_id(category_id)
    await message.answer(
        'Выберите подкатегорию',
        reply_markup=subcategories_markup(subcategories)
    )
    await GetProductFromCatalogStates.get_subcategory.set()








