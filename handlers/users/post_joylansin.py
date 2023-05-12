from aiogram import types

from loader import dp, db_ts


@dp.callback_query_handler(regexp="ha:+")
async def yes(call: types.CallbackQuery):
    data = call.data.split(':')
    try:
        db_ts.update_test_post(data[1], data[2], 1)
        await call.answer(text=f"{data[2]} - kodli test natijasi kanalingizga avtomatik ravishda joylanadi ✅", show_alert=True)
        await call.message.answer(text=f"{data[2]} - kodli test natijasi kanalingizga avtomatik ravishda joylanadi ✅")
        await call.message.delete()
    except:
        await call.answer(text="Xatolik yuz berdi, bot adminiga xabar qilishingiz mumkin.", show_alert=True)
        await call.message.delete()


@dp.callback_query_handler(regexp="yuq:+")
async def no(call: types.CallbackQuery):
    data = call.data.split(':')
    await call.message.answer(text=f"<i>{data[2]} - kodli test natijasi kanalingizga avtomatik ravishda joylanmaydi ❌</i>")
    await call.message.delete()
