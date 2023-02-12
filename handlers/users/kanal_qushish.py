from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.botgautish import kanal_guruh, kanalga_qush
from keyboards.default.bekor_qilish import bekor_qil
from keyboards.default import menu
from loader import dp, db_users, Limitlar_oddiy, Limitlar_blok, premium_narxi, temp_data, bot
import pytz, asyncio
from datetime import datetime, timedelta



@dp.callback_query_handler(text=["atmen_kanal", "xullas_atem_kanal"], state="kanal_qushish")
async def atmen(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Kanal yoki guruhingizni albatta qo'shing❗️\nBu bot imkoniyatlarini to`liq ko`rsatib beradi✅\nIstalgan payt <i>🛠Sozlamalar/🖇Bog'langan kanal/guruh</i> bo'limida kanal yoki guruhingizni qo'shishingiz mumkin!</b>", reply_markup=menu.menu)
    await state.finish()

@dp.message_handler(state="kanal_qushish")
async def atmen(msg : types.Message, state : FSMContext):
    await msg.answer("<b>Iltimos 👆 bu masalani hal qiling, bu juda muhim ❗️</b>")
    await msg.delete()
    await asyncio.sleep(3)
    await bot.delete_message(msg.from_user.id, (msg.message_id + 1))
    
    
    
    
    
    
@dp.callback_query_handler(state="kanal_qushish", text="kanal_qushish")
async def qush(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Qanday kanal yoki guruh bog'lamoqchisiz❓</b>\n<i>*Iltimos,bu jarayonda e'tiborli bo'ling</i>", reply_markup=kanal_guruh)
    
    
    
    
    
@dp.callback_query_handler(state="kanal_qushish", text="okanal")
async def qush(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Ommaviy kanal bog'lamoqchisiz</b>", reply_markup=bekor_qil)
    # photo_id 
    photo = "AgACAgIAAxkBAAIF9WPkJ3wPnZ54TBr-Eam6Lq4PmQWoAALixDEbV2QgS8djLlipj9UkAQADAgADeAADLgQ"
    await call.message.answer_photo(photo=photo, caption="<b>Yaxshi, endi botni ommaviy kanalingizga admin sifatida qo'shing.</b>\n<i>Rasmda ko'rsatilgan tugmani bosing va kanalingizga admin sifatida qo`shing.\n\n❗️Bot kanalingizga qo'shilganiga ishonch hosil qilib, </i><code>Tayyor✅</code><i> tugmasini bosing.</i>", reply_markup=kanalga_qush)
    await state.set_state("okanal")
    
@dp.callback_query_handler(state="kanal_qushish", text="skanal")
async def qush(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Shaxsiy kanal bog'lamoqchisiz</b>", reply_markup=bekor_qil)
    # photo_id 
    photo = "AgACAgIAAxkBAAIF9WPkJ3wPnZ54TBr-Eam6Lq4PmQWoAALixDEbV2QgS8djLlipj9UkAQADAgADeAADLgQ"
    await state.set_state("skanal")
    await call.message.answer_photo(photo=photo, caption="<b>Yaxshi, endi botni shaxsiy kanalingizga admin sifatida qo'shing.</b>\n<i>Rasmda ko'rsatilgan tugmani bosing va kanalingizga admin sifatida qo`shing.\n\n❗️Bot kanalingizga qo'shilganiga ishonch hosil qilib, </i><code>Tayyor✅</code><i> tugmasini bosing.</i>", reply_markup=kanalga_qush)
    
@dp.callback_query_handler(state="kanal_qushish", text="oguruh")
async def qush(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Ommaviy guruh bog'lamoqchisiz</b>", reply_markup=bekor_qil)
    # photo_id 
    photo = "AgACAgIAAxkBAAIF9WPkJ3wPnZ54TBr-Eam6Lq4PmQWoAALixDEbV2QgS8djLlipj9UkAQADAgADeAADLgQ"
    await state.set_state("oguruh")
    await call.message.answer_photo(photo=photo, caption="<b>Yaxshi, endi botni ommaviy guruhingizga qo'shing.</b>\n<i>Rasmda ko'rsatilgan tugmani bosing va  guruhingizga qo`shing.\n*Buning uchun siz guruh admini bo'lishingiz kerak.\n\n❗️Bot guruhingizga qo'shilganiga ishonch hosil qilib, </i><code>Tayyor✅</code><i> tugmasini bosing.</i>", reply_markup=kanalga_qush)
    
@dp.callback_query_handler(state="kanal_qushish", text="sguruh")
async def qush(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Shaxsiy guruh bog'lamoqchisiz</b>", reply_markup=bekor_qil)
    # photo_id 
    photo = "AgACAgIAAxkBAAIF9WPkJ3wPnZ54TBr-Eam6Lq4PmQWoAALixDEbV2QgS8djLlipj9UkAQADAgADeAADLgQ"
    await state.set_state("sguruh")
    await call.message.answer_photo(photo=photo, caption="<b>Yaxshi, endi botni shaxsiy guruhingizga qo`shing.</b>\n<i>Rasmda ko'rsatilgan tugmani bosing va guruhingizga qo`shing.\n*Buning uchun siz guruh admini bo'lishingiz kerak.\n\n❗️Bot guruhingizga qo'shilganiga ishonch hosil qilib, </i><code>Tayyor✅</code><i> tugmasini bosing.</i>", reply_markup=kanalga_qush)
    

    
