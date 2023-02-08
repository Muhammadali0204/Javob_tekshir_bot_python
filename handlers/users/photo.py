from aiogram import types
from aiogram.types import Message
from loader import dp

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def salom(msg : types.Message):
    print(msg.photo[-1].file_id)