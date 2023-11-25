from loader import dp, db_users
from keyboards.default.admin import admin_key
from aiogram.dispatcher import FSMContext
from keyboards.default.bekor_qilish import bekor_qil
from data.config import ADMINS
from aiogram import types


@dp.message_handler(text="Id bilan topish", chat_id=ADMINS)
async def admin(msg: types.Message, state: FSMContext):
    await msg.answer(
        text="<b>Foydalanuvchi id'sini yuboring : </b>", reply_markup=bekor_qil
    )
    await state.set_state("id_bn_topish")


@dp.message_handler(state="id_bn_topish", chat_id=ADMINS)
async def admin(msg: types.Message, state: FSMContext):
    user = db_users.select_user_id(msg.text)
    answer = f"<b>Ismi : </b><i>{user[1]}</i>\n"
    answer += f"<b>Id : </b><i>{user[0]}</i>\n"
    answer += f"<b>Username : </b><i>{user[2]}</i>\n"
    if user[3] != "0":
        answer += f"<b>Status : </b><i>{user[3]}</i>\n"
        answer += f"<b>Kanali : </b><i>{user[4]}</i>\n\n"
    else:
        answer += f"<b>Status : </b><i>{user[3]}</i>\n\n"

    await msg.answer(text=answer, reply_markup=admin_key)
    await state.finish()
