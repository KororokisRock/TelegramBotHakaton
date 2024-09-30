1) Создать папку витрульного окружения командой
(в командной строке, находясь в папке TelegramBotHakaton):
python -m venv venv


2) Перед установкой всех нужных библиотек, активировать виртуальную среду командой
(в командной строке, находясь в папке TelegramBotHakaton):
venv\scripts\activate.bat


3) Находясь в витруальном окружении, скачать все библиотеки командой:
pip install -r requirements.txt


4) создать файл .env в этих папках (относительно главной директории):
Web_site\kai_rating\
Web_site\accounts\
TGBot\


5) Вписать в эти файлы:
переменные окружения

 
6) Запустить телеграмм бота:
py TG_bot/telegram_bot.py


7) Запустить локальный сервер:
py web_site/kai_rating/manage.py runserver



