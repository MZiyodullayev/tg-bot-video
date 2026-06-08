from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# async def format_btn(url_id):
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Видео", callback_data=f"video|{url_id}")],
#         [InlineKeyboardButton(text="Аудио", callback_data=f"audio|{url_id}")]


#     ])
#     return keyboard


async def format_btn(url_id, url=""):
    # Pinterest uchun faqat Видео va Фото
    if "pinterest.com" in url or "pin.it" in url:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=" Видео", callback_data=f"video|{url_id}")],
            [InlineKeyboardButton(text=" Фото", callback_data=f"photo|{url_id}")],
        ])
    else:
        # Boshqa saytlar uchun faqat Видео va Аудио
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=" Видео", callback_data=f"video|{url_id}")],
            [InlineKeyboardButton(text=" Аудио", callback_data=f"audio|{url_id}")],
        ])
    return keyboard
