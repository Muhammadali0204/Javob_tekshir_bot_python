from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from keyboards.default.sozlamalar import sozlama_keyboard
from keyboards.default.bekor_qilish import bekor_qil

from loader import dp

@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), text="🛠Sozlamalar")
async def sozlama(msg : types.Message, state : FSMContext):
    await msg.answer("<b>🛠Sozlamalar :</b>", reply_markup=sozlama_keyboard)
    await state.set_state("Sozlamalar")


    
