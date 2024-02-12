import logging
import os

from celery import Celery
from dotenv import load_dotenv

# from core.rabbitmq.rabbitmq_healper import rabbitmq
from tasks.db_updater import MenuLoader
from tasks.parser import MenuParser, menu_parser

load_dotenv()

RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")
RABBITMQ_DEFAULT_PORT = os.getenv("RABBITMQ_DEFAULT_PORT")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

CELERY_STATUS = os.getenv("CELERY_STATUS")


celery = Celery(
    "tasks",
    broker=(
        f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@"
        f"{RABBITMQ_HOST}:{RABBITMQ_DEFAULT_PORT}"
    ),
)


@celery.task(
    default_retry_delay=15,
    max_retries=None,
)
def update_db():
    try:
        FILE_PATH = "/menu_app_FastApi/admin/Menu.xlsx"
        # Создаем парсер и получаем JSON-объект с данными о меню
        parser = MenuParser(FILE_PATH)
        menu_json = parser.to_json()

        # Создаем загрузчик и загружаем данные в базу данных
        loader = MenuLoader(menu_json)
        loader.load_menu_to_db()

    except Exception as error:
        logging.error(error)
        raise error
