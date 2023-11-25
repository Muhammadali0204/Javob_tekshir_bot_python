from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from loader import dp
from data.config import ADMINS
from keyboards.default.admin import admin_key


@dp.message_handler(
    filters.ChatTypeFilter(types.ChatType.PRIVATE),
    commands="cancel",
    state="*",
    chat_id=ADMINS,
)
@dp.message_handler(
    filters.ChatTypeFilter(types.ChatType.PRIVATE),
    text="❌Bekor qilish",
    state="*",
    chat_id=ADMINS,
)
async def cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer("<b>❌Bekor qilindi.</b>")
    await msg.answer(text="<b><i>📋Menu : </i></b>", reply_markup=admin_key)
