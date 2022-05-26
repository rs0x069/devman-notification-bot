import logging
import os
import requests
import time

from dotenv import load_dotenv

from telegram_logger import TelegramLogsHandler


def main():
    load_dotenv()

    devman_token = os.getenv("DEVMAN_TOKEN")
    telegram_api = os.getenv("TELEGRAM_API")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': devman_token
    }
    requests_params = {}

    logger = logging.getLogger("Logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(telegram_api, int(telegram_chat_id)))
    logger.info('Bot is started')

    while True:
        try:
            response = requests.get(url, headers=headers, timeout=60, params=requests_params)
            response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError as err:
            logger.error(err)
            time.sleep(1)
        except requests.exceptions.HTTPError as err:
            logger.error(err)
            time.sleep(1)
        else:
            lesson_checking = response.json()
            lesson_status = lesson_checking['status']

            if lesson_status == 'timeout':
                timestamp = lesson_checking['timestamp_to_request']
                requests_params = {'timestamp': timestamp}
            elif lesson_status == 'found':
                last_attempt = lesson_checking['new_attempts'][0]
                lesson_title = last_attempt['lesson_title']
                lesson_is_negative = last_attempt['is_negative']
                lesson_url = last_attempt['lesson_url']
                message_title = f'У вас проверили работу "{lesson_title}"'

                if lesson_is_negative:
                    message_body = (
                        f'{message_title}\n\n'
                        f'К сожалению, в работе нашлись ошибки\n\n'
                        f'{lesson_url}'
                    )
                else:
                    message_body = (
                        f'{message_title}\n\n'
                        f'Преподавателю всё понравилось, можно приступать к следующему уроку!\n\n'
                        f'{lesson_url}'
                    )

                logger.info(message_body)

                timestamp = lesson_checking['last_attempt_timestamp']
                requests_params = {'timestamp': timestamp}
            else:
                print('Status:', lesson_status)


if __name__ == '__main__':
    main()
