from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

minutlar  = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="0️⃣0️⃣", callback_data="00"),
            InlineKeyboardButton(text="1️⃣0️⃣", callback_data="10")
        ],
        [
            InlineKeyboardButton(text="2️⃣0️⃣", callback_data="20"),
            InlineKeyboardButton(text="3️⃣0️⃣", callback_data="30")
        ],
        [
            InlineKeyboardButton(text="4️⃣0️⃣", callback_data="40"),
            InlineKeyboardButton(text="5️⃣0️⃣", callback_data="50")
        ]
    ]
)