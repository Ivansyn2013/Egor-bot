from difflib import get_close_matches
from io import BytesIO

from PIL import ImageFile
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from acces_reader import db_mysql_request, db_mysql_all_products
from create_obj import bot
from features import get_answer_str
from inline_butn import inline_button_gen
from keybords import kb_search, kb_client
from sql_bd import sql_read

ImageFile.LOAD_TRUNCATED_IMAGES = True


class FSMSearch(StatesGroup):
    fs_search = State()
    option_search = State()


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
            await FSMSearch.option_search.set()
            print (await state.get_state())
        else:
            image_data = res['image'][0]

            # print(res.keys())
            res.pop('image')
            res.pop('Картинка')
            # print(res.keys())
            print(res.items())

            await message.delete()

            await bot.send_photo(message.from_user.id,
                                 image_data,
                                 get_answer_str(res)
                                 )
            await state.finish()


async def search_options_db(message: types.Message, state=FSMSearch.option_search):
    async with state.proxy() as data:
        await bot.send_message(message.from_user.id, f'{data["search_text"]}')

        search_list = await db_mysql_all_products()
        search_option_list = get_close_matches(f'{data["search_text"]}', search_list,
                                               n=5, cutoff=0.5)
        await bot.send_message(message.from_user.id,
                               'Возможно вы искали:',
                               reply_markup=await inline_button_gen(search_option_list))


# commands='Выйти из поиска'
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
    dp.register_message_handler(cancel_search_handler, commands=['Выйти из поиска',
                                                                 'отмена',
                                                                 'Отмена'],
                                state='*')
    dp.register_message_handler(search_options_db, state=FSMSearch.option_search)
