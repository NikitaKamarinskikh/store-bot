from typing import List, Tuple
from aiogram import types
from aiogram.dispatcher import FSMContext
from web.products.models import Products
from main import dp, bot
from messages_texts import OrdersMessagesText
from keyboards.inline.product_markups import categories_markup, categories_callback,\
    subcategories_markup, subcategories_callback, products_pair_markup, products_pair_callback, add_product_to_basket_markup
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
                           GetProductFromCatalogStates.chose_product,
                           GetProductFromCatalogStates.get_product_quantity
                           ])
async def get_back(message: types.Message, state: FSMContext):
    """
    TODO:
        - must be refactored
    """
    current_state = await state.get_state()
    basket_info = basket.get_info(message.from_user.id)
    state_data = await state.get_data()
    category_id = state_data.get('category_id')
    if category_id is None:
        await message.answer(
            CATALOG_MESSAGE_TEXT,
            reply_markup=make_order_markup(basket_info.as_string())
        )
        await state.finish()
        return
    if current_state == 'GetProductFromCatalogStates:get_category':
        await message.answer(
            CATALOG_MESSAGE_TEXT,
            reply_markup=make_order_markup(basket_info.as_string())
        )
        await state.finish()
    elif current_state == 'GetProductFromCatalogStates:get_subcategory':
        await _ask_category(message)
    elif current_state == 'GetProductFromCatalogStates:chose_product':
        subcategories = products_model.get_subcategories_by_category_id(category_id)
        if len(subcategories) != 0:
            await _ask_subcategory(message, state)
        else:
            await _ask_category(message)
    elif current_state == 'GetProductFromCatalogStates:get_product_quantity':
        subcategories = products_model.get_subcategories_by_category_id(category_id)
        if len(subcategories) != 0:
            await _ask_subcategory(message, state)
        else:
            await _ask_category(message)


@dp.message_handler(text=OrdersMessagesText.catalog)
async def catalog(message: types.Message):
    await _ask_category(message)


@dp.callback_query_handler(categories_callback.filter(), state=GetProductFromCatalogStates.get_category)
async def get_category(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    category_id = callback_data.get('id')
    await state.update_data(category_id=category_id)
    subcategories = products_model.get_subcategories_by_category_id(category_id)
    if len(subcategories) != 0:
        await _ask_subcategory(callback.message, state)
    else:
        await state.update_data(subcategory_id=None, current_product_index=0)
        await _show_product(callback, state)
        await GetProductFromCatalogStates.chose_product.set()


@dp.callback_query_handler(subcategories_callback.filter(), state=GetProductFromCatalogStates.get_subcategory)
async def get_subcategory(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    await state.update_data(subcategory_id=callback_data.get('id'), current_product_index=0)
    await _show_product(callback, state)
    await GetProductFromCatalogStates.chose_product.set()


@dp.callback_query_handler(product_markups.next_product_callback.filter(), state=GetProductFromCatalogStates.chose_product)
async def next_product(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    next_product_index = int(callback_data.get('next_product_index'))
    await state.update_data(current_product_index=next_product_index)
    await _show_product(callback, state)


async def _show_product(callback: types.CallbackQuery, state: FSMContext) -> None:
    state_data = await state.get_data()
    category_id = state_data.get('category_id')
    subcategory_id = state_data.get('subcategory_id')
    current_product_index = state_data.get('current_product_index')
    images_id = state_data.get('images_id')
    products = products_model.get_products_by_category_or_category_and_subcategory(category_id, subcategory_id)
    product = products[current_product_index]
    product_image = products_model.get_first_image(product.pk)

    if images_id is not None:
        for image_id in images_id:
            await bot.delete_message(
                chat_id=callback.from_user.id,
                message_id=image_id.message_id
            )
            await state.update_data(images_id=None)
    await callback.message.delete()

    if product_image is not None:
        album = _image_to_album(product_image)
        images_id = await callback.message.answer_media_group(media=album)
        await state.update_data(images_id=images_id)
    else:
        await state.update_data(images_id=None)

    await callback.message.answer(
        product.name,
        reply_markup=product_markups.chose_product_markup(
            product.pk,
            current_product_index,
            len(products)
        )
    )


def _image_to_album(image: ProductImages) -> types.MediaGroup:
    album = types.MediaGroup()
    album.attach_photo(image.telegram_id)
    return album


@dp.callback_query_handler(product_markups.additional_product_callback.filter(), state='*')
async def add_additional_product(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    additional_product_id = callback_data.get('id')
    product_id = callback_data.get('product_id')
    additional_products_list = state_data.get('additional_products_list')
    if additional_products_list is None:
        additional_products_list = []
    
    if _is_additional_product_chosen(additional_products_list, int(additional_product_id)):
        additional_products_list = _remove_additional_product(additional_products_list, int(additional_product_id))
    else:
        additional_products_list.append(
            (int(product_id), int(additional_product_id))
        )

    await state.update_data(additional_products_list=additional_products_list)

    chosen_additional_products = [i[1] for i in additional_products_list]
    additional_products = products_model.get_additional_products_by_product_id(product_id)

    if callback.message is not None:
        await callback.message.edit_reply_markup(
            reply_markup=add_product_to_basket_markup(product_id, additional_products, chosen_additional_products)
        )
    else: # Request from inline mode
        await bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=add_product_to_basket_markup(product_id, additional_products, chosen_additional_products)
        )


def _remove_additional_product(additional_products, additional_product_id: int):
    new_additional_products = []
    for item in additional_products:
        if item[1] != additional_product_id:
            new_additional_products.append(item)
    return new_additional_products


def _is_additional_product_chosen(additional_products, additional_product_id: int) -> bool:
    for item in additional_products:
        if item[1] == additional_product_id:
            return True
    return False


@dp.callback_query_handler(product_markups.add_product_to_basket_callback.filter(), state='*')
async def add_product_to_basket(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    product_id = callback_data.get('product_id')
    await state.update_data(product_id=product_id)
    if callback.message is not None:
        await _ask_product_quantity(callback.message)
    else: # Request from inline mode
        await bot.send_message(
            chat_id=callback.from_user.id,
            text='Укажите количество товара'
        )
        await GetProductFromCatalogStates.get_product_quantity.set()


@dp.message_handler(state=GetProductFromCatalogStates.get_product_quantity)
async def get_product_quantity(message: types.Message, state: FSMContext):
    product_quantity = message.text
    if product_quantity.isdigit():
        await state.update_data(product_quantity=int(product_quantity))
        await _add_product_to_basket(message, state)
    else:
        await message.answer('Количество товара должно быть указано числом')


async def _add_product_to_basket(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    product_id = state_data.get('product_id')
    additional_products_list = state_data.get('additional_products_list')
    product_quantity = state_data.get('product_quantity')
    additional_products_ids = _get_additional_products_ids_from_chosen_additional_products(additional_products_list, int(product_id))

    basket.add(message.from_user.id, product_id, additional_products_ids, product_quantity)

    basket_info = basket.get_info(message.from_user.id)
    
    await message.answer(
        f'Товар успешно добавлен в корзину',
        reply_markup=get_product_from_catalog_markup(basket_info.as_string())
    )


async def _ask_product_quantity(message: types.Message) -> None:
    await message.answer('Укажите количество товара')
    await GetProductFromCatalogStates.get_product_quantity.set()


def _get_additional_products_ids_from_chosen_additional_products(additional_products: List[Tuple[int, int]], product_id: int) -> List[int]:
    if not additional_products:
        return []
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
    basket_info = basket.get_info(message.from_user.id)
    await message.answer(
        'Выберите категорию',
        reply_markup=get_product_from_catalog_markup(basket_info.as_string())
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





