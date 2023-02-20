import logging
import typing
from difflib import get_close_matches
from aiogram import exceptions
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from acces_reader import db_mysql_request, db_mysql_all_products, \
    db_mysql_category_request
from create_obj import bot
from features import get_answer_str
from inline_butn import cd_data
from inline_butn import get_product_list_kb
from inline_butn import inline_button_gen
from inline_butn.search_inline_but import inline_buttons_gen_category
from keybords import kb_search, kb_client

kb_list = []


class FSMSearch(StatesGroup):
    '''
    State for work with seacrh
    '''
    fs_search = State()
    option_search = State()
    callback_search_state = State()


async def cancel_search_handler(message: types.Message, state: FSMContext):
    # current_state = await state.get_state()
    # if current_state is None:
    #     await message.reply('Выход',
    #                         reply_markup=kb_client)
    await state.finish()
    await message.reply('Команда отмены: ok',
                        reply_markup=kb_client)


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,
                               'Привет обжорам!!!\n',
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
    '''function start search and redirect message to {search_go_to_db} '''
    if message.text == 'Поиск':
        await FSMSearch.fs_search.set()
        await message.reply('Введи название продукта',
                            reply_markup=kb_search)


# поиск по категориям
async def start_category_search(message: types.Message):
    await message.reply('Категории продуктов',
                        reply_markup=await inline_buttons_gen_category())


async def callback_category(query: types.CallbackQuery,
                            callback_data: typing.Dict[str, str]):
    global kb_list

    dict_for_kb = {}
    for but in query.message.reply_markup.inline_keyboard:
        for context in but:
            if query.data == context["callback_data"]:
                category_product_in = context.text

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

    print(len(kb_list))

    await query.answer()
    await query.message.edit_text(f'{context.text}',
                                  reply_markup=kb_list[0])


async def search_go_to_db(message: types.Message, state=FSMContext):
    if message.text == 'Искать':
        await bot.send_message(message.from_user.id,
                               'Введи название продукта:')
    elif message.text == 'Выйти из поиска':
        await state.finish()
        await bot.send_message(message.from_user.id,
                               'Отмена поиска',
                               reply_markup=kb_client)

    else:
        async with state.proxy() as data:
            data['search_text'] = message.text

            res = await db_mysql_request(data['search_text'])
            print(data['search_text'])
            await bot.send_message(message.from_user.id,
                                   'Ищу')
            if res is None:
                await bot.send_message(message.from_user.id,
                                       'То что Вы искали, я не нашел, но может быть Вам '
                                       'подойдет что-то из этого:')

                # await FSMSearch.option_search.set()
                # print(await state.get_state())
                # await search_options_db(message,FSMSearch.option_search)

                # await bot.send_message(message.from_user.id, f'{data["search_text"]}')

                search_dict = await db_mysql_all_products()

                search_option_list = get_close_matches(f'{data["search_text"]}',
                                                       list(search_dict.keys()),
                                                       n=5, cutoff=0.5)
                print(search_option_list)
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
                    await FSMSearch.fs_search.set()


            else:
                if all(map(lambda x: x is None, res.get('image'))):
                    await message.delete()
                    await bot.send_message(message.from_user.id,
                                            f'{get_answer_str(res)}',
                                            parse_mode='html',
                                           )
                    await state.finish()

                else:
                    image_data = res['image'][0]
                    res.pop('image')
                    res.pop('Картинка')
                    print(res.items())
                    await message.delete()
                    await bot.send_photo(message.from_user.id,
                                         image_data,
                                         f'{get_answer_str(res)}',
                                         parse_mode='html'
                                         )
                    await state.finish()


async def search_callback(query: types.CallbackQuery,
                          callback_data: typing.Dict[str, str],
                          state=FSMContext):
    ''''''
    async with state.proxy() as data:
        # print(data['bd_dict'])
        # print(callback_data['bd_id'])
        request = [x for x, y in data['bd_dict'].items()
                   if y == int(callback_data['bd_id'])]

        res = await db_mysql_request(request[0])

    if res is None:
        await bot.send_message(query.from_user.id,
                               text="Ничего не найдено")
        await state.finish()
        await bot.send_message(query.from_user.id, 'Будем еще искать?')

    else:
        image_data = res['image'][0]
        res.pop('image')
        res.pop('Картинка')

        await bot.send_photo(
            query.from_user.id,
            image_data,
            f'{get_answer_str(res)}',
            parse_mode='html'
        )
        await FSMSearch.fs_search.set()
        print(await state.get_state())


# commands='Выйти из поиска'


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
               if y == int(callback_data['bd_id'])]
    res = await db_mysql_request(request[0])

    if res is None:
        await bot.send_message(query.from_user.id,
                               text="Ничего не найдено")

        await query.answer()

    else:
        image_data = res['image'][0]
        res.pop('image')
        res.pop('Картинка')
    try:
        await bot.send_photo(
            query.from_user.id,
            image_data,
            f'{get_answer_str(res)}',
            parse_mode='html'
        )
        await query.answer()
    except exceptions.BadRequest as error:
        logging.CRITICAL('No photo in requst from DB from product_list_enter function')
        logging.CRITICAL(f'{error}')
        await bot.send_message(
            query.from_user.id,
            f'{get_answer_str(res)}',
            parse_mode='html'
        )
        await query.answer()

# action back and next
async def product_list_callback_next(query: types.CallbackQuery,
                                     callback_data: typing.Dict[str, str]):
    print(callback_data['kb_number'])
    kb_number = int(callback_data['kb_number']) - 1
    if kb_number >= len(kb_list) - 1:
        await  query.answer()
    else:
        await query.answer()
        await query.message.edit_text('Список продуктов',
                                      reply_markup=kb_list[kb_number + 1])


async def product_list_callback_back(query: types.CallbackQuery,
                                     callback_data: typing.Dict[str, str]):
    print(callback_data['kb_number'])
    kb_number = int(callback_data['kb_number']) - 1
    if kb_number == 0:
        await  query.answer()
    else:
        await query.answer()
        await query.message.edit_text('Список продуктов',
                                      reply_markup=kb_list[kb_number - 1])


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_author, commands=['Авторизация'])
    #    dp.register_message_handler(start_searching, commands=['Искать', 'Поиск'])
    dp.register_message_handler(start_searching, Text(equals=['Поиск'],
                                                      ignore_case=True))
    dp.register_message_handler(command_product_list,
                                Text(
                                    equals=['Список '
                                            'продуктов'],
                                    ignore_case=True))

    dp.register_message_handler(search_go_to_db, state=FSMSearch.fs_search)
    #    dp.register_message_handler(search_options_db, state=FSMSearch.option_search)
    dp.register_message_handler(cancel_search_handler,
                                Text(
                                    equals=['Выйти из поиска',
                                            'Отмена'],
                                    ignore_case=True),
                                state='*'
                                )
    dp.register_message_handler(cancel_search_handler,
                                Text(equals='отмена',
                                     ignore_case=True),
                                state="*",
                                )
    dp.register_message_handler(start_category_search,
                                Text(equals=['Категории продуктов'],
                                     ignore_case=True
                                     ))

    dp.register_callback_query_handler(search_callback,
                                       cd_data.filter(action='search'),
                                       state=FSMSearch.callback_search_state)
    # dp.register_message_handler(command_product_list, Text(equals='Список продуктов',
    #                                                        ignore_case=True))

    dp.register_callback_query_handler(product_list_callback_next,
                                       cd_data.filter(action='next'))
    dp.register_callback_query_handler(product_list_callback_back,
                                       cd_data.filter(action='back'))
    dp.register_callback_query_handler(product_list_enter,
                                       cd_data.filter(action='search_in'))
    dp.register_callback_query_handler(callback_category,
                                       cd_data.filter(action='category'))
