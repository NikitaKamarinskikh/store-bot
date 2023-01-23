from aiogram import Dispatcher
from .admin_only import AdminOnly


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminOnly)



