import logging
from config import CHANEL_ID, TOKEN
from aiogram import Bot, html
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from datebase import ReadUser, AddUser


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

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
        if len(CHANEL_ID) >= 2:
            await bot.send_message(
                chat_id=user_id, text=f"⚠️ {html.bold('Botdan foydalanish uchun barcha kanallarga obuna bo\'ling.')}", reply_markup=btn.as_markup()
            )
        else:
            await bot.send_message(
                chat_id=user_id, text=f"⚠️ {html.bold('Botdan foydalanish uchun kanalga obuna bo\'ling.')}", reply_markup=btn.as_markup()
            )   
        return False
    return True


canal = InlineKeyboardBuilder()
canal.add(InlineKeyboardButton(text='💫 Botdan foydalanish', callback_data='canal_admin'))
canal.add(InlineKeyboardButton(text='👤 Admin', url="https://t.me/xudoybergan0v"))
canal.adjust(1)


menu = InlineKeyboardBuilder()
menu.add(InlineKeyboardButton(text='🔝 Asosiy menyu', callback_data='canal_main'))