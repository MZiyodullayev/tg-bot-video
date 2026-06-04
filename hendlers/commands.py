from aiogram import Router 
from aiogram.filters import CommandStart
from aiogram.types import Message

import hendlers.function as hf 
import url_storage as storage
import keyboards.inline_kb as in_kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Приветствую тебя, я бот для отправки видео. Просто отправь мне видео и я тебе его отправлю обратно!")

@router.message(lambda message: "tiktok.com" in message.text or "youtube.com" in message.text or "youtu.be" in message.text or "instagram.com" in message.text or "pinterest.com" in message.text)
async def video_request(message: Message):
    url = message.text.strip()
    url_id = hf.generate_url_id(url)
    storage.urls_storage[url_id] = url
    storage.save_urls_storage(storage.urls_storage)
    storage.urls_storage = storage.load_urls_storage()
    await message.answer("Видео получено, выберите формат загрузки", reply_markup= await in_kb.format_btn(url_id))

    
    # Дальше идёт логика скачивания...