from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
router = Router()


@router.message(CommandStart())
async def start_bot(message: Message):
    await message.answer("Пришлите ссылку")



