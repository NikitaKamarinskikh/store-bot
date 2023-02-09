from aiogram import types
from main import dp
from db_api import products as products_model
from keyboards.inline.product_markups import add_product_to_basket_markup


@dp.inline_handler()
async def query(query: types.InlineQuery):
    product_name = query.query
    if not product_name:
        return
    products = products_model.get_products_by_name_pattern(product_name)
    print(products)
    results = []
    for product in products:
        additional_products = products_model.get_additional_products_by_product_id(product.pk)
        image = products_model.get_first_image(product.pk)
        results.append(
            types.InlineQueryResultArticle(
                id=product.pk,
                title=product.name,
                input_message_content=types.InputTextMessageContent(
                    message_text=product.name,
                ),
                reply_markup=add_product_to_basket_markup(product.pk, additional_products)
            )
        )
        if image is not None:
            results.append(
                types.InlineQueryResultCachedPhoto(
                    id=product.pk * 100,
                    photo_file_id=image.telegram_id
                )
            )
    await query.answer(
        results=results,
        cache_time=3,
    )
    




