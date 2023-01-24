from __future__ import annotations
from typing import Union
from web.bot_admins.models import BotAdmins


def get_by_telegram_id_or_none(telegram_id: str | int) -> Union[BotAdmins, None]:
    return BotAdmins.objects.filter(telegram_id=telegram_id).first()



