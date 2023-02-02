from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def channels_keyboard(kanallar, holat):
    channels = InlineKeyboardMarkup(row_width=1)
    for i in range(0, len(kanallar)):
        channels.insert(InlineKeyboardButton(text=f"{i+1} - KANAL", url=kanallar[i]))
    channels.insert(InlineKeyboardButton(text="Tekshirish✅", callback_data=f"obunani_tekshir:{holat}"))
    return channels
