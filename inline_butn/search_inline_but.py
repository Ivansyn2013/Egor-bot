from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import uuid
from aiogram.filters.callback_data import CallbackData
from acces_reader.mysql_connet_connector import db_mysql_category_request


class MyCallbackData(CallbackData, prefix='my'):

    button: str
    id: str
    bd_id: str
    action: str
    kb_number: int


async def inline_button_gen(search_dict_ready: dict) -> InlineKeyboardMarkup:
    '''get list with search options
    :return inline_key_board'''

    global cd_data

    inline_but_kb = InlineKeyboardMarkup(row_width=3)
    sl = search_dict_ready

    for name, id in sl.items():
        b = InlineKeyboardButton(text=f'{name}',
                                 callback_data=MyCallbackData(
                                     id=str(uuid.uuid4()),
                                     action='search',
                                     bd_id=id,
                                     kb_number=0,
                                     button=''
                                 ).pack(),
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


    buttons_list = []

    for name, id in c_d.items():
        if type(id) is list:
            id = 'list'
        b = InlineKeyboardButton(text=f'{name}',
                                 callback_data=MyCallbackData(
                                     id=str(uuid.uuid4()),
                                     action='category',
                                     bd_id=id,
                                     kb_number=0,
                                     button=f'',
                                 ).pack(),
                                 )
        buttons_list.append(b)
    inline_but_kb = InlineKeyboardMarkup(inline_keyboard=[buttons_list[i:i + 2] for i in range(0,
                                                                                               len(buttons_list),
                                                                                               2)])

    return inline_but_kb
