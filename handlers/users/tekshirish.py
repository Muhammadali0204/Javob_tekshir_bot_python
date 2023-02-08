from loader import dp, kanallar, bot
from utils.misc.subscription import check
from data.config import ADMINS
from keyboards.default import test_turi, bekor_qilish
from aiogram.dispatcher import FSMContext
from keyboards.inline import info
from aiogram import types, filters

@dp.callback_query_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), regexp="obunani_tekshir:+")
async def salom(call : types.CallbackQuery, state : FSMContext):
    azo_bulmagan_kanallar = []
    id = call.from_user.id
    final_status = True
    for kanal in kanallar:
        try :
            status = await check(user_id=id, channel=kanal)
            final_status *= status
            if not status:
                kanal = await bot.get_chat(kanal)
                invite_link = await kanal.export_invite_link()
                azo_bulmagan_kanallar.append(invite_link)
        except Exception as e:
            for admin in ADMINS:
                await bot.send_message(int(admin), f"A`zo bo`linishi kerak bo`lgan kanal bo`yicha nosozlik\n{e}")
    if final_status:
        holat = call.data.split(':')[1]
        await call.answer("Botdan to`liq foydalanishingiz mumkin✅", show_alert=True)
        await call.message.delete()
        if holat == "javob_ber":
            await call.message.answer("<b>Yaxshi, test kodini yuboring : </b>", reply_markup=bekor_qilish.bekor_qil)
            await state.set_state("test_kodi")
        elif holat == "test_tuz":
            await call.message.answer(
            text="<b>Yaxshi, qanday test tuzmoqchisiz?</b>",reply_markup= info.info
            )
            await call.message.answer("<b>Tanlang: 👇</b>", reply_markup=test_turi.tur)
            await state.set_state("test_turi")
    else:
        await call.answer("Siz barcha kanallarga a`zo bo`lmadingiz ❗️", show_alert=True)
        
@dp.callback_query_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), regexp="obunani_tekshir:+", state='*')
async def salom(call : types.CallbackQuery):
    await call.message.delete()