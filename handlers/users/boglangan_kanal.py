from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.botgautish import kanal_guruh, kanalga_qush
from keyboards.default.bekor_qilish import bekor_qil
from keyboards.default.menu import menu
from keyboards.inline.botgautish import kanal_qushish
from loader import dp, db_users, Limitlar_oddiy, Limitlar_blok, premium_narxi, temp_data, bot
import pytz, asyncio
from datetime import datetime, timedelta



@dp.message_handler(text="🖇Bog'langan kanal/guruh", state="sozlamalar")
async def kanal(msg : types.Message, state : FSMContext):
    await msg.answer("<b>Bu bo'lim ishlab chiqish jarayonida</b>")
    # user = db_users.select_user_id(msg.from_user.id)
    # if user == None:
    #     await msg.answer("<b>Iltimos /start ni bosing va ism familiyangizni kiriting!</b>", reply_markup=menu)
    #     await state.finish()
    #     return
    
    # if user[3] == '-1':
    #     answer = "<b>Siz kanal yoki guruhingizni bog'lay olmaysiz❗️\n🏆Buning uchun premium foydalanuvchi bo'lishingiz kerak.</b>\n\n<i>Batafsil 👇👇👇\n\n🛠Sozlamalar/⬆️Limitlarni oshirish</i>"
    #     await msg.answer(answer, reply_markup=menu)
    #     await state.finish()
    
    # elif user[3] == '0':
    #     answer = "<b>Siz kanal yoki guruhingizni bog'lay olmaysiz❗️\n🏆Buning uchun premium foydalanuvchi bo'lishingiz kerak.</b>\n\n<i>Batafsil 👇👇👇\n\n🛠Sozlamalar/⬆️Limitlarni oshirish\n\n*Sizda, 10 kun muddatga foydalanib ko'rish imkoningiz bor✅</i>"
    #     await msg.answer(answer, reply_markup=menu)
    #     await state.finish()
    # else :
    #     if user[4] == None:
    #         answer = "<b>Sizda kanal yoki guruh bog'lash imkoniyati bor ✅\nLekin hech qanday kanal yoki guruh bog'lamagansiz ❌</b>"
    #         await msg.answer(answer, reply_markup=kanal_qushish)
    #         await state.set_state("kanal_qushish")
    #     else :
    #         kanal = user[4].split(',')
    #         answer = f"<b>Sizning kanalingiz : \n</b><i>{kanal[1]}</i>"
    #         await msg.answer(answer)
            