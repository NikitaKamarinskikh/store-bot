from typing import NamedTuple

GET_BACK_MESSAGE_TEXT = 'Назад'

MAIN_MENU_TEXT = """
Главное меню:
1. Заказ - для выбора из каталога, оформления нестандартного заказа, а так же оптового заказа.
2. Поиск - поиск по каталогу. Нажмите кнопку и начните вводить то что ищите.
3. Кошелек - ваши бонусные монеты, за заказы и приглашения, которые можете потратить на заказ снаряжения
4. Общая информация"""

CATALOG_MESSAGE_TEXT="""
1. Каталог - выбор в каталоге по категориям
2. Оптовый заказ - опишите что нужно и количество единиц
3. Нет в каталоге, но хотите заказать
4. Вернуться в главное меню
5. Посмотреть корзину
"""


class MainMenuMessagesTexts(NamedTuple):
    make_order = 'Заказ'
    search_product = 'Поиск'
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
    activate_certificate = 'Активировать сертификат'
    back = 'Назад'



