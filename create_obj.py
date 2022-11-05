from aiogram import Bot
from aiogram import Dispatcher
import os


bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)
