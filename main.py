from aiogram import Bot, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder
import dotenv
import os
import asyncio

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=Bot(BOT_TOKEN))






async def main():
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())

