# Телеграм-бот уведомлений о проверке работ
Бот отправляет уведомления, как только работа будет проверена преподавателем.

## Требования
* Python (3.8, 3.9, 3.10)

### Зависимые модули
* python-dotenv==0.20.0
* python-telegram-bot==13.11
* requests==2.27.1

## Установка
* Создать бота в Телеграм
* Склонировать проект
```commandline
git clone https://github.com/rs0x069/devman-notification-bot.git
```
* Перейти в папку `devman-notification-bot`
* Установить пакеты
```commandline
pip install -r requirements.txt
```
* Создать файл `.env` со следующими переменными окружения:
  + DEVMAN_TOKEN
  + TELEGRAM_API
  + TELEGRAM_CHAT_ID
* Разрешить боту отправлять вам уведомления
* Запустить проект командой:
```commandline
python main.py
```

***
Учебный проект для курсов web-разработчиков [dvmn](https://dvmn.org). 