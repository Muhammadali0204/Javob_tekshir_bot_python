from loader import dp, db_users
from keyboards.default.admin import admin_key
from keyboards.default.bekor_qilish import bekor_qil
from data.config import ADMINS
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="Premium foydalanuvchilar", chat_id = ADMINS)
async def admin(msg : types.Message):
    users = db_users.select_all_users()
    answer = "<b>Premium foydalanuvchilar : </b>\n\n"
    premium = 0
    for user in users:
        if user[3] not in ['0', '-1']:
            answer += f"<b>{premium + 1} - foydalanuvchi : \nIsmi : </b><i>{user[1]}</i>\n"
            answer += f"<b>Id : </b><i>{user[0]}</i>\n"
            answer += f"<b>Username : </b><i>{user[2]}</i>\n"
            answer += f"<b>Status : </b><i>{user[3]}</i>\n"
            answer += f"<b>Kanali : </b><i>{user[4]}</i>\n\n"
            premium += 1
        
        if premium % 25 == 0 and premium != 0:
            await msg.answer(answer)
            answer = "<b>Davomi : </b>\n\n"
    
    answer += f"<b>Premium obunachilar soni : </b><i>{premium} ta</i>"
    await msg.answer(text=answer, reply_markup=admin_key)
    
@dp.message_handler(text="Premium narxi", chat_id = ADMINS)
async def admin(msg : types.Message):
    data = db_users.select_user_id(5)
    await msg.answer(f"<b>Premkium narxi = {data[2]} so'm</b>", reply_markup=admin_key)
    
@dp.message_handler(text="Premium narxni o`zgartirish", chat_id = ADMINS)
async def admin(msg : types.Message, state : FSMContext):
    await msg.answer("<b>Yangi narxni yuboring : </b>", reply_markup=bekor_qil)
    await state.set_state("premium narxini o'zgartirishda narx")

@dp.message_handler(state="premium narxini o'zgartirishda narx", chat_id = ADMINS)
async def admin(msg : types.Message, state : FSMContext):
    if msg.text.isnumeric():
        db_users.update_username(5, msg.text)
        await msg.answer(f"<b>Premium obuna narxi {msg.text} ga o'zgardi, botni qayta ishga tushuring</b>", reply_markup=admin_key)
        await state.finish()
    else :
        await msg.answer("<b>Son kiriting : </b>", reply_markup=admin_key)
        await state.finish()