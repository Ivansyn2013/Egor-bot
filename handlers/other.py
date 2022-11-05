import json
import string

from aiogram import types
from create_obj import dp, bot
from aiogram.dispatcher import Dispatcher


@dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
        message.text.split(' ') }.intersection(set(json.load(open('cenz\cenz.json')))) != set():
        await message.reply("Мат запрещен")
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
