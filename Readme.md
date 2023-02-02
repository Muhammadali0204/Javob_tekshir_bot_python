# Javob tekshir bot (python)

## O'rnatish

Clonlab olish
```shell
$ git clone https://github.com/Muhammadali0204/Javob_tekshir_bot_python
```

Virtual muhit o'rnatish
```shell
$ python3 -m pip install virtualenv
```
Agar bu ishlamasa:
```shell
$ sudo apt install python3-venv
```

Virtual muhit sozlash
```shell
$ python3 -m venv venv
```

Virtual muhitga kirish
```shell
$ source venv/bin/activate
```

Kerakli kutubxonalarni o'rnatish
```shell
$ pip install -r requirements.txt
```

`.env` fayl yaratish
```shell
$ cp .env.dist .env
```

`.env` fayliga kirib bot tokeni va boshqa parametrlarni sozlash
```shell
$ nano .env
```


## Dasturni ishga tushirish
```shell
$ python app.py
```

## Deploy (har doim ishga tushadigan qilib qo'yish)

Servis faylni nusxalash
```shell
$ sudo cp testbot.service /etc/systemd/system/
```

Servis fayllarni yangilash
```shell
$ sudo systemctl daemon-reload
```
Bot servis fayliga ruxsat berish
```shell
$ sudo systemctl enable testbot
```

Bot servis faylini ishga tushirish
```shell
$ sudo systemctl start testbot.service
```

Servis fayl statusini ko'rish
```shell
$ sudo systemctl status testbot.service
```

Servis faylni  o'chirish
```shell
$ sudo systemctl stop testbot.service
```

Servis faylni perezagruzka qilish
```shell
$ sudo systemctl restart testbot.service
```
