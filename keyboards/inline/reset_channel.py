from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

reset_channel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="♻️O'zgartirish", callback_data="qayta_kanal_kiritish"),
        ],
        [
            InlineKeyboardButton(text="🔴Kanal/guruhni o'chirish", callback_data="kanal/guruhni_ochirish")
        ]
    ]
)