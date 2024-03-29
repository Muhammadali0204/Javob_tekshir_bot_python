from aiogram import types
from loader import (
    dp,
    db_users,
    Limitlar_oddiy,
    Limitlar_blok,
    foydalanuvchi_limitlari_oddiy,
    foydalanuvchi_limitlari_blok,
    db_ts,
    db_bj,
    bot,
    kitoblar,
)
from datetime import datetime
import asyncio
import pytz, random
from data.config import ADMINS


@dp.message_handler(text="Vaqt yuborilishi12345678")
async def hahaha(msg: types.Message):
    pass


@dp.message_handler(text="jdhkjhfvkijdhsfviuefthgreolt", chat_id=ADMINS, state="*")
async def buyruq(msg: types.Message):
    await msg.delete()
    t = datetime.now(pytz.timezone("Asia/Tashkent"))
    soat_minut = t.strftime("%H:%M")
    sana = t.strftime("%d.%m.%Y")
    sek = t.strftime("%S")

    await bot.send_message(ADMINS[1], f"{soat_minut}:{sek} {sana}")

    # Limitlarni yangilash
    if soat_minut == "00:00":
        users = db_users.select_all_users()

        for user in users:
            if user[3] == sana:
                db_users.update_status_user("-1", user[0])
                try:
                    await bot.send_message(
                        user[0],
                        "<b>Premium obunangiz muddati tugadi</b>\n\n<i>Qayta faollashtirish uchun \n\n🛠Sozlamalar/⬆️Limitlarni oshirish \n\nbo'limiga o'ting</i>",
                    )
                except:
                    pass

        users = db_users.select_all_users()

        for user in users:
            if user[3] in ["-1", "0"]:
                foydalanuvchi_limitlari_oddiy[user[0]] = [
                    Limitlar_oddiy[0],
                    Limitlar_oddiy[1],
                ]
                foydalanuvchi_limitlari_blok[user[0]] = [
                    Limitlar_blok[0],
                    Limitlar_blok[1],
                ]
            else:
                foydalanuvchi_limitlari_oddiy[user[0]] = [
                    Limitlar_oddiy[2],
                    Limitlar_oddiy[3],
                ]
                foydalanuvchi_limitlari_blok[user[0]] = [
                    Limitlar_blok[2],
                    Limitlar_blok[3],
                ]

    # ----------------

    javob_berganlar_malumoti_oddiy = (
        db_bj.select_all_javob_berganlar_tartiblangan_oddiy()
    )
    javob_berganlar_malumoti_blok = db_bj.select_all_javob_berganlar_tartiblangan_blok()

    tuzilgan_savol_oddiy = db_ts.all_tests_oddiy_vaqt()
    tuzilgan_savol_blok = db_ts.all_tests_blok_vaqt()

    for oddiy_test in tuzilgan_savol_oddiy:
        vaqt = oddiy_test[4].split(",")
        vaqt1 = f"{vaqt[0]}:{vaqt[1]}"
        vaqt2 = f"{vaqt[2]}:{vaqt[3]}"

        if vaqt1 == soat_minut and oddiy_test[5] == 0:
            try:
                db_ts.update_test_faollik("Oddiy_test", oddiy_test[1])
                await bot.send_message(
                    oddiy_test[0],
                    f"<b>Siz tuzgan <i>{oddiy_test[1]}</i> - test faollashdi.</b>\n\n<i>Test {vaqt2} da yakunlanadi</i>",
                )
            except:
                pass

        elif vaqt2 == soat_minut:
            if oddiy_test[5] == 1:
                test_kodi = oddiy_test[1]

                javob_berganlar = []  # [(1, 2, 3), (4, 5, 6, ) ... ]
                for user in javob_berganlar_malumoti_oddiy:
                    if user[1] == test_kodi:
                        javob_berganlar.append([db_users.select_user_id(user[0]), user])
                if javob_berganlar != []:
                    # Test egasiga ------------------------------
                    ragbat = "🥇"
                    bal = javob_berganlar[0][1][2]
                    answer = f"<b>Test yakunlandi✅</b>\n\n🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Oddiy</i>\n{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{oddiy_test[2]}</i>\n<b>🔢Savollar soni : </b> <i>{len(oddiy_test[3])} ta</i>\n\n<b>📊Natijalar : </b>\n\n"
                    for i in range(0, len(javob_berganlar)):
                        if bal > javob_berganlar[i][1][2]:
                            if ragbat == "🥇":
                                ragbat = "🥈"
                            elif ragbat == "🥈":
                                ragbat = "🥉"
                            elif ragbat == "🥉":
                                ragbat = ""
                            bal = javob_berganlar[i][1][2]
                        answer += f"<b>{i+1}. <i>{javob_berganlar[i][0][1]}</i></b> <i>{javob_berganlar[i][1][2]} ta</i>{ragbat}\n"

                    answer += "\n\n<b>✅To`g`ri javoblar : </b>\n\n"
                    soni = 0
                    if len(oddiy_test[3]) < 6:
                        soni = 3
                    elif len(oddiy_test[3]) < 16:
                        soni = 4
                    else:
                        soni = 5
                    for j in range(0, len(oddiy_test[3])):
                        if (j + 1) % soni == 0:
                            answer += f"<b>{j+1} - <i>{oddiy_test[3][j]}</i></b>\n"
                        else:
                            answer += f"<b>{j+1} - <i>{oddiy_test[3][j]}</i></b>  "

                    answer += "\n\n<b>Testda qatnashgan barchaga rahmat 😊</b>"

                    try:
                        await bot.send_message(
                            oddiy_test[0], f"{test_kodi} - kodli test yakunlandi✅"
                        )
                        await bot.send_message(oddiy_test[0], answer)
                    except:
                        pass

                        # Testlarni o`chirish-----------------
                    db_bj.delete_answers_oddiy_by_test_kodi(test_kodi)
                    db_ts.delete_answers_oddiy_by_test_kodi(test_kodi)

                    if oddiy_test[6] == "1":
                        kanal = db_users.select_user_id(oddiy_test[0])[4]
                        if kanal == None:
                            try:
                                await bot.send_message(
                                    oddiy_test[0],
                                    f"<b>Kanalga post joylash bo'yicha xatolik!\n\n</b><i>Kanal yoki guruh bog'lanmagan ❌</i>",
                                )
                            except:
                                pass
                        else:
                            kanal = kanal.split(",")
                            try:
                                await bot.send_message(kanal[0], text=answer)
                                await bot.send_message(
                                    oddiy_test[0],
                                    f"<b><code>{kanal[1]}</code> kanal/guruhiga natijalar yuborildi.</b>",
                                )
                            except Exception as e:
                                await bot.send_message(
                                    oddiy_test[0],
                                    f"Kanalga post joylash bo'yicha xatolik!\n{e}",
                                )
                                await bot.send_message(
                                    oddiy_test[0],
                                    "<i>Adminga murojaat qiling va yuqoridagi xabarni yuboring!</i>",
                                )

                    await asyncio.sleep(0.05)
                else:
                    try:
                        await bot.send_message(
                            oddiy_test[0],
                            f"<b>{test_kodi} - kodli test yakunlandi</b>✅\n<i>Hech kim javob bermagan</i>",
                        )
                        db_ts.delete_answers_oddiy_by_test_kodi(test_kodi)
                        await asyncio.sleep(0.05)
                    except:
                        pass

    for data_test_blok in tuzilgan_savol_blok:
        vaqt = data_test_blok[5].split(",")
        vaqt1 = f"{vaqt[0]}:{vaqt[1]}"
        vaqt2 = f"{vaqt[2]}:{vaqt[3]}"

        if vaqt1 == soat_minut and data_test_blok[6] == 0:
            db_ts.update_test_faollik("Blok_test", data_test_blok[1])
            try:
                await bot.send_message(
                    data_test_blok[0],
                    f"<b>Siz tuzgan <i>{data_test_blok[1]}</i> - test faollashdi.</b>\n\n<i>Test {vaqt2} da yakunlanadi</i>",
                )
            except:
                pass

        elif vaqt2 == soat_minut:
            if data_test_blok[6] == 1:
                test_kodi = data_test_blok[1]

                javob_berganlar = []  # [(1, 2, 3), (4, 5, 6, ) ... ]
                for user in javob_berganlar_malumoti_blok:
                    if user[1] == int(test_kodi):
                        javob_berganlar.append([db_users.select_user_id(user[0]), user])

                if javob_berganlar != []:
                    fan_nomlari = data_test_blok[2].split(",")
                    javoblar = data_test_blok[3].split(",")
                    beriladigan_ballar = data_test_blok[4].split(",")

                    db_bj.delete_answers_blok_by_test_kodi(test_kodi)
                    db_ts.delete_answers_blok_by_test_kodi(test_kodi)

                    # Test egasiga ------------------------------
                    answer = f"<b>Test yakunlandi ✅</b>\n\n🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Blok test</i>\n🟢<b>Fanlar soni : </b><i>{len(fan_nomlari)} ta</i>\n\n"
                    umumiy_ball = 0
                    q = [1, len(javoblar[0])]
                    for i in range(0, len(fan_nomlari)):
                        if i != 0:
                            q[0] += len(javoblar[i - 1])
                            q[1] += len(javoblar[i])
                        answer += f"<b>{i+1} - fan : </b>\n"
                        answer += (
                            f"<b>{kitoblar[i]}Fan nomi : </b><i>{fan_nomlari[i]}</i>\n"
                        )
                        answer += f"<b>🔢Savollar soni : <i>{len(javoblar[i])} ta</i></b><i> ({q[0]}-{q[1]})</i>\n"
                        answer += f"<b>❕Ball : </b><i>{beriladigan_ballar[i]}</i>\n"
                        umumiy_ball += len(javoblar[i]) * float(beriladigan_ballar[i])
                        answer += f"<i>Fan uchun beriladigan ball : {round(len(javoblar[i]) * float(beriladigan_ballar[i]), 4)}</i>\n\n"
                    answer += f"<b>Jami savollar soni : </b><i>{q[1]} ta</i>\n"
                    answer += f"<b>Umumiy ball : </b><i>{round(umumiy_ball, 4)}</i>\n\n<b>📊Natijalar : </b>\n\n"
                    ragbat = "🥇"
                    bal = javob_berganlar[0][1][4]
                    for i in range(0, len(javob_berganlar)):
                        if bal > javob_berganlar[i][1][4]:
                            if ragbat == "🥇":
                                ragbat = "🥈"
                            elif ragbat == "🥈":
                                ragbat = "🥉"
                            elif ragbat == "🥉":
                                ragbat = ""
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
                        else:
                            soni = 5

                        for j in range(0, len(javoblar[i])):
                            if (j + 1) % soni == 0:
                                answer += f"<b>{j+1} - <i>{javoblar[i][j]}</i></b>\n"
                            else:
                                answer += f"<b>{j+1} - <i>{javoblar[i][j]}</i></b>  "

                        answer += "\n\n"

                    answer += "\n<b>Testda qatnashgan barchaga rahmat 😊</b>"

                    try:
                        await bot.send_message(
                            data_test_blok[0],
                            f"<b>{test_kodi} - kodli test yakunlandi✅</b>",
                        )
                        await bot.send_message(data_test_blok[0], answer)
                    except:
                        pass

                    if data_test_blok[7] == "1":
                        kanal = db_users.select_user_id(data_test_blok[0])[4]
                        if kanal == None:
                            try:
                                await bot.send_message(
                                    data_test_blok[0],
                                    f"<b>Kanalga post joylash bo'yicha xatolik!\n\n</b><i>Kanal yoki guruh bog'lanmagan ❌</i>",
                                )
                            except:
                                pass
                        else:
                            kanal = kanal.split(",")
                            try:
                                await bot.send_message(kanal[0], text=answer)
                                await bot.send_message(
                                    data_test_blok[0],
                                    f"<b><code>{kanal[1]}</code> kanal/guruhiga natijalar yuborildi.</b>",
                                )
                            except Exception as e:
                                await bot.send_message(
                                    data_test_blok[0],
                                    f"Kanalga post joylash bo'yicha xatolik!\n{e}",
                                )
                                await bot.send_message(
                                    data_test_blok[0],
                                    "<i>Adminga murojaat qiling va yuqoridagi xabarni yuboring!</i>",
                                )

                else:
                    try:
                        await bot.send_message(
                            data_test_blok[0],
                            f"<b>{test_kodi} - kodli test yakunlandi</b>✅\n\n<i>Hech kim javob bermagan</i>",
                        )
                        db_ts.delete_answers_blok_by_test_kodi(test_kodi)
                        await asyncio.sleep(0.05)
                    except:
                        pass

    # tuzilgan_testlarni o`chirish 3 kunlikdagilarni
    if soat_minut == "23:30":
        tuzilgan_savollar_oddiy = db_ts.all_tests_oddiy_sana(sana)
        tuzilgan_savollar_blok = db_ts.all_tests_blok_sana(sana)

        for oddiy_test in tuzilgan_savollar_oddiy:
            test_kodi = oddiy_test[1]

            javob_berganlar = []  # [(1, 2, 3), (4, 5, 6, ) ... ]
            for user in javob_berganlar_malumoti_oddiy:
                if user[1] == test_kodi:
                    javob_berganlar.append([db_users.select_user_id(user[0]), user])
            if javob_berganlar != []:
                # Test egasiga ------------------------------
                ragbat = "🥇"
                bal = javob_berganlar[0][1][2]
                answer = f"<b>Test yakunlandi✅</b>\n\n🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Oddiy</i>\n{kitoblar[random.randint(0, 4)]}<b>Fan nomi : </b><i>{oddiy_test[2]}</i>\n<b>🔢Savollar soni : </b> <i>{len(oddiy_test[3])} ta</i>\n\n<b>📊Natijalar : </b>\n\n"
                for i in range(0, len(javob_berganlar)):
                    if bal > javob_berganlar[i][1][2]:
                        if ragbat == "🥇":
                            ragbat = "🥈"
                        elif ragbat == "🥈":
                            ragbat = "🥉"
                        elif ragbat == "🥉":
                            ragbat = ""
                        bal = javob_berganlar[i][1][2]
                    answer += f"<b>{i+1}. <i>{javob_berganlar[i][0][1]}</i></b> <i>{javob_berganlar[i][1][2]} ta</i>{ragbat}\n"

                answer += "\n\n<b>✅To`g`ri javoblar : </b>\n\n"
                soni = 0
                if len(oddiy_test[3]) < 6:
                    soni = 3
                elif len(oddiy_test[3]) < 16:
                    soni = 4
                else:
                    soni = 5
                for j in range(0, len(oddiy_test[3])):
                    if (j + 1) % soni == 0:
                        answer += f"<b>{j+1} - <i>{oddiy_test[3][j]}</i></b>\n"
                    else:
                        answer += f"<b>{j+1} - <i>{oddiy_test[3][j]}</i></b>  "

                answer += "\n\n<b>Testda qatnashgan barchaga rahmat 😊</b>"

                try:
                    await bot.send_message(
                        oddiy_test[0], f"{test_kodi} - kodli test yakunlandi✅"
                    )
                    await bot.send_message(oddiy_test[0], answer)
                except:
                    pass

                    # Testlarni o`chirish-----------------
                db_bj.delete_answers_oddiy_by_test_kodi(test_kodi)
                db_ts.delete_answers_oddiy_by_test_kodi(test_kodi)
                await asyncio.sleep(0.05)
            else:
                try:
                    await bot.send_message(
                        oddiy_test[0],
                        f"<b>{test_kodi} - kodli test yakunlandi</b>✅\n<i>Hech kim javob bermagan</i>",
                    )
                    db_ts.delete_answers_oddiy_by_test_kodi(test_kodi)
                    await asyncio.sleep(0.05)
                except:
                    pass

        for data_test_blok in tuzilgan_savollar_blok:
            test_kodi = data_test_blok[1]

            javob_berganlar = []  # [(1, 2, 3), (4, 5, 6, ) ... ]
            for user in javob_berganlar_malumoti_blok:
                if user[1] == int(test_kodi):
                    javob_berganlar.append([db_users.select_user_id(user[0]), user])

            if javob_berganlar != []:
                fan_nomlari = data_test_blok[2].split(",")
                javoblar = data_test_blok[3].split(",")
                beriladigan_ballar = data_test_blok[4].split(",")

                db_bj.delete_answers_blok_by_test_kodi(test_kodi)
                db_ts.delete_answers_blok_by_test_kodi(test_kodi)

                # Test egasiga ------------------------------
                answer = f"<b>Test yakunlandi ✅</b>\n\n🔑<b>Test kodi : </b><i>{test_kodi}</i>\n🗂<b>Test turi : </b><i>Blok test</i>\n🟢<b>Fanlar soni : </b><i>{len(fan_nomlari)} ta</i>\n\n"
                umumiy_ball = 0
                q = [1, len(javoblar[0])]
                for i in range(0, len(fan_nomlari)):
                    if i != 0:
                        q[0] += len(javoblar[i - 1])
                        q[1] += len(javoblar[i])
                    answer += f"<b>{i+1} - fan : </b>\n"
                    answer += (
                        f"<b>{kitoblar[i]}Fan nomi : </b><i>{fan_nomlari[i]}</i>\n"
                    )
                    answer += f"<b>🔢Savollar soni : <i>{len(javoblar[i])} ta</i></b><i> ({q[0]}-{q[1]})</i>\n"
                    answer += f"<b>❕Ball : </b><i>{beriladigan_ballar[i]}</i>\n"
                    umumiy_ball += len(javoblar[i]) * float(beriladigan_ballar[i])
                    answer += f"<i>Fan uchun beriladigan ball : {round(len(javoblar[i]) * float(beriladigan_ballar[i]), 4)}</i>\n\n"
                answer += f"<b>Jami savollar soni : </b><i>{q[1]} ta</i>\n"
                answer += f"<b>Umumiy ball : </b><i>{round(umumiy_ball, 4)}</i>\n\n<b>📊Natijalar : </b>\n\n"
                ragbat = "🥇"
                bal = javob_berganlar[0][1][4]
                for i in range(0, len(javob_berganlar)):
                    if bal > javob_berganlar[i][1][4]:
                        if ragbat == "🥇":
                            ragbat = "🥈"
                        elif ragbat == "🥈":
                            ragbat = "🥉"
                        elif ragbat == "🥉":
                            ragbat = ""
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
                    else:
                        soni = 5

                    for j in range(0, len(javoblar[i])):
                        if (j + 1) % soni == 0:
                            answer += f"<b>{j+1} - <i>{javoblar[i][j]}</i></b>\n"
                        else:
                            answer += f"<b>{j+1} - <i>{javoblar[i][j]}</i></b>  "

                    answer += "\n\n"

                answer += "\n<b>Testda qatnashgan barchaga rahmat 😊</b>"

                try:
                    await bot.send_message(
                        data_test_blok[0],
                        f"<b>{test_kodi} - kodli test yakunlandi✅</b>",
                    )
                    await bot.send_message(data_test_blok[0], answer)
                    await asyncio.sleep(0.05)
                except:
                    pass
            else:
                db_ts.delete_answers_blok_by_test_kodi(test_kodi)
                try:
                    await bot.send_message(
                        oddiy_test[0],
                        f"<b>{test_kodi} - kodli test yakunlandi</b>✅\n\n<i>Hech kim javob bermagan</i>",
                    )
                    await asyncio.sleep(0.05)
                except:
                    pass
