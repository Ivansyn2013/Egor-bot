import logging
import typing

from aiogram import Dispatcher
from aiogram import F
from aiogram import exceptions as aio_except
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from acces_reader import db_mysql_request, db_mysql_all_products, \
    db_mysql_category_request
from create_obj import bot
from create_obj import router
from features import get_answer_str
from features import my_fuzzy_search
from handlers.admin import MyFilter
from inline_butn import get_product_list_kb
from inline_butn import inline_button_gen
from inline_butn.search_inline_but import MyCallbackData
from inline_butn.search_inline_but import inline_buttons_gen_category
from keybords import kb_search, kb_client, get_inline_search_kb

kb_list = []

cd_data = MyCallbackData


class FSMSearch(StatesGroup):
    """
    State for work with seacrh
    """
    fs_search = State()
    option_search = State()
    callback_search_state = State()


async def cancel_search_handler(message: types.Message, state: FSMContext):
    '''
    function for canceling state
    :param message:
    :param state: FSMContext
    :return: finish state
    '''

    await state.clear()
    await message.reply('Команда отмены: ok',
                        reply_markup=kb_client)


async def command_start(message: types.Message):
    '''
    answer for none found questions
    :param message:
    :return: message + keyborad
    '''
    try:
        await bot.send_message(message.from_user.id,
                               'Привет!!!\n',
                               reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Напишите боту в ЛС')


# @dp.message_handler(commands=['Поиск'])
async def command_search(message: types.Message):
    '''
    fubction to start search in products
    :param message:
    :return: message with keyboard
    '''

    await bot.send_message(message.from_user.id, 'Поиск продуктов',
                           reply_markup=kb_search)


# commands=['Искать']
# @router.message(F.text == 'Поиска')
async def start_searching(message: types.Message, state: FSMContext):
    """function start search and redirect message to {search_go_to_db} """
    # if message.text == 'Поиск':
    #     await state.set_state(FSMSearch.fs_search)
    #     await message.reply('Введи название продукта',
    #                         reply_markup=kb_search)
    bot_info = await bot.get_me()
    await message.reply(text="Нажмите на кнопку ниже и вводите продукт в формате @ibs_doc_bot *продукт* Поиск "
                             "начинается с 3 напечатанных букв",
                        reply_markup=get_inline_search_kb(bot_info))

# поиск по категориям
async def start_category_search(message: types.Message):
    """
    :param message:
    :return: message with inline keyboard of category products
    """
    await message.reply('Категории продуктов',
                        reply_markup=await inline_buttons_gen_category())


async def callback_category(query: types.CallbackQuery,
                            callback_data: MyCallbackData):
    global kb_list

    dict_for_kb = {}
    for row in query.message.reply_markup.inline_keyboard:
        for but in row:
            if query.data == but.callback_data:
                category_product_in = but.text
                break

    category_poducts_all = await db_mysql_category_request()

    all_products = await db_mysql_all_products()
    for name, id in all_products.items():
        for category_name in category_poducts_all.keys():
            category_name_red = str(category_name).replace('\t', '')
            category_product_in = category_product_in.lstrip()
            if category_name_red == category_product_in:
                if id in category_poducts_all[category_name]:
                    dict_for_kb.update([(name, id)])
                # else:
                # print('Ошибка в получение значений ключа словаря категорий')

    # print(dict_for_kb)

    kb_list = await get_product_list_kb(dict_for_kb)

    await query.answer()
    await query.message.edit_text(f'{category_product_in}',
                                  reply_markup=kb_list[0])


async def search_go_to_db(message: types.Message, state: FSMContext):
    if message.text == 'Искать':
        await bot.send_message(message.from_user.id,
                               'Введи название продукта:')
    elif message.text == 'Выйти из поиска':
        await state.clear()
        await bot.send_message(message.from_user.id,
                               'Отмена поиска',
                               reply_markup=kb_client)

    else:
        data = {}
        data['search_text'] = message.text
        await state.update_data(search_text=message.text)
        res = await db_mysql_request(data['search_text'])
        # тут логер что ищет пользователь
        print(data['search_text'])
        await bot.send_message(message.from_user.id,
                               'Ищу')
        if res is None:
            await bot.send_message(message.from_user.id,
                                   'То что Вы искали, я не нашел, но может быть Вам '
                                   'подойдет что-то из этого:')

            search_dict = await db_mysql_all_products()

            # поиск через библиотеку diffflib
            # search_option_list = get_close_matches(f'{data["search_text"]}',
            #                                        list(search_dict.keys()),
            #                                        n=5, cutoff=0.5)
            #
            search_option_list = await my_fuzzy_search(list(search_dict.keys()),
                                                       f'{data["search_text"]}')

            logging.debug(search_option_list)
            search_dict_ready = {x: search_dict[x] for x in search_dict
                                 if x in search_option_list}
            data['bd_dict'] = search_dict_ready
            if search_dict_ready != {}:
                await bot.send_message(message.from_user.id,
                                       'Возможно вы искали:',
                                       reply_markup=await inline_button_gen(
                                           search_dict_ready))
                await FSMSearch.callback_search_state.set()
            else:
                await bot.send_message(message.from_user.id,
                                       'Ой, ничего похожего\n Попробуй еще раз',
                                       reply_markup=kb_search)
                await state.set_state(FSMSearch.fs_search)


        else:
            if all(map(lambda x: x is None, res.get('image'))):
                await message.delete()
                await bot.send_message(message.from_user.id,
                                       f'{get_answer_str(res)}',
                                       parse_mode='html',
                                       )
                await state.clear()

            else:
                image_data = types.BufferedInputFile(res['image'][0], filename=f'{data["search_text"]}.jpg')
                res.pop('image')
                res.pop('Картинка')
                await message.delete()
                await bot.send_photo(message.from_user.id,
                                     image_data,
                                     caption=f'{get_answer_str(res)}',
                                     parse_mode='html'
                                     )
                await state.clear()


async def search_callback(query: types.CallbackQuery,
                          callback_data: typing.Dict[str, str],
                          state: FSMContext):
    '''

    :param query: CallbackQuery
    :param callback_data: cd_data.filter(action='search')
    :param state: FSMSearch.callback_search_state
    :return: inline buttons or product cart
    '''
    async with state.proxy() as data:
        # print(data['bd_dict'])
        # print(callback_data['bd_id'])
        request = [x for x, y in data['bd_dict'].items()
                   if y == int(callback_data['bd_id'])]

        res = await db_mysql_request(request[0])

    if res is None:
        await bot.send_message(query.from_user.id,
                               text="Ничего не найдено")
        await state.clear()
        await bot.send_message(query.from_user.id, 'Будем еще искать?')

    else:
        # image_data = res['image'][0]
        # res.pop('image')
        # res.pop('Картинка')

        await bot.send_photo(
            query.from_user.id,
            'Пока нет',
            f'{get_answer_str(res)}',
            parse_mode='html'
        )
        await state.set_state(FSMSearch.fs_search)
        print(await state.get_state())


# @dp.message_handler(commands=['Авторизация'])
async def command_author(message: types.Message):
    await bot.send_message(message.from_user.id, 'Кнопки с аторизацией')


# Список продуктов
async def command_product_list(message: types.Message):
    global kb_list
    kb_list = await get_product_list_kb(await db_mysql_all_products())
    if kb_list is None:
        await bot.send_message(message.from_user.id, 'Список продуктов пуст')
    else:
        await bot.send_message(message.from_user.id,
                               'Список продуктов',
                               reply_markup=kb_list[0])


# Callback для списка продуктов
#
async def product_list_enter(query: types.CallbackQuery,
                             callback_data: typing.Dict[str, str]):
    '''function get product id from callback_data and redirest it in db_request
    send result to user'''

    search_dict = await db_mysql_all_products()

    request = [x for x, y in search_dict.items()
               if y == int(callback_data.bd_id)]
    res = await db_mysql_request(request[0])

    if res is None:
        await bot.send_message(query.from_user.id,
                               text="Ничего не найдено")

        await query.answer()

    else:
        print()
        image_data = res['image'][0]
        res.pop('image')
        res.pop('Картинка')
    try:
        await bot.send_photo(
            query.from_user.id,
            photo=types.BufferedInputFile(image_data, filename=res['Название продукта'][0]),
            caption=f'{get_answer_str(res)}',
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await query.answer()
    except aio_except.TelegramBadRequest as error:
        logging.critical('No photo in requst from DB from product_list_enter function')
        logging.critical(f'{error}')
        await bot.send_message(
            query.from_user.id,
            f'{get_answer_str(res)}',
            parse_mode=ParseMode.MARKDOWN_V2
        )
        await query.answer()


# action back and next
async def product_list_callback_next(query: types.CallbackQuery,
                                     callback_data: MyCallbackData):
    global kb_list
    kb_number = int(callback_data.kb_number)
    if kb_number >= len(kb_list) - 1:
        await  query.answer()
    else:
        await query.answer()
        await query.message.edit_text('Список продуктов',
                                      reply_markup=kb_list[kb_number + 1])


async def product_list_callback_back(query: types.CallbackQuery,
                                     callback_data: MyCallbackData):
    global kb_list
    kb_number = int(callback_data.kb_number)
    if kb_number == 0:
        await  query.answer()
    else:
        await query.answer()
        await query.message.edit_text('Список продуктов',
                                      reply_markup=kb_list[kb_number - 1])


@router.callback_query(MyCallbackData.filter(F.action == "category"))
async def test_callback(query: types.CallbackQuery,
                        # callback_data: MyCallbackData
                        ):
    await query.answer('test query')


def register_handlers_client(dp: Dispatcher):
    dp.message.register(command_author, Command('Авторизация'), MyFilter())
    dp.message.register(start_searching, F.text(equals=['Поиск'],
                                                ignore_case=True))
    dp.message.register(start_searching, F.text == 'Поиск')
    dp.message.register(command_start, CommandStart())
    dp.message.register(command_product_list,
                        F.text == 'Список продуктов')
    dp.message.register(search_go_to_db, FSMSearch.fs_search)
    dp.message.register(
        cancel_search_handler,
        F.text.in_(['Выйти из поиска', 'Отмена']),
    )
    dp.message.register(cancel_search_handler,
                        F.text == 'отмена'
                        )
    dp.message.register(start_category_search,
                        F.text == 'Категории продуктов')
    dp.callback_query.register(search_callback,
                               cd_data.filter(F.action == 'search'),
                               )
    dp.callback_query.register(product_list_callback_next,
                               cd_data.filter(F.action == 'next'))
    dp.callback_query.register(product_list_callback_back,
                               cd_data.filter(F.action == 'back'))
    dp.callback_query.register(product_list_enter,
                               cd_data.filter(F.action == 'search_in'))
    dp.callback_query.register(callback_category,
                               MyCallbackData.filter(F.action == 'category'))
