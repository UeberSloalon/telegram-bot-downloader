import asyncio
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
import requests
import uuid
from pathlib import Path
import re
import os

router = Router()

async def ask_pinterest_link(callback: CallbackQuery):
    await callback.message.answer(
        "📌 Пришлите ссылку на Pinterest видео\n\n"
        "Примеры:\n"
        "• https://www.pinterest.com/pin/1234567890/\n"
        "• https://pinterest.com/pin/1234567890/\n\n"
        "• https://pin.it/1nI8zhzhd"
        "⚠️ Работает только для видео пинов!\n\n"
        "⚠️ Ссылки типа https://ru.pinterest.com/pin/420875527696637521/ - не обрабатываются!"
    )
    await callback.answer()


async def download_pinterest_video(url: str, filename: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    try:
        response = await asyncio.to_thread(lambda: requests.get(url, headers=headers, timeout=15))
        if response.status_code != 200:
            raise Exception(f"Ошибка доступа к странице: {response.status_code}")

        html_content = response.text
        video_url = None


        patterns = [
            r'"videos":\s*{.*?"url"\s*:\s*"(https?://[^"]+\.mp4[^"]*)"',
            r'"video_list":\s*{.*?"url"\s*:\s*"(https?://[^"]+\.mp4[^"]*)"',
            r'<meta property="og:video" content="(https?://[^"]+\.mp4[^"]*)"',
            r'<meta property="og:video:url" content="(https?://[^"]+\.mp4[^"]*)"',
            r'<video[^>]+src="(https?://[^"]+\.mp4[^"]*)"',
            r'<source[^>]+src="(https?://[^"]+\.mp4[^"]*)"',
            r'(https?://[^"]+\.mp4[^"]*)',
        ]

        for pattern in patterns:
            match = re.search(pattern, html_content, re.DOTALL)
            if match:
                video_url = match.group(1).replace('\\/', '/')
                break

        if not video_url:
            raise Exception("Видео URL не найден в коде страницы")

        video_response = await asyncio.to_thread(
            lambda: requests.get(video_url, headers=headers, stream=True, timeout=30)
        )
        if video_response.status_code != 200:
            raise Exception(f"Ошибка скачивания видео: {video_response.status_code}")

        with open(filename, 'wb') as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        if os.path.getsize(filename) == 0:
            raise Exception("Файл пустой")

        return filename

    except Exception as e:
        if os.path.exists(filename):
            os.remove(filename)
        raise Exception(f"Ошибка Pinterest: {str(e)}")


async def process_pinterest_url(message: Message, url: str):
    processing_msg = await message.answer("Анализирую ссылку...")

    try:
        if "/pin/" not in url:
            await processing_msg.edit_text("Это не ссылка на Pinterest pin!")
            return

        temp_dir = Path("pinterest_videos")
        temp_dir.mkdir(exist_ok=True)
        filepath = temp_dir / f"pinterest_{uuid.uuid4().hex}.mp4"

        await processing_msg.edit_text("Скачиваю видео...")

        await download_pinterest_video(url, str(filepath))

        await processing_msg.edit_text("Видео скачано! Отправляю...")

        await message.answer_video(
            video=types.FSInputFile(filepath),
            caption=" Видео с Pinterest успешно скачано!"
        )

    except Exception as e:
        error_msg = str(e)
        if "Видео URL не найден" in error_msg:
            error_msg = (
                "Не удалось найти видео в этом пине. Возможно:\n"
                "Это изображение, а не видео\n"
                "Видео недоступно\n"
                "Ссылка неверная"
            )
        await processing_msg.edit_text(error_msg)
        print(f"Pinterest error: {e}")

    finally:
        if os.path.exists(filepath):
            filepath.unlink()


@router.message(F.text.startswith("https://pin.it/"))
async def handle_pinit_link(message: Message):
    short_url = message.text.strip()
    processing_msg = await message.answer("Распознаю короткую ссылку...")

    try:
        response = await asyncio.to_thread(
            lambda: requests.head(short_url, allow_redirects=True, timeout=10)
        )
        final_url = response.url
        await processing_msg.delete()
        await process_pinterest_url(message, final_url)

    except Exception as e:
        await processing_msg.edit_text(f"Ошибка при обработке короткой ссылки: {e}")


@router.message(F.text.regexp(r"^https?://(www\.)?pinterest\.com/"))
async def handle_pinterest_link(message: Message):
    await process_pinterest_url(message, message.text.strip())
