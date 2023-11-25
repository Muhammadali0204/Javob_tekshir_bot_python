from aiogram import types, filters
from keyboards.default.bekor_qilish import bekor_qil
from keyboards.inline.inline_ha_yoq import tasdiq_keyboard
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from keyboards.inline import mytest_oddiy_test, test_list
from keyboards.default import ortga, menu, bekor_qilish
from keyboards.inline.test_egasiga import test_owner
from loader import dp, db_users, db_bj, db_ts, bot, kitoblar, temp_data
from utils.misc import isbelgi
import asyncio
import random


@dp.callback_query_handler(state="my_tests_oddiy")
async def my_tests_oddiy(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    test_kodi = call.data
    test = db_ts.select_test_oddiy_by_test_kodi(test_kodi)
    answer = f"🔑<b>Test kodi : </b><i>{test[1]}</i>\n🗂<b>Test turi : </b><i>Oddiy</i>\n{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{test[2]}</i>\n🔢<b>Savollar soni : </b><i>{len(test[3])} ta</i>\n"
    if test[4].find(",") != -1:
        data_vaqt = test[4].split(",")
        answer += (
            f"<b>🕐Test boshlanish vaqti : <i>{data_vaqt[0]}:{data_vaqt[1]}</i></b>\n"
        )
        answer += f"<b>🕑Test tugash vaqti : <i>{data_vaqt[2]}:{data_vaqt[3]}</i></b>\n"

    await state.set_state("oddiy_testni_tahrirlash")
    await call.message.answer(answer, reply_markup=mytest_oddiy_test.test_list1(test))


@dp.callback_query_handler(state="oddiy_testni_tahrirlash", text="ortga")
async def ortgaa(call: types.CallbackQuery, state: FSMContext):
    tests_oddiy = db_ts.select_tests_by_user_id_oddiy(call.from_user.id)
    await call.message.delete()
    await call.message.answer(
        "<b>📕Oddiy testlar : </b>", reply_markup=test_list.test_listt_oddiy(tests_oddiy)
    )
    await state.set_state("my_tests_oddiy")


@dp.callback_query_handler(
    state="oddiy_testni_tahrirlash", regexp="javob_berganlar_soni:+"
)
async def qatnashganlar_soni(call: types.CallbackQuery, state: FSMContext):
    n = db_bj.count_answers_oddiy_test(call.data.split(":")[1])
    await call.answer(text=f"📜Javob berganlar soni : {n[0]} ta", show_alert=True)


@dp.callback_query_handler(
    state="oddiy_testni_tahrirlash", regexp="fan_nomini_tahrirlash:+"
)
async def qatnashganlar_soni(call: types.CallbackQuery, state: FSMContext):
    test_kodi = call.data.split(":")[1]
    temp_data[call.from_user.id] = test_kodi
    await call.message.delete()
    await call.message.answer(
        "<b>Yangi nomni yuboring : </b>", reply_markup=ortga.ortga
    )
    await state.set_state("oddiy_testni_nomini_tahrirlash")


@dp.message_handler(state="oddiy_testni_nomini_tahrirlash", text="◀️Ortga")
async def ortgaa(msg: types.Message, state: FSMContext):
    test = db_ts.select_test_oddiy_by_test_kodi(temp_data[msg.from_user.id])
    answer = f"🔑<b>Test kodi : </b><i>{test[1]}</i>\n🗂<b>Test turi : </b><i>Oddiy</i>\n{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{test[2]}</i>\n🔢<b>Savollar soni : </b><i>{len(test[3])} ta</i>\n"
    if test[4].find(",") != -1:
        data_vaqt = test[4].split(",")
        answer += (
            f"<b>🕐Test boshlanish vaqti : <i>{data_vaqt[0]}:{data_vaqt[1]}</i></b>\n"
        )
        answer += f"<b>🕑Test tugash vaqti : <i>{data_vaqt[2]}:{data_vaqt[3]}</i></b>\n"

    await state.set_state("oddiy_testni_tahrirlash")
    await msg.answer(answer, reply_markup=mytest_oddiy_test.test_list1(test))
    temp_data[msg.from_user.id] = None


@dp.message_handler(state="oddiy_testni_nomini_tahrirlash")
async def ortgaa(msg: types.Message, state: FSMContext):
    if all(x.isalpha() or x.isspace() or isbelgi.isbelgi(x) for x in msg.text):
        if len(msg.text) > 2 and len(msg.text) < 31:
            fan_nomi = msg.text
            fan_nomi = fan_nomi.lower().capitalize()
            db_ts.update_fan_nomi_oddiy_test(temp_data[msg.from_user.id], fan_nomi)
            await msg.answer(
                f"<b>{temp_data[msg.from_user.id]} - kodli testning nomi {fan_nomi} ga o'zgardi ♻️</b>",
                reply_markup=menu.menu,
            )
            await state.finish()
            temp_data[msg.from_user.id] = None
        else:
            await msg.answer(
                "<b>Fan nomidagi belgilar soni 2 tadan 30 tagacha bo`lishi mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>",
                reply_markup=bekor_qilish.bekor_qil,
            )
    else:
        await msg.answer(
            "<b>Faqat harf va bo`sh joy yuborishingiz mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>",
            reply_markup=bekor_qilish.bekor_qil,
        )


@dp.callback_query_handler(
    regexp="kanal_guruh_joylash_yoqish:+", state="oddiy_testni_tahrirlash"
)
async def kkncsknskd(call: types.CallbackQuery, state: FSMContext):
    test_kodi = call.data.split(":")[1]
    user = db_users.select_user_id(call.from_user.id)
    answer = f"{test_kodi} - test natijasi {user[4].split(',')[1]} kanal/guruhingizga avtomatik ravishda joylanadi ✅"
    db_ts.update_test_post("Oddiy_test", test_kodi, "1")
    await call.answer(answer, show_alert=True)
    await call.message.delete()
    await call.message.answer("<b><i>Menu : </i></b>", reply_markup=menu.menu)
    await state.finish()


@dp.callback_query_handler(
    regexp="kanal_guruh_joylash_ochirish:+", state="oddiy_testni_tahrirlash"
)
async def kkncsknskd(call: types.CallbackQuery, state: FSMContext):
    test_kodi = call.data.split(":")[1]
    user = db_users.select_user_id(call.from_user.id)
    answer = f"{test_kodi} - test natijasi {user[4].split(',')[1]} kanal/guruhingizga avtomatik ravishda joylash o'chirildi ❎"
    db_ts.update_test_post("Oddiy_test", test_kodi, "0")
    await call.answer(answer, show_alert=True)
    await call.message.delete()
    await call.message.answer("<b><i>Menu : </i></b>", reply_markup=menu.menu)
    await state.finish()


@dp.callback_query_handler(regexp="boshlash:+", state="oddiy_testni_tahrirlash")
async def djcnk(call: types.CallbackQuery, state: FSMContext):
    test_kodi = call.data.split(":")[1]
    db_ts.update_test_faollik("Oddiy_test", test_kodi)
    await call.answer(f"{test_kodi} - kodli test faollashdi ✅", show_alert=True)
    await call.message.delete()
    await call.message.answer(
        f"<b>{test_kodi} - kodli test faollashdi ✅</b>", reply_markup=menu.menu
    )
    await state.finish()


@dp.callback_query_handler(regexp="tugatish:+", state="oddiy_testni_tahrirlash")
async def djcnk(call: types.CallbackQuery, state: FSMContext):
    test_kodi = call.data.split(":")[1]
    javob_berganlar_malumoti = (
        db_bj.select_all_javob_berganlar_tartiblangan_oddiy_by_testkodi(test_kodi)
    )
    javob_berganlar = []  # [(1, 2, 3), (4, 5, 6, ) ... ]
    data_test_oddiy = db_ts.select_test_oddiy_by_test_kodi(test_kodi)
    for user in javob_berganlar_malumoti:
        javob_berganlar.append([db_users.select_user_id(user[0]), user])

    if javob_berganlar == []:
        await call.message.delete()
        answer = f"<b>Test yakunlandi✅</b>\n\n🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Oddiy</i>\n{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{data_test_oddiy[2]}</i>\n<b>🔢Savollar soni : </b> <i>{len(data_test_oddiy[3])} ta</i>\n\n<i>Hech kim javob bermagan ☹️</i>\n\n"
        await call.message.answer(answer, reply_markup=menu.menu)
        # Testlarni o`chirish-----------------
        db_bj.delete_answers_oddiy_by_test_kodi(test_kodi)
        db_ts.delete_answers_oddiy_by_test_kodi(test_kodi)
        await state.finish()

    else:
        await state.finish()
        # Test egasiga ------------------------------
        ragbat = "🥇"
        bal = javob_berganlar[0][1][2]
        answer = f"<b>Test yakunlandi✅</b>\n\n🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Oddiy</i>\n{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{data_test_oddiy[2]}</i>\n<b>🔢Savollar soni : </b> <i>{len(data_test_oddiy[3])} ta</i>\n\n<b>📊Natijalar : </b>\n\n"
        for i in range(0, len(javob_berganlar)):
            if bal > javob_berganlar[i][1][2]:
                if ragbat == "🥇":
                    ragbat = "🥈"
                elif ragbat == "🥈":
                    ragbat = "🥉"
                elif ragbat == "🥉":
                    ragbat = ""
                bal = javob_berganlar[i][1][2]
            answer += f"<b>{i+1}. <i>{javob_berganlar[i][0][1]}</i></b> <i>{javob_berganlar[i][1][2]} ta</i>{ragbat}\n"

        answer += "\n\n<b>✅To`g`ri javoblar : </b>\n\n"
        soni = 0
        if len(data_test_oddiy[3]) < 6:
            soni = 3
        elif len(data_test_oddiy[3]) < 16:
            soni = 4
        else:
            soni = 5
        for j in range(0, len(data_test_oddiy[3])):
            if (j + 1) % soni == 0:
                answer += f"<b>{j+1} - <i>{data_test_oddiy[3][j]}</i></b>\n"
            else:
                answer += f"<b>{j+1} - <i>{data_test_oddiy[3][j]}</i></b>  "

        answer += "\n\n<b>Testda qatnashgan barchaga rahmat 😊</b>"

        await call.answer(f"{test_kodi} - kodli test yakunlandi✅", show_alert=True)
        await call.message.delete()
        await call.message.answer(answer)

        # Testlarni o`chirish-----------------
        db_bj.delete_answers_oddiy_by_test_kodi(test_kodi)
        db_ts.delete_answers_oddiy_by_test_kodi(test_kodi)

        if data_test_oddiy[6] == "1":
            kanal = db_users.select_user_id(call.from_user.id)[4]
            if kanal == None:
                try:
                    await call.message.answer(
                        f"<b>Post joylash bo'yicha xatolik!\n\n</b><i>Kanal yoki guruh bog'lanmagan ❌</i>"
                    )
                except:
                    pass
            else:
                kanal = kanal.split(",")
                try:
                    await bot.send_message(kanal[0], text=answer)
                    await call.message.answer(
                        f"<b><code>{kanal[1]}</code> kanal/guruhiga natijalar yuborildi.</b>"
                    )
                except Exception as e:
                    await call.message.answer(
                        f"<b>Kanalga post joylash bo'yicha xatolik!</b>\n{e}"
                    )
                    await call.message.answer(
                        "<i>Adminga murojaat qiling va yuqoridagi xabarni yuboring!</i>"
                    )
