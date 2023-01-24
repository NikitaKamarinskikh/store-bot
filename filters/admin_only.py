from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from db_api import bot_admins


class AdminOnly(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        user = bot_admins.get_by_telegram_id_or_none(message.from_user.id)
        return user is not None


