from aiogram import types, filters
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from utils.misc.isbelgi import isbelgi
from data.config import ADMINS
from loader import dp, bot, db_users, foydalanuvchi_limitlari_oddiy, foydalanuvchi_limitlari_blok, Limitlar_oddiy, Limitlar_blok
from keyboards.default.menu import menu

@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.PRIVATE))
async def bot_start(message: types.Message, state : FSMContext):
    try:
        data = db_users.select_user_id(message.from_user.id)
        if data == None:
            db_users.add_user(message.from_user.id, message.from_user.full_name, message.from_user.username, 0, None)
            foydalanuvchi_limitlari_oddiy[message.from_user.id] = [Limitlar_oddiy[0], Limitlar_oddiy[1]]
            foydalanuvchi_limitlari_blok[message.from_user.id] = [Limitlar_oddiy[0], Limitlar_oddiy[1]]
            await state.set_state("ism")
            await message.answer(f"👋<b>Salom, <i>{message.from_user.get_mention(message.from_user.full_name)}</i>\nXush kelibsiz❗️</b>")
            await message.answer("✍️<i>Ism familiyangizni kiriting : </i>\n")
        else:
            await message.answer(f"<b>👋Salom, <i>{message.from_user.get_mention(message.from_user.full_name)}</i></b>")
            await message.answer("<b><i>📋Menu : </i></b>", reply_markup=menu)
            db_users.update_username(message.from_user.id, message.from_user.username)
    except Exception as e: 
        print(e)
        
        

@dp.message_handler(state="ism")
async def ism(msg : types.Message, state : FSMContext):
    if len(msg.text) > 2 and all(x.isalpha() or x.isspace() or isbelgi(x) for x in msg.text):
        db_users.update_user_name(msg.from_user.id, msg.text)
        await msg.answer("🎉<b>Tabriklaymiz!\nBotdan foydalanishingiz mumkin!</b>😊")
        await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu)
        await state.finish()
        await bot.send_message(ADMINS[0], f"<b>Yangi foydalanuvchi qo`shildi,</b> <i>{msg.from_user.get_mention(msg.text)}</i>")
    else:
        await msg.answer("<b>Iltimos ism kiriting.</b>")
        
@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.SUPERGROUP))
async def bot_start(message: types.Message):
    await message.reply("<b>Bu bot faqat shaxsiy chatda ishlaydi❗️</b>")