from aiogram import Router, F
from aiogram.types import Message

from handler import pinterest

router = Router()

@router.message(F.text.regex(r"^https?://"))
async def handle_https(message: Message):
    url = message.text

    match url:
        case u if "pinterest.com" in u or "pin.it" in u:
            return await pinterest.ask_pinterest_link(message, url)

        case _:
            await message.answer(
                "❌ Неизвестная платформа.\n"
                "Поддерживаются: Pinterest, YouTube, TikTok, Instagram."
            )
