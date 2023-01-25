from environs import Env
from enum import Enum

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")


class OrderStatuses(str, Enum):
    PROCESSED = 'Обработан'
    PAID = 'Оплачен'
    REJECTED = 'Откланен'

    @classmethod
    def choices(cls) -> tuple:
        return tuple((item.name, item.value) for item in cls)



