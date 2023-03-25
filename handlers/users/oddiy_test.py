from aiogram import types
from aiogram.types import Message, ReplyKeyboardRemove
from datetime import datetime as d
import time
from aiogram.dispatcher import FSMContext
from keyboards.inline.inline_ha_yoq import tasdiq_keyboard
from keyboards.inline.avto_qulda import avto_qul, avto_qul2
from keyboards.default import menu, bekor_qilish, test_turi
from loader import dp, db_users, db_ts, db_bj, bot, foydalanuvchi_limitlari_oddiy


@dp.message_handler(text="📘Oddiy test", state="test_turi")
async def tur(msg: types.Message, state: FSMContext):
    await msg.answer(text="<b>📘Oddiy test</b>", reply_markup=ReplyKeyboardRemove())
    await msg.answer(
        text="<b>Tuzmoqchi bo`lgan testingiz <i>Avto</i> yakunlansinmi yoki o`zingiz yakunlaysizmi ❓</b>",
        reply_markup=avto_qul
    )
    await state.set_state("avto_qul_oddiy")


@dp.callback_query_handler(text="avto", state="avto_qul_oddiy")
async def avto(call: types.CallbackQuery, state: FSMContext):
    try:
        if foydalanuvchi_limitlari_oddiy[call.from_user.id][1] < 1:
            await call.answer(text="Afsuski bunday test tuzolmaysiz❗️\nLimitingiz tugagan.Batafsil : \n🛠Sozlamalar/⬆️Limitlarni oshirish", show_alert=True)
            await call.message.delete()
            await call.message.answer(text="<b>Test tuzish : </b>",
                                      reply_markup=test_turi.tur)
            await state.set_state("test_turi")
        else:
            await call.message.delete()
            await call.message.answer(text="<b>Yaxshi, fan nomini yuboring!</b>\n\n<i>Masalan : Matematika</i>", reply_markup=bekor_qilish.bekor_qil)
            await state.set_state("fan_nomi_avto_oddiy")
    except:
        await call.message.delete()
        await call.message.answer("<b>Iltimos /start ni bosing va ism familiyangizni kiriting!</b>", reply_markup=menu.menu)
        await state.finish()


@dp.callback_query_handler(text="qul", state="avto_qul_oddiy")
async def qul(call: types.CallbackQuery, state: FSMContext):
    try:
        if foydalanuvchi_limitlari_oddiy[call.from_user.id][0] < 1:
            await call.message.delete()
            await call.answer(text="Afsuski bunday test tuzolmaysiz❗️\nLimitingiz tugagan.Batafsil : \n🛠Sozlamalar/⬆️Limitlarni oshirish", show_alert=True)
            await call.message.answer(text="<b>Test tuzish : </b>",
                                      reply_markup=test_turi.tur)
            await state.set_state("test_turi")
        else:
            await call.message.delete()
            await call.message.answer(text="<b>Yaxshi, fan nomini yuboring!</b>\n\n<i>Masalan : Matematika</i>", reply_markup=bekor_qilish.bekor_qil)
            await state.set_state("fan_nomi_qul_oddiy")
    except:
        await call.message.delete()
        await call.message.answer("<b>Iltimos /start ni bosing va ism familiyangizni kiriting!</b>", reply_markup=menu.menu)
        await state.finish()


@dp.callback_query_handler(text="info", state="avto_qul_oddiy")
async def info(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.answer("Batafsil ma`lumot👇")
    await call.message.answer(text="<b>*Manual - tuzgan testingizni tugma bosish orqali yakunlaysiz.\nTest tuzilganidan boshlab faol ya'ni foydalanuvchilar javob berishi mumkin bo`ladi.</b>\n" +
                              "<b>*Avto - tuzgan testingiz siz ko`rsatgan vaqtda avtomatik ravishda boshlanib, yakunlanish vaqti yetganda avtomatik yakunlanadi.\nTest tuzilganidan boshlab faol bo`lmaydi ya`ni boshlanish vaqti yetmaguncha hech kim javob bera olmaydi.\n</b><b><i>*Test ishtirokchilariga avvaldan test kodi va test haqida ma`lumotlar berish uchun qulay✅\nTest siz ko`rsatgan muddatda bo`lib o`tadi😎</i></b>\n<i>(Testni muddatidan avval ham yakunlashingiz mumkin!)</i>", reply_markup=avto_qul2)


@dp.callback_query_handler(text="ortga", state="avto_qul_oddiy")
async def ortga(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        text="Qanday test tuzmoqchisiz?", reply_markup=test_turi.tur
    )
    await state.set_state("test_turi")
