from aiogram import types, filters
from keyboards.default.bekor_qilish import bekor_qil
from keyboards.inline.inline_ha_yoq import tasdiq_keyboard
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from keyboards.inline import oddiy_blok_test, test_list
from keyboards.default import ortga, menu
from keyboards.inline.test_egasiga import test_owner
from loader import dp, db_users, db_bj, db_ts, bot
import asyncio


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), text="📋Mening testlarim")
async def mytest(msg: types.Message, state: FSMContext):
    await msg.answer("📋Mening testlarim", reply_markup=types.ReplyKeyboardRemove())
    await msg.answer("<b>Test turini tanlang 👇</b>", reply_markup=oddiy_blok_test.oddiy_blok)
    await state.set_state("my_tests")


@dp.message_handler(state=['my_tests', 'my_tests_blok', 'my_tests_oddiy'], content_types=types.ContentTypes.ANY)
async def func(msg: types.Message):
    await msg.delete()
    await msg.answer("<b>Yuqoridagi tugmalardan foydalaning 👆</b>")
    await asyncio.sleep(3)
    await bot.delete_message(msg.from_user.id, msg.message_id + 1)


@dp.callback_query_handler(text="oddiy", state="my_tests")
async def my_tests_oddiy(call: types.CallbackQuery, state: FSMContext):
    tests_oddiy = db_ts.select_tests_by_user_id_oddiy(call.from_user.id)

    if tests_oddiy == []:
        await call.answer("Sizda faol oddiy testlar mavjud emas ❎", show_alert=True)
        await call.message.delete()
        await call.message.answer("<b>Sizda faol oddiy testlar mavjud emas ❎</b>")
        await call.message.answer("<b>Test turini tanlang 👇</b>", reply_markup=oddiy_blok_test.oddiy_blok)
        await state.set_state("my_tests")
    else:
        await call.message.delete()
        await call.message.answer("<b>📕Oddiy testlar : </b>", reply_markup=test_list.test_listt_oddiy(tests_oddiy))
        await state.set_state("my_tests_oddiy")


@dp.callback_query_handler(text="blok", state="my_tests")
async def my_tests_blok(call: types.CallbackQuery, state: FSMContext):
    tests_blok = db_ts.select_tests_by_user_id_blok(call.from_user.id)
    if tests_blok == []:
        await call.answer("Sizda faol blok testlar mavjud emas ❎", show_alert=True)
        await call.message.delete()
        await call.message.answer("<b>Sizda faol blok testlar mavjud emas ❎</b>")
        await call.message.answer("<b>Test turini tanlang 👇</b>", reply_markup=oddiy_blok_test.oddiy_blok)
        await state.set_state("my_tests")
    else:
        await call.message.delete()
        await call.message.answer("<b>📚Blok testlar : </b>", reply_markup=test_list.test_listt_blok(tests_blok))
        await state.set_state("my_tests_blok")


@dp.callback_query_handler(text="ortga", state="my_tests")
async def ortga(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
    await state.finish()


@dp.callback_query_handler(state=['my_tests_oddiy', 'my_tests_blok'], text="ortga")
async def ortgaa(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Tanlang 👇</b>", reply_markup=oddiy_blok_test.oddiy_blok)
    await state.set_state("my_tests")
