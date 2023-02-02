from aiogram import types
from aiogram.types import Message, CallbackQuery
from datetime import datetime, timedelta
import pytz
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from utils.misc.isbelgi import isbelgi
from keyboards.inline.post_joyla import post
from keyboards.inline.soatlar import soatlar
from keyboards.inline.minutlar import minutlar
from keyboards.inline.tushunarli import tushundim
from keyboards.inline.inline_ha_yoq import tasdiq_keyboard
from keyboards.inline.qayta import qayta
from keyboards.default import bekor_qilish, menu
import random
from loader import dp, db_users, db_ts,bot, temp_data, foydalanuvchi_limitlari_oddiy, kitoblar


@dp.message_handler(state="fan_nomi_avto_oddiy")
async def diqqat(msg : Message, state : FSMContext):
    if all(x.isalpha() or x.isspace() or isbelgi(x) for x in msg.text):
        if len(msg.text) > 2 and len(msg.text) < 31:
            fan_nomi = msg.text
            fan_nomi = fan_nomi.lower().capitalize()
            temp_data[msg.from_user.id] = [fan_nomi, "", []]
            await state.set_state("test_javob_avto_oddiy")
            await msg.answer(text=f"<b>{kitoblar[random.randint(0, 4)]}Fan nomi : </b><i>{fan_nomi}</i>\n<b>🔡Endi esa, bu fanning javoblarini yuboring :</b>\n\n<i>abcd... 👈ko`rinishida</i>", reply_markup=bekor_qilish.bekor_qil)
        else:
            await msg.answer("<b>Fan nomidagi belgilar soni 2 tadan 30 tagacha bo`lishi mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup= bekor_qilish.bekor_qil)
    else:
        await msg.answer("<b>Faqat harf va bo`sh joy yuborishingiz mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup=bekor_qilish.bekor_qil)
    
        
    
@dp.message_handler(state="test_javob_avto_oddiy")
async def javob(msg : Message, state : FSMContext):
    javob = msg.text
    if javob.isalpha():
        if len(javob) > 2 and len(javob) < 101:
            javob = javob.lower()
            temp_data[msg.from_user.id][1] = javob
            answer = f"<b>🔢Savollar soni : </b><i>{len(javob)} ta\n</i>"
            n = 1
            for harf in javob:
                answer += f"<i>{n} - {harf}\n</i>"
                n += 1
            answer += "\n<b>Javoblar to`g`riligiga ishonch hosil qiling❗️</b>\n<i>Tasdiqlaysizmi ❓</i>"
            await msg.answer(text=answer, reply_markup=tasdiq_keyboard)
            await state.set_state("javobni_tasdiqlash_avto_oddiy")
        else:
            await msg.reply("<b>Javoblar soni 3 tadan 100 tagacha bo`lishi mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup= bekor_qilish.bekor_qil)
    else :
        await msg.answer("<b>Javoblar faqat harflardan iborat bo`lishi kerak!</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup=bekor_qilish.bekor_qil)
        
@dp.callback_query_handler(text= "yes", state="javobni_tasdiqlash_avto_oddiy")
async def javob_ol(call : types.CallbackQuery, state : FSMContext):
    t = datetime.now(pytz.timezone("Asia/Tashkent"))
    vaqt = t.strftime("%H:%M")
    vaqt1 = int(t.strftime('%H'))
    if vaqt1 == 0:
        answer = f"<b>{kitoblar[random.randint(0, 4)]}Fan nomi : </b><i>{temp_data[call.from_user.id][0]}</i>\n<b>Savollar soni : </b><i>{len(temp_data[call.from_user.id][1])} ta</i>\n\n<b>Endi esa test boshlanish va tugash vaqtlarini kiriting.\n‼️Diqqat‼️\nTest boshlanish vaqtini kiritishda kiritiladigan vaqt hozirgi vaqtdan keyingi birinchi keladigan vaqt hisoblanadi.</b>\n"+"<b>Tugash vaqti esa test boshlanish vaqtidan keyin birinchi kelgan vaqt hisoblanadi.</b>"
    else :
        oldingi_vaqt = vaqt1 - 1
        answer = f"<b>{kitoblar[random.randint(0, 4)]}Fan nomi : </b><i>{temp_data[call.from_user.id][0]}</i>\n<b>Savollar soni : </b><i>{len(temp_data[call.from_user.id][1])} ta</i>\n\n<b>Endi esa test boshlanish va tugash vaqtlarini kiriting.\n‼️Diqqat‼️\nTest boshlanish vaqtini kiritishda kiritiladigan vaqt hozirgi vaqtdan keyingi birinchi keladigan vaqt hisoblanadi.</b>\n"
        answer += f"<i>Misol uchun, hozirgi vaqt : {vaqt}\nTest boshlanish vaqtini {oldingi_vaqt}:00 kiritsangiz ertangi kungi {oldingi_vaqt}:00 da test boshlanadi.</i>\n"
        answer += "<b>Tugash vaqti esa, test boshlangan vaqtdan keyingi birinchi kelgan vaqt hisoblanadi.</b>\n"
        answer += f"<i>Misol uchun, test boshlanish vaqtini 18:00, test tugash vaqtini 16:00 kiritilsa,shu kungi 18:00 da test boshlanib, ertangi kuni 16:00 da yakunlanadi!</i>\n<b>Vaqt kiritishda e`tiborli bo`ling❗️</b>.\n"
        answer += "<b><i>Test boshlanish va tugash vaqtlari teng bo`lishi mumkin emas❗️</i></b>."
    await call.message.delete()
    await call.message.answer(text=answer, reply_markup=tushundim)
    await state.set_state("tushundi_oddiy")
    
    
@dp.callback_query_handler(text = "no", state="javobni_tasdiqlash_avto_oddiy")
async def yoq(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await state.set_state("test_javob_avto_oddiy")
    await call.message.answer("Javoblarni tog`rilab, qayta yuboring!\n", reply_markup=bekor_qilish.bekor_qil)
    
    
    



@dp.callback_query_handler(state="tushundi_oddiy")
async def tuzz(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete_reply_markup()
    await call.message.answer(f"<b>Test boshlanish soatini tanlang : </b>\n"+ 
            "<i>Masalan, 20:30 uchun, test boshlanish soati  2️⃣0️⃣</i>", reply_markup=soatlar)
    await state.set_state("boshlanish_soat_qabul_oddiy")

@dp.callback_query_handler(state="boshlanish_soat_qabul_oddiy")
async def soat(call : CallbackQuery, state : FSMContext):
    soat = call.data
    temp_data[call.from_user.id][2].append(soat)
    await call.message.delete()
    await call.answer()
    await call.message.answer(f"<b>{soat} tanlandi.\nEndi esa test boshlanish daqiqasini tanlang.</b>\n"
                        + "<i>Masalan, 20:30 uchun, test boshlanish daqiqasi 3️⃣0️⃣</i>", reply_markup=minutlar)
    await state.set_state("boshlanish_minut_qabul_oddiy")


@dp.callback_query_handler(state="boshlanish_minut_qabul_oddiy")
async def minut(call : CallbackQuery, state : FSMContext):
        minut = call.data
        temp_data[call.from_user.id][2].append(minut)
        vaqt = temp_data[call.from_user.id][2]
        await call.message.delete()
        await call.answer()
        await call.message.answer(f"<b>Test boshlanish vaqti : <i>{vaqt[0]}:{vaqt[1]}</i>.</b>\n"
                        + "<b>Endi esa test tugash soatini tanlang.</b>\n"+"<i>Masalan, 22:30 uchun, test tugash soati 2️⃣2️⃣</i>", reply_markup=soatlar)
        await state.set_state("tugash_soat_qabul_oddiy")
        
@dp.callback_query_handler(state="tugash_soat_qabul_oddiy")
async def soat(call : CallbackQuery, state : FSMContext):
    soat = call.data
    temp_data[call.from_user.id][2].append(soat)
    await call.message.delete()
    await call.answer()
    await call.message.answer(f"<b>{soat} tanlandi.\nEndi esa, test tugash vaqtining daqiqasini tanlang.</b>\n"
                        + "<i>Masalan, 22:30 uchun, test tugash vaqti 3️⃣0️⃣</i>", reply_markup=minutlar)
    await state.set_state("tugash_minut_qabul_oddiy")
    
@dp.callback_query_handler(text="qayta_vaqt_kiritish", state="tugash_minut_qabul_oddiy")
async def salomm(call : types.CallbackQuery, state : FSMContext):
    temp_data[call.from_user.id][2] = []
    await call.message.delete()
    await call.message.answer(f"<b>Test boshlanish soatini tanlang : </b>\n"+ 
            "<i>Masalan, 20:30 uchun, test boshlanish soati  2️⃣0️⃣</i>", reply_markup=soatlar)
    await state.set_state("boshlanish_soat_qabul_oddiy")
    
@dp.callback_query_handler(text="test_atmen", state="tugash_minut_qabul_oddiy")
async def nima(call:types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<b>❌Jarayon bekor qilindi.</b>")
    await state.finish()
    await call.message.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
    
@dp.callback_query_handler(state="tugash_minut_qabul_oddiy")
async def minut(call : CallbackQuery, state : FSMContext):
    minut = call.data
    temp_data[call.from_user.id][2].append(minut)
    vaqt = temp_data[call.from_user.id][2]
    if vaqt[0] == vaqt[2] and vaqt[1]==vaqt[3]:
        answer = "<b>Test boshlanish vaqti bilan  tugash vaqti teng bo`lmasligi lozim❗️</b>\n"
        answer += "<i>Qaytadan kiriting yoki /cancel buyrug`ini bosing</i>"
        await call.answer("❌Vaqt bo`yicha xatolik")
        await call.message.delete()
        await call.message.answer(text=answer, reply_markup=qayta)
    else:
        hozir = datetime.now(pytz.timezone("Asia/Tashkent"))
        t = hozir.strftime("%Y-%m-%d,%H:%M:%S")
        t2 = t.split(',')
        
        
        sana = t2[0].split('-')
        vaqt_hozir = t2[1].split(':')
        
        
        hozirgi_vaqt = datetime(int(sana[0]), int(sana[1]), int(sana[2]), int(vaqt_hozir[0]), int(vaqt_hozir[1]), int(vaqt_hozir[2]))
        foydalanuvchi_kiritgan_vaqt_boshlanish = datetime(int(sana[0]), int(sana[1]), int(sana[2]), int(vaqt[0]), int(vaqt[1]))
        foydalanuvchi_kiritgan_vaqt_tugash = datetime(int(sana[0]), int(sana[1]), int(sana[2]), int(vaqt[2]), int(vaqt[3]))
        if foydalanuvchi_kiritgan_vaqt_boshlanish == hozirgi_vaqt:
            await call.message.delete()
            await call.message.answer("<b>Xatolik! Qayta urinib ko`ring. </b>", reply_markup=menu.menu)
            await state.finish()
        else :
            if foydalanuvchi_kiritgan_vaqt_boshlanish < hozirgi_vaqt:
                foydalanuvchi_kiritgan_vaqt_boshlanish = foydalanuvchi_kiritgan_vaqt_boshlanish + timedelta(days=1)
                foydalanuvchi_kiritgan_vaqt_tugash = foydalanuvchi_kiritgan_vaqt_tugash + timedelta(days=1)
            if foydalanuvchi_kiritgan_vaqt_boshlanish > foydalanuvchi_kiritgan_vaqt_tugash:
                foydalanuvchi_kiritgan_vaqt_tugash = foydalanuvchi_kiritgan_vaqt_tugash + timedelta(days=1)
            davomiylik = (foydalanuvchi_kiritgan_vaqt_tugash - foydalanuvchi_kiritgan_vaqt_boshlanish).seconds
            vaqt.append(str(davomiylik))
            davom_etish_vaqti = [davomiylik // 3600, (davomiylik - 3600 * (davomiylik // 3600)) // 60]
            boshlanish_vaqt = foydalanuvchi_kiritgan_vaqt_boshlanish.strftime("%H:%M %d-%m-%Y")
            tugash_vaqt = foydalanuvchi_kiritgan_vaqt_tugash.strftime("%H:%M %d-%m-%Y")
            test_kodi = db_users.take_test_kodi()
            vaqt = ",".join(vaqt)
            try :
                db_ts.add_test_oddiy(call.from_user.id, test_kodi, temp_data[call.from_user.id][0], temp_data[call.from_user.id][1], vaqt, 0, None)
            except Exception as e:
                for admin in ADMINS:
                    await bot.send_message(int(admin), f"<b>Test bazaga qo`shishda xatolik yuz berdi(Test kodi : {test_kodi}) : \n{e}</b>")
                await call.message.delete()
                await call.answer("Bazaga qo`shishda xatolik yuz berdi\nQayta urining, qayta xatolik takrorlansa, adminga murojaat qiling!", show_alert=True)
                await state.finish()
            
            await call.answer("Test bazaga qo`shildi✅", show_alert=True)
            await call.message.delete()
            answer = f"🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Oddiy</i>\n{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{temp_data[call.from_user.id][0]}</i>\n🔢<b>Savollar soni : </b><i>{len(temp_data[call.from_user.id][1])} ta</i>\n"
            answer += f"<b>🕐Test boshlanish vaqti : <i>{boshlanish_vaqt}</i></b>\n"
            answer += f"<b>🕑Test tugash vaqti : <i>{tugash_vaqt}</i></b>\n"
            if davom_etish_vaqti[0] == 0:
                answer += f"<b>⏳Test davomiyligi : </b><i>{davom_etish_vaqti[1]} daqiqa.</i>"
            elif davom_etish_vaqti[1] == 0:
                answer += f"<b>⏳Test davomiyligi : </b><i>{davom_etish_vaqti[0]} soat.</i>"
            else:
                answer += f"<b>⏳Test davomiyligi : </b><i>{davom_etish_vaqti[0]} soat, {davom_etish_vaqti[1]} daqiqa</i>"
                
            answer += "\n\n<b>Testda qatnashuvchilar\n\n<i>@Javob_tekshir_bot</i> 👈\n\nga javoblarini yuborishlari mumkin.</b>"
            
            
            await call.message.answer(answer, reply_markup=menu.menu) 
            foydalanuvchi_limitlari_oddiy[call.from_user.id][1] -= 1
            await state.finish()
            
            user = db_users.select_user_id(call.from_user.id)
            if user[3] != '0':
                answer = "<b>Bu test natijasi kanalingizga joylansinmi ❓</b>\n<i>*Testni yakunlaganingizda, test natijasi bot tomonidan kanalga joylanadi.</i>"
                await call.message.answer(text=answer, reply_markup=post(test_kodi, "Oddiy_test"))
            
            temp_data[call.from_user.id] = None