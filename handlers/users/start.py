from aiogram import types, filters
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from utils.misc.isbelgi import isbelgi
from data.config import ADMINS
from loader import (
    dp,
    bot,
    db_users,
    foydalanuvchi_limitlari_oddiy,
    foydalanuvchi_limitlari_blok,
    Limitlar_oddiy,
    Limitlar_blok,
    temp_data,
)
from keyboards.default.menu import menu


@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.PRIVATE))
async def bot_start(message: types.Message, state: FSMContext):
    try:
        data = db_users.select_user_id(message.from_user.id)
        if data == None:
            db_users.add_user(
                message.from_user.id,
                message.from_user.full_name,
                message.from_user.username,
                0,
                None,
            )
            foydalanuvchi_limitlari_oddiy[message.from_user.id] = [
                Limitlar_oddiy[0],
                Limitlar_oddiy[1],
            ]
            foydalanuvchi_limitlari_blok[message.from_user.id] = [
                Limitlar_blok[0],
                Limitlar_blok[1],
            ]
            await state.set_state("ism")
            await message.answer(
                f"👋<b>Salom, <i>{message.from_user.get_mention(message.from_user.full_name)}</i>\nXush kelibsiz❗️</b>"
            )
            await message.answer("✍️<i>Ism familiyangizni kiriting : </i>\n")
        else:
            await message.answer(
                f"<b>👋Salom, <i>{message.from_user.get_mention(message.from_user.full_name)}</i></b>"
            )
            await message.answer("<b><i>📋Menu : </i></b>", reply_markup=menu)
            db_users.update_username(message.from_user.id, message.from_user.username)
    except Exception as e:
        print(e)


@dp.message_handler(state="ism")
async def ism(msg: types.Message, state: FSMContext):
    if len(msg.text) > 2 and all(
        x.isalpha() or x.isspace() or isbelgi(x) for x in msg.text
    ):
        db_users.update_user_name(msg.from_user.id, msg.text)
        await msg.answer("🎉<b>Tabriklaymiz!\nBotdan foydalanishingiz mumkin!</b>😊")
        await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu)
        await state.finish()
        await bot.send_message(
            ADMINS[0],
            f"<b>Yangi foydalanuvchi qo`shildi,</b> <i>{msg.from_user.get_mention(msg.text)}</i>",
        )
    else:
        await msg.answer("<b>Iltimos ism kiriting.</b>")


# Chalaaa
@dp.message_handler(
    CommandStart(),
    filters.ChatTypeFilter([types.ChatType.GROUP, types.ChatType.SUPERGROUP]),
)
async def bot_start(msg: types.Message):
    try:
        if temp_data[int(msg.text.split(" ")[1])] == "start_bosadi":
            try:
                admins = await bot.get_chat_administrators(msg.chat.id)
                for admin in admins:
                    if msg.from_user.id == admin["user"]["id"]:
                        name_user = msg.from_user.full_name
                        chat_id = msg.chat.id
                        chat_name = msg.chat.full_name
                        username = msg.chat.username
                        if username:
                            db_users.update_kanal_user(
                                f"{chat_id},{chat_name}(@{username})", msg.from_user.id
                            )
                        else:
                            db_users.update_kanal_user(
                                f"{chat_id},{chat_name}", msg.from_user.id
                            )
                        await msg.reply(
                            f"<b>@Javob_tekshir_bot <u>{name_user}</u> tomonidan <u>{chat_name}</u> guruhiga bog'landi</b>"
                        )
                        return
                await msg.reply("<b>Siz bu guruhda adminstrator emasssiz ❌</b>")
                return
            except Exception as e:
                print(e)
        await msg.reply("<b>Bu bot faqat shaxsiy chatda ishlaydi❗️</b>")
    except:
        await msg.reply("<b>Bu bot faqat shaxsiy chatda ishlaydi</b>")
