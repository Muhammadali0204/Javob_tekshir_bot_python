from loader import dp, bot
from keyboards.default.menu import menu

from aiogram import types, filters

@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE),state=None)
async def func(msg : types.Message):
    await msg.answer("<b>Iltimos menudan foydalaning.</b>")
    await msg.answer(text="<b><i>📋Menu : </i></b>", reply_markup=menu)
    