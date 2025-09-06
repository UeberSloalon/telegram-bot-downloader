import asyncio
import dotenv
import os

from aiogram import Bot, Dispatcher
from handler import pinterest_router, handlers_router, instagram_router, youtube_router, tiktok_router
from handler.handlers import set_commands

dotenv.load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(youtube_router)
dp.include_router(tiktok_router)
dp.include_router(instagram_router)
dp.include_router(pinterest_router)
dp.include_router(handlers_router)

async def main():
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())