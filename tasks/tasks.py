import asyncio
import logging
import os

from celery import Celery
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from tasks.db_updater import DatabaseUpdater
from tasks.parser import MenuParser

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

FILE_PATH = "/menu_app_FastApi/admin/Menu.xlsx"


async def update_db_async(
    session: AsyncSession,
):
    menu_parser = MenuParser(FILE_PATH)
    menu_data = menu_parser.parse()

    loader = DatabaseUpdater(menu_data, session=session)
    await loader.add_menu_items(menu_data)
    del menu_parser


@celery.task(
    default_retry_delay=15,
    max_retries=None,
)
def update_db():
    try:
        session = db_helper.get_scoped_session()
        asyncio.get_event_loop().run_until_complete(update_db_async(session))

    except Exception as error:
        logging.error(error)
        raise error
    finally:
        update_db.retry()
