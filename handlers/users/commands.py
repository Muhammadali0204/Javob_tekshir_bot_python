from aiogram import types, filters
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher import FSMContext
from keyboards.default.menu import menu
from loader import dp, db_users

        
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), text="🧮Bot statistikasi")
async def stat(msg : types.Message):
        await msg.answer(text=f"👤<b>Botdan foydalanuvchilar soni : </b><i>{db_users.count_users()[0]} ta</i>")