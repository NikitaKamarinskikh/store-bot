from environs import Env
from dataclasses import dataclass, field
from typing import NamedTuple, List
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


@dataclass
class OrderData:
    client_telegram_id: int
    recipient_full_name: str
    recipient_phone_number: str
    transport_company_id: int
    delivery_address: str
    desired_completion_date: str
    last_completion_date: str
    products: list = field(default_factory=list) # BasketProducts


@dataclass
class StoreInfoDescription:
    text: str = ''
    images: list = field(default_factory=list)
    videos: list = field(default_factory=list)


order_points = {
    'receiver_full_name': 'ФИО',
    'receiver_phone_number': 'Номер телефона',
    'transport_company': 'Транспортная компания',
    'delivery_address': 'Адрес доставки',
    'desired_completion_date': 'Желаемая дата доставки',
    'last_completion_date': 'Крайний срок доставки'
}

