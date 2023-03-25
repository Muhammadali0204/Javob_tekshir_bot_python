from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from keyboards.default.test_turi import tur
from keyboards.default.menu import menu
from keyboards.inline.avto_qulda import avto_qul, avto_qul2
from keyboards.default.bekor_qilish import fanlar_soni
from aiogram.dispatcher import FSMContext
from loader import dp, foydalanuvchi_limitlari_blok, temp_data


@dp.message_handler(text="📚Blok test", state="test_turi")
async def bloktest(msg: types.Message, state: FSMContext):
    await msg.answer(text="📚Blok test", reply_markup=ReplyKeyboardRemove())
    await msg.answer(
        text="<b>Tuzmoqchi bo`lgan testingiz <i>Avto</i> yakunlansinmi yoki o`zingiz yakunlaysizmi ❓</b>",
        reply_markup=avto_qul
    )
    await state.set_state("avto_qul_blok")


@dp.callback_query_handler(text="avto", state="avto_qul_blok")
async def avto(call: types.CallbackQuery, state: FSMContext):
    try:
        if foydalanuvchi_limitlari_blok[call.from_user.id][1] < 1:
            await call.answer(text="Afsuski bunday test tuzolmaysiz❗️\nLimitingiz tugagan.Batafsil : \n🛠Sozlamalar/⬆️Limitlarni oshirish", show_alert=True)
            await call.message.delete()
            await call.message.answer(text="<b>Test tuzish : </b>",
                                      reply_markup=tur)
            await state.set_state("test_turi")
        else:
            temp_data[call.from_user.id] = [[], [], None, [], [], 0, 0]
            await call.message.delete()
            await call.message.answer(text="<b>Yaxshi, fanlar soni nechta ?</b>\n<i>Tanlang : </i>", reply_markup=fanlar_soni)
            await state.set_state("fanlar_soni_blok")
    except:
        await call.message.delete()
        await call.message.answer("<b>Iltimos /start ni bosing va ism familiyangizni kiriting!</b>", reply_markup=menu)
        await state.finish()


@dp.callback_query_handler(text="qul", state="avto_qul_blok")
async def qul(call: types.CallbackQuery, state: FSMContext):
    try:
        if foydalanuvchi_limitlari_blok[call.from_user.id][0] < 1:
            await call.message.delete()
            await call.answer(text="Afsuski bunday test tuzolmaysiz❗️\nLimitingiz tugagan.Batafsil : \n🛠Sozlamalar/⬆️Limitlarni oshirish", show_alert=True)
            await call.message.answer(text="<b>Test tuzish : </b>",
                                      reply_markup=tur)
            await state.set_state("test_turi")
        else:
            temp_data[call.from_user.id] = [[], [], None, [], None, 1, 0]
            await call.message.delete()
            await call.message.answer(text="<b>Yaxshi, fanlar soni nechta ?</b>\n<i>Tanlang : </i>", reply_markup=fanlar_soni)
            await state.set_state("fanlar_soni_blok")
    except:
        await call.message.delete()
        await call.message.answer("<b>Iltimos /start ni bosing va ism familiyangizni kiriting!</b>", reply_markup=menu)
        await state.finish()


@dp.callback_query_handler(text="info", state="avto_qul_blok")
async def info(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Batafsil ma`lumot👇")
    await call.message.delete()
    await call.message.answer(text="<b>*Manual - tuzgan testingizni tugma bosish orqali yakunlaysiz.\nTest tuzilganidan boshlab faol ya'ni foydalanuvchilar javob berishi mumkin bo`ladi.</b>\n" +
                              "<b>*Avto - tuzgan testingiz siz ko`rsatgan vaqtda avtomatik ravishda boshlanib, yakunlanish vaqti yetganda avtomatik yakunlanadi.\nTest tuzilganidan boshlab faol bo`lmaydi ya`ni boshlanish vaqti yetmaguncha hech kim javob bera olmaydi.\n</b><b><i>*Test ishtirokchilariga avvaldan test kodi va test haqida ma`lumotlar berish uchun qulay✅\nTest siz ko`rsatgan muddatda bo`lib o`tadi😎</i></b>\n<i>(Testni muddatidan avval ham yakunlashingiz mumkin!)</i>", reply_markup=avto_qul2)


@dp.callback_query_handler(text="ortga", state="avto_qul_blok")
async def ortga(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        text="Qanday test tuzmoqchisiz?", reply_markup=tur
    )
    await state.set_state("test_turi")
