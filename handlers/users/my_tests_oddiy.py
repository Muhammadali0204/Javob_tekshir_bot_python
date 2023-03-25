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
    if test[4].find(',') != -1:
        data_vaqt = test[4].split(',')
        answer += f"<b>🕐Test boshlanish vaqti : <i>{data_vaqt[0]}:{data_vaqt[1]}</i></b>\n"
        answer += f"<b>🕑Test tugash vaqti : <i>{data_vaqt[2]}:{data_vaqt[3]}</i></b>\n"

    await state.set_state("oddiy_testni_tahrirlash")
    await call.message.answer(answer, reply_markup=mytest_oddiy_test.test_list1(test))


@dp.callback_query_handler(state="oddiy_testni_tahrirlash", text="ortga")
async def ortgaa(call: types.CallbackQuery, state: FSMContext):
    tests_oddiy = db_ts.select_tests_by_user_id_oddiy(call.from_user.id)
    await call.message.delete()
    await call.message.answer("<b>📕Oddiy testlar : </b>", reply_markup=test_list.test_listt_oddiy(tests_oddiy))
    await state.set_state("my_tests_oddiy")


@dp.callback_query_handler(state="oddiy_testni_tahrirlash", regexp="javob_berganlar_soni:+")
async def qatnashganlar_soni(call: types.CallbackQuery, state: FSMContext):
    n = db_bj.count_answers_oddiy_test(call.data.split(':')[1])
    await call.answer(text=f"📜Javob berganlar soni : {n[0]} ta", show_alert=True)


@dp.callback_query_handler(state="oddiy_testni_tahrirlash", regexp="fan_nomini_tahrirlash:+")
async def qatnashganlar_soni(call: types.CallbackQuery, state: FSMContext):
    test_kodi = call.data.split(":")[1]
    temp_data[call.from_user.id] = test_kodi
    await call.message.delete()
    await call.message.answer("<b>Yangi nomni yuboring : </b>", reply_markup=ortga.ortga)
    await state.set_state("oddiy_testni_nomini_tahrirlash")


@dp.message_handler(state="oddiy_testni_nomini_tahrirlash", text="◀️Ortga")
async def ortgaa(msg: types.Message, state: FSMContext):
    test = db_ts.select_test_oddiy_by_test_kodi(temp_data[msg.from_user.id])
    answer = f"🔑<b>Test kodi : </b><i>{test[1]}</i>\n🗂<b>Test turi : </b><i>Oddiy</i>\n{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{test[2]}</i>\n🔢<b>Savollar soni : </b><i>{len(test[3])} ta</i>\n"
    if test[4].find(',') != -1:
        data_vaqt = test[4].split(',')
        answer += f"<b>🕐Test boshlanish vaqti : <i>{data_vaqt[0]}:{data_vaqt[1]}</i></b>\n"
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
            db_ts.update_fan_nomi_oddiy_test(
                temp_data[msg.from_user.id], fan_nomi)
            await msg.answer(f"<b>{temp_data[msg.from_user.id]} - kodli testning nomi {fan_nomi} ga o'zgardi ♻️</b>", reply_markup=menu.menu)
            await state.finish()
            temp_data[msg.from_user.id] = None
        else:
            await msg.answer("<b>Fan nomidagi belgilar soni 2 tadan 30 tagacha bo`lishi mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup=bekor_qilish.bekor_qil)
    else:
        await msg.answer("<b>Faqat harf va bo`sh joy yuborishingiz mumkin❗️</b>\n<i>Qayta yuboring yoki /cancel ni bosing.</i>", reply_markup=bekor_qilish.bekor_qil)
