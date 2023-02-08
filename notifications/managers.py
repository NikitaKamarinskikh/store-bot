from db_api import managers as managers_model
from .common import send_message


async def notify_managers_about_new_order(text: str) -> None:
    await _send_message_to_managers(text)


async def notify_managers_about_wholesale_order(text: str) -> None:
    await _send_message_to_managers(text)


async def notify_managers_about_product_not_in_catalog(text: str) -> None:
    await _send_message_to_managers(text)


async def _send_message_to_managers(text: str) -> None:
    managers = managers_model.get_all()
    for manager in managers:
        await send_message(manager.telegram_id, text)

