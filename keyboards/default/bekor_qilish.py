from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


bekor_qil = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌Bekor qilish")]], resize_keyboard=True
)

fanlar_soni = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="2️⃣"), KeyboardButton(text="3️⃣")],
        [KeyboardButton(text="4️⃣"), KeyboardButton(text="5️⃣")],
        [KeyboardButton(text="❌Bekor qilish")],
    ],
    resize_keyboard=True,
)
