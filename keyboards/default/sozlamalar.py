from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

sozlama_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="♻️Ismni tahrirlash"),
            KeyboardButton(text="⬆️Limitlarni oshirish")
        ],
        [
            KeyboardButton(text="🖇Bog'langan kanal"),
            KeyboardButton(text="◀️Ortga")
        ]
    ], resize_keyboard=True
)