from aiogram import types
from aiogram.types import Message
from loader import dp, bot
import asyncio


@dp.message_handler(
    state=["avto_qul_oddiy", "avto_qul_blok"], content_types=types.ContentTypes.ANY
)
async def iye(msg: Message):
    await msg.delete()
    await msg.answer("<b>Yuqoridagi tugmalardan foydalaning 👆</b>")
    await asyncio.sleep(3)
    await bot.delete_message(msg.from_user.id, msg.message_id + 1)
