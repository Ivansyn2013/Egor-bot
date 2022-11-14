import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # хранилище в ОП
from aiogram.dispatcher import Dispatcher

storage = MemoryStorage()
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)
