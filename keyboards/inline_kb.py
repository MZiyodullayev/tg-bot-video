from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def format_btn(url_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Видео", callback_data=f"video|{url_id}")],
        [InlineKeyboardButton(text="Аудио", callback_data=f"audio|{url_id}")]

    ])
    return keyboard
