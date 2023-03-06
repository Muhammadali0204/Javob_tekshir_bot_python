from aiogram import types, filters
from datetime import datetime as d
import pytz, random, asyncio
from loader import dp, db_bj, db_users, db_ts, kitoblar, bot


@dp.callback_query_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE),regexp="tugatish:+")
async def tugatish(call : types.CallbackQuery):
    test_kodi = call.data.split(':')[1]
    try:
        data_test_oddiy = db_ts.select_test_oddiy_by_test_kodi(test_kodi)
        data_test_blok = db_ts.select_test_blok_by_test_kodi(test_kodi)
    except Exception as e:
        print(e)
    if data_test_blok == None and data_test_oddiy == None:
        await call.answer(f"{test_kodi} - kodli test allaqachon yakunlangan❗️", show_alert=True)
        await call.message.delete()
    else:
        if data_test_blok == None: # Test oddiy bo`lsa
            javob_berganlar_malumoti = db_bj.select_all_javob_berganlar_tartiblangan_oddiy_by_testkodi(test_kodi)
            javob_berganlar = [] # [(1, 2, 3), (4, 5, 6, ) ... ]
            for user in javob_berganlar_malumoti:
                javob_berganlar.append([db_users.select_user_id(user[0]), user])
                    
            # Test egasiga ------------------------------
            ragbat = '🥇'
            bal = javob_berganlar[0][1][2]
            answer = f"<b>Test yakunlandi✅</b>\n\n🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Oddiy</i>\n{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{data_test_oddiy[2]}</i>\n<b>🔢Savollar soni : </b> <i>{len(data_test_oddiy[3])} ta</i>\n\n<b>📊Natijalar : </b>\n\n"
            for i in range(0, len(javob_berganlar)):
                if bal > javob_berganlar[i][1][2]:
                    if ragbat == '🥇':
                        ragbat = '🥈'
                    elif ragbat == '🥈':
                        ragbat = '🥉'
                    elif ragbat == '🥉':
                        ragbat = ''
                    bal = javob_berganlar[i][1][2]
                answer += f"<b>{i+1}. <i>{javob_berganlar[i][0][1]}</i></b> <i>{javob_berganlar[i][1][2]} ta</i>{ragbat}\n"
                
                
            answer += "\n\n<b>✅To`g`ri javoblar : </b>\n\n"
            soni = 0
            if len(data_test_oddiy[3]) < 6:
                soni = 3
            elif len(data_test_oddiy[3]) < 16:
                soni = 4
            else :
                soni = 5
            for j in range(0, len(data_test_oddiy[3])):
                if (j+1) % soni == 0:
                    answer += f"<b>{j+1} - <i>{data_test_oddiy[3][j]}</i></b>\n"
                else:
                    answer += f"<b>{j+1} - <i>{data_test_oddiy[3][j]}</i></b>  "
                                        
            answer += "\n\n<b>Testda qatnashgan barchaga rahmat 😊</b>"
                
            await call.answer(f"{test_kodi} - kodli test yakunlandi✅", show_alert=True)
            await call.message.delete()
            await call.message.answer(answer)
            
            # Testlarni o`chirish-----------------
            db_bj.delete_answers_oddiy_by_test_kodi(test_kodi)
            db_ts.delete_answers_oddiy_by_test_kodi(test_kodi)
            
            if data_test_oddiy[6] != None:
                kanal = db_users.select_user_id(call.from_user.id)[4].split(',')
                try:
                    await bot.send_message(kanal[0], text=answer)
                    await call.message.answer(f"<b><code>{kanal[1]}</code> kanal/guruhiga natijalar yuborildi.</b>")
                except Exception as e:
                    await call.message.answer(f"<b>Xatolik!</b>\n{e}")
                    await call.message.answer("<i>Adminga murojaat qiling va yuqoridagi xabarni yuboring!</i>")
                        
            # javob berganlar -- [(5035718776, 'Muhammad Ali', 'None', '0', None), (5035718776,      112,      4,          ''   )]
 #                                      id            ismi    username  sta  kanal     user_id       kodi    javoblar  xato javoblar          
         
        elif data_test_oddiy == None: # Test blok test bo`lsa
            
            javob_berganlar_malumoti = db_bj.select_all_javob_berganlar_tartiblangan_blok_by_testkodi(test_kodi)
            javob_berganlar = [] # [(1, 2, 3), (4, 5, 6, ) ... ]
            for user in javob_berganlar_malumoti:
                javob_berganlar.append([db_users.select_user_id(user[0]), user])
            
            
            fan_nomlari = data_test_blok[2].split(',')
            javoblar = data_test_blok[3].split(',')
            beriladigan_ballar = data_test_blok[4].split(',')
            
            db_bj.delete_answers_blok_by_test_kodi(test_kodi)
            db_ts.delete_answers_blok_by_test_kodi(test_kodi)
            
             # Test egasiga ------------------------------
            answer = f"<b>Test yakunlandi ✅</b>\n\n🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Blok test</i>\n🟢<b>Fanlar soni : </b><i>{len(fan_nomlari)} ta</i>\n\n"
            umumiy_ball = 0
            q = [1, len(javoblar[0])]
            for i in range(0, len(fan_nomlari)):
                if i != 0:
                    q[0] += len(javoblar[i-1])
                    q[1] += len(javoblar[i])
                answer += f"<b>{i+1} - fan : </b>\n"
                answer += f"<b>{kitoblar[i]}Fan nomi : </b><i>{fan_nomlari[i]}</i>\n"
                answer += f"<b>🔢Savollar soni : <i>{len(javoblar[i])} ta</i></b><i> ({q[0]}-{q[1]})</i>\n"
                answer += f"<b>❕Ball : </b><i>{beriladigan_ballar[i]}</i>\n"
                umumiy_ball += len(javoblar[i]) * float(beriladigan_ballar[i])
                answer += f"<i>Fan uchun beriladigan ball : {round(len(javoblar[i]) * float(beriladigan_ballar[i]), 4)}</i>\n\n"
            answer += f"<b>Jami savollar soni : </b><i>{q[1]} ta</i>\n"
            answer += f"<b>Umumiy ball : </b><i>{round(umumiy_ball, 4)}</i>\n\n<b>📊Natijalar : </b>\n\n"
            ragbat = '🥇'
            bal = javob_berganlar[0][1][4]
            for i in range(0, len(javob_berganlar)):
                if bal > javob_berganlar[i][1][4]:
                    if ragbat == '🥇':
                        ragbat = '🥈'
                    elif ragbat == '🥈':
                        ragbat = '🥉'
                    elif ragbat == '🥉':
                        ragbat = ''
                    bal = javob_berganlar[i][1][4]
                answer += f"<b>{i+1}. <i>{javob_berganlar[i][0][1]}</i></b> <i>{round(float(javob_berganlar[i][1][4]), 4)} ball</i>{ragbat}\n"
            
            answer += "\n<b>✅To`g`ri javoblar : </b>\n\n"
            for i in range(0, len(fan_nomlari)):
                answer += f"<b>{i+1} - fan : {kitoblar[random.randint(0, 4)]}<i>{fan_nomlari[i]}</i></b>\n"
                soni = 0
                if len(javoblar[i]) < 6:
                    soni = 3
                elif len(javoblar[i]) < 16:
                    soni = 4
                else :
                    soni = 5
                    
                for j in range(0, len(javoblar[i])):
                    if (j+1) % soni == 0:
                        answer += f"<b>{j+1} - <i>{javoblar[i][j]}</i></b>\n"
                    else:
                        answer += f"<b>{j+1} - <i>{javoblar[i][j]}</i></b>  "
                        
                answer += "\n\n"
                                        
            answer += "\n<b>Testda qatnashgan barchaga rahmat 😊</b>"
            
                
            await call.answer(f"{test_kodi} - kodli test yakunlandi✅", show_alert=True)
            await call.message.delete()
            await call.message.answer(answer)
            
            
            
            
            if data_test_blok[7] != None:
                kanal = db_users.select_user_id(call.from_user.id)[4].split(',')
                try:
                    await bot.send_message(kanal[0], text=answer)
                    await call.message.answer(f"<b><code>{kanal[1]}</code> kanal/guruhiga natijalar yuborildi.</b>")
                except Exception as e:
                    await call.message.answer(f"<b>Kanalga post joylash bo'yicha xatolik!</b>\n{e}")
                    await call.message.answer("<i>Adminga murojaat qiling va yuqoridagi xabarni yuboring!</i>")
            