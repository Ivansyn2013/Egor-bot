from aiogram import types
from aiogram import Dispatcher
from create_obj import bot
from keybords import kb_client
from sql_bd import sql_read


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

#@dp
async def command_show(message: types.Message):
    await sql_read(message)




# не знаю почему, но так работает, во всяком случае на python 3.7 и на 10 тоже
# dp.register_message_handler(command_start, commands=['start', 'help'])
# dp.register_message_handler(command_author, commands=['Авторизация'])
# dp.register_message_handler(command_search, commands=['Поиск'])
# dp.register_message_handler(command_show, commands='Show')
#dp.register_message_handler(test_mes)

# не знаю нужно ли так
def register_handlers_client(dp: Dispatcher):

    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_author, commands=['Авторизация'])
    dp.register_message_handler(command_search, commands=['Поиск'])
    dp.register_message_handler(command_show, commands='Show')

