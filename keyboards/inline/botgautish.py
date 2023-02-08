from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

botga = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🤖Botga o`tish", url="https://t.me/Javob_tekshir_admin_bot")
        ]
    ]
)

botga2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🆓Sinab ko'rish", callback_data="10_kunga_sinash")
        ],
        [
            InlineKeyboardButton(text="🏆1 oyga obuna bo'lish", url="https://t.me/Javob_tekshir_admin_bot"),
        ]
    ]
)

kanal_qushish = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🆕Kanal qo'shish", callback_data="kanal_qushish")
        ],
        [
            InlineKeyboardButton(text="🚫Kanal qo'shmayman", callback_data="atmen_kanal"),
        ]
    ]
)

kanal_guruh = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ommaviy Kanal", callback_data="okanal")
        ],
        [
            InlineKeyboardButton(text="Shaxsiy Kanal", callback_data="skanal")
        ],
        [
            InlineKeyboardButton(text="Ommaviy Guruh", callback_data="oguruh"),
        ],
        [
            InlineKeyboardButton(text="Shaxsiy Guruh", callback_data="sguruh"),
        ],
        [
            InlineKeyboardButton(text="❌Bekor qilish", callback_data="xullas_atem_kanal"),
        ]
    ]
)

kanalga_qush = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Tayyor✅", callback_data="tayyor")
        ],
        [
            InlineKeyboardButton(text="❌Bekor qilish", callback_data="xullas_atem_kanal")
        ],
        
    ]
)