from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.menu import menu
from loader import dp
@dp.message_handler(text="◀️Ortga", state=["Sozlamalar","test_turi"])
async def orqaga(msg : types.Message, state : FSMContext):
        await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu)
        await state.finish()