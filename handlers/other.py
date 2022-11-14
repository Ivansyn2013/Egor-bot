import json
import string

from aiogram import types
from aiogram.dispatcher import Dispatcher

from create_obj import  bot
from keybords import kb_client


#@dp.message_handler()
async def cenz_filter(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
        message.text.split(' ')}.intersection(
        set(json.load(open('cenz\cenz.json')))) != set():
        await message.reply("Мат запрещен")
        await message.delete()


async def test_mes(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Привет! Егор большой борец за здоровье нас и нашей планеты, '
                           'он попросил меня помочь ему снизить выделение парниковых '
                           'газов!\nВот что я могу:\n'
                           'набери /moderator\n'
                           'Load для загрузки инфрмации , напиши отмена чтобы выйти\n'
                           'Show для показа того что есть',
                           reply_markup=kb_client)
    print('Есть сообщение')
    print(message.text)
    with open("log.txt", 'a+', encoding='utf-8') as f:
        f.write(message.date.ctime())
        f.write(message.from_user.username)
        f.write(f': {message.text}')
        f.write('\n')


# @dp.message_handler() эхо
# async def echo_send(message: types.Message):
#     await message.answer(message.text)
#     await message.reply(message.text)
#     await bot.send_message(message.from_user.id, message.text)

#dp.register_message_handler(test_mes)

def register_handlers_other(dp: Dispatcher):
    # dp.register_message_handler(echo_send)
    dp.register_message_handler(test_mes)
