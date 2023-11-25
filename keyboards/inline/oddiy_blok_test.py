from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

oddiy_blok = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📕Oddiy test", callback_data="oddiy")],
        [InlineKeyboardButton(text="📚Blok test", callback_data="blok")],
        [InlineKeyboardButton(text="◀️Ortga", callback_data="ortga")],
    ]
)
