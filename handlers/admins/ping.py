import time
from aiogram import types
from loader import dp
from data.config import ADMINS


@dp.message_handler(user_id=ADMINS, commands="ping")
async def ping_command_handler(msg: types.Message):
    t1 = time.time()
    m: types.Message = await msg.reply("Pong") 
    t2 = time.time()
    ping = round((t2-t1) / 1000)
    await m.edit(f"PING: {ping} ms")
    