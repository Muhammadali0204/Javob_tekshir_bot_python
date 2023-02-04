from aiogram import types, filters
from keyboards.default.bekor_qilish import bekor_qil
from keyboards.inline.inline_ha_yoq import tasdiq_keyboard
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from keyboards.inline.test_egasiga import test_owner
from loader import dp, db_users, db_bj, db_ts, bot

@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), text="📋Mening testlarim")
async def mytest(msg : types.Message):
    await msg.answer("<b>Bu bo'lim ishlab chiqish jarayonida</b>")