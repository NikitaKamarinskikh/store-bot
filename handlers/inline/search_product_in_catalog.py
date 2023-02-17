from aiogram import types
from main import dp
from db_api import products as products_model
from keyboards.inline.product_markups import product_info_markup
from config import MEDIA_URL


@dp.inline_handler()
async def query(query: types.InlineQuery):
    product_name = query.query
    if not product_name:
        return
    products = products_model.get_products_by_name_pattern(product_name)
    results = []
    for product in products:
        preview_url = None
        if product.preview_url is not None:
            f'{MEDIA_URL}{product.preview_url}'
        results.append(
            types.InlineQueryResultArticle(
                id=product.pk,
                title=product.name,
                input_message_content=types.InputTextMessageContent(
                    message_text=f'{product.name}',
                ),
                reply_markup=product_info_markup(product.pk),
                thumb_url=preview_url
            ),
        )
    await query.answer(
        results=results,
        cache_time=3,
    )
