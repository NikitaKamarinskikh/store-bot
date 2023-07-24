from aiogram import types

from main import dp
from messages_texts import MainMenuMessagesTexts
from exceptions.exceptions import InfoDoesNotExists
from db_api.store_info import get_info
from config import StoreInfoDescription


@dp.message_handler(text=MainMenuMessagesTexts.info)
async def store_info(message: types.Message):
    try:
        info = get_info()
        await message.answer(info.text)
        if info.images or info.videos:
            await _send_media(message, info)

    except InfoDoesNotExists:
        await message.answer('Мастерская "BearGear", находится в Челябинске.')


async def _send_media(message: types.Message, info: StoreInfoDescription) -> None:
    album = types.MediaGroup()
    for image_telegram_id in info.images:
        album.attach_photo(image_telegram_id)
    for video_telegram_id in info.videos:
        album.attach_video(video_telegram_id)

    await message.answer_media_group(media=album)


