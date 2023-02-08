from aiogram import types
from main import dp
from db_api import products as products_model


@dp.inline_handler()
async def query(query: types.InlineQuery):
    product_name = query.query
    if not product_name:
        return
    products = products_model.get_products_by_name_pattern(product_name)
    results = []
    for product in products:
        results.append(
            types.InlineQueryResultArticle(
                id=product.pk,
                title=product.name,
                input_message_content=types.InputTextMessageContent(
                    message_text=product.name,
                ),
            )
        )
    await query.answer(
        results=results,
        cache_time=3
    )
    




