from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.misc.isbelgi import isbelgi
from keyboards.default import menu, bekor_qilish
from loader import dp, db_users


@dp.message_handler(text="♻️Ismni tahrirlash", state="sozlamalar")
async def ism_tah(msg : types.Message, state : FSMContext):
    await msg.answer("<b>♻️Ismni tahrirlash\n\nIsm familiyangizni yuboring : </b>\n<i>Masalan : Aliyev G`ani</i>", reply_markup=bekor_qilish.bekor_qil)
    await state.set_state("ism_tah")
    
        
@dp.message_handler(state="ism_tah")
async def tahrirla(msg : types.Message, state : FSMContext):
    if len(msg.text) > 2 and all(x.isalpha() or x.isspace() or isbelgi(x) for x in msg.text):
        db_users.update_user_name(msg.from_user.id, msg.text)
        await msg.answer(f"♻️Sizning ismingiz {msg.text}ga o`zgartirildi!", reply_markup=menu.menu)
        await state.finish()
    else:
        await msg.answer("<b>Iltimos ism kiriting.\n<i>Qayta kiriting : </i></b>")
    
    