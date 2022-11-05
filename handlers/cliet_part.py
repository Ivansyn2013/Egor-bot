from aiogram import types
from aiogram import Dispatcher
from create_obj import bot, dp
from keybords import kb_client

async def test_mes(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Привет! Егор большой борец за здоровье нас и нашей планеты, '
                           'он попросил меня помочь ему снизить выделение парниковых '
                           'газов!\nВот что я могу:',
                           reply_markup=kb_client)
    print('Есть сообщение')
    print(message.text)
    with open("log.txt", 'a+', encoding='utf-8') as f:
        f.write(message.from_user.username)
        f.write(f': {message.text}')
        f.write('\n')

# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,
                               'Привет обжорам!!!',
                               reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Напишите боту в ЛС')


# @dp.message_handler(commands=['Поиск'])
async def command_search(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пошел поиск')


# @dp.message_handler(commands=['Авторизация'])
async def command_author(message: types.Message):
    await bot.send_message(message.from_user.id, 'Кнопки с аторизацией')


# @dp.message_handler()
async def echo_send(message: types.Message):
    await message.answer(message.text)
    await message.reply(message.text)
    await bot.send_message(message.from_user.id, message.text)


# не знаю почему, но так работает, во всяком случае на python 3.7 и на 10 тоже
dp.register_message_handler(command_start, commands=['start', 'help'])
dp.register_message_handler(command_author, commands=['Авторизация'])
dp.register_message_handler(command_search, commands=['Поиск'])
dp.register_message_handler(test_mes)

# не знаю нужно ли так
def register_handlers_client(dp: Dispatcher):

    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_author, commands=['Авторизация'])
    dp.register_message_handler(command_search, commands=['Поиск'])
    dp.register_message_handler(test_mes)
