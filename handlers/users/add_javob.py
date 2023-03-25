from aiogram import types, filters
from keyboards.default.menu import menu
from keyboards.default.bekor_qilish import bekor_qil
from keyboards.inline.inline_ha_yoq import tasdiq_keyboard
from aiogram.dispatcher import FSMContext
from keyboards.inline.test_egasiga import test_owner
from utils.misc.subscription import check
from keyboards.inline.channels import channels_keyboard
from keyboards.inline.javob_yuborishni_boshlash import boshlash
from loader import dp, db_users, db_bj, db_ts, bot, temp_data, kitoblar, kanallar
from data.config import ADMINS
import random


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), text='🟢Testga javob berish')
async def javob(msg: types.Message, state: FSMContext):
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
            answer = "<b>Testga javob bera olish uchun quyidagi kanallarga obuna bo`ling❗️</b>"
            await msg.answer(answer, disable_web_page_preview=True, reply_markup=channels_keyboard(azo_bulmagan_kanallar, "javob_ber"))
        else:
            user = db_users.select_user_id(msg.from_user.id)
            if user == None:
                await msg.answer("<b>Iltimos /start ni bosing va ism familiyangizni kiriting!</b>")
                return
            await msg.answer("<b>Yaxshi, test kodini yuboring : </b>", reply_markup=bekor_qil)
            await state.set_state("test_kodi")
    else:
        user = db_users.select_user_id(msg.from_user.id)
        if user == None:
            await msg.answer("<b>Iltimos /start ni bosing va ism familiyangizni kiriting!</b>")
            return
        await msg.answer("<b>Yaxshi, test kodini yuboring : </b>", reply_markup=bekor_qil)
        await state.set_state("test_kodi")


@dp.message_handler(state="test_kodi")
async def test_kodii(msg: types.Message, state: FSMContext):
    kod = msg.text
    if kod.isnumeric():
        try:
            data_test_oddiy = db_ts.select_test_oddiy_by_test_kodi(kod)
            data_test_blok = db_ts.select_test_blok_by_test_kodi(kod)
        except Exception as e:
            print(e)

        if data_test_blok == None and data_test_oddiy == None:
            test_kodi = int(kod)
            hozirgi_kod = int(db_users.select_test_kodi())
            if test_kodi < hozirgi_kod:
                await msg.answer("<b>Bu test allaqachon yakunlangan!</b>\n", reply_markup=menu)
            else:
                await msg.answer(text="<b>Bunday kodli test mavjud emas!</b>", reply_markup=menu)
            await state.finish()
        else:
            if data_test_blok == None:
                if data_test_oddiy[5] == 1:
                    # Javob oddiy testga berilmoqda
                    javob_bergan = db_bj.javob_berganmi_oddiy(
                        kod, msg.from_user.id)
                    if javob_bergan == None:
                        temp_data[msg.from_user.id] = [
                            int(kod), len(data_test_oddiy[3]), ""]

                        answer = f"🔑<b>Test kodi : {kod}</b>\n\n"
                        answer += f"{kitoblar[random.randint(0, 4)]}<b>Fan nomi : {data_test_oddiy[2]}</b>\n"
                        answer += f"🔢<b>Savollar soni : {len(data_test_oddiy[3])} ta</b>\n\n"
                        answer += "<b>🔡Javobingizni yuboring : </b>\n\n"
                        answer += f"<i>abcd... 👈ko`rinishida</i>"
                        await msg.answer(answer, reply_markup=bekor_qil)
                        await state.set_state("javoblar_junatiladi")
                    else:
                        await msg.answer(f"<b>Siz {kod} - kodli testga javob berib bo`lgansiz❗️</b>", reply_markup=menu)
                        await state.finish()
                else:
                    vaqt = data_test_oddiy[4].split(',')
                    answer = f"<b>Bu test faol emas❗️\n</b><i>🕐{vaqt[0]}:{vaqt[1]} dan so`ng javob yuborishingiz mumkin.</i>"
                    await msg.answer(answer, reply_markup=menu)
                    await state.finish()
            else:
                # Javob blok testga berilmoqda
                if data_test_blok[6] == 1:
                    javob_bergan = db_bj.javob_berganmi_blok(
                        kod, msg.from_user.id)
                    if javob_bergan == None:
                        # temp_data[id] = [fanlar_soni, fan_nomlari, haqiqiy_javoblar,  berilgan_javob, nechinchi_savol, test_kodi]
                        fan_soni = data_test_blok[2].split(',')
                        temp_data[msg.from_user.id] = [
                            len(fan_soni), [], data_test_blok[3], [], 0, kod]
                        fanlar = data_test_blok[2].split(',')
                        javoblar = temp_data[msg.from_user.id][2].split(',')
                        beriladigan_ballar = data_test_blok[4].split(',')
                        answer = f"🔑<b>Test kodi : {kod}\n🗂Test turi : Blok test\n🟢Fanlar soni : {temp_data[msg.from_user.id][0]} ta</b>\n\n"
                        umumiy_ball = 0
                        q = [1, len(javoblar[0])]
                        for i in range(0, temp_data[msg.from_user.id][0]):
                            if i != 0:
                                q[0] += len(javoblar[i-1])
                                q[1] += len(javoblar[i])
                            temp = ""
                            temp += f"<b>{i+1} - fan : </b>\n"
                            temp += f"<b>{kitoblar[i]}Fan nomi : </b><i>{fanlar[i]}</i>\n"
                            temp += f"<b>🔢Savollar soni : <i>{len(javoblar[i])} ta </i></b><i>({q[0]}-{q[1]})</i>\n"
                            temp += f"<b>❕Ball : </b><i>{beriladigan_ballar[i]}</i>\n"
                            umumiy_ball += len(javoblar[i]) * \
                                float(beriladigan_ballar[i])
                            temp += f"<i>Fan uchun beriladigan ball : {round(len(javoblar[i]) * float(beriladigan_ballar[i]), 4)} ball</i>\n\n"
                            answer += temp
                            temp_data[msg.from_user.id][1].append(
                                f"{temp}~{q[0]}~{q[1]}")
                        answer += f"<b>Jami savollar soni : </b><i>{q[1]} ta</i>\n"
                        answer += f"<b>Umumiy ball : </b><i>{round(umumiy_ball, 4)} ball</i>\n\n"
                        answer += "<i>Javob yuborishni boshlash uchun :\n\nJavob yuborishni boshlash➡️\n\ntugmasini bosing.</i>"
                        await msg.answer(answer, reply_markup=boshlash)
                        await state.set_state("javob_yuborishni_boshlash_blok")
                    else:
                        await msg.answer(f"<b>Siz {kod} - kodli blok testga javob berib bo`lgansiz❗️</b>", reply_markup=menu)
                        await state.finish()
                else:
                    vaqt = data_test_blok[5].split(',')
                    answer = f"<b>Bu test faol emas❗️\n</b><i>🕐{vaqt[0]}:{vaqt[1]} dan so`ng javob yuborishingiz mumkin.</i>"
                    await msg.answer(answer, reply_markup=menu)
                    await state.finish()
    else:
        await msg.answer("<b>Test kodi natural son!</b>\n<i>Qayta kiriting yoki bekor qiling❗️</i>", reply_markup=bekor_qil)
