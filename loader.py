from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api import sqlite
from data import config
from datetime import datetime

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_users = sqlite.Database("data/Users.db")
db_ts = sqlite.Database("data/Tuzilgan_savollar.db")
db_bj = sqlite.Database("data/Berilgan_javoblar.db")
Vaqt = datetime(2023, 1, 1, 0, 0, 0)
users = db_users.select_all_users()
premium_narxi = ""
try:
    premium_narxi = db_users.select_premium_narxi()[0]
    limits = db_users.select_limits_oddiy()
    listt = limits[2].split(",")
    Limitlar_oddiy = [int(listt[0]), int(listt[1]), int(listt[2]), int(listt[3])]
    foydalanuvchi_limitlari_oddiy = {}

    for i in range(0, len(users)):
        if users[i][3] == "0" or users[i][3] == "-1":
            foydalanuvchi_limitlari_oddiy[users[i][0]] = [
                Limitlar_oddiy[0],
                Limitlar_oddiy[1],
            ]
        else:
            foydalanuvchi_limitlari_oddiy[users[i][0]] = [
                Limitlar_oddiy[2],
                Limitlar_oddiy[3],
            ]
except Exception as e:
    print(e)

try:
    limits_blok = db_users.select_limits_blok()
    listt_blok = limits_blok[2].split(",")
    Limitlar_blok = [
        int(listt_blok[0]),
        int(listt_blok[1]),
        int(listt_blok[2]),
        int(listt_blok[3]),
    ]
    foydalanuvchi_limitlari_blok = {}
    for i in range(0, len(users)):
        if users[i][3] == "0" or users[i][3] == "-1":
            foydalanuvchi_limitlari_blok[users[i][0]] = [
                Limitlar_blok[0],
                Limitlar_blok[1],
            ]
        else:
            foydalanuvchi_limitlari_blok[users[i][0]] = [
                Limitlar_blok[2],
                Limitlar_blok[3],
            ]
except Exception as e:
    print(e)
temp_data = {}
vaqt_junat = False
kitoblar = ["📕", "📗", "📘", "📙", "📗"]
kanallar = db_users.kanallar()[0].split(",")
