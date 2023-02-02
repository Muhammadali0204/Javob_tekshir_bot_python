from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def test_owner(test_kodi):
    ega = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Natijalarni ko`rish", callback_data=f"natija:{test_kodi}")
            ],
            [
                InlineKeyboardButton(text="Bu testni tugatish", callback_data=f"tugatish:{test_kodi}")
            ]
        ]
    )
    return ega