from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import os
from dotenv import load_dotenv
from features.author_messages import AUTHOR_MESSAGES
from create_obj import bot
from keybords import admin_kb_check
from acces_reader import db_mysql_search_product_id, db_mysql_update_photo

load_dotenv()
AUTHOR_PASS = os.getenv('AUTHOR_PASS')
ID = None


class FSMAdmin(StatesGroup):

    authorized = State()
    name = State()
    description = State()
    category = State()
    fodmap = State()
    search_product_id = State()
    photo = State()
    data_check = State()
    update_photo_state = State()

async def make_changes_command(message: types.Message):
    print('moderator on')
    await FSMAdmin.authorized.set()
    await bot.send_message(message.from_user.id, 'Введи пароль:')

    # await bot.send_message(message.from_user.id, 'Изменение базы данных',
    #                        reply_markup=admin_kb.button_case_admin)
    # #await message.delete()

async def check_author(message: types.Message, state: FSMContext):
    print('author on')
    if message.text == AUTHOR_PASS:
        await FSMAdmin.search_product_id.set()
        await message.delete()
        await bot.send_message(message.from_user.id,
                               AUTHOR_MESSAGES['check_author'])
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, 'Неверный пароль. Выход')

async def set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['name'] = message.text

        except Exception as er:
            print(er + ' error from set_name')
            state.finish()

        await FSMAdmin.next()
        await bot.send_message(message.from_user.id,
                               'Жду описание:')
async def set_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['description'] = message.text

        except Exception as er:
            print(er + ' error from set_description')
            state.finish()

        await FSMAdmin.next()
        await bot.send_message(message.from_user.id,
                               'Жду категорию:')
async def set_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['category'] = message.text

        except Exception as er:
            print(er + ' error from set_category')
            state.finish()

        await FSMAdmin.next()
        await bot.send_message(message.from_user.id,
                               'Жду fodmap:')

async def set_fodmap(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['fodmap'] = message.text

        except Exception as er:
            print(er + ' error from set_name')
            state.finish()

    await FSMAdmin.photo.set()
    await bot.send_message(message.from_user.id,
                           'Жду photo:')

async def set_search_product_id(message: types.Message, state: FSMContext):
    product_id = await db_mysql_search_product_id(message.text)
    if product_id:
        async with state.proxy() as data:
            data['product_id'] = product_id
        await bot.send_message(message.from_user.id,
                         'Объект найден. Жду фото:')
        await FSMAdmin.photo.set()
    else:
        await bot.send_message(message.from_user.id,
                               'Не найдено. Выход')
        state.finish()


async def set_photo(message: types.Message, state: FSMContext):
    print('режим фото')
    async with state.proxy() as data:
        try:
            await message.photo[-1].download(destination_file='tmp/tmp.jpg')
            #data['photo'] = open('tmp/tmp.jpg', 'rb')

            data['chat_id'] = message.from_user.id
            await bot.send_message(message.from_user.id,
                                   f'Что получилось:')
            await bot.send_photo(message.from_user.id,
                                 open('tmp/tmp.jpg','rb'),
                                 data['product_id'])


        except Exception as er:
            print(er)
            print(' error from set_name')
            await state.finish()


    await bot.send_message(message.from_user.id,
                           'Проверь данные',
                           reply_markup=admin_kb_check)
    await FSMAdmin.update_photo_state.set()

async def update_photo(message: types.Message, state: FSMContext):
    with open('tmp/tmp.jpg', 'rb') as f:
        b_photo = f.read()
    async with state.proxy() as data:

        request = await db_mysql_update_photo(data['product_id'], b_photo)
        if request:
            await bot.send_message(data['chat_id'],
                             'Картинка успешно добавлена')
            await state.finish()
        else:
            await bot.send_message(data['chat_id'],
                             'Запрос к базе данных вернул ошибку')
            await state.finish()
async def update_photo_cancel(state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(data['chat_id'],
                               'Отмена')
        await state.finish()


# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply('Загрузи фото')


# обработка ответа пользователя
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название')


# next FAM answer
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Введи описание')

# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Укажи цену')

# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    # async with state.proxy() as data:
    # await message.reply(str(data))
    # await message.answer('Готово')
    # запись в базу

    # вызод из машинных состояний
    await state.finish()

# отмена машинного состояния
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Команда отмены: ok')

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands='moderator')
    dp.register_message_handler(check_author, state=FSMAdmin.authorized)
    dp.register_message_handler(set_name, state=FSMAdmin.name)
    dp.register_message_handler(set_category, state=FSMAdmin.category)
    dp.register_message_handler(set_description, state=FSMAdmin.description)
    dp.register_message_handler(set_search_product_id, state=FSMAdmin.search_product_id)
    dp.register_message_handler(set_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(set_fodmap, state=FSMAdmin.fodmap)
    dp.register_message_handler(update_photo,
                                state=FSMAdmin.update_photo_state,
                                #commands=['OK']
                                )
    dp.register_message_handler(update_photo_cancel, state=FSMAdmin.update_photo_state,
                                commands=['NOT OK'])


    dp.register_message_handler(load_description, state=FSMAdmin.description)

    dp.register_message_handler(cancel_handler, Text(equals='отмена',
                                                     ignore_case=True), state="*")
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
