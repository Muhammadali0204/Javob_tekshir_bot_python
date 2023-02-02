from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🖌Test tuzish"),
            KeyboardButton(text="🟢Testga javob berish")
        ],
        [
            KeyboardButton(text = "📋Mening testlarim"),
            KeyboardButton(text = "👤Men haqimda")
        ],
        [
            KeyboardButton(text = "🗞Botdan foydalanish"),
            KeyboardButton(text = "🛠Sozlamalar")
        ],
        [
            KeyboardButton(text="💬Adminga murojaat"),
            KeyboardButton(text="🧮Bot statistikasi")
        ]
    ],
    resize_keyboard=True
)