import io

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from PIL import Image, ImageFile

from io import BytesIO
from create_obj import bot
from keybords import kb_search, kb_client
from sql_bd import sql_read
from acces_reader import db_mysql_request

ImageFile.LOAD_TRUNCATED_IMAGES = True

class FSMSearch(StatesGroup):
    fs_search = State()


def png_convert(img):
    with BytesIO() as f:
        img.save(f, format='JPEG')
        return f.getvalue()

# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,
                               'Привет обжорам!!!\n'
                               'https://mastergroosha.github.io/aiogram-3-guide/fsm/ ',
                               reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Напишите боту в ЛС')


# @dp.message_handler(commands=['Поиск'])
async def command_search(message: types.Message):
    await bot.send_message(message.from_user.id, 'Поиск продуктов',
                           reply_markup=kb_search)


# commands=['Искать']
async def start_searching(message: types.Message):
    await FSMSearch.fs_search.set()
    await message.reply('Введи название продукта')


async def search_go_to_db(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['search_text'] = message.text

        res = db_mysql_request(data['search_text'])
        print(data['search_text'])
        await bot.send_message(message.from_user.id,
                               'Ищу')
        if res is None:
            await bot.send_message(message.from_user.id,
                                   'Ничего не нашел')


        image_data = res['image'][0]
        #image = Image.open(io.BytesIO(image_data))

        print(res.keys())

        await message.delete()

        await bot.send_photo(message.from_user.id,
                             image_data,
                             f'{res["Название продукта"][0]}\n'
                             f'{res["Цвет"][0]}{res["high low medium"]}'
                             f'{res["Цвет"][0]}\n'
                             f'{res["Доза"]}\n'
                             f'Фруктоза {res["Цвет"]} {res["Фруктаны"]}\n'
                             f'{res["Порция"]}')
        await state.finish()


async def cancel_search_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        print('Команда отмены возврат')
        return
    await state.finish()
    await message.reply('Команда отмены: ok')


# @dp.message_handler(commands=['Авторизация'])
async def command_author(message: types.Message):
    await bot.send_message(message.from_user.id, 'Кнопки с аторизацией')


# @dp
async def command_show(message: types.Message):
    await sql_read(message)


# не знаю почему, но так работает, во всяком случае на python 3.7 и на 10 тоже
# dp.register_message_handler(command_start, commands=['start', 'help'])
# dp.register_message_handler(command_author, commands=['Авторизация'])
# dp.register_message_handler(command_search, commands=['Поиск'])
# dp.register_message_handler(command_show, commands='Show')
# dp.register_message_handler(test_mes)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_author, commands=['Авторизация'])
    dp.register_message_handler(command_search, commands=['Поиск'])
    dp.register_message_handler(command_show, commands='Show')
    dp.register_message_handler(start_searching, commands='Искать')
    dp.register_message_handler(search_go_to_db, state=FSMSearch.fs_search)
    dp.register_message_handler(cancel_search_handler, commands='Выйти из поиска',
                                state='*')
