from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from hendlers.function import download_and_send_media
import url_storage as storage


router = Router()

@router.callback_query(lambda callback: 'video' in callback.data or 'audio' in callback.data)
async def format_sellection(callback: CallbackQuery, bot: Bot):
    storage.urls_storage = storage.load_urls_storage()
    action, url_id = callback.data.split("|")
    url = storage.urls_storage.get(url_id)

    if not url:
        await callback.answer("Ошибка: URL не найден.")
        return
    await callback.answer("Подверждено!")
    if action == "video":
        await callback.answer("Начинаю загрузку видео...")
        await download_and_send_media(bot, callback.message.chat.id, url, media_type="video")
    elif action == "audio":
        await callback.answer("Начинаю загрузку аудио...")
        await download_and_send_media(bot, callback.message.chat.id, url, media_type="audio")
        