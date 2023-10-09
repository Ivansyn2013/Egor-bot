import logging
import typing
from difflib import get_close_matches

from aiogram import Dispatcher
from aiogram import exceptions
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
from features import my_fuzzy_search
import hashlib


async def inline_handler(query: types.InlineQuery):
    print('Инлайн сообщение')
    text = query.query
    id_code = hashlib.md5(text.encode()).hexdigest()
    product_dict = await db_mysql_all_products()
    filtered_product_list = await my_fuzzy_search(list(product_dict.keys()), text)

    search_dict_ready = {x: product_dict[x] for x in product_dict
                         if x in filtered_product_list}
    df= 1
    print('dfsdf')
    responce = [types.InlineQueryResultArticle(
        id=id_code,
        title='xfd',

        input_message_content=types.InputTextMessageContent(message_text=text)
                                               )]
    await query.answer(responce, cache_time=2, is_personal=True)

def register_handlers_inline(dp: Dispatcher):
    dp.register_inline_handler(inline_handler)
