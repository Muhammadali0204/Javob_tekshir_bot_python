from loader import dp, db_users
from keyboards.default.admin import admin_key
from data.config import ADMINS
from aiogram import types


@dp.message_handler(text="Barcha foydalanuvchilar", chat_id = ADMINS)
async def admin(msg : types.Message):
    users = db_users.select_all_users()
    answer = f"<b>Foydalanuvchilar soni : </b><i>{len(users)} ta</i>\n\n"
    n = 1
    premium = 0
    for user in users:
        answer += f"<b>{n} - foydalanuvchi : \nIsmi : </b><i>{user[1]}</i>\n"
        answer += f"<b>Id : </b><i>{user[0]}</i>\n"
        answer += f"<b>Username : </b><i>{user[2]}</i>\n"
        if user[3] != '0':
            premium += 1
            answer += f"<b>Status : </b><i>{user[3]}</i>\n"
            answer += f"<b>Kanali : </b><i>{user[4]}</i>\n\n"
        else:
            answer += f"<b>Status : </b><i>{user[3]}</i>\n\n"
        n += 1
        
        if n % 26 == 0:
            await msg.answer(answer)
            answer = "<b>Davomi : </b>\n\n"
    
    answer += f"<b>Premium obunachilar soni : </b><i>{premium} ta</i>"
    await msg.answer(text=answer, reply_markup=admin_key)