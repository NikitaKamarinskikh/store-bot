from datetime import datetime, timezone
from notifications.client_notification import notify_client_about_product_in_basket
from db_api import basket, clients as clients_model

HOUR_IN_SECONDS = 60 * 60
FIVE_OUR_IN_SECONDS = HOUR_IN_SECONDS * 5
DAY_IN_SECONDS = HOUR_IN_SECONDS * 24
THREE_DAYS_IN_SECONDS = DAY_IN_SECONDS * 3
WEEK_IN_SECONDS = DAY_IN_SECONDS * 7

COMPARATIVE_RANGE_IN_SECONDS = 60


async def check_basket():
    now = datetime.now(timezone.utc)
    clients = clients_model.get_all()
    for client in clients:
        client_basket_products = basket.get_products_by_client_telegram_id(client.telegram_id)
        if not client_basket_products:
            continue
        for product in client_basket_products:
            timedelta_in_seconds = (now - product.created_at).seconds

            if _is_notification_timedelta(timedelta_in_seconds):
                await notify_client_about_product_in_basket(client.telegram_id)
                break

            elif _is_critical_timedelta(timedelta_in_seconds):
                basket.clear(client.telegram_id)


def _is_notification_timedelta(timedelta: int) -> bool:
    return _is_almost_equal(timedelta, HOUR_IN_SECONDS) or\
            _is_almost_equal(timedelta, FIVE_OUR_IN_SECONDS) or\
            _is_almost_equal(timedelta, DAY_IN_SECONDS) or\
            _is_almost_equal(timedelta, THREE_DAYS_IN_SECONDS)


def _is_critical_timedelta(timedelta: int) -> bool:
    return _is_almost_equal(timedelta, WEEK_IN_SECONDS)


def _is_almost_equal(lhs: int, rhs: int, comparative_range: int = COMPARATIVE_RANGE_IN_SECONDS) -> bool:
    return abs(lhs - rhs) in range(comparative_range)

