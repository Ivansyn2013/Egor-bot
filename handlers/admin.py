from aiogram import Dispatcher
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from tqdm import tqdm
from features.author_messages import AUTHOR_MESSAGES
from create_obj import bot
from keybords import admin_kb_check, ADMIN_KB_SENDMESSAGE
from acces_reader import db_mysql_search_product_id, db_mysql_update_photo
from aiogram.filters import Command, Filter
from aiogram import F
from loguru import logger
from models import Subscriber, db



class MyFilter(Filter):
    def __init__(self, *args, **kwargs) -> None:
        self.my_text = args

    async def __call__(self, message: types.Message) -> bool:
        return message.text == self.my_text

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
    #для отправки сообщений всем
    send_message_state = State()
    ready_to_send_mes_state = State()
    chose_action_state = State()


async def make_changes_command(message: types.Message, state: FSMContext):
    """First method in bot admin state"""
    logger.info(f'Moderator mode on by user {message.from_user.id}')
    await state.set_state(FSMAdmin.authorized)
    await bot.send_message(message.from_user.id, 'Введи пароль:')

async def ready_to_send_mes_state(message: types.Message, state: FSMContext):
    """For sendiing message for all subsribers. Work after admin auth"""
    await state.set_state(FSMAdmin.send_message_state)
    await message.reply('Готов к отправке. Следующее сообщение будет отправлено пользователям бота')



async def send_message_to_subsribers(message: types.Message, state: FSMContext):
    """For sendiing message for all subsribers. Work after admin auth"""
    try:
        subscribers = db.query(Subscriber.user_id)
        count = subscribers.count()
    except SQLAlchemyError:
        logger.exception('Ошибка при получении списка подписчиков из базы')
        await state.clear()
        await message.reply("Произошла ошибка")
        return

    try:
        i = 1
        for subscriber in subscribers:
            progress_bar = tqdm(total=count,
                                desc=f'Отправка пользователю {i} из {count}',
                                unit='пользователь')
            i += 1
            await bot.send_message(subscriber.user_id, message.text)
            progress_bar.update(1)
            await message.edit_text(str(progress_bar), parse_mode=None)
        progress_bar.close()

    except Exception as e:
        logger.error(f"Ошибка при отправке сообщений пользователям\n {e}" )
        await state.clear()
        await message.reply("Произошла ошибка")
        progress_bar.close()
        return

    await state.clear()
    await message.reply("Сообщения отправлены")

async def check_author(message: types.Message, state: FSMContext):
    """Next step after auth, check pass , work when first step set auth state"""
    logger.info('author on')
    if message.text == AUTHOR_PASS:
        await state.set_state(FSMAdmin.chose_action_state)
        await bot.send_message(message.from_user.id,
                               AUTHOR_MESSAGES['check_author'],
                               reply_markup=ADMIN_KB_SENDMESSAGE,
                               )
    else:
        await state.clear()
        await bot.send_message(message.from_user.id, 'Неверный пароль. Выход')

async def set_name(message: types.Message, state: FSMContext):
    """Not work"""
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
    """Not work"""
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
    """Not work"""
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
    """Not work"""
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
    """Not work"""
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
    """Not work"""
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
    """Not work"""
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
    """Not work"""
    async with state.proxy() as data:
        await bot.send_message(data['chat_id'],
                               'Отмена')
        await state.finish()

async def cm_start(message: types.Message):
    """Not work"""
    await FSMAdmin.photo.set()
    await message.reply('Загрузи фото')

async def load_photo(message: types.Message, state: FSMContext):
    """Not work"""
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название')


async def load_name(message: types.Message, state: FSMContext):
    """Not work. Change proxy . It's absent in new version"""
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Введи описание')

async def load_description(message: types.Message, state: FSMContext):
    """Not work """
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Укажи цену')

async def load_price(message: types.Message, state: FSMContext):
    """Not work. Change proxy . It's absent in new version'"""
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
    await state.clear()
    await message.reply('Команда отмены: ok')

def register_handlers_admin(dp: Dispatcher):
    dp.message.register(make_changes_command, Command('moderator'))
    dp.message.register(check_author, FSMAdmin.authorized)
    dp.message.register(ready_to_send_mes_state,
                        FSMAdmin.chose_action_state,
                        F.text == "/Отправить сообщение" )
    dp.message.register(send_message_to_subsribers, FSMAdmin.send_message_state)
    dp.message.register(set_name, FSMAdmin.name)
    dp.message.register(set_category, FSMAdmin.category)
    dp.message.register(set_description, FSMAdmin.description)
    dp.message.register(set_search_product_id, F.state == FSMAdmin.search_product_id)
    dp.message.register(set_photo, F.state == FSMAdmin.photo, F.content == ['photo'])
    dp.message.register(set_fodmap, F.state == FSMAdmin.fodmap)
    dp.message.register(update_photo,
                                F.state == FSMAdmin.update_photo_state,
                                #commands=['OK']
                                )
    dp.update.register(update_photo_cancel, F.state == FSMAdmin.update_photo_state,
                                Command('NOT OK'), MyFilter())


    dp.update.register(load_description, F.state == FSMAdmin.description)

    dp.update.register(cancel_handler, F.text(equals='отмена',
                                                     ignore_case=True))
    dp.update.register(cancel_handler, Command('отмена'), MyFilter())
