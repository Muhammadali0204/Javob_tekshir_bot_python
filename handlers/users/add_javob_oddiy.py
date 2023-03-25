from aiogram import types
from keyboards.default.menu import menu
from keyboards.default.bekor_qilish import bekor_qil
from keyboards.inline.inline_ha_yoq import tasdiq_keyboard
from aiogram.dispatcher import FSMContext
from keyboards.inline.test_egasiga import test_owner
from keyboards.inline.javob_yuborishni_boshlash import boshlash
from loader import dp, db_users, db_bj, db_ts, bot, temp_data, kitoblar
import random


@dp.message_handler(state="javoblar_junatiladi")
async def keldi_javoblar(msg: types.Message, state: FSMContext):
    berilgan_javob = msg.text
    if berilgan_javob.isalpha():
        berilgan_javob_size = len(berilgan_javob)
        haqiqiy_javob_uzunligi = temp_data[msg.from_user.id][1]
        if haqiqiy_javob_uzunligi == berilgan_javob_size:
            berilgan_javob = berilgan_javob.lower()
            temp_data[msg.from_user.id][2] = berilgan_javob
            answer = ""
            n = 1
            for harf in berilgan_javob:
                answer += f"<i>{n} - {harf}\n</i>"
                n += 1
            answer += "<b>To`g`ri ekanligiga ishonch hosil qiling❗️</b>\n<i>Tasdiqlaysizmi ❓</i>"
            await msg.answer(answer, reply_markup=tasdiq_keyboard)
            await state.set_state("berilgan_javobni_tasdiqlash")
        else:
            await msg.answer(f"<b>Bu testning javoblari soni {haqiqiy_javob_uzunligi} ta.\nAmmo siz {berilgan_javob_size} ta javob yubordingiz❌</b>\n<i>Savollar soniga mos holda javoblarni qayta yuboring : </i>", reply_markup=bekor_qil)
    else:
        await msg.answer("<b>Testning javobi faqat lotin harflaridan iborat!</b>\n<i>Qayta kiriting yoki bekor qiling.</i>", reply_markup=bekor_qil)


@dp.callback_query_handler(text='yes', state="berilgan_javobni_tasdiqlash")
async def tekshir(call: types.CallbackQuery, state: FSMContext):
    kod = temp_data[call.from_user.id][0]
    data_test = db_ts.select_test_oddiy_by_test_kodi(kod)
    if data_test == None:
        await call.answer("😕")
        await call.message.delete()
        await call.message.answer("<b>Afsuski test yakunlandi❌</b>\n<i>Biroz kechikdingiz!</i>", reply_markup=menu)
        await state.finish()
    else:
        bergan_javobi = temp_data[call.from_user.id][2]
        aniq_javob_size = len(data_test[3])
        aniq_javob = data_test[3]
        xato_javoblari = ""
        xato_javoblari_list = []
        tuplagan_bal = 0
        for i in range(0, aniq_javob_size):
            if bergan_javobi[i] == aniq_javob[i]:
                tuplagan_bal += 1
            else:
                xato_javoblari_list.append(i+1)
        xato_javoblari += ",".join([
            f"{item}" for item in xato_javoblari_list
        ])
        try:
            db_bj.add_javob_oddiy(call.from_user.id, kod,
                                  tuplagan_bal, xato_javoblari)
        except Exception as e:
            print(e)
        answer = f"🔑<b>Test kodi : </b><i>{kod}</i>\n🗂<b>Test turi : </b><i>Oddiy</i>\n{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{data_test[2]}</i>\n✅<b>To`g`ri javoblar soni : </b><i>{tuplagan_bal} ta</i>\n❌<b>Xato javoblar soni : </b><i>{aniq_javob_size - tuplagan_bal} ta\n\n</i>"
        vergul = data_test[4].find(',')
        if vergul != -1:
            vaqt = data_test[4].split(',')
            answer += f"🕐<i>Test {vaqt[2]}:{vaqt[3]} da yakunlanadi.</i>\n\n"
        await call.message.answer(answer, reply_markup=menu)
        await call.answer(f"{kod} - testga javob berdingiz ✅", show_alert=True)
        await call.message.delete()
        await state.finish()
        temp_data[call.from_user.id] = None
        user = db_users.select_user_id(call.from_user.id)
        if user[2] == None:
            username = "username mavjud emas!"
        else:
            username = f"@{user[2]}"
        answer_admin = f"<b>{kod} - testga </b><i>{user[1]}</i><b><i>({username})</i> javob jo`natdi.</b>"
        await bot.send_message(data_test[0], answer_admin, reply_markup=test_owner(kod))


@dp.callback_query_handler(text='no', state="berilgan_javobni_tasdiqlash")
async def tekshir(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Javoblarni tog`rilab, qayta yuboring!\n</b>", reply_markup=bekor_qil)
    await state.set_state("javoblar_junatiladi")
