from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

tasdiq_keyboard  = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text = "❌", callback_data="no"), InlineKeyboardButton(text = "✅", callback_data="yes")
    ],
])