from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
router = Router()


@router.message(CommandStart())
async def start_bot(message: Message):
    start_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Pinterest", callback_data="pinterest")]
        ]
    )
    await message.answer("Выбери платформу:", reply_markup=start_keyboard)


@router.callback_query(F.data == "pinterest")
async def pinterest_callback(callback: CallbackQuery):
    from pinterest import ask_pinterest_link
    await ask_pinterest_link(callback)
