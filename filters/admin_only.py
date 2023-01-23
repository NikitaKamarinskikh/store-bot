from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class AdminOnly(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        return True


