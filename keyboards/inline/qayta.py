from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

qayta = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔵Qayta", callback_data="qayta_vaqt_kiritish"),
        ],
        [
            InlineKeyboardButton(
                text="🔴Test tuzishni bekor qilish", callback_data="test_atmen"
            )
        ],
    ]
)
