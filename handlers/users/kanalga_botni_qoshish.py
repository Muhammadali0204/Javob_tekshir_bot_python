from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.botgautish import kanal_guruh, kanalga_qush, guruhga_start
from keyboards.default.bekor_qilish import bekor_qil
from loader import (
    dp,
    db_users,
    Limitlar_oddiy,
    Limitlar_blok,
    premium_narxi,
    temp_data,
    bot,
)
import pytz
import asyncio
from datetime import datetime, timedelta


@dp.callback_query_handler(text="tayyor", state="okanal")
async def kanal(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        text="<b>Endi esa, kanalingiz havolasini <code>@kanalingiz_havolasi</code> ko'rinishida yuboring.</b>\n<i>Misol uchun : @online_test_matematika1</i>"
    )
    await state.set_state("o_kanal_havolasi")


@dp.callback_query_handler(text="tayyor", state="skanal")
async def kanal(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        text="<b>Endi esa, kanalingizdan istalgan postni havolasi bilan yuboring.</b>"
    )
    await state.set_state("s_kanal_posti")
