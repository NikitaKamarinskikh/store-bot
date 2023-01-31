from typing import NamedTuple


class MainMenuMessagesTexts(NamedTuple):
    make_order = 'Заказ'
    catalog = 'Поиск'
    bonuses = 'Кошелек'
    info = 'Общая информация'


class RegistrationMessagesTexts(NamedTuple):
    accept_welcome_message = 'Продолжить'
    accept_privacy_policy_message = 'Принять'


class OrdersMessagesText(NamedTuple):
    catalog = 'Каталог'
    product_not_in_catalog = 'Нет в каталоге'
    wholesale_order = 'Оптовый заказ'
    back = 'Назад'
    backet = 'Корзина'


class ReferralProgramMessagesTexts(NamedTuple):
    invite_user = 'Пригласить'
    back = 'Назад'



