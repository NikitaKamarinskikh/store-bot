from main import bot


async def send_message(chat_id: int, text: str) -> None:
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text
        )
    except:
        ...




