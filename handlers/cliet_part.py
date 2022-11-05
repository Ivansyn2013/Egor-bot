from aiogram import types
from aiogram import Dispatcher
from create_obj import bot, dp


async def test_mes(message: types.Message):
    print('Есть сообщение')
    print(message.text)

# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет обжорам!!!')
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


# не знаю почему, но так работает, во всяком случае на python 3.7
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
