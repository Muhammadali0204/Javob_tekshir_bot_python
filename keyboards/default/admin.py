from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_key = ReplyKeyboardMarkup(
    row_width=2,resize_keyboard=True
)
admin_key.insert(KeyboardButton(text="Barcha foydalanuvchilar"))
admin_key.insert(KeyboardButton(text="Id bilan topish"))
admin_key.insert(KeyboardButton(text="Tt test kodi bn"))
admin_key.insert(KeyboardButton(text="Test kodi"))
admin_key.insert(KeyboardButton(text="Foydalanuvchiga xabar"))
admin_key.insert(KeyboardButton(text="Reklama"))
# admin_key.insert(KeyboardButton(text="Barcha foydalanuvchilar"))