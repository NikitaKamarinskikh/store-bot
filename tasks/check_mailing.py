from typing import List
from web.mailing.models import MailingLists
from web.clients.models import Clients
from db_api import clients as clients_model
from config import ClientsCategories
from main import bot


async def check_mailing():
    mailings = MailingLists.objects.all()
    for mailing in mailings:
        await _exec_mainling(mailing)


async def _exec_mainling(mailing: MailingLists) -> None:
    if mailing.clients_category == ClientsCategories.ALL.name:
        await _exec_mailing_for_all_clients(mailing)
    elif mailing.clients_category == ClientsCategories.HAS_ORDERS.name:
        await _exec_mailing_for_clients_with_orders(mailing)
    elif mailing.clients_category == ClientsCategories.HAS_NO_ORDER.name:
        await _exec_mailing_for_clientss_with_no_orders(mailing)


async def _exec_mailing_for_all_clients(mailing: MailingLists) -> None:
    clients = clients_model.get_all()
    await _send_mailing_data(clients, mailing)


async def _exec_mailing_for_clients_with_orders(mailing: MailingLists) -> None:
    clients = clients_model.get_all_who_has_orders()
    await _send_mailing_data(clients, mailing)


async def _exec_mailing_for_clientss_with_no_orders(mailing: MailingLists) -> None:
    clients = clients_model.get_all_who_has_no_order()
    await _send_mailing_data(clients, mailing)


async def _send_mailing_data(clients: List[Clients], mailing: MailingLists) -> None:
    for client in clients:
        await _send_message(client.telegram_id, mailing.text)


async def _send_message(chat_id: int, text: str) -> None:
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text
        )
    except:
        ...
