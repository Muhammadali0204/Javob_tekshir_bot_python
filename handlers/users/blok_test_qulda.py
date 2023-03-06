from loader import db_users, db_ts, temp_data, dp, kitoblar, foydalanuvchi_limitlari_blok
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from keyboards.default.bekor_qilish import bekor_qil
from utils.misc.isbelgi import isbelgi
from utils.misc.isnuqta import isnuqta
from keyboards.inline.post_joyla import post
from keyboards.inline.inline_ha_yoq import tasdiq_keyboard
from keyboards.inline.tushunarli import tushundim
from keyboards.default.menu import menu
from datetime import datetime, timedelta
import pytz




@dp.message_handler(state="fanlar_soni_blok")
async def soni(msg : Message, state : FSMContext):
    text = msg.text
    if text == "2️⃣":
        temp_data[msg.from_user.id][2] = 2
    elif text == "3️⃣":
        temp_data[msg.from_user.id][2] = 3
    elif text == "4️⃣":
        temp_data[msg.from_user.id][2] = 4
    elif text == "5️⃣":
        temp_data[msg.from_user.id][2] = 5
    else :
        await msg.answer("<b>👇Quyidagi tugmalardan foydalaning : </b>")
        return
    
    await msg.answer(text="<b>Yaxshi, 1 - fan nomini yuboring : </b>", reply_markup=bekor_qil)
    await state.set_state("fan_nomlari_blok")

@dp.message_handler(state="fan_nomlari_blok")
async def salom(msg : Message, state : FSMContext):
    if all(x.isalpha() or x.isspace() or isbelgi(x) for x in msg.text):
        if len(msg.text) > 2 and len(msg.text) < 31:
            text = msg.text
            text = text.lower().capitalize()
            temp_data[msg.from_user.id][0].append(text)
            await msg.answer(text=f"<b>{kitoblar[temp_data[msg.from_user.id][6]]}{temp_data[msg.from_user.id][6] + 1} - fanning nomi : {text}\n\n🔡Endi esa, bu fanning javoblarini yuboring : </b>\n\n<i>abcd... 👈ko`rinishida</i>")
            await state.set_state("fan_javobi_blok")
        else:
            await msg.answer("<b>Fan nomidagi belgilar soni 2 tadan 30 tagacha bo`lishi mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup= bekor_qil)
    else:
        await msg.answer("<b>Faqat harf va bo`sh joy yuborishingiz mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup=bekor_qil)
        
@dp.message_handler(state="fan_javobi_blok")
async def salom(msg : Message, state : FSMContext):
    text = msg.text
    if text.isalpha():
        if len(text) > 2 and len(text) < 51:
            text = text.lower()
            temp_data[msg.from_user.id][1].append(text)
            fan_nomi = temp_data[msg.from_user.id][0]
            answer = f"<b>{kitoblar[temp_data[msg.from_user.id][6]]}Fan nomi : {fan_nomi[temp_data[msg.from_user.id][6]]}\n🔡Javoblar soni : {len(text)} ta</b>\n\n"
            n = 1
            for harf in text:
                answer += f"<i>{n} - {harf}\n</i>"
                n += 1
            answer += "<b>Javoblar to`g`riligiga ishonch hosil qiling❗️</b>\n<i>Tasdiqlaysizmi ❓</i>"
            await msg.answer(text=answer, reply_markup=tasdiq_keyboard)
            await state.set_state("javob_tasdiqlash_blok")
        else:
            await msg.reply("<b>Javoblar soni 3 tadan 50 tagacha bo`lishi mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup= bekor_qil)
    else :
        await msg.answer("<b>Javoblar faqat harflardan iborat bo`lishi kerak❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup=bekor_qil)
        
@dp.callback_query_handler(text="yes", state="javob_tasdiqlash_blok")
async def salomm(call : CallbackQuery, state : FSMContext):
    await call.answer("Qabul qilindi!")
    await call.message.delete()
    await call.message.answer("<b>Endi esa, bu fanga beriladigan ballni kiriting : </b>\n\n<i>Misol uchun : 3.1\n*Musbat o`nli kasr son kiritishingiz mumkin!\n</i>")
    await state.set_state("fanga_bal")
    
@dp.callback_query_handler(text="no", state="javob_tasdiqlash_blok")
async def salomm(call : CallbackQuery, state : FSMContext):
    temp_data[call.from_user.id][1].pop(-1)
    await call.message.delete()
    await call.message.answer("<b>Javoblarni tog`rilab, qayta yuboring!</b>\n", reply_markup=bekor_qil)
    await state.set_state("fan_javobi_blok")
    
    
@dp.message_handler(state="fanga_bal")
async def salommm(msg : Message, state : FSMContext):
    if all(x.isnumeric() or isnuqta(x) for x in msg.text):
        son = float(msg.text)
        if son > 0 and son <= 10:
            temp_data[msg.from_user.id][3].append(str(son))
            temp_data[msg.from_user.id][6] += 1
            await state.set_state("fan_nomlari_blok")
            if temp_data[msg.from_user.id][6] == temp_data[msg.from_user.id][2]:
                if temp_data[msg.from_user.id][5] == 0:
                    t = datetime.now(pytz.timezone("Asia/Tashkent"))
                    vaqt = t.strftime("%H:%M")
                    vaqt1 = int(t.strftime('%H'))
                    if vaqt1 == 0:
                        answer = f"<b>Endi esa test boshlanish va tugash vaqtlarini kiriting.\n‼️Diqqat‼️\nTest boshlanish vaqtini kiritishda kiritiladigan vaqt hozirgi vaqtdan keyingi birinchi keladigan vaqt hisoblanadi.</b>\n"+"<b>Tugash vaqti esa test boshlanish vaqtidan keyin birinchi kelgan vaqt hisoblanadi.</b>"
                    else :
                        oldingi_vaqt = vaqt1 - 1
                        answer = f"<b>Endi esa test boshlanish va tugash vaqtlarini kiriting.\n‼️Diqqat‼️\nTest boshlanish vaqtini kiritishda kiritiladigan vaqt hozirgi vaqtdan keyingi birinchi keladigan vaqt hisoblanadi.</b>\n"
                        answer += f"<i>Misol uchun, hozirgi vaqt : {vaqt}\nTest boshlanish vaqtini {oldingi_vaqt}:00 kiritsangiz ertangi kungi {oldingi_vaqt}:00 da test boshlanadi.</i>\n"
                        answer += "<b>Tugash vaqti esa, test boshlangan vaqtdan keyingi birinchi kelgan vaqt hisoblanadi.</b>\n"
                        answer += f"<i>Misol uchun, test boshlanish vaqtini 18:00, test tugash vaqtini 16:00 kiritilsa,shu kungi 18:00 da test boshlanib, ertangi kuni 16:00 da yakunlanadi!</i>\n<b>Vaqt kiritishda e`tiborli bo`ling❗️</b>.\n"
                        answer += "<b><i>Test boshlanish va tugash vaqtlari teng bo`lishi mumkin emas❗️</i></b>."
                    await msg.answer(text=answer, reply_markup=tushundim)
                    await state.set_state("blok_test_avto_vaqt")
                elif temp_data[msg.from_user.id][5] == 1:
                    test_kodi = db_users.take_test_kodi()
                    a0 = ",".join(temp_data[msg.from_user.id][0])
                    a1 = ",".join(temp_data[msg.from_user.id][1])
                    a3 = ",".join(temp_data[msg.from_user.id][3])
                    t = datetime.now(pytz.timezone("Asia/Tashkent"))
                    t = t + timedelta(days=3)
                    sana = t.strftime("%d.%m.%Y")
                    db_ts.add_test_blok(msg.from_user.id, test_kodi, a0, a1, a3, sana, 1, None)
                    await msg.answer("<b>Test bazaga qo`shildi✅</b>")
                    foydalanuvchi_limitlari_blok[msg.from_user.id][0] -= 1
                    fanlar = temp_data[msg.from_user.id][0]
                    javoblar = temp_data[msg.from_user.id][1]
                    beriladigan_ballar = temp_data[msg.from_user.id][3]
                    answer = f"🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Blok test</i>\n🟢<b>Fanlar soni : </b><i>{temp_data[msg.from_user.id][2]} ta</i>\n\n"
                    umumiy_ball = 0
                    q = [1, len(javoblar[0])]
                    for i in range(0, temp_data[msg.from_user.id][2]):
                        if i != 0:
                                q[0] += len(javoblar[i-1])
                                q[1] += len(javoblar[i])
                        answer += f"<b>{i+1} - fan : </b>\n"
                        answer += f"<b>{kitoblar[i]}Fan nomi : </b><i>{fanlar[i]}</i>\n"
                        answer += f"<b>🔢Savollar soni : <i>{len(javoblar[i])} ta</i></b><i> ({q[0]}-{q[1]})</i>\n"
                        answer += f"<b>❕Ball : </b><i>{beriladigan_ballar[i]}</i>\n"
                        umumiy_ball += len(javoblar[i]) * float(beriladigan_ballar[i])
                        answer += f"<i>Fan uchun beriladigan ball : {round(len(javoblar[i]) * float(beriladigan_ballar[i]), 4)} ball</i>\n\n"
                    answer += f"<b>Jami savollar soni : </b><i>{q[1]} ta</i>\n"
                    answer += f"<b>Umumiy ball : </b><i>{round(umumiy_ball, 4)} ball</i>"
                    answer += "\n\n<b>Testda qatnashuvchilar\n\n<i>@Javob_tekshir_bot</i> 👈\n\nga javoblarini yuborishlari mumkin.</b>"
                    await msg.answer(text=answer, reply_markup=menu)
                    await state.finish()
                    
                    user = db_users.select_user_id(msg.from_user.id)
                    if user[3] != '0' and user[3] != '-1' and user[4] != None:
                        kanal = user[4].split(',')[1]
                        answer = f"<b>Bu test natijasi {kanal} kanal/guruhingizga joylansinmi ❓</b>\n\n<i>*Testni yakunlaganingizda, test natijasi bot tomonidan kanalga joylanadi.</i>"
                        await msg.answer(text=answer, reply_markup=post(test_kodi, "Blok_test"))
                    
                    temp_data[msg.from_user.id] = None
            else:
                await msg.answer(f"<b>Yaxshi, {temp_data[msg.from_user.id][6] + 1} - fan nomini yuboring : </b>")
        else:
            await msg.reply("<b>Ball 0 dan katta va 10 dan kichik bo`lishi mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup= bekor_qil)
    else:
        await msg.answer("<b>Son kiriting❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup=bekor_qil)