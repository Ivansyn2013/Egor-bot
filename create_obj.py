import os
from mysql.connector import connect

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # хранилище в ОП
from aiogram.dispatcher import Dispatcher
from aiogram import types
from dotenv import load_dotenv

load_dotenv()
storage = MemoryStorage()
bot = Bot(token=os.getenv("TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
try:
    db_test_connect = connect(host=os.getenv('DB_HOST'),
                              port=3300,
                              user='test',
                              password=os.getenv('BD_PASS'),
                              database='egor_db',
                              ).is_connected()
except Exception as e:
    print('Error in db connectind')
    print(e)
