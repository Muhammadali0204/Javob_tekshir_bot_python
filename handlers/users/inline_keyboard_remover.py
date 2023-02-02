from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from loader import dp

@dp.callback_query_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE) ,state='*')
async def remove(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()