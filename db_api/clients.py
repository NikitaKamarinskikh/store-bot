from __future__ import annotations
from typing import Union, List

from web.clients.models import Clients


def create(telegram_id: int | str, username: str | None,
           bonus_coins_quantity: int | None = None,
           referrer_telegram_id: int | None = None
           ) -> Clients:
    if bonus_coins_quantity is None:
        bonus_coins_quantity = 0
    
    referrer = None
    if referrer_telegram_id is not None:
        referrer = Clients.objects.get(telegram_id=referrer_telegram_id)
    return Clients.objects.create(
        telegram_id=telegram_id,
        username=username,
        coins=bonus_coins_quantity,
        referrer=referrer
    )


def get_by_telegram_id_or_none(telegram_id: int | str) -> Union[Clients, None]:
    return Clients.objects.filter(telegram_id=telegram_id).first()


def get_client_referrals_quantity(client_telegrm_id: int) -> int:
    client = Clients.objects.get(telegram_id=client_telegrm_id)
    return Clients.objects.filter(referrer=client).count()


def add_coins(client_telegram_id: int, coins_quantity: int) -> Clients:
    client = Clients.objects.get(telegram_id=client_telegram_id)
    client.coins += coins_quantity
    client.save()
    return client


def get_all() -> List[Clients]:
    return list(Clients.objects.all())


def get_all_who_has_orders() -> List[Clients]:
    return Clients.objects.filter(orders_quantity__gt=0)


def get_all_who_has_no_order() -> List[Clients]:
    return Clients.objects.filter(orders_quantity=0)


def increment_orders_quantity(client_telegram_id: int) -> None:
    client = Clients.objects.get(telegram_id=client_telegram_id)
    client.orders_quantity = client.orders_quantity + 1
    client.save()



