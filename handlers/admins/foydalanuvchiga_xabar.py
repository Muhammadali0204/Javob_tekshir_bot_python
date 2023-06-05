from loader import dp, bot, temp_data
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.admin import admin_key
from keyboards.default.bekor_qilish import bekor_qil
import asyncio
from data.config import ADMINS
from keyboards.inline.forward_copy import inline_key



@dp.message_handler(text="Foydalanuvchiga xabar", chat_id = ADMINS)
async def message(msg : types.Message, state : FSMContext):
    await msg.answer("<b>Foydalanuvchi id'sini yuboring : </b>", reply_markup=bekor_qil)
    await state.set_state("foydalanuvchi_idsi")


@dp.message_handler(state="foydalanuvchi_idsi")
async def sendmessage(msg : types.Message, state : FSMContext):
    if msg.text.isnumeric():
        temp_data[msg.from_user.id] = int(msg.text)
        await msg.answer(text="<b>Reklama yuborish : </b>\n<i>(Oddiy xabar, Rasm, Video, Dokument)</i>", reply_markup=bekor_qil)
        await msg.answer("<b>Forward yoki copy ? </b>", reply_markup=inline_key)
        await state.set_state("reklama_turi1")
    else :
        await msg.answer("<b>Id yuboring.</b>", reply_markup=admin_key)
        await state.finish()
    
@dp.callback_query_handler(text="for", state="reklama_turi1")
async def func(call : types.CallbackQuery, state : FSMContext):
    await call.message.answer("<b>Xabarni yuboring : <i>(Forward)</i></b>")
    await state.set_state("forward1")
    await call.message.delete()
    
@dp.callback_query_handler(text="copy", state="reklama_turi1")
async def func(call : types.CallbackQuery, state : FSMContext):
    await call.message.answer("<b>Xabarni yuboring : <i>(Copy)</i></b>")
    await state.set_state("copy1")
    await call.message.delete()
    
@dp.message_handler(state="forward1", content_types=types.ContentType.ANY)
async def func(msg : types.Message, state : FSMContext):
    try:
        await bot.forward_message(temp_data[msg.from_user.id], msg.from_user.id, msg.message_id)
    except:
        pass
        
    await msg.answer(f"<b>Foydalanuvchiga xabar yuborildi ✅</b>", reply_markup=admin_key)
    await state.finish()
    
@dp.message_handler(state="copy1", content_types=types.ContentType.ANY)
async def func(msg : types.Message, state : FSMContext):
    try:
        await bot.copy_message(temp_data[msg.from_user.id], msg.from_user.id, msg.message_id)
    except:
        pass
        
    await msg.answer(f"<b>Foydalanuvchiga xabar yuborildi ✅</b>", reply_markup=admin_key)
    await state.finish()