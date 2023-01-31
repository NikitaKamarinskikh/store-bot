from __future__ import annotations
from typing import Union

from web.clients.models import Clients


def create(telegram_id: int | str, username: str | None) -> Clients:
    return Clients.objects.create(
        telegram_id=telegram_id,
        username=username
    )


def get_by_telegram_id_or_none(telegram_id: int | str) -> Union[Clients, None]:
    return Clients.objects.filter(telegram_id=telegram_id).first()


def get_client_referrals_quantity(client_telegrm_id: int) -> int:
    client = Clients.objects.get(telegram_id=client_telegrm_id)
    return Clients.objects.filter(referrer=client).count()


