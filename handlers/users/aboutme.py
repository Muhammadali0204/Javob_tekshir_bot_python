from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from loader import dp, db_users, db_bj, db_ts, bot

@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), text="👤Men haqimda")
async def men(msg : types.Message):
    user = db_users.select_user_id(msg.from_user.id)
    await msg.answer(text=f"<b>Sizning ismingiz : {user[1]}</b>\n<i>O`zgartirishni xohlasangiz 🛠Sozlamalar tugmasini bosing.</i>")