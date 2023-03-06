from loader import dp, db_ts
from keyboards.default.admin import admin_key
from keyboards.default.bekor_qilish import bekor_qil
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from aiogram import types


@dp.message_handler(text="Test haqida ma'lumot", chat_id = ADMINS)
async def admin(msg : types.Message, state : FSMContext):
    await msg.answer(text="<b>Test kodini yuboring : </b>", reply_markup=bekor_qil)
    await state.set_state("tt_test_kodi")
    
    
@dp.message_handler(state="tt_test_kodi", chat_id = ADMINS)
async def admin(msg : types.Message, state : FSMContext):
    
    test_oddiy = db_ts.select_test_oddiy_by_test_kodi(msg.text)
    test_blok = db_ts.select_test_blok_by_test_kodi(msg.text)
    if test_oddiy != None:
        pass
    elif test_blok != None:
        pass
    else:
        await msg.answer("<b>Bunday test mavjud emas</b>", reply_markup=admin_key)
        
    await state.finish()