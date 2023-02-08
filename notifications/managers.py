from db_api import managers as managers_model
from .common import send_message


async def notify_managers_about_new_order(text: str) -> None:
    managers = managers_model.get_all()
    for manager in managers:
        await send_message(manager.telegram_id, text)



