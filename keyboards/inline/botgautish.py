from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

botga = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🤖Botga o`tish", url="https://t.me/Javob_tekshir_admin_bot"
            )
        ]
    ]
)

botga2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🆓Sinab ko'rish", callback_data="10_kunga_sinash")],
        [
            InlineKeyboardButton(
                text="🏆1 oyga obuna bo'lish",
                url="https://t.me/Javob_tekshir_admin_bot?start=premium",
            ),
        ],
    ]
)

botga3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🤖Botga o`tish",
                url="https://t.me/Javob_tekshir_admin_bot?start=premium",
            )
        ]
    ]
)

kanal_qushish = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🆕Kanal bog'lash", callback_data="kanal_qushish")],
        [
            InlineKeyboardButton(
                text="🚫Kanal bog'lamayman", callback_data="atmen_kanal"
            ),
        ],
    ]
)

kanal_guruh = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ommaviy kanal", callback_data="okanal")],
        [InlineKeyboardButton(text="Shaxsiy kanal", callback_data="skanal")],
        [
            InlineKeyboardButton(text="Ommaviy/Shaxsiy guruh", callback_data="oguruh"),
        ],
        [
            InlineKeyboardButton(
                text="❌Bekor qilish", callback_data="xullas_atem_kanal"
            ),
        ],
    ]
)

kanalga_qush = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕Kanalga qo'shish",
                url="https://t.me/javob_tekshir_bot?startchannel",
            )
        ],
        [InlineKeyboardButton(text="Tayyor✅", callback_data="tayyor")],
        [InlineKeyboardButton(text="❌Bekor qilish", callback_data="xullas_atem_kanal")],
    ]
)


def guruhga_start(id):
    guruhga_start123 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Guruhni tanlash",
                    url=f"https://t.me/javob_tekshir_bot?startgroup={id}",
                )
            ],
            [InlineKeyboardButton(text="Tayyor✅", callback_data="tayyor_guruh")],
            [InlineKeyboardButton(text="❌Bog'lanmadi", callback_data="boglanmadi")],
        ]
    )

    return guruhga_start123
