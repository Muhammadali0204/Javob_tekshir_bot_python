from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


boshlash = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Javob yuborishni boshlash➡️", callback_data="javob_yuborishni_boshla")
        ],
        [
            InlineKeyboardButton(text="Bekor qilish❌", callback_data="javob_yuborishni_bekor_qil")
        ]
    ]
)