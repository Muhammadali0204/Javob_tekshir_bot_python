from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.default.menu import menu


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), commands="cancel", state='*')
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), text="❌Bekor qilish", state='*')
async def cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer("<b>❌Bekor qilindi.</b>")
    await msg.answer(text="<b><i>📋Menu : </i></b>", reply_markup=menu)
