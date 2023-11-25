from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

tur = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📘Oddiy test"),
            KeyboardButton("📚Blok test"),
        ],
        [
            KeyboardButton(text="◀️Ortga"),
        ],
    ],
    resize_keyboard=True,
)
