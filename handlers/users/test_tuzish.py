from aiogram import types, filters
from datetime import datetime as d
import time
from aiogram.dispatcher import FSMContext
from keyboards.inline.info import info
from keyboards.default import test_turi
from data.config import ADMINS
from loader import dp, bot, kanallar
from utils.misc.subscription import check
from keyboards.inline.channels import channels_keyboard


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), text="🖌Test tuzish")
async def tuz(msg: types.Message, state: FSMContext):
    if kanallar[0] != '':
        azo_bulmagan_kanallar = []
        id = msg.from_user.id
        final_status = True
        for kanal in kanallar:
            try:
                status = await check(user_id=id, channel=kanal)
                final_status *= status
                if not status:
                    kanal = await bot.get_chat(kanal)
                    invite_link = await kanal.export_invite_link()
                    azo_bulmagan_kanallar.append(invite_link)
            except Exception as e:
                for admin in ADMINS:
                    await bot.send_message(int(admin), f"A`zo bo`linishi kerak bo`lgan kanal bo`yicha nosozlik\n{e}")
        if not final_status:
            answer = "<b>Test tuza olish uchun quyidagi kanallarga obuna bo`ling❗️</b>"
            await msg.answer(answer, disable_web_page_preview=True, reply_markup=channels_keyboard(azo_bulmagan_kanallar, "test_tuz"))
        else:
            await msg.answer(
                text="<b>Yaxshi, qanday test tuzmoqchisiz?</b>", reply_markup=info
            )
            await msg.answer("<b>Tanlang: 👇</b>", reply_markup=test_turi.tur)
            await state.set_state("test_turi")
    else:
        await msg.answer(
            text="<b>Yaxshi, qanday test tuzmoqchisiz?</b>", reply_markup=info
        )
        await msg.answer("<b>Tanlang: 👇</b>", reply_markup=test_turi.tur)
        await state.set_state("test_turi")