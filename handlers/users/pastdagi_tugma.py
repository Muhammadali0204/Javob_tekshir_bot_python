from aiogram import types
from aiogram.types import Message
from loader import dp


@dp.message_handler(state=["test_turi","Sozlamalar"])
async def iye(msg : Message):
    await msg.answer("<b>Quyidagi tugmalardan foydalaning</b>\n<i>Yoki /cancel ni bosing!</i>")