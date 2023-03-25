from aiogram import types, filters
from datetime import datetime as d
import pytz
from loader import dp, db_bj, db_users


@dp.callback_query_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), regexp="natija:+")
async def natija(call: types.CallbackQuery):
    kod = call.data.split(':')[1]
    javob_berganlar_user_ids = db_bj.select_all_javob_berganlar_by_test_kodi(
        kod)
    if javob_berganlar_user_ids != []:
        javob_berganlar_ismlari = []
        for user_id in javob_berganlar_user_ids:
            ism = db_users.select_user_id(user_id[0])
            javob_berganlar_ismlari.append(ism[1])
        answer = f"<b>🔑Test kodi : {kod}</b>\n"
        answer += f"<b>🔢Javob berganlar soni : </b><i>{len(javob_berganlar_ismlari)} ta</i>\n\n"

        for i in range(0, len(javob_berganlar_ismlari)):
            answer += f"<b><i>{i+1}. {javob_berganlar_ismlari[i]}</i></b>\n"
        t = d.now(pytz.timezone("Asia/Tashkent"))
        soat_minut = t.strftime("%H:%M")
        answer += f"\n<i>🕐Ma`lumot olingan vaqt : {soat_minut}</i>"
        await call.answer(f"{kod} - kodli test")
        await call.message.answer(answer)
    else:
        await call.answer(f"{kod} - kodli test yakunlangan❗️", show_alert=True)
        await call.message.delete()
