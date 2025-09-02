import os
import asyncio
import dotenv
import yt_dlp
import uuid
from pathlib import Path

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

dotenv.load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_platform = {}


@dp.message(CommandStart())
async def main_start(message: types.Message):
    start_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Скачать с TikTok", callback_data="tiktok_download")],
            [InlineKeyboardButton(text="Скачать с Instagram", callback_data="instagram_download")],
            [InlineKeyboardButton(text="Скачать с YouTube", callback_data="youtube_download")],
        ]
    )
    await message.answer("Выбери платформу для скачивания:", reply_markup=start_keyboard)


async def download_video_async(url: str, filename: str) -> str:
    ydl_options = {
        'outtmpl': filename,
        'format': 'best[height<=720]',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }

    try:
        await asyncio.to_thread(
            lambda: yt_dlp.YoutubeDL(ydl_options).download([url])
        )
        return filename
    except Exception as e:
        raise Exception(f"Ошибка загрузки: {str(e)}")


@dp.callback_query(F.data.in_({"tiktok_download", "instagram_download", "youtube_download"}))
async def ask_link(callback: types.CallbackQuery):
    platform = callback.data.split("_")[0]
    user_platform[callback.from_user.id] = platform
    await callback.message.answer(f"Пришли ссылку на {platform} видео")
    await callback.answer()


@dp.message(F.text.startswith("http"))
async def final_download(message: types.Message):
    if message.from_user.id not in user_platform:
        await message.answer("Сначала выберите платформу через /start!")
        return

    url = message.text.strip()
    platform = user_platform[message.from_user.id]

    await message.answer("Скачиваю видео...")

    try:
        temp_dir = Path("temp_videos")
        temp_dir.mkdir(exist_ok=True)

        filepath = temp_dir / f"{message.from_user.id}_{uuid.uuid4().hex}.mp4"

        await download_video_async(url, str(filepath))


        await message.answer_video(
            video=types.FSInputFile(filepath),
            caption="видео скачано"
        )

        filepath.unlink()

    except Exception as e:
        print(f"Error: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())