from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import uuid
from aiogram.filters.callback_data import CallbackData
from acces_reader.mysql_connet_connector import db_mysql_category_request


class MyCallbackData(CallbackData, prefix='my'):

    button: str
    id: str
    bd_id: str
    action: str
    kb_number: str


async def inline_button_gen(search_dict_ready: dict) -> InlineKeyboardMarkup:
    '''get list with search options
    :return inline_key_board'''

    global cd_data

    inline_but_kb = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
    sl = search_dict_ready

    for name, id in sl.items():
        b = InlineKeyboardButton(text=f'{name}',
                                 callback_data=MyCallbackData(
                                     id=str(uuid.uuid4()),
                                     action='search',
                                     bd_id=id,
                                     kb_number='s_s'
                                 ),
                                 )
        inline_but_kb.add(b)
    return inline_but_kb


async def inline_buttons_gen_category() -> InlineKeyboardMarkup:
    """get list with category dict from db with id of product
        :return inline_key_board
    """
    c_d = await db_mysql_category_request()

    if c_d is None:
        return None

    inline_but_kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons_list = []

    for name, id in c_d.items():
        if type(id) is list:
            id = 'list'
        b = InlineKeyboardButton(text=f'{name}',
                                 callback_data=MyCallbackData(
                                     id=str(uuid.uuid4()),
                                     action='category',
                                     bd_id=id,
                                     kb_number='s_s'
                                 ).pack(),
                                 )
        buttons_list.append(b)
    inline_but_kb.add(*buttons_list)
    return inline_but_kb
