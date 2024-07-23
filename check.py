import logging
from config import CHANEL_ID, TOKEN
from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


bot = Bot(token=TOKEN)

async def chatjoin(user_id: int) -> bool:
    btn = InlineKeyboardBuilder()
    is_subscribed = True

    for ch in CHANEL_ID:
        try:
            user_status = await bot.get_chat_member(f"@{ch}", user_id)
        except Exception as e:
            logging.error(f"Error checking user status in channel {ch}: {e}")
            continue

        if user_status.status not in ["creator", "administrator", "member"]:
            btn.add(
                InlineKeyboardButton(text="Obuna bo'lish", url=f"https://t.me/{ch}")
            )
            is_subscribed = False

    btn.add(InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="result"))
    btn.adjust(1)

    if not is_subscribed:
        await bot.send_message(
            chat_id=user_id, text="⚠️ Botdan foydalanish uchun barcha kanallarga obuna bo'ling.", reply_markup=btn.as_markup()
        )
        return False
    return True


canal = InlineKeyboardBuilder()
canal.add(InlineKeyboardButton(text='⚜️ Kanalga admin qilish', callback_data='canal_admin'))
canal.add(InlineKeyboardButton(text='💫 Yordam', callback_data='canal_help'))
canal.adjust(1)