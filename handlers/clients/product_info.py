from typing import List, Union
from aiogram import types
from web.products.models import Products, ProductImages
from main import dp, bot
from keyboards.inline.product_markups import product_info_callback, add_product_to_basket_markup
from db_api import products as products_model


@dp.callback_query_handler(product_info_callback.filter(), state='*')
async def show_product_info(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    product_id = callback_data.get('product_id')
    product = products_model.get_product_by_id(product_id)
    product_info = _get_product_info(product)

    additional_products = products_model.get_additional_products_by_product_id(product.pk)
    product_images = products_model.get_product_images_by_product_id(product.pk)

    album = _get_photo_album(product_images)
    if album is not None:
        if callback.message is None: # request form inline query
            await bot.send_media_group(
                chat_id=callback.from_user.id,
                media=album
            )
        else:
            await callback.message.answer_media_group(album)

    if callback.message is None: # request form inline query
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=product_info,
            reply_markup=add_product_to_basket_markup(product.pk, additional_products)
        )
    else:
        await callback.message.answer(
            product_info,
            reply_markup=add_product_to_basket_markup(product.pk, additional_products)
        )


def _get_product_info(product: Products) -> str:
    info = f'<b>{product.name}</b> \n{product.description}'
    if product.sizes:
        info += f'Размеры: {product.sizes}'
    return info


def _get_photo_album(product_images: List[ProductImages]) -> Union[types.MediaGroup, None]:
    if product_images[0] is None and product_images[1] is None:
        return None
    album = types.MediaGroup()
    for product_image in product_images:
        album.attach_photo(product_image.telegram_id)
    return album


