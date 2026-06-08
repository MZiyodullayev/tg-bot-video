from aiogram import Router 
from aiogram.filters import CommandStart
from aiogram.types import Message

import re
import hendlers.function as hf 
import url_storage as storage
import keyboards.inline_kb as in_kb

# router = Router()

# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.answer("Приветствую тебя, я бот для отправки видео. Просто отправь мне видео и я тебе его отправлю обратно!")

# @router.message(lambda message: "tiktok.com" in message.text or "youtube.com" in message.text or "youtu.be" in message.text or "instagram.com" in message.text or "pinterest.com" in message.text)
# async def video_request(message: Message):
#     url = message.text.strip()
#     url_id = hf.generate_url_id(url)
#     storage.urls_storage[url_id] = url
#     storage.save_urls_storage(storage.urls_storage)
#     storage.urls_storage = storage.load_urls_storage()
#     await message.answer("Видео получено, выберите формат загрузки", reply_markup= await in_kb.format_btn(url_id))

    
#     # Дальше идёт логика скачивания...


router = Router()

SUPPORTED_DOMAINS = [
    "youtube.com", "youtu.be",
    "tiktok.com",
    "instagram.com",
    "vk.com", "vkvideo.ru",
    "snapchat.com",
    "pinterest.com", "pin.it",
    "twitter.com", "x.com",
    "facebook.com", "fb.watch",
    "reddit.com",
    "twitch.tv",
    "dailymotion.com",
    "vimeo.com",
    "ok.ru",
    "rutube.ru",
]

def extract_url(text: str) -> str | None:
    url_pattern = r'https?://[^\s]+'
    match = re.search(url_pattern, text)
    return match.group(0) if match else None

def is_supported_url(text: str):
    url = extract_url(text)
    if not url:
        return False
    return any(domain in url for domain in SUPPORTED_DOMAINS)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для загрузки видео, фото и аудио.\n"
    )

@router.message(lambda message: message.text and is_supported_url(message.text))
async def video_request(message: Message):
    url = extract_url(message.text)
    url_id = hf.generate_url_id(url)
    storage.urls_storage[url_id] = url
    storage.save_urls_storage(storage.urls_storage)
    storage.urls_storage = storage.load_urls_storage()
    await message.answer(" Ссылка получена, выберите формат загрузки:", reply_markup=await in_kb.format_btn(url_id, url=url))


