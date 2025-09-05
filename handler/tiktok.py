import os
import yt_dlp
from aiogram import Router, F
from aiogram.types import Message, FSInputFile

router = Router()

@router.message(F.text.regexp(r"(https?://)?(www\.)?(tiktok\.com|vm\.tiktok\.com)/"))
async def download_tiktok(message: Message):
    url = message.text.strip()
    await message.answer("Скачиваю видео с TikTok...")

    try:

        output_dir = "tiktok_downloads"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, "tiktok.mp4")


        ydl_opts = {
            "format": "mp4",
            "outtmpl": filepath,
            "quiet": True,
            "merge_output_format": "mp4",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


        video = FSInputFile(filepath)
        await message.answer_video(video, caption="Скачано в @")


        os.remove(filepath)

    except Exception as e:
        await message.answer(f"Ошибка при скачивании: {e}")
