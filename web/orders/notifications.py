import requests
from config import env


def notify_client_about_order_in_progress_status(client_telegram_id: int, order_id: int) -> None:
    message_text = f'Ваш заказ {order_id} подтвержден, передан в работу.'
    _send_message_by_telegram_bot_api(client_telegram_id, message_text)


def notify_client_about_order_in_delivery_status(client_telegram_id: int, order_id: int) -> None:
    message_text = f'Ваш заказ {order_id} готов, передан в доставку'
    _send_message_by_telegram_bot_api(client_telegram_id, message_text)


def notify_client_about_order_in_sent_status(client_telegram_id: int, order_id: int, track_number: str) ->  None:
    message_text = f'Ваш заказ {order_id} отправлен. Трек номер: {track_number}'
    _send_message_by_telegram_bot_api(client_telegram_id, message_text)


def _send_message_by_telegram_bot_api(client_telegram_id: int, text: str) -> None:
    bot_token = env.str('BOT_TOKEN')
    link = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=' \
            f'{client_telegram_id}&text={text}'
    requests.post(link)



