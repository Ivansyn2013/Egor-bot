import logging

import os
import sys

from mysql.connector import connect
from features import CustomFilter
from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage  # хранилище в ОП
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import types
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram import Router

load_dotenv()
storage = MemoryStorage()
bot = Bot(token=os.getenv("TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()
dp.include_router(router)
if os.getenv('DEBUG'):
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s %(message)s")
else:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
my_logger = logging.getLogger(__name__)
my_logger.addHandler(logging.StreamHandler(sys.stdout))
my_logger.addFilter(CustomFilter())

#dp.middleware.setup(LoggingMiddleware(logger=my_logger))




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