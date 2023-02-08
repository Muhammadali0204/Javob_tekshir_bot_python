from aiogram import types
from keyboards.default.menu import menu
from keyboards.default.bekor_qilish import bekor_qil
from keyboards.inline.inline_ha_yoq import tasdiq_keyboard
from aiogram.dispatcher import FSMContext
from keyboards.inline.test_egasiga import test_owner
from keyboards.inline.javob_yuborishni_boshlash import boshlash
from loader import dp, db_users, db_bj, db_ts, bot, temp_data, kitoblar
import random

@dp.callback_query_handler(text="javob_yuborishni_boshla", state="javob_yuborishni_boshlash_blok")
async def salom(call : types.CallbackQuery, state : FSMContext):
    # temp_data[id] = [fanlar_soni, tayyor_fan_nomlari, haqiqiy_javoblar,  berilgan_javob, nechinchi_savol, test_kodi]
    #                        0              1                 2                     3               4           5
    q = temp_data[call.from_user.id][1]
    gap = q[0].split('~')
    answer = f"{gap[0]}<b>{gap[1]} - {gap[2]} savollarning javobini yuboring : </b>\n\n<i>abcd... 👈ko`rinishida</i>"
    await call.message.delete()
    await call.message.answer(text=answer)
    await state.set_state("javob_yuborish_blok")
    

@dp.callback_query_handler(text="javob_yuborishni_bekor_qil", state="javob_yuborishni_boshlash_blok")
async def salommm(call : types.CallbackQuery, state : FSMContext):
    await call.answer("Bekor qilindi❌")
    await call.message.delete()
    await call.message.answer("Bekor qilindi❌", reply_markup=menu)
    await state.finish()
    
@dp.message_handler(state="javob_yuborish_blok")
async def javoblar(msg : types.Message, state : FSMContext):
    berilgan_javob = msg.text
    if berilgan_javob.isalpha():
        idd = msg.from_user.id
        berilgan_javob_size = len(berilgan_javob)
        javoblar = temp_data[idd][2].split(',')
        haqiqiy_javob_uzunligi = len(javoblar[temp_data[idd][4]])
        if haqiqiy_javob_uzunligi == berilgan_javob_size:
            q = temp_data[idd][1]
            gap = q[temp_data[idd][4]].split('~')
            berilgan_javob = berilgan_javob.lower()
            temp_data[idd][3].append(berilgan_javob)
            answer = ""
            n = int(gap[1])
            for harf in berilgan_javob:
                answer += f"<i>{n} - {harf}\n</i>"
                n += 1
            answer += "<b>To`g`ri ekanligiga ishonch hosil qiling❗️</b>\n<i>Tasdiqlaysizmi ❓</i>"
            await msg.answer(answer, reply_markup=tasdiq_keyboard)
            await state.set_state("berilgan_javobni_tasdiqlash_blok")
        else:
            await msg.answer(f"<b>Bu testning javoblari soni {haqiqiy_javob_uzunligi} ta.\nAmmo siz {berilgan_javob_size} ta javob yubordingiz❌</b>\n<i>Savollar soniga mos holda javoblarni qayta yuboring : </i>", reply_markup=bekor_qil)
    else:
        await msg.answer("<b>Testning javobi faqat lotin harflaridan iborat!</b>\n<i>Qayta kiriting yoki bekor qiling.</i>", reply_markup=bekor_qil)
        
@dp.callback_query_handler(text="yes", state="berilgan_javobni_tasdiqlash_blok")
async def yes(call : types.CallbackQuery, state : FSMContext):
    temp_data[call.from_user.id][4] += 1
    if temp_data[call.from_user.id][4] != temp_data[call.from_user.id][0]:
        q = temp_data[call.from_user.id][1]
        gap = q[temp_data[call.from_user.id][4]].split('~')
        answer = f"{gap[0]}<b>Endi esa, {gap[1]} - {gap[2]} savollarning javobini yuboring : </b>\n\n<i>abcd... 👈ko`rinishida</i>"
        await call.answer(f"{temp_data[call.from_user.id][4]} - fanning javoblari qabul qilindi✅")
        await call.message.delete()
        await call.message.answer(text=answer)
        await state.set_state("javob_yuborish_blok")
    else:
        user_id = call.from_user.id
        test_kodi = temp_data[user_id][5]
        data_test = db_ts.select_test_blok_by_test_kodi(test_kodi)
        if data_test == None:
            await call.answer("😕")
            await call.message.delete()
            await call.message.answer("<b>Afsuski test yakunlandi❌</b>\n<i>Biroz kechikdingiz!</i>", reply_markup=menu)
            await state.finish()
        else:
            q = temp_data[call.from_user.id][1]
            fan_nomlari = data_test[2].split(',')
            beriladigan_ballar = data_test[4].split(',')
            fanlar_soni = len(fan_nomlari)
            haqiqiy_javoblar = data_test[3].split(',')
            berilgan_javob = temp_data[user_id][3]
            tuplagan_ballari_temp = []
            temp_xato_javoblari = []
            tuplagan_ballari = ""
            xato_javoblari = ""
            for i in range(0, fanlar_soni):
                temp_bali = 0
                
                for j in range(0, len(haqiqiy_javoblar[i])):
                    if haqiqiy_javoblar[i][j] == berilgan_javob[i][j]:
                        temp_bali += 1
                    else:
                        if i != 0:
                            gap = q[i-1].split('~')
                            temp_xato_javoblari.append(j+1+int(gap[2]))
                        else:
                            temp_xato_javoblari.append(j+1)
                tuplagan_ballari_temp.append(round(float(beriladigan_ballar[i]) * temp_bali,4))
            
            tuplagan_ballari = ",".join([
                    f"{item}" for item in tuplagan_ballari_temp
                    ])
            xato_javoblari = ",".join([
                    f"{item}" for item in temp_xato_javoblari
                    ])
            summ = sum(tuplagan_ballari_temp)
            try:
                db_bj.add_javob_blok(user_id, test_kodi, tuplagan_ballari, xato_javoblari, summ)
            except Exception as e:
                print(e)
            
            answer = f"🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Blok test</i>\n✅<b>Sizning natijangiz : </b>\n"
            for qwe in range(0, len(fan_nomlari)):
                answer += f"<b>{kitoblar[random.randint(0,4)]}{fan_nomlari[qwe]} : </b><i>{tuplagan_ballari_temp[qwe]} ball</i>\n"
            answer += f"<b>Umumiy natijangiz : </b><i>{summ} ball</i>\n\n"
            
            vergul = data_test[5].find(',')
            if vergul != -1:
                vaqt = data_test[5].split(',')
                answer += f"⏱<i>Test {vaqt[2]}:{vaqt[3]} da yakunlanadi.\n\n</i>"
            await call.message.answer(answer, reply_markup=menu)
            await call.answer(f"{test_kodi} - testga javob berdingiz ✅", show_alert=True)
            await call.message.delete()
            await state.finish()
            temp_data[user_id] = None
            user = db_users.select_user_id(call.from_user.id)
            if user[2] == None:
                username = "username mavjud emas!"
            else:
                username = f"@{user[2]}"
            answer_admin = f"<b>{test_kodi} - testga </b><i>{user[1]}</i><b><i>({username})</i> javob jo'natdi.</b>"
            await bot.send_message(data_test[0], answer_admin, reply_markup=test_owner(test_kodi))
            
            
            
@dp.callback_query_handler(text='no', state="berilgan_javobni_tasdiqlash_blok")
async def tekshir(call : types.CallbackQuery, state : FSMContext):
    temp_data[call.from_user.id][3].pop(-1)
    await call.message.delete()
    await call.message.answer("<b>Javoblarni tog`rilab, qayta yuboring!\n</b>", reply_markup=bekor_qil)
    await state.set_state("javob_yuborish_blok")