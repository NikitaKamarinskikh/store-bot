from aiogram import types
from typing import List
from web.mailing.models import MailingLists, MailingListsImages, MailingListsVideos
from web.clients.models import Clients
from db_api import clients as clients_model
from config import ClientsCategories
from main import bot


async def check_mailing():
    mailings = MailingLists.objects.all()
    for mailing in mailings:
        await _exec_mainling(mailing)
        mailing.delete()


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
        await _send_media(client.telegram_id, mailing)


async def _send_message(chat_id: int, text: str) -> None:
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text
        )
    except:
        ...


async def _send_media(chat_id: int, mailing: MailingLists) -> None:
    images = MailingListsImages.objects.filter(mailing=mailing)
    videos = MailingListsVideos.objects.filter(mailing=mailing)

    images_list = [image.telegram_id for image in images]
    videos_list = [video.telegram_id for video in videos]

    if videos_list or images_list:
        album = types.MediaGroup()
        for image in images_list:
            album.attach_photo(image)
        for video in videos_list:
            album.attach_video(video)
        
        try:
            await bot.send_media_group(
                chat_id=chat_id,
                media=album
            )
        except:
            ...

