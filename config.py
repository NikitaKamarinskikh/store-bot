from environs import Env
from enum import Enum


env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')

PRIVACY_POLICY_FILE_TELEGRAM_ID = env.str('PRIVACY_POLICY_FILE_TELEGRAM_ID')


class OrderStatuses(str, Enum):
    PENDING_PROCESSING = 'Ожидает обработки'
    PROCESSED = 'Обработан'
    PAID = 'Оплачен'
    REJECTED = 'Отклонен'

    @classmethod
    def choices(cls) -> tuple:
        return tuple((item.name, item.value) for item in cls)






