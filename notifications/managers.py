from .common import send_message


async def notify_manager_about_new_order(manager_telegram_id: int, text: str) -> None:
    await send_message(manager_telegram_id, text)



