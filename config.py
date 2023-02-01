from environs import Env
from dataclasses import dataclass, field
from typing import NamedTuple, List
from enum import Enum


env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')

PRIVACY_POLICY_FILE_TELEGRAM_ID = env.str('PRIVACY_POLICY_FILE_TELEGRAM_ID')


class ClientsCategories(str, Enum):
    ALL = 'Все'
    HAS_ORDERS = 'Всем кто делал заказы'
    HAS_NO_ORDER = 'Всем кто не делал заказы'

    @classmethod
    def choices(cls) -> tuple:
        return tuple((item.name, item.value) for item in cls)


class OrderStatuses(str, Enum):
    PENDING_PROCESSING = 'Ожидает обработки'
    IN_PROGRESS = 'В работе'
    IN_DELIVERY = 'Передан в доставку'
    SENT = 'Отправлен'
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


@dataclass
class BasketInfo:
    products_quantity: int = 0
    amount_in_rub: int = 0

    def as_string(self) -> str:
        return f'Корзина - ({self.products_quantity}) - {self.amount_in_rub} руб.'



