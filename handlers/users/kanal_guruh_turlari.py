from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.botgautish import kanal_guruh, kanalga_qush
from keyboards.default.bekor_qilish import bekor_qil
from loader import dp, db_users, Limitlar_oddiy, Limitlar_blok, premium_narxi, temp_data, bot
import pytz, asyncio
from datetime import datetime, timedelta


@dp.callback_query_handler(text="tayyor", state="okanal")
async def kanal(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    photo_id = "AgACAgIAAxkBAAEUA_Vj5mkIFh5ZGQRablCSNOHMa00vfgACg8QxG2QpOUtiflWjFZipaAEAAwIAA3kAAy4E"
    await call.message.answer_photo(photo_id, "<b>Endi esa, kanalingiz havolasini <code>@kanalingiz_havolasi</code> ko'rinishida yuboring.</b>\n<i>Misol uchun : @online_test_matematika1</i>")
    await state.set_state("o_kanal_havolasi")

@dp.callback_query_handler(text="tayyor", state="skanal")
async def kanal(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    photo_id = "AgACAgIAAxkBAAEUA_Vj5mkIFh5ZGQRablCSNOHMa00vfgACg8QxG2QpOUtiflWjFZipaAEAAwIAA3kAAy4E"
    await call.message.answer_photo(photo_id, caption="<b>Endi esa, kanalingizdan istalgan postni havolasi bilan yuboring.</b><i>*Rasmga qarang❗️</i>")
    await state.set_state("s_kanal_posti")

@dp.callback_query_handler(text="tayyor", state="oguruh")
async def kanal(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    photo_id = "AgACAgIAAxkBAAEUA_Vj5mkIFh5ZGQRablCSNOHMa00vfgACg8QxG2QpOUtiflWjFZipaAEAAwIAA3kAAy4E"
    await call.message.answer_photo(photo=photo_id, caption="<b>Endi esa guruhingiz havolasini <code>@guruhingiz_havolasi</code> ko'rinishida yuboring.</b>\n<i>Misol uchun : @online_test_matematika1</i>")
    await state.set_state("o_guruh_havolasi")

@dp.callback_query_handler(text="tayyor", state="sguruh")
async def kanal(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    photo_id = "AgACAgIAAxkBAAEUA_Vj5mkIFh5ZGQRablCSNOHMa00vfgACg8QxG2QpOUtiflWjFZipaAEAAwIAA3kAAy4E"                                                                  # o'zgartirish kk👇
    await call.message.answer_photo(photo_id, caption="<b>Endi esa, guruhingizga o'ting va <code>/start@sinov1_bot_bot</code> xabarini guruhingizga yuboring.</b>\n<i>*Rasmga qarang❗️</i>")
    await state.set_state("s_guruh_start")
    temp_data[call.from_user.id] = "start"