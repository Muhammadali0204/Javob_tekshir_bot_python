from aiogram import types, filters
from keyboards.default.bekor_qilish import bekor_qil
from keyboards.inline.inline_ha_yoq import tasdiq_keyboard
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from keyboards.inline import mytest_blok_test, test_list, blok_test_fan_tah
from keyboards.default import ortga, menu, bekor_qilish
from keyboards.inline.test_egasiga import test_owner
from loader import dp, db_users, db_bj, db_ts, bot, kitoblar, temp_data
from utils.misc import isbelgi
import asyncio
import random


@dp.callback_query_handler(state="my_tests_blok")
async def my_tests_oddiy(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    test_kodi = call.data
    test = db_ts.select_test_blok_by_test_kodi(test_kodi)
    answer = f"🔑<b>Test kodi : </b><i>{test[1]}</i>\n🗂<b>Test turi : </b><i>Blok</i>\n"
    fan_nomlari = test[2].split(',')
    answer += f"<b>🔢Fanlar soni : {len(fan_nomlari)}\n📚Fanlar : \n</b>"
    javoblar = test[3].split(',')
    ballar = test[4].split(',')
    for n in range(0, len(fan_nomlari)):
        answer += f"{kitoblar[random.randint(0, 4)]}<b>{fan_nomlari[n]} <i>{len(javoblar[n])} ta savol, {ballar[n]} ball</i></b>\n"

    if test[5].find(',') != -1:
        data_vaqt = test[5].split(',')
        answer += f"<b>🕐Test boshlanish vaqti : <i>{data_vaqt[0]}:{data_vaqt[1]}</i></b>\n"
        answer += f"<b>🕑Test tugash vaqti : <i>{data_vaqt[2]}:{data_vaqt[3]}</i></b>\n"
    await call.message.answer(answer, reply_markup=mytest_blok_test.test_list2(test))
    await state.set_state('blok_testni_tahrirlash')


@dp.callback_query_handler(state="blok_testni_tahrirlash", text="ortga")
async def ortgaaa(call: types.CallbackQuery, state: FSMContext):
    tests_blok = db_ts.select_tests_by_user_id_blok(call.from_user.id)
    await call.message.delete()
    await call.message.answer("<b>📚Blok testlar : </b>", reply_markup=test_list.test_listt_blok(tests_blok))
    await state.set_state("my_tests_blok")


@dp.callback_query_handler(state="blok_testni_tahrirlash", regexp="javob_berganlar_soni:+")
async def qatnashganlar_soni(call: types.CallbackQuery, state: FSMContext):
    n = db_bj.count_answers_blok_test(call.data.split(':')[1])
    await call.answer(text=f"📜Javob berganlar soni : {n[0]} ta", show_alert=True)


@dp.callback_query_handler(state="blok_testni_tahrirlash", regexp="fan_nomini_tahrirlash:+")
async def qatnashganlar_soni(call: types.CallbackQuery, state: FSMContext):
    test_kodi = call.data.split(':')[1]
    temp_data['blok_testning_fan_nomini_tahrirlash'] = test_kodi
    test_blok = db_ts.select_test_blok_by_test_kodi(test_kodi)
    fanlar = test_blok[2].split(',')
    await call.message.answer("<b>Tahrirlamoqchi bo'lgan faningizni tanlang 👇</b>", reply_markup=blok_test_fan_tah.blok_test_fanlar(fanlar, test_kodi))
    await state.set_state("blok_test_fan_tahrirlash")
    await call.message.delete()


@dp.callback_query_handler(state="blok_test_fan_tahrirlash", regexp="ortga:+")
async def qatnashganlar_soni(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    test_kodi = call.data.split(':')[1]
    test = db_ts.select_test_blok_by_test_kodi(test_kodi)
    answer = f"🔑<b>Test kodi : </b><i>{test[1]}</i>\n🗂<b>Test turi : </b><i>Blok</i>\n"
    fan_nomlari = test[2].split(',')
    answer += f"<b>🔢Fanlar soni : {len(fan_nomlari)}\n📚Fanlar : \n</b>"
    javoblar = test[3].split(',')
    ballar = test[4].split(',')
    for n in range(0, len(fan_nomlari)):
        answer += f"{kitoblar[random.randint(0, 4)]}<b>{fan_nomlari[n]} <i>{len(javoblar[n])} ta savol, {ballar[n]} ball</i></b>\n"

    if test[5].find(',') != -1:
        data_vaqt = test[5].split(',')
        answer += f"<b>🕐Test boshlanish vaqti : <i>{data_vaqt[0]}:{data_vaqt[1]}</i></b>\n"
        answer += f"<b>🕑Test tugash vaqti : <i>{data_vaqt[2]}:{data_vaqt[3]}</i></b>\n"
    await call.message.answer(answer, reply_markup=mytest_blok_test.test_list2(test))
    await state.set_state('blok_testni_tahrirlash')


@dp.callback_query_handler(state="blok_test_fan_tahrirlash")
async def qatnashganlar_soni(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = call.data.split(':')
    answer = f"<b>Tahrirlanayotgan fan {data[2]}\n\nYangi nom yuboring 👇</b>"
    temp_data[call.from_user.id] = data
    await call.message.answer(answer, reply_markup=ortga.ortga)
    await state.set_state("blok_test_fan_tahrirlash1")

@dp.message_handler(state="blok_test_fan_tahrirlash1", text="◀️Ortga")
async def sddfb(msg: types.Message, state: FSMContext):
    try :
        test_kodi = temp_data["blok_testning_fan_nomini_tahrirlash"]
    except :
        await msg.answer("<b><i>Menu : </i></b>", reply_markup=menu.menu)
        await state.finish()
    test_blok = db_ts.select_test_blok_by_test_kodi(test_kodi)
    fanlar = test_blok[2].split(',')
    await msg.answer("<b>Tahrirlamoqchi bo'lgan faningizni tanlang 👇</b>", reply_markup=blok_test_fan_tah.blok_test_fanlar(fanlar, test_kodi))
    await state.set_state("blok_test_fan_tahrirlash")

@dp.message_handler(state="blok_test_fan_tahrirlash1")
async def tahrirlash(msg: types.Message, state: FSMContext):
    if all(x.isalpha() or x.isspace() or isbelgi.isbelgi(x) for x in msg.text):
        if len(msg.text) > 2 and len(msg.text) < 31:
            fan_nomi = msg.text
            fan_nomi = fan_nomi.lower().capitalize()
            test = db_ts.select_test_blok_by_test_kodi(
                temp_data[msg.from_user.id][0])
            fan_nomlari = test[2].split(',')
            fan_nomlari[int(temp_data[msg.from_user.id][1])] = fan_nomi
            fan_nomi1 = ",".join(fan_nomlari)
            db_ts.update_fan_nomi_blok_test(
                temp_data[msg.from_user.id][0], fan_nomi1)
            await msg.answer(f"<b>{temp_data[msg.from_user.id][0]} - kodli blok testning {int(temp_data[msg.from_user.id][1]) + 1} - fani nomi {fan_nomi} ga o'zgardi ♻️</b>", reply_markup=menu.menu)
            await state.finish()
            temp_data[msg.from_user.id] = None
        else:
            await msg.answer("<b>Fan nomidagi belgilar soni 2 tadan 30 tagacha bo`lishi mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup=bekor_qilish.bekor_qil)
    else:
        await msg.answer("<b>Faqat harf va bo`sh joy yuborishingiz mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup=bekor_qilish.bekor_qil)
        
    
    
@dp.callback_query_handler(regexp="kanal_guruh_joylash_yoqish:+", state="blok_testni_tahrirlash")
async def kkncsknskd(call : types.CallbackQuery, state  :FSMContext):
    test_kodi = call.data.split(':')[1]
    user = db_users.select_user_id(call.from_user.id)
    answer = f"{test_kodi} - test natijasi {user[4].split(',')[1]} kanal/guruhingizga avtomatik ravishda joylanadi ✅"
    db_ts.update_test_post("Blok_test", test_kodi, "1")
    await call.answer(answer, show_alert=True)
    await call.message.delete()
    await call.message.answer("<b><i>Menu : </i></b>", reply_markup=menu.menu)
    await state.finish()
    
    
@dp.callback_query_handler(regexp="kanal_guruh_joylash_ochirish:+", state="blok_testni_tahrirlash")
async def kkncsknskd(call : types.CallbackQuery, state  :FSMContext):
    test_kodi = call.data.split(':')[1]
    user = db_users.select_user_id(call.from_user.id)
    answer = f"{test_kodi} - test natijasi {user[4].split(',')[1]} kanal/guruhingizga avtomatik ravishda joylash o'chirildi ❎"
    db_ts.update_test_post("Blok_test", test_kodi, "0")
    await call.answer(answer, show_alert=True)
    await call.message.delete()
    await call.message.answer("<b><i>Menu : </i></b>", reply_markup=menu.menu)
    await state.finish()


@dp.callback_query_handler(regexp = "boshlash:+", state = "blok_testni_tahrirlash")
async def djcnk(call : types.CallbackQuery, state : FSMContext):
    test_kodi = call.data.split(":")[1]
    db_ts.update_test_faollik("Blok_test", test_kodi)
    await call.answer(f"{test_kodi} - kodli test faollashdi ✅", show_alert=True)
    await call.message.delete()
    await call.message.answer(f"<b>{test_kodi} - kodli test faollashdi ✅</b>", reply_markup=menu.menu)
    await state.finish()


@dp.callback_query_handler(regexp = "tugatish:+", state = "blok_testni_tahrirlash")
async def djcnk(call : types.CallbackQuery, state : FSMContext):
    test_kodi = call.data.split(":")[1]
    javob_berganlar_malumoti = db_bj.select_all_javob_berganlar_tartiblangan_blok_by_testkodi(
                test_kodi)
    javob_berganlar = []  # [(1, 2, 3), (4, 5, 6, ) ... ]
    data_test_blok = db_ts.select_test_blok_by_test_kodi(test_kodi)
    for user in javob_berganlar_malumoti:
        javob_berganlar.append(
            [db_users.select_user_id(user[0]), user])

    fan_nomlari = data_test_blok[2].split(',')
    javoblar = data_test_blok[3].split(',')
    beriladigan_ballar = data_test_blok[4].split(',')

    db_bj.delete_answers_blok_by_test_kodi(test_kodi)
    db_ts.delete_answers_blok_by_test_kodi(test_kodi)
    
    if javob_berganlar == []:
        await call.message.delete()
        answer = f"<b>Test yakunlandi ✅</b>\n\n🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Blok test</i>\n🟢<b>Fanlar soni : </b><i>{len(fan_nomlari)} ta\n\nHech kimjavob bermagan ☹️</i>"
        await call.message.answer(answer, reply_markup=menu.menu)
        await state.finish()
        
    else:
        await state.finish()
        # Test egasiga ------------------------------
        answer = f"<b>Test yakunlandi ✅</b>\n\n🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Blok test</i>\n🟢<b>Fanlar soni : </b><i>{len(fan_nomlari)} ta</i>\n\n"
        umumiy_ball = 0
        q = [1, len(javoblar[0])]
        for i in range(0, len(fan_nomlari)):
            if i != 0:
                q[0] += len(javoblar[i-1])
                q[1] += len(javoblar[i])
            answer += f"<b>{i+1} - fan : </b>\n"
            answer += f"<b>{kitoblar[i]}Fan nomi : </b><i>{fan_nomlari[i]}</i>\n"
            answer += f"<b>🔢Savollar soni : <i>{len(javoblar[i])} ta</i></b><i> ({q[0]}-{q[1]})</i>\n"
            answer += f"<b>❕Ball : </b><i>{beriladigan_ballar[i]}</i>\n"
            umumiy_ball += len(javoblar[i]) * float(beriladigan_ballar[i])
            answer += f"<i>Fan uchun beriladigan ball : {round(len(javoblar[i]) * float(beriladigan_ballar[i]), 4)}</i>\n\n"
        answer += f"<b>Jami savollar soni : </b><i>{q[1]} ta</i>\n"
        answer += f"<b>Umumiy ball : </b><i>{round(umumiy_ball, 4)}</i>\n\n<b>📊Natijalar : </b>\n\n"
        ragbat = '🥇'
        bal = javob_berganlar[0][1][4]
        for i in range(0, len(javob_berganlar)):
            if bal > javob_berganlar[i][1][4]:
                if ragbat == '🥇':
                    ragbat = '🥈'
                elif ragbat == '🥈':
                    ragbat = '🥉'
                elif ragbat == '🥉':
                    ragbat = ''
                bal = javob_berganlar[i][1][4]
            answer += f"<b>{i+1}. <i>{javob_berganlar[i][0][1]}</i></b> <i>{round(float(javob_berganlar[i][1][4]), 4)} ball</i>{ragbat}\n"

        answer += "\n<b>✅To`g`ri javoblar : </b>\n\n"
        for i in range(0, len(fan_nomlari)):
            answer += f"<b>{i+1} - fan : {kitoblar[random.randint(0, 4)]}<i>{fan_nomlari[i]}</i></b>\n"
            soni = 0
            if len(javoblar[i]) < 6:
                soni = 3
            elif len(javoblar[i]) < 16:
                soni = 4
            else:
                soni = 5

            for j in range(0, len(javoblar[i])):
                if (j+1) % soni == 0:
                    answer += f"<b>{j+1} - <i>{javoblar[i][j]}</i></b>\n"
                else:
                    answer += f"<b>{j+1} - <i>{javoblar[i][j]}</i></b>  "

            answer += "\n\n"

        answer += "\n<b>Testda qatnashgan barchaga rahmat 😊</b>"

        await call.answer(f"{test_kodi} - kodli test yakunlandi✅", show_alert=True)
        await call.message.delete()
        await call.message.answer(answer)

        if data_test_blok[7] == '1':
            kanal = db_users.select_user_id(call.from_user.id)[4]
            if kanal == None:
                try:
                    await call.message.answer(f"<b>Kanalga post joylash bo'yicha xatolik!\n\n</b><i>Kanal yoki guruh bog'lanmagan ❌</i>")
                except:
                    pass
            else:
                kanal = kanal.split(",")
                try:
                    await bot.send_message(kanal[0], text=answer)
                    await call.message.answer(f"<b><code>{kanal[1]}</code> kanal/guruhiga natijalar yuborildi.</b>")
                except Exception as e:
                    await call.message.answer(f"<b>Kanalga post joylash bo'yicha xatolik!</b>\n{e}")
                    await call.message.answer("<i>Adminga murojaat qiling va yuqoridagi xabarni yuboring!</i>")