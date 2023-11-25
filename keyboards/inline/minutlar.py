from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

minutlar = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="0️⃣0️⃣", callback_data="00"),
        ],
        [InlineKeyboardButton(text="3️⃣0️⃣", callback_data="30")],
    ]
)
