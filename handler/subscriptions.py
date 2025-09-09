from aiogram import Router, F, types
from aiogram.exceptions import TelegramAPIError
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

REQUIRED_CHANNELS = [""]  # указать каналы

async def check_subscription(bot, user_id: int) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(f"@{channel}", user_id)
            if member.status not in ("creator", "administrator", "member"):
                return False
        except Exception as e:
            print(f"Ошибка проверки канала @{channel}: {e}")
            return False
    return True

async def ask_to_subscribe(message: types.Message):
    kb = InlineKeyboardBuilder()
    for ch in REQUIRED_CHANNELS:
        kb.button(text=f"Подписаться на {ch}", url=f"https://t.me/{ch}")
    kb.button(text="Проверить подписки", callback_data="check_subs")
    kb.adjust(1)
    await message.answer(
        " Чтобы пользоваться ботом, подпишись на каналы и нажми кнопку ниже:",
        reply_markup=kb.as_markup()
    )

@router.callback_query(F.data == "check_subs")
async def check_subs_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if await check_subscription(callback.bot, user_id):
        await callback.message.edit_text(" Отлично! Вы подписаны на все каналы.\nТеперь можно пользоваться ботом 🚀")
    else:
        await callback.answer(" Вы ещё не подписаны на все каналы!", show_alert=True)
