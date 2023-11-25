from aiogram.dispatcher import FSMContext
from aiogram import types
from keyboards.default.admin import admin_key
from loader import dp
from data.config import ADMINS


@dp.message_handler(text="Admin", chat_id=ADMINS)
async def admin(msg: types.Message, state: FSMContext):
    await msg.answer("<b>Admin panel</b>", reply_markup=admin_key)
