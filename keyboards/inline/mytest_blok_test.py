from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db_users


def test_list2(test):
    nomm = InlineKeyboardMarkup(row_width=1)
    user = db_users.select_user_id(test[0])

    if test[5].find(".") != -1:
        nomm.insert(
            InlineKeyboardButton(
                text="🔢Javob berganlar soni",
                callback_data=f"javob_berganlar_soni:{test[1]}",
            )
        )
        nomm.insert(
            InlineKeyboardButton(
                text="♻️Fan nomini tahrirlash",
                callback_data=f"fan_nomini_tahrirlash:{test[1]}",
            )
        )

        if test[7] == "0" and user[3] == "0":
            pass
        elif test[7] == "0" and user[3] != "0" and user[4] != None:
            nomm.insert(
                InlineKeyboardButton(
                    text="🟢Kanal/guruhga joylashni yoqish",
                    callback_data=f"kanal_guruh_joylash_yoqish:{test[1]}",
                )
            )
        elif test[7] == "1" and user[4] != None:
            nomm.insert(
                InlineKeyboardButton(
                    text="🔴Kanal/guruhga joylashni o'chirish",
                    callback_data=f"kanal_guruh_joylash_ochirish:{test[1]}",
                )
            )
        nomm.insert(
            InlineKeyboardButton(
                text="🔴Testni yakunlash", callback_data=f"tugatish:{test[1]}"
            )
        )
    else:
        nomm.insert(
            InlineKeyboardButton(
                text="🔢Javob berganlar soni",
                callback_data=f"javob_berganlar_soni:{test[1]}",
            )
        )
        nomm.insert(
            InlineKeyboardButton(
                text="♻️Fan nomini tahrirlash",
                callback_data=f"fan_nomini_tahrirlash:{test[1]}",
            )
        )
        if test[7] == "0" and user[3] != "0" and user[4] != None:
            nomm.insert(
                InlineKeyboardButton(
                    text="🟢Kanal/guruhga joylashni yoqish",
                    callback_data=f"kanal_guruh_joylash_yoqish:{test[1]}",
                )
            )
        elif test[7] == "1" and user[4] != None:
            nomm.insert(
                InlineKeyboardButton(
                    text="🔴Kanal/guruhga joylashni o'chirish",
                    callback_data=f"kanal_guruh_joylash_ochirish:{test[1]}",
                )
            )

        if test[6] == 0:
            nomm.insert(
                InlineKeyboardButton(
                    text="🟢Muddatdan oldin boshlash",
                    callback_data=f"boshlash:{test[1]}",
                )
            )
            nomm.insert(
                InlineKeyboardButton(
                    text="🔴Testni o'chirish", callback_data=f"tugatish:{test[1]}"
                )
            )
        elif test[6] == 1:
            nomm.insert(
                InlineKeyboardButton(
                    text="🔴Muddatdan oldin yakunlash",
                    callback_data=f"tugatish:{test[1]}",
                )
            )

    nomm.insert(InlineKeyboardButton(text="◀️Ortga", callback_data="ortga"))

    return nomm
