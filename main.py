import asyncio, logging
from aiogram import Bot, Dispatcher, F, html
from aiogram.filters.command import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from config import TOKEN
from check import chatjoin, canal, menu
from aiogram.types import (
    Message, 
    CallbackQuery, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    InputMediaVideo, 
    InputMediaPhoto,
    InputMediaDocument
)
from datebase import (
    Add_db, 
    Read_db, 
    UpdateLike, 
    UpdateDislike, 
    AddUser, 
    ReadUser,
    DeleteUser
)     


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

👍/👎- <b>Bot yordamida kanalingizga tashlangan xabarlaringizga like va dislike tugmalarini qo'yishingiz mumkin.</b>
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

👍/👎- <b>Bot yordamida kanalingizga tashlangan xabarlaringizga like va dislike tugmalarini qo'yishingiz mumkin.</b>
            """,
            reply_markup=canal.as_markup()
        )


@dp.callback_query(F.data.startswith('canal_'))
async def qoshish(call: CallbackQuery):
    await call.message.delete()
    action = call.data.split('_')
    second = action[1]

    if second == 'main':
        await call.message.answer(
            text="""
                🏠 <b>Asosiy menyu.

👍/👎- Bot yordamida kanalingizga tashlangan xabarlaringizga like va dislike tugmalarini qo'yishingiz mumkin.</b>
            """,
            reply_markup=canal.as_markup()
        )

    elif second == 'admin':
        await call.message.answer(
            text=f"""
                <b>⚜️ Shartlar :
1. Botni (@likeipostbot) kanalingizga qo'shing.
    
2. Botni kanalingizda administratorlar ro'yxatiga qo'shing.</b>
            """, reply_markup=menu.as_markup()
        )
    

# @dp.channel_post()
# async def post(message: Message):
#     Add_db(chat_id=message.chat.id, message_id=message.message_id, like=0, dislike=0)
#     await bot.edit_message_text(
#         chat_id=str(message.chat.id),
#         message_id=str(message.message_id),
#         text=message.text,
#         reply_markup=InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text="👍", callback_data='post_like'), InlineKeyboardButton(text="👎", callback_data='post_dislike')]
#             ]
#         )
#     )

@dp.channel_post()
async def post(message: Message):
    Add_db(chat_id=message.chat.id, message_id=message.message_id, like=0, dislike=0)
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👍", callback_data='post_like'), InlineKeyboardButton(text="👎", callback_data='post_dislike')]
        ]
    )

    if message.text:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=message.text,
            reply_markup=reply_markup
        )

    elif message.photo:
        await bot.edit_message_media(
            media=InputMediaPhoto(
                media=message.photo[-1].file_id,
                caption=message.caption or ''
            ),
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=reply_markup
        )

    elif message.video:
        await bot.edit_message_media(
            media=InputMediaVideo(
                media=message.video.file_id,
                caption=message.caption or ''
            ),
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=reply_markup
        )

    elif message.document:
        await bot.edit_message_media(
            media=InputMediaDocument(
                media=message.document.file_id,
                caption=message.caption or ''
            ),
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=reply_markup
        )


@dp.callback_query(F.data.startswith('post'))
async def edit(call: CallbackQuery):
    action = call.data.split('_')
    btn = action[1]

    users = ReadUser()
    for user in users:
        if (user[0] == call.from_user.id) and (user[1] == call.message.chat.id) and (user[2] == call.message.message_id):
            variant = user[3]

            if variant != btn:
                await call.answer(text="Ovoz bergansiz")
                return

            elif (btn == 'like') and (variant == btn):
                posts = Read_db()
                for post in posts:
                    if (post[0] == call.message.chat.id) and (post[1] == call.message.message_id):
                        like = int(post[2]) - 1
                        dislike = post[3]
                        UpdateLike(like=like, chat_id=call.message.chat.id, message_id=call.message.message_id)                        
                        DeleteUser(user_id=call.from_user.id, chat_id=call.message.chat.id, message_id=call.message.message_id)

                        txt = call.message.text
                        await bot.edit_message_text(
                            chat_id=str(call.message.chat.id),
                            message_id=str(call.message.message_id),
                            text=txt,                    
                            reply_markup=InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [InlineKeyboardButton(text=f"👍{like}", callback_data='post_like'), InlineKeyboardButton(text=f"👎{dislike}", callback_data='post_dislike')]
                                ]
                            )
                        )
                        await call.answer(text="👍-1 @likeipostbot")
        
            elif (variant == 'dislike') and (variant == btn):
                posts = Read_db()
                for post in posts:
                    if (post[0] == call.message.chat.id) and (post[1] == call.message.message_id):
                        like = post[2]
                        dislike = post[3] - 1
                        UpdateDislike(dislike=dislike, chat_id=call.message.chat.id, message_id=call.message.message_id)
                        DeleteUser(user_id=call.from_user.id, chat_id=call.message.chat.id, message_id=call.message.message_id)

                        txt = call.message.text
                        await bot.edit_message_text(
                            chat_id=str(call.message.chat.id),
                            message_id=str(call.message.message_id),
                            text=txt,                    
                            reply_markup=InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [InlineKeyboardButton(text=f"👍{like}", callback_data='post_like'), InlineKeyboardButton(text=f"👎{dislike}", callback_data='post_dislike')]
                                ]
                            )
                        )
                        await call.answer(text="👎-1 @likeipostbot")
            return                
            
    else:    
        AddUser(user_id=call.from_user.id, chat_id=call.message.chat.id, message_id=call.message.message_id, click=btn)    

        if btn == 'like':
            posts = Read_db()
            for post in posts:
                if (post[0] == call.message.chat.id) and (post[1] == call.message.message_id):
                    like = int(post[2]) + 1
                    dislike = post[3]
                    UpdateLike(like=like, chat_id=call.message.chat.id, message_id=call.message.message_id)
                    
                    txt = call.message.text
                    await bot.edit_message_text(
                        chat_id=str(call.message.chat.id),
                        message_id=str(call.message.message_id),
                        text=txt,                    
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text=f"👍{like}", callback_data='post_like'), InlineKeyboardButton(text=f"👎{dislike}", callback_data='post_dislike')]
                            ]
                        )
                    )
                    await call.answer(text="👍+1 @likeipostbot")
        
        elif btn == 'dislike':
            posts = Read_db()
            for post in posts:
                if (post[0] == call.message.chat.id) and (post[1] == call.message.message_id):
                    like = post[2]
                    dislike = post[3] + 1
                    UpdateDislike(dislike=dislike, chat_id=call.message.chat.id, message_id=call.message.message_id)

                    txt = call.message.text
                    await bot.edit_message_text(
                        chat_id=str(call.message.chat.id),
                        message_id=str(call.message.message_id),
                        text=txt,                    
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text=f"👍{like}", callback_data='post_like'), InlineKeyboardButton(text=f"👎{dislike}", callback_data='post_dislike')]
                            ]
                        )
                    )
                    await call.answer(text="👎+1 @likeipostbot")






@dp.message(F.text)
async def restart(message: Message):
    await message.reply("botni qayta ishga tushirish uchun /start ni boshing.")


    # chat_id = '-1002066217705'
    # admins = await bot.get_chat_administrators(chat_id)
    # admin_usernames = [admin.user.username for admin in admins if admin.user.username]
    # admin_names = [admin.user.first_name for admin in admins if not admin.user.username]
    # response = "Administrators in this chat:\n"
    # response += "\n".join(admin_usernames + admin_names)
    # print(response)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot o`chdi")   
        