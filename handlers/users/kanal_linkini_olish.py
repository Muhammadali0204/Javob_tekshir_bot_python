from aiogram import types, filters
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.inline.botgautish import kanal_guruh, kanalga_qush
from keyboards.default.menu import menu
from keyboards.default.bekor_qilish import bekor_qil
from loader import dp, db_users, Limitlar_oddiy, Limitlar_blok, premium_narxi, temp_data, bot
import pytz
import asyncio
from datetime import datetime, timedelta


@dp.message_handler(state="o_kanal_havolasi")
async def kanal(msg: types.Message, state: FSMContext):
    havola = msg.text
    try:
        chat = await bot.get_chat(havola)
        admins = await bot.get_chat_administrators(havola)
        for admin in admins:
            if msg.from_user.id == admin['user']['id']:
                chat_id = chat['id']
                title = chat['title']
                username = chat['username']
                answer = f"<b>🎉Tabriklaymiz kanalingiz muvaffaqqiyatli bog'landi.✅</b>\n\n<b>Kanal : </b><i>{title}</i>\n<b>Username : </b><i>@{username}</i>\n\n*Botni kanalingizdan chiqarib yubormang❗️"
                db_users.update_kanal_user(
                    f"{chat_id},{title}(@{username})", msg.from_user.id)
                await msg.answer(answer, reply_markup=menu)
                await state.finish()
                return
    except:
        await msg.answer("<b>Botni kanalingizga qo'shmagansiz ❌</b>\n\n<i>Qayta urinib ko'ring</i>", reply_markup=menu)
        await state.finish()
        return
    await msg.answer("<b>Siz bu kanalda adminstrator emassiz ❌</b>", reply_markup=menu)
    await state.finish()


@dp.message_handler(state="s_kanal_posti", content_types=types.ContentType.ANY)
async def kanal(msg: types.Message, state: FSMContext):
    try:
        if msg.forward_from_chat:
            if msg.forward_from_chat['type'] == 'channel':
                chat_id = msg.forward_from_chat['id']
                chat = await bot.get_chat(chat_id)
                admins = await bot.get_chat_administrators(chat_id)
                for admin in admins:
                    if admin['user']['id'] == msg.from_user.id:
                        title = chat['title']
                        answer = f"<b>🎉Tabriklaymiz kanalingiz muvaffaqqiyatli bog'landi.✅</b>\n\n<b>Kanal : </b><i>{title}</i>\n\n*Botni kanalingizdan chiqarib yubormang❗️"
                        db_users.update_kanal_user(
                            f"{chat_id},{title}", msg.from_user.id)
                        await msg.answer(answer, reply_markup=menu)
                        await state.finish()
                        return
        else:
            await msg.answer("<b>Yuborayotgan kanalingiz kanal havolasi bilan birga bo'lsin❗️</b>\n<i>*Qayta urinib ko'ring</i>", reply_markup=bekor_qil)
            return
    except:
        await msg.answer("<b>Botni kanalingizga qo'shmagansiz ❌ yoki </b>\n\n<i>Qayta urinib ko'ring</i>", reply_markup=menu)
        await state.finish()
        return
    await msg.answer("<b>Siz bu kanalda adminstrator emassiz ❌</b>", reply_markup=menu)
    await state.finish()
