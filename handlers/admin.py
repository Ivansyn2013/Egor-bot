from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_obj import bot
from keybords import admin_kb


ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# хендлер для админа
# @dp.message_hendler(commands=["moderator"],is_chat_admin=True `указание на модератора
# группы`)
async def make_changes_command(message: types.Message):
    print('moderator on')
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Изменение базы данных',
                           reply_markup=admin_kb.button_case_admin)
    await message.delete()


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


# dp.register_message_handler(make_changes_command, commands='moderator')
# dp.register_message_handler(cm_start, commands=['Загрузить','Load'], state=None)
# dp.register_message_handler(load_description, state=FSMAdmin.description)
# dp.register_message_handler(load_name, state=FSMAdmin.name)
# dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
# dp.register_message_handler(load_price, state=FSMAdmin.price)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands='moderator')
    dp.register_message_handler(cm_start, commands=['Загрузить', 'Load'], state=None)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_name, state=FSMAdmin.price)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, Text(equals='отмена',
                                                     ignore_case=True), state="*")
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
