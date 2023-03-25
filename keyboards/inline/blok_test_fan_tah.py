from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def blok_test_fanlar(data, test_kodi):
    fanlar = InlineKeyboardMarkup(
        row_width=1
    )
    for i in range(0, len(data)):
        fanlar.insert(InlineKeyboardButton(text=data[i], callback_data=f"{test_kodi}:{i}:{data[i]}"))
        
    fanlar.insert(InlineKeyboardButton(text="◀️Ortga", callback_data="ortga"))
    
    return fanlar