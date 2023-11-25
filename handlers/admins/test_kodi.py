from loader import dp, db_users
from keyboards.default.admin import admin_key
from data.config import ADMINS
from aiogram import types


@dp.message_handler(text="Test kodi", chat_id=ADMINS)
async def admin(msg: types.Message):
    kod = db_users.select_test_kodi()
    await msg.answer(text=f"<b>Hozirgi vaqtdagi test kodi : </b><i>{kod}</i>")
