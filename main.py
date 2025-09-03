import asyncio
import dotenv
import os
from aiogram import Bot, Dispatcher

from handlers import router as handlers_router
from pinterest import router as pinterest_router

dotenv.load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


dp.include_router(pinterest_router)
dp.include_router(handlers_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())