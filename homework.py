import os
import sys
import time

import requests
import logging

from dotenv import load_dotenv
from logging import StreamHandler
from telegram import Bot
from requests.exceptions import RequestException

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

bot = Bot(token=TELEGRAM_TOKEN)


def parse_homework_status(homework):
    homework_name = homework.get('lesson_name')
    if homework_name is None:
        logging.error('Can not get "lesson_name".')
        return 'Ошибка. Не удается получить значение "lesson_name".'
    if homework.get('status') is None:
        logging.error('Can not get "status".')
        return 'Ошибка. Не удается получить значение "status".'
    status = homework.get('status')
    comment_reviewer = homework.get('reviewer_comment')
    comment = f'Комментарий ревьюера: "{comment_reviewer}"'
    if comment_reviewer is None:
        comment = 'Ревьюер не оставил комментариев по вашей работе.'
    all_homework_name = {
        'rejected': f'У вас проверили работу "{homework_name}"!\n\n'
                    f'К сожалению в работе нашлись ошибки.\n\n{comment}',
        'reviewing': f'Ваша работа {homework_name} проходит ревью',
        'approved': f'У вас проверили работу "{homework_name}"!\n\n'
                    'Ревьюеру всё понравилось, можно '
                    f'приступать к следующему уроку.\n\n{comment}',
    }
    check_homework = all_homework_name.get(status)
    if check_homework is None:
        logging.error('Undefined status homework')
        return error_description('Неизвестный статус работы')
    return check_homework


def get_homework_statuses(current_timestamp):
    if current_timestamp is None:
        current_timestamp = int(time.time())

    try:
        homework_statuses = requests.get(
            'https://praktikum.yandex.ru/api/user_api/homework_statuses/',
            params={'from_date': current_timestamp},
            headers={'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
        )
    except RequestException as e:
        logging.exception("Exception occurred")
        send_message(error_description(e), bot)
        return {}

    try:
        return homework_statuses.json()
    except ValueError as e:
        logging.exception("Exception occurred")
        send_message(error_description(e), bot)
        return {}


def send_message(message, bot_client):
    return bot_client.send_message(chat_id=CHAT_ID, text=message)


def error_description(error):
    return f'Бот столкнулся с ошибкой: {error}'


def main():

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)

    current_timestamp = int(time.time())
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(
                    new_homework.get('homeworks')[0]), bot)
                logging.info('Message sent')
            current_timestamp = new_homework.get(
                'current_date', current_timestamp)
        except Exception as e:
            logging.exception("Exception occurred")
            send_message(error_description(e), bot)
        time.sleep(300)


if __name__ == '__main__':
    main()
