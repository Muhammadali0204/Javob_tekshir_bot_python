from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from keyboards.default import menu
from loader import dp, db_users, db_bj, db_ts, bot, foydalanuvchi_limitlari_oddiy, foydalanuvchi_limitlari_blok

@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), text="👤Men haqimda")
async def men(msg : types.Message):
    user = db_users.select_user_id(msg.from_user.id)
    if user == None:
        await msg.answer("<b>Iltimos /start ni bosing va ism familiyangizni kiriting!</b>", reply_markup=menu.menu)
        return
    answer = f"<b>Sizning ismingiz : {user[1]}</b>\n\n<i>*O`zgartirish uchun 🛠Sozlamalar/♻️Ismni tahrirlash bo'limiga o'ting.</i>"
    answer += f"<b>Qolgan limitlaringiz : </b>\n\n"
    answer += f"<b>📕Oddiy test, <i>manual</i> </b><i>{foydalanuvchi_limitlari_oddiy[0]} ta\n</i>"
    answer += f"<b>📘Oddiy test, <i>avto</i> </b><i>{foydalanuvchi_limitlari_oddiy[1]} ta\n</i>"
    answer += f"<b>📚Blok test, <i>manual</i> </b><i>{foydalanuvchi_limitlari_blok[0]} ta\n</i>"
    answer += f"<b>📚Blok test, <i>avto</i> </b><i>{foydalanuvchi_limitlari_blok[1]} ta\n\n</i>"
    answer += f"<b>Siz 🏆Premium foydalanuvchi emassiz"
    await msg.answer(text=answer)