from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

info = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="ℹ️Info", callback_data="info_test_turi"),
        ]
    ]
)