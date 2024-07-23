import asyncio, logging
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from config import TOKEN
from check import chatjoin, canal


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    user = message.from_user.full_name
    if await chatjoin(user_id=user_id):
        await message.answer(
            text=f"""
                🤝 Assalomu alaykum {html.bold(user)}.

👍/👎- Bot yordamida kanalingizga tashlangan postlaringizga like va dislike tugmalarini qo‘yishingiz mumkin.
            """,
            reply_markup=canal.as_markup()
        )


@dp.callback_query(F.data == 'result')        
async def result(call: CallbackQuery):
    await call.message.delete()
    user = call.from_user.full_name
    user_id = call.from_user.id
    if await chatjoin(user_id=user_id):
        await call.message.answer(
            text=f"""
                🤝 Assalomu alaykum {html.bold(user)} xush kelibsiz, botdan foydalanishingiz mumkin.

👍/👎- Bot yordamida kanalingizga tashlangan postlaringizga like va dislike tugmalarini qo'yishingiz mumkin.
            """,
            reply_markup=canal.as_markup()
        )


# @dp.callback_query(F.data == 'canal_admin')
# async def qoshish(call: CallbackQuery):
#     sd = await bot.get_chat_administrators('-1002066217705')
#     print(sd)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot o`chdi")   
        