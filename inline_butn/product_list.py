from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import uuid
from aiogram.utils.callback_data import CallbackData
from aiogram import types
from inline_butn.search_inline_but import cd_data
from acces_reader import db_mysql_all_products

cd_data = CallbackData('button', 'id', 'bd_id', 'action', 'kb_number')


async def get_product_list_kb(all_product_dict: dict) -> types.InlineKeyboardButton:
    global cd_data

    test = []
    pd = all_product_dict
    kb_list = []
    but_list = []
    inline_but_kb = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

    for name, id in sorted(pd.items()):
        b = InlineKeyboardButton(text=f'{name}',
                                 callback_data=cd_data.new(
                                     id=str(uuid.uuid4()),
                                     action='search_in',
                                     bd_id=id,
                                     kb_number=0,
                                 ),
                                 )
        but_list.append(b)
    start=0
    for index in range(14,len(but_list),14):
        inline_but_kb.add(*but_list[start:index])

        inline_but_kb.row(InlineKeyboardButton(text='Назад',
                                               callback_data=cd_data.new(
                                                   id=str(uuid.uuid4()),
                                                   action='back',
                                                   bd_id=id,
                                                   kb_number=index // 14,
                                               )
                                               ),
                          InlineKeyboardButton(text='Вперед',
                                               callback_data=cd_data.new(
                                                   id=str(uuid.uuid4()),
                                                   action='next',
                                                   bd_id=id,
                                                   kb_number=index // 14,
                                               )
                                               ))
        test.append(index // 14)
        start = index
        kb_list.append(inline_but_kb)
        inline_but_kb = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    print(test)
    print(len(kb_list))
    return kb_list


if __name__ == '__main__':
    # print(type(db_mysql_all_products()))
    dad = db_mysql_all_products()
    # print(type(get_product_list_kb(dad)))
