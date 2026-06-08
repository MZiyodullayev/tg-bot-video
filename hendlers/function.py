import hashlib
import os
import glob
import yt_dlp
import time
from aiogram.types import FSInputFile, URLInputFile
import aiohttp
import re

# def generate_url_id(url: str):
#     return hashlib.md5(url.encode()).hexdigest()

# async def download_and_send_media(bot, chat_id, url, media_type):
#     ydl_opts = {
#         # 'format': "best[ext=mp4][vcodec!=none][acodec!=none]/best[ext=mp4]/best" if media_type == "video" else "bestaudio[ext=m4a]/bestaudio/best",  <-- original format option
#         'format': "best[ext=mp4][filesize<50M]/best[ext=mp4]/best" if media_type == "video" else "bestaudio[ext=m4a][filesize<50M]/bestaudio[filesize<50M]/best[filesize<50M]",
#         'outtmpl': f"downloads/%(title)s.{'mp4' if media_type == 'video' else 'm4a'}",
#     }
#     try:
#         start_time = time.time()

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=True)
#             filename = ydl.prepare_filename(info)
            

#         end_time = time.time()
#         elapsed_time = end_time - start_time

#         file_size = os.path.getsize(filename)
#         if file_size > 50 * 1024 * 1024:
#             size_mb = file_size // 1024 // 1024
#             await bot.send_message(chat_id, f"Fayl juda katta ({size_mb}MB).\nTelegram 50MB dan katta fayllarni qabul qilmaydi.")
#             os.remove(filename)
#             return

#         media_file = FSInputFile(filename)
#         if media_type == "video":
#             await bot.send_video(chat_id, media_file, caption=f"Видео успешно загружено! Время загрузки: {elapsed_time:.2f} секунд.")
#         else:
#             await bot.send_audio(chat_id, media_file, caption=f"Аудио успешно загружено! Время загрузки: {elapsed_time:.2f} секунд.")

#         os.remove(filename)

#     except Exception as e:
#         await bot.send_message(chat_id, f"Ошибка: {e}")


def generate_url_id(url: str):
    return hashlib.md5(url.encode()).hexdigest()

async def download_pinterest(bot, chat_id, url, url_id, media_type):

    try:
        if media_type == "video":
            video_filename = f"downloads/{url_id}.mp4"
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio/best[ext=mp4]/best',
                'outtmpl': video_filename,
                'quiet': True,
                'nocheckcertificate': True,
                'merge_output_format': 'mp4',
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.extract_info(url, download=True)
            except Exception:
                ydl_opts['format'] = 'best'
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.extract_info(url, download=True)

            if os.path.exists(video_filename):
                video_file = FSInputFile(video_filename)
                await bot.send_video(chat_id, video_file, caption="Пинтерест видео!")
                os.remove(video_filename)
            else:
                await bot.send_message(chat_id, "В этом постe нет видео.")

        elif media_type == "photo":
            ydl_opts = {'quiet': True, 'skip_download': True, 'nocheckcertificate': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            thumbnails = info.get('thumbnails', [])
            photo_url = None
            if thumbnails:
                photo_url = sorted(thumbnails, key=lambda x: x.get('width', 0) or 0, reverse=True)[0].get('url')
            if not photo_url:
                photo_url = info.get('thumbnail')

            if photo_url:
                photo_filename = f"downloads/{url_id}.jpg"
                headers = {'User-Agent': 'Mozilla/5.0'}
                async with aiohttp.ClientSession() as session:
                    async with session.get(photo_url, headers=headers) as resp:
                        with open(photo_filename, 'wb') as f:
                            f.write(await resp.read())
                photo_file = FSInputFile(photo_filename)
                await bot.send_photo(chat_id, photo_file, caption="Пинтерест фото!")
                os.remove(photo_filename)
            else:
                await bot.send_message(chat_id, "В этом постe нет фото.")

        return True

    except Exception as e:
        await bot.send_message(chat_id, f"Ошибка: {e}")
        return True

        
async def download_and_send_media(bot, chat_id, url, media_type):
    url_id = generate_url_id(url)
    ext = 'mp4' if media_type == 'video' else 'm4a'
    filename = f"downloads/{url_id}.{ext}"

    os.makedirs("downloads", exist_ok=True)

    if "pinterest.com" in url or "pin.it" in url:
        success = await download_pinterest(bot, chat_id, url, url_id, media_type)  # ← media_type qo'shildi
        if not success:
            await bot.send_message(chat_id, "Не удалось загрузить медиа с Pinterest.")
        return

    ydl_opts = {
        'format': "best[ext=mp4][filesize<50M]/best[ext=mp4]/best" if media_type == "video" else "bestaudio[ext=m4a][filesize<50M]/bestaudio[filesize<50M]/best[filesize<50M]",
        'outtmpl': filename,
    }

    try:
        start_time = time.time()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            is_photo = (
                info.get('ext') in ['jpg', 'jpeg', 'png', 'webp'] or
                not info.get('formats')
            )

            if is_photo:
                photo_url = info.get('url') or info.get('thumbnail')
                if photo_url:
                    photo_filename = f"downloads/{url_id}.jpg"
                    async with aiohttp.ClientSession() as session:
                        async with session.get(photo_url) as resp:
                            with open(photo_filename, 'wb') as f:
                                f.write(await resp.read())
                    photo_file = FSInputFile(photo_filename)
                    await bot.send_photo(chat_id, photo_file, caption="🖼 Rasm!")
                    os.remove(photo_filename)
                else:
                    await bot.send_message(chat_id, "Фото не найдено.")
                return

            ydl.download([url])

        end_time = time.time()
        elapsed_time = end_time - start_time

        if not os.path.exists(filename):
            await bot.send_message(chat_id, "Не удалось загрузить медиа. Повторите попытку.")
            return

        file_size = os.path.getsize(filename)
        if file_size > 50 * 1024 * 1024:
            size_mb = file_size // 1024 // 1024
            await bot.send_message(chat_id, f"Файл слишком большой ({size_mb}MB).\nTelegram не принимает файлы больше 50MB.")
            os.remove(filename)
            return

        media_file = FSInputFile(filename)
        if media_type == "video":
            await bot.send_video(chat_id, media_file, caption=f"✅ Видео загружено! Время: {elapsed_time:.2f} сек.")
        else:
            await bot.send_audio(chat_id, media_file, caption=f"✅ Аудио загружено! Время: {elapsed_time:.2f} сек.")

        os.remove(filename)

    except Exception as e:
        await bot.send_message(chat_id, f"Ошибка: {e}")