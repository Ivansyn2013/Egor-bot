import logging

import os
import sys

from mysql.connector import connect
from features import CustomFilter
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # хранилище в ОП
from aiogram.dispatcher import Dispatcher
from aiogram import types
from dotenv import load_dotenv
from aiogram.contrib.middlewares.logging import LoggingMiddleware, LoggingFilter

load_dotenv()
storage = MemoryStorage()
bot = Bot(token=os.getenv("TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
my_logger = logging.getLogger(__name__)
my_logger.addHandler(logging.StreamHandler(sys.stdout))
my_logger.addFilter(CustomFilter())

dp.middleware.setup(LoggingMiddleware(logger=my_logger))




try:
    db_test_connect = connect(host=os.getenv('DB_HOST'),
                              port=os.getenv('DB_PORT'),
                              user=os.getenv('MYSQL_USER'),
                              password=os.getenv('MYSQL_PASSWORD'),
                              database=os.getenv('MYSQL_DATABASE'),
                              ).is_connected()

except Exception as e:
    print('Error in db connecting')
    print(e)
    db_test_connect = None