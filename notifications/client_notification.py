from main import bot



async def notify_client_about_new_referral(client_telegram_id: int, bonus_coins_quantity: int) -> None:
    text = f'Ваш друг зарегистрировался по вашей ссылке. При первом заказе вам будет начислено {bonus_coins_quantity} монет. Спасибо за доверие.'
    await _send_message(client_telegram_id, text)


async def notify_client_about_firts_order_of_his_referral(client_telegram_id: int, bonus_coins_quantity: int) -> None:
    text = f'Вам начислено {bonus_coins_quantity} монет за первый заказ друга'
    await _send_message(client_telegram_id, text)


async def notify_client_about_new_order_of_his_referral(client_telegram_id: int, bonus_coins_quantity: int) -> None:
    text = f'Вам начислено {bonus_coins_quantity} монет за заказ вашим другом'
    await _send_message(client_telegram_id, text)


async def notify_client_about_product_in_basket(client_telegram_id: int) -> None:
    text = 'Внимание! В вашей корзине находятся неоформленные товары!'
    await _send_message(client_telegram_id, text)


async def _send_message(chat_id: int, text: str) -> None:
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text
        )
    except:
        ...





