from aiogram import types, filters

from loader import dp, db_bj

@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), text="🗞Botdan foydalanish")
async def myanswers(msg : types.Message):
    pass