import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # хранилище в ОП
from aiogram.dispatcher import Dispatcher
from aiogram import types

storage = MemoryStorage()
bot = Bot(token=os.getenv("TOKEN"),parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
