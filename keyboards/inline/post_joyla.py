from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def post(test_kodi, test_turi):
    post_joylash  = InlineKeyboardMarkup(
        inline_keyboard=[
        [
            InlineKeyboardButton(text = "❌", callback_data=f"yuq:{test_turi}:{test_kodi}"), InlineKeyboardButton(text = "✅", callback_data=f"ha:{test_turi}:{test_kodi}")
        ],
    ])
    
    return post_joylash