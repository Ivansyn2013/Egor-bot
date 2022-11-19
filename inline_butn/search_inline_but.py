from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import uuid
from aiogram.utils.callback_data import CallbackData

cd_data = CallbackData('button', 'id', 'bd_id', 'action')


async def inline_button_gen(search_dict_ready: dict):
    '''get list with search options
    :return inline_key_board'''

    global cd_data

    inline_but_kb = InlineKeyboardMarkup(row_width=3, resize_keybasrd=True)
    sl = search_dict_ready

    for name, id in sl.items():
        b = InlineKeyboardButton(text=f'{name}',
                                 callback_data=cd_data.new(
                                     id=str(uuid.uuid4()),
                                     action='search',
                                     bd_id=id,
                                 ),
                                 )
        inline_but_kb.add(b)
    return inline_but_kb
