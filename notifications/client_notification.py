from common import send_message



async def notify_client_about_new_referral(client_telegram_id: int, bonus_coins_quantity: int) -> None:
    text = f'Ваш друг зарегистрировался по вашей ссылке. При первом заказе вам будет начислено {bonus_coins_quantity} монет. Спасибо за доверие.'
    await send_message(client_telegram_id, text)


async def notify_client_about_firts_order_of_his_referral(client_telegram_id: int, bonus_coins_quantity: int) -> None:
    text = f'Вам начислено {bonus_coins_quantity} монет за первый заказ друга'
    await send_message(client_telegram_id, text)


async def notify_client_about_new_order_of_his_referral(client_telegram_id: int, bonus_coins_quantity: int) -> None:
    text = f'Вам начислено {bonus_coins_quantity} монет за заказ вашим другом'
    await send_message(client_telegram_id, text)


async def notify_client_about_product_in_basket(client_telegram_id: int) -> None:
    text = 'Внимание! В вашей корзине находятся неоформленные товары!'
    await send_message(client_telegram_id, text)





