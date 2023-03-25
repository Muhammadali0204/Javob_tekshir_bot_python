from aiogram import types
from aiogram.types import CallbackQuery
from datetime import datetime, timedelta
import pytz
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from keyboards.inline.post_joyla import post
from keyboards.inline.soatlar import soatlar
from keyboards.inline.minutlar import minutlar
from keyboards.inline.qayta import qayta
from keyboards.default import menu
from loader import dp, db_users, db_ts, bot, temp_data, foydalanuvchi_limitlari_blok, kitoblar


@dp.callback_query_handler(state="blok_test_avto_vaqt")
async def tuzz(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await call.message.answer(f"<b>Test boshlanish soatini tanlang : </b>\n" +
                              "<i>Masalan, 20:30 uchun, test boshlanish soati  2️⃣0️⃣</i>", reply_markup=soatlar)
    await state.set_state("boshlanish_soat_qabul_blok")


@dp.callback_query_handler(state="boshlanish_soat_qabul_blok")
async def soat(call: CallbackQuery, state: FSMContext):
    soat = call.data
    temp_data[call.from_user.id][4].append(soat)
    await call.message.delete()
    await call.answer()
    await call.message.answer(f"<b>{soat} tanlandi.\nEndi esa test boshlanish daqiqasini tanlang.</b>\n"
                              + "<i>Masalan, 20:30 uchun, test boshlanish daqiqasi 3️⃣0️⃣</i>", reply_markup=minutlar)
    await state.set_state("boshlanish_minut_qabul_blok")


@dp.callback_query_handler(state="boshlanish_minut_qabul_blok")
async def minut(call: CallbackQuery, state: FSMContext):
    minut = call.data
    temp_data[call.from_user.id][4].append(minut)
    vaqt = temp_data[call.from_user.id][4]
    await call.message.delete()
    await call.answer()
    await call.message.answer(f"<b>Test boshlanish vaqti : <i>{vaqt}</i>.</b>\n"
                              + "<b>Endi esa test tugash soatini tanlang.</b>\n"+"<i>Masalan, 22:30 uchun, test tugash soati 2️⃣2️⃣</i>", reply_markup=soatlar)
    await state.set_state("tugash_soat_qabul_blok")


@dp.callback_query_handler(state="tugash_soat_qabul_blok")
async def soat(call: CallbackQuery, state: FSMContext):
    soat = call.data
    temp_data[call.from_user.id][4].append(soat)
    await call.message.delete()
    await call.answer()
    await call.message.answer(f"<b>{soat} tanlandi.\nEndi esa, test tugash vaqtining daqiqasini tanlang.</b>\n"
                              + "<i>Masalan, 22:30 uchun, test tugash vaqti 3️⃣0️⃣</i>", reply_markup=minutlar)
    await state.set_state("tugash_minut_qabul_blok")


@dp.callback_query_handler(text="qayta_vaqt_kiritish", state="tugash_minut_qabul_blok")
async def salomm(call: types.CallbackQuery, state: FSMContext):
    temp_data[call.from_user.id][4] = []
    await call.message.delete()
    await call.message.answer(f"<b>Test boshlanish soatini tanlang : </b>\n" +
                              "<i>Masalan, 20:30 uchun, test boshlanish soati  2️⃣0️⃣</i>", reply_markup=soatlar)
    await state.set_state("boshlanish_soat_qabul_blok")


@dp.callback_query_handler(text="test_atmen", state="tugash_minut_qabul_blok")
async def nima(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("<b>❌Jarayon bekor qilindi.</b>")
    await state.finish()
    await call.message.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)


@dp.callback_query_handler(state="tugash_minut_qabul_blok")
async def minut(call: CallbackQuery, state: FSMContext):
    minut = call.data
    temp_data[call.from_user.id][4].append(minut)
    vaqt = temp_data[call.from_user.id][4]
    if vaqt[0] == vaqt[2] and vaqt[1] == vaqt[3]:
        answer = "<b>Test boshlanish vaqti bilan  tugash vaqti teng bo`lmasligi lozim❗️</b>\n"
        answer += "<i>Qaytadan kiriting yoki /cancel buyrug`ini bosing</i>"
        await call.answer("❌Vaqt bo`yicha xatolik")
        await call.message.delete()
        await call.message.answer(text=answer, reply_markup=qayta)
    else:
        hozir = datetime.now(pytz.timezone("Asia/Tashkent"))
        t = hozir.strftime("%Y-%m-%d,%H:%M:%S")
        t2 = t.split(',')

        sana = t2[0].split('-')
        vaqt_hozir = t2[1].split(':')

        hozirgi_vaqt = datetime(int(sana[0]), int(sana[1]), int(sana[2]), int(
            vaqt_hozir[0]), int(vaqt_hozir[1]), int(vaqt_hozir[2]))
        foydalanuvchi_kiritgan_vaqt_boshlanish = datetime(
            int(sana[0]), int(sana[1]), int(sana[2]), int(vaqt[0]), int(vaqt[1]))
        foydalanuvchi_kiritgan_vaqt_tugash = datetime(
            int(sana[0]), int(sana[1]), int(sana[2]), int(vaqt[2]), int(vaqt[3]))
        if foydalanuvchi_kiritgan_vaqt_boshlanish == hozirgi_vaqt:
            await call.message.delete()
            await call.message.answer("<b>Xatolik! Qayta urinib ko`ring. </b>", reply_markup=menu.menu)
            await state.finish()
        else:
            if foydalanuvchi_kiritgan_vaqt_boshlanish < hozirgi_vaqt:
                foydalanuvchi_kiritgan_vaqt_boshlanish = foydalanuvchi_kiritgan_vaqt_boshlanish + \
                    timedelta(days=1)
                foydalanuvchi_kiritgan_vaqt_tugash = foydalanuvchi_kiritgan_vaqt_tugash + \
                    timedelta(days=1)
            if foydalanuvchi_kiritgan_vaqt_boshlanish > foydalanuvchi_kiritgan_vaqt_tugash:
                foydalanuvchi_kiritgan_vaqt_tugash = foydalanuvchi_kiritgan_vaqt_tugash + \
                    timedelta(days=1)
            davomiylik = (foydalanuvchi_kiritgan_vaqt_tugash -
                          foydalanuvchi_kiritgan_vaqt_boshlanish).seconds
            vaqt.append(str(davomiylik))
            davom_etish_vaqti = [davomiylik // 3600,
                                 (davomiylik - 3600 * (davomiylik // 3600)) // 60]
            boshlanish_vaqt = foydalanuvchi_kiritgan_vaqt_boshlanish.strftime(
                "%H:%M %d-%m-%Y")
            tugash_vaqt = foydalanuvchi_kiritgan_vaqt_tugash.strftime(
                "%H:%M %d-%m-%Y")
            test_kodi = db_users.take_test_kodi()
            vaqt = ",".join(vaqt)
            a0 = ",".join(temp_data[call.from_user.id][0])
            a1 = ",".join(temp_data[call.from_user.id][1])
            a3 = ",".join(temp_data[call.from_user.id][3])
            try:
                db_ts.add_test_blok(call.from_user.id,
                                    test_kodi, a0, a1, a3, vaqt, 0, None)
            except Exception as e:
                for admin in ADMINS:
                    await bot.send_message(int(admin), f"Test bazaga qo`shishda xatolik yuz berdi : \n{e}")
                await call.message.delete()
                await call.answer("Bazaga qo`shishda xatolik yuz berdi\nQayta urining, qayta xatolik takrorlansa, adminga murojaat qiling!", show_alert=True)
                await state.finish()

            await call.answer("Test bazaga qo`shildi✅", show_alert=True)
            await call.message.delete()
            foydalanuvchi_limitlari_blok[call.from_user.id][0] -= 1
            fanlar = temp_data[call.from_user.id][0]
            javoblar = temp_data[call.from_user.id][1]
            beriladigan_ballar = temp_data[call.from_user.id][3]
            answer = f"🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Blok test</i>\n🟢<b>Fanlar soni : </b><i>{temp_data[call.from_user.id][2]} ta</i>\n\n"
            umumiy_ball = 0
            q = [1, len(javoblar[0])]
            for i in range(0, temp_data[call.from_user.id][2]):
                if i != 0:
                    q[0] += len(javoblar[i-1])
                    q[1] += len(javoblar[i])
                answer += f"<b>{i+1} - fan : </b>\n"
                answer += f"<b>{kitoblar[i]}Fan nomi : </b><i>{fanlar[i]}</i>\n"
                answer += f"<b>🔢Savollar soni : <i>{len(javoblar[i])} ta</i></b> <i>({q[0]}-{q[1]})</i>\n"
                answer += f"<b>❕Ball : </b><i>{beriladigan_ballar[i]}</i>\n"
                umumiy_ball += len(javoblar[i]) * float(beriladigan_ballar[i])
                answer += f"<i>Fan uchun beriladigan ball : {round(len(javoblar[i]) * float(beriladigan_ballar[i]), 4)} ball</i>\n\n"
            answer += f"<b>Jami savollar soni : </b><i>{q[1]} ta</i>\n"
            answer += f"<b>Umumiy ball : </b><i>{round(umumiy_ball, 4)} ball</i>\n\n"
            answer += f"<b>🕐Test boshlanish vaqti : <i>{boshlanish_vaqt}</i></b>\n"
            answer += f"<b>🕑Test tugash vaqti : <i>{tugash_vaqt}</i></b>\n"
            if davom_etish_vaqti[0] == 0:
                answer += f"<b>⏳Test davomiyligi : </b><i>{davom_etish_vaqti[1]} daqiqa.</i>"
            elif davom_etish_vaqti[1] == 0:
                answer += f"<b>⏳Test davomiyligi : </b><i>{davom_etish_vaqti[0]} soat.</i>"
            else:
                answer += f"<b>⏳Test davomiyligi : </b><i>{davom_etish_vaqti[0]} soat, {davom_etish_vaqti[1]} daqiqa</i>"
            answer += "\n\n<b>Testda qatnashuvchilar\n\n<i>@Javob_tekshir_bot</i> 👈\n\nga javoblarini yuborishlari mumkin.</b>"
            await call.message.answer(text=answer, reply_markup=menu.menu)
            await state.finish()

            user = db_users.select_user_id(call.from_user.id)
            if user[3] != '0' and user[3] != '-1' and user[4] != None:
                kanal = user[4].split(',')[1]
                answer = f"<b>Bu test natijasi {kanal} kanal/guruhingizga joylansinmi ❓</b>\n\n<i>*Testni yakunlaganingizda, test natijasi bot tomonidan kanalga joylanadi.</i>"
                await call.message.answer(text=answer, reply_markup=post(test_kodi, "Blok_test"))

            temp_data[call.from_user.id] = None
