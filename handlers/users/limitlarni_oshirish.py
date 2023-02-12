from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.botgautish import botga, botga2, kanal_qushish
from keyboards.default import menu, bekor_qilish
from loader import dp, db_users, Limitlar_oddiy, Limitlar_blok, premium_narxi, temp_data, bot
import pytz, asyncio
from datetime import datetime, timedelta



@dp.message_handler(state="sozlamalar", text="⬆️Limitlarni oshirish")
async def limit(msg : types.Message, state : FSMContext):
    await msg.answer("<b>Bu bo'lim ishlab chiqish jarayonida</b>")
    
#     user = db_users.select_user_id(msg.from_user.id)
#     if user == None:
#         await msg.answer("<b>Iltimos /start ni bosing va ism familiyangizni kiriting!</b>", reply_markup=menu.menu)
#         await state.finish()
#         return
#     await msg.answer("⬆️Limitlarni oshirish")
#     if user[3] == '-1':
#         answer = "<b>Bot foydalanuvchilari chekli miqdorda test tuza oladilar</b>\n\n"
#         answer += f"<b>📕Oddiy test, <i>manual</i> </b><i>{Limitlar_oddiy[0]} ta\n</i>"
#         answer += f"<b>📘Oddiy test, <i>avto</i> </b><i>{Limitlar_oddiy[1]} ta\n</i>"
#         answer += f"<b>📚Blok test, <i>manual</i> </b><i>{Limitlar_blok[0]} ta\n</i>"
#         answer += f"<b>📚Blok test, <i>avto</i> </b><i>{Limitlar_blok[1]} ta\n\n</i>"
#         answer += f"<b>Bu limitlar ko'proq bo'lishi uchun premium foydalanuvchi bo'lishingiz kerak !</b>\n"
#         answer += f"<b>Premium foydalanuvchilar quyidagicha limitlar : \n\n</b>"
#         answer += f"<b>📕Oddiy test, <i>manual</i> </b><i>{Limitlar_oddiy[2]} ta\n</i>"
#         answer += f"<b>📘Oddiy test, <i>avto</i> </b><i>{Limitlar_oddiy[3]} ta\n</i>"
#         answer += f"<b>📚Blok test, <i>manual</i> </b><i>{Limitlar_blok[2]} ta\n</i>"
#         answer += f"<b>📚Blok test, <i>avto</i> </b><i>{Limitlar_blok[3]} ta\n\n</i>"
#         answer += f"<b>Va yana <a href = 'https://telegra.ph/Premium-obunachi-02-08'>bir qancha</a> qo'shimcha funksiyalarga ega bo'lishadi\n\n</b>"
#         answer += f"<b>Bir oylik premium obuna narxi : <i>{premium_narxi}</i> so'm\n</b>\n\n"
#         answer += "<i>Obuna bo'lish uchun <a href = 'https://t.me/Javob_tekshir_admin_bot'>Murojaat Bot</a>ga yozing.</i>"
#         await msg.answer(answer, reply_markup=botga)
#     elif user[3] == '0':
#         answer = "<b>Bot foydalanuvchilari chekli miqdorda test tuza oladilar</b>\n\n"
#         answer += f"<b>📕Oddiy test, <i>manual</i> </b><i>{Limitlar_oddiy[0]} ta\n</i>"
#         answer += f"<b>📘Oddiy test, <i>avto</i> </b><i>{Limitlar_oddiy[1]} ta\n</i>"
#         answer += f"<b>📚Blok test, <i>manual</i> </b><i>{Limitlar_blok[0]} ta\n</i>"
#         answer += f"<b>📚Blok test, <i>avto</i> </b><i>{Limitlar_blok[1]} ta\n\n</i>"
#         answer += f"<b>Bu limitlar ko'proq bo'lishi uchun premium foydalanuvchi bo'lishingiz kerak !</b>\n"
#         answer += f"<b>Premium foydalanuvchilar quyidagicha limitlar : \n\n</b>"
#         answer += f"<b>📕Oddiy test, <i>manual</i> </b><i>{Limitlar_oddiy[2]} ta\n</i>"
#         answer += f"<b>📘Oddiy test, <i>avto</i> </b><i>{Limitlar_oddiy[3]} ta\n</i>"
#         answer += f"<b>📚Blok test, <i>manual</i> </b><i>{Limitlar_blok[2]} ta\n</i>"
#         answer += f"<b>📚Blok test, <i>avto</i> </b><i>{Limitlar_blok[3]} ta\n\n</i>"
#         answer += f"<b>Va yana <a href = 'https://telegra.ph/Premium-obunachi-02-08'>bir qancha</a> qo'shimcha funksiyalarga ega bo'lishadi\n\n</b>"
#         answer += f"<b>Bir oylik premium obuna narxi : <i>{premium_narxi}</i> so'm\n\n</b>"
#         answer += "<i>Bepul 10 kun muddatga sinab ko'rishingiz mumkin!\n*Bepul sinab ko'rish imkoni faqat bir marta</i>"
#         await msg.answer(text=answer, reply_markup=botga2)
        
#     else:
#         answer = f"<b>🏆Siz premium obunachisiz!\nObunaning muddati : <i>{user[3]} gacha!</i></b>"
#         if user[4] == None:
#             answer += "\n\n<i>❗️Hech qanday kanal yoki guruh bog'lanmagan.\nKanal yoki guruh bog'lamoqchi bo'lsangiz <i>🛠Sozlamalar/🖇Bog'langan kanal/guruh</i> bo'limiga o'ting.</i>"
#         await msg.answer(answer, reply_markup=menu.menu)
#         await state.finish()
    
    
# @dp.callback_query_handler(text="10_kunga_sinash", state="sozlamalar")
# async def sinov(call : types.CallbackQuery, state : FSMContext):
#     user = db_users.select_user_id(call.from_user.id)
#     if user[3] == '0':
#         t = datetime.now(pytz.timezone("Asia/Tashkent"))
#         t += timedelta(days=10)
#         sana = t.strftime("%d.%m.%Y")
#         db_users.update_status_user(sana, call.from_user.id)
#         await call.answer(f"🎉Tabriklaymiz, obuna bo'ldingiz.\nMuddat : {sana} gacha", show_alert=True)
#         await call.message.delete()
#         await state.set_state("kanal_qushish")
#         answer = "<b>Bot imkoniyatlaridan to'liq foydalanishingiz uchun online test o'tkazadigan kanalingiz yoki guruhingizni qo'shishingiz kerak!</b>"
#         await call.message.answer(answer, reply_markup=kanal_qushish)
#     else:
#         await call.message.delete()
