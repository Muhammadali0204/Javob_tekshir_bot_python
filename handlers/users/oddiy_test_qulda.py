from aiogram import types
from aiogram.types import Message
from datetime import datetime as d, timedelta
import pytz
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from utils.misc.isbelgi import isbelgi
from keyboards.inline.post_joyla import post
from keyboards.inline.inline_ha_yoq import tasdiq_keyboard
from keyboards.default import menu, bekor_qilish, test_turi
import random
from loader import dp, db_users, db_ts, bot, foydalanuvchi_limitlari_oddiy, temp_data, kitoblar

@dp.message_handler(state="fan_nomi_qul_oddiy")
async def tuzz(msg : types.Message, state : FSMContext):    
    if all(x.isalpha() or x.isspace() or isbelgi(x) for x in msg.text):
        if len(msg.text) > 2 and len(msg.text) < 31:
            fan_nomi = msg.text
            fan_nomi = fan_nomi.lower().capitalize()
            temp_data[msg.from_user.id] = [fan_nomi, ""]
            await msg.answer(f"{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{fan_nomi}</i>\n<b>🔡Endi esa, bu fanning javoblarini yuboring :</b>\n\n<i>abcd... 👈ko`rinishida</i>", reply_markup=bekor_qilish.bekor_qil)
            await state.set_state("test_javob_qul_oddiy")
        else:
            await msg.answer("<b>Fan nomidagi belgilar soni 2 tadan 30 tagacha bo`lishi mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup= bekor_qilish.bekor_qil)
    else:
        await msg.answer("<b>Faqat harf va bo`sh joy yuborishingiz mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup=bekor_qilish.bekor_qil)
        
@dp.message_handler(state="test_javob_qul_oddiy")
async def tasdiqlash(msg : types.Message, state : FSMContext):
    javob = msg.text
    if javob.isalpha():
        if len(javob) > 2 and len(javob) < 101:
            javob = javob.lower()
            temp_data[msg.from_user.id][1] = javob
            answer = f"<b>🔢Savollar soni : </b><i>{len(javob)} ta</i>\n"
            n = 1
            for harf in javob:
                answer += f"<i>{n} - {harf}\n</i>"
                n += 1
            answer += "<b>Javoblar to`g`riligiga ishonch hosil qiling❗️</b>\n<i>Tasdiqlaysizmi ❓</i>"
            await msg.answer(text=answer, reply_markup=tasdiq_keyboard)
            await state.set_state("javobni_tasdiqlash_qul_oddiy")
        else:
            await msg.reply("<b>Javoblar soni 3 tadan 100 tagacha bo`lishi mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup= bekor_qilish.bekor_qil)
    else :
        await msg.answer("<b>Javoblar faqat harflardan iborat bo`lishi kerak!</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup=bekor_qilish.bekor_qil)
    
@dp.callback_query_handler(text= "yes", state="javobni_tasdiqlash_qul_oddiy")
async def javob_ol(call : types.CallbackQuery, state : FSMContext):
    test_kodi = db_users.take_test_kodi()
    t = d.now(pytz.timezone("Asia/Tashkent"))
    t = t + timedelta(days=3)
    sana = t.strftime("%d.%m.%Y")
    try :
        db_ts.add_test_oddiy(call.from_user.id, test_kodi, temp_data[call.from_user.id][0], temp_data[call.from_user.id][1], sana, 1, None)
    except Exception as e:
        for admin in ADMINS:
            await bot.send_message(int(admin), f"Test bazaga qo`shishda xatolik yuz berdi : \n{e}")
        await call.message.delete()
        await call.answer("Bazaga qo`shishda xatolik yuz berdi\nQayta urining, qayta xatolik takrorlansa, adminga murojaat qiling!", show_alert=True)
        await state.finish()
        return
    foydalanuvchi_limitlari_oddiy[call.from_user.id][0] -= 1
    await state.finish()
    await call.answer("Bazaga qo`shildi✅", show_alert=True)
    await call.message.delete()
    await call.message.answer(f"🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Oddiy</i>\n{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{temp_data[call.from_user.id][0]}</i>\n🔢<b>Savollar soni : </b><i>{len(temp_data[call.from_user.id][1])} ta</i>\n\n<b>Testda qatnashuvchilar\n\n<i>@Javob_tekshir_bot</i> 👈\n\nga javoblarini yuborishlari mumkin.</b>", reply_markup=menu.menu)
    user = db_users.select_user_id(call.from_user.id)
    if user[3] != '0':
        answer = "<b>Bu test natijasi kanalingizga joylansinmi ❓</b>\n<i>*Testni yakunlaganingizda, test natijasi bot tomonidan kanalga joylanadi.</i>"
        await call.message.answer(text=answer, reply_markup=post(test_kodi, "Oddiy_test"))
    temp_data[call.from_user.id] = None
    
    
@dp.callback_query_handler(text = "no", state="javobni_tasdiqlash_qul_oddiy")
async def yoq(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await state.set_state("test_javob_qul_oddiy")
    await call.message.answer("<b>Javoblarni tog`rilab, qayta yuboring!\n</b>", reply_markup=bekor_qilish.bekor_qil)