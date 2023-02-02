from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

avto_qul = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🦾Avto", callback_data="avto"),
            InlineKeyboardButton(text="💪Manual", callback_data="qul")
        ],
        [
            InlineKeyboardButton(text="ℹ️Info", callback_data="info"),
        ],
        [
            InlineKeyboardButton(text="◀️Ortga", callback_data="ortga")
        ]
    ]
)

avto_qul2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🦾Avto", callback_data="avto"),
            InlineKeyboardButton(text="💪Manual", callback_data="qul")
        ],
        [
            InlineKeyboardButton(text="◀️Ortga", callback_data="ortga")
        ]
    ]
)