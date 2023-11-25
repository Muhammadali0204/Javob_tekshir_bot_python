from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def test_listt_oddiy(test_list_oddiy):
    listt = InlineKeyboardMarkup(row_width=1)
    for oddiy in test_list_oddiy:
        listt.insert(
            InlineKeyboardButton(text=f"{oddiy[1]}-{oddiy[2]}", callback_data=oddiy[1])
        )
    listt.insert(InlineKeyboardButton(text="◀️Ortga", callback_data="ortga"))

    return listt


def test_listt_blok(test_list_blok):
    listt = InlineKeyboardMarkup(row_width=1)
    for blok in test_list_blok:
        soni = len(blok[2].split(","))
        listt.insert(
            InlineKeyboardButton(
                text=f"{blok[1]} - {soni} ta fan", callback_data=blok[1]
            )
        )
    listt.insert(InlineKeyboardButton(text="◀️Ortga", callback_data="ortga"))

    return listt
