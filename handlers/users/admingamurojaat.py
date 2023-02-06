from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from keyboards.inline.botgautish import botga
from loader import dp, db_users


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), text="💬Adminga murojaat")
async def adminga(msg : types.Message, state : FSMContext):
    answer = "<b>❔Savollaringiz yoki 📨 takliflaringiz bo`lsa, quyidagi botga xabar yuboring 📤</b>\n<i>*Tez orada javob beriladi</i>"
    await msg.answer(text=answer, reply_markup=botga)