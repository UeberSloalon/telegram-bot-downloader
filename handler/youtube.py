import os
import asyncio
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
import yt_dlp

router = Router()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube(url: str, output_path: str) -> str:

    ydl_opts = {
        "format": "best[height<=720][ext=mp4]/best[ext=mp4]/best",
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info).replace(".webm", ".mp4")


@router.message(F.text.regexp(r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/"))
async def youtube_handler(message: Message):
    url = message.text.strip()
    await message.answer(" Скачиваю видео...")

    try:
        loop = asyncio.get_event_loop()
        filepath = await loop.run_in_executor(None, download_youtube, url, DOWNLOAD_DIR)

        video_file = FSInputFile(filepath)
        await message.answer_video(video_file, caption="Скачано в @")


        os.remove(filepath)

    except Exception as e:
        await message.answer(f" Ошибка при скачивании: {e}")
