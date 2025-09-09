from aiogram import Router, F, Bot
from aiogram.types import Message, BotCommand
from aiogram.filters import CommandStart, Command


router = Router()

@router.message(CommandStart())
async def start_bot(message: Message):
    await message.answer("👋 Привет!\n\n"
"📥 Я скачиваю фото/видео с YouTube, TikTok, Instagram, Pinterest без водяных знаков.\n\n"
"🚀 Отправь ссылку на фото/видео – и я загружу его!")
    print("🔥 Вызван /start")


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота 🚀"),

    ]
    await bot.set_my_commands(commands)


print("✅ handlers_router загружен")


