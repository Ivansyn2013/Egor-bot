from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import uuid
from aiogram.filters.callback_data import CallbackData
from aiogram import types
from acces_reader import db_mysql_all_products

class MyCallbackData(CallbackData, prefix='my'):
    button: str
    id: str
    bd_id: str
    action: str
    kb_number: str


async def get_product_list_kb(all_product_dict: dict) -> types.InlineKeyboardButton:
    '''

    :param all_product_dict:dict with product name: product id from db
    :return:inline_kb
    '''
    global cd_data

    pd = all_product_dict
    kb_list = []
    but_list = []
    inline_but_kb = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

    for name, id in sorted(pd.items()):
        b = InlineKeyboardButton(text=f'{name}',
                                 callback_data=MyCallbackData(
                                     id=str(uuid.uuid4()),
                                     action='search_in',
                                     bd_id=id,
                                     kb_number=0,
                                 ).pack(),
                                 )
        but_list.append(b)

    if len(but_list) > 15:

        for index in range(0, len(but_list), 14):
            inline_but_kb.add(*but_list[index:index + 14])

            inline_but_kb.row(InlineKeyboardButton(text='Назад',
                                                   callback_data=MyCallbackData(
                                                       id=str(uuid.uuid4()),
                                                       action='back',
                                                       bd_id=id,
                                                       kb_number=index // 14,
                                                   ).pack()
                                                   ),
                              InlineKeyboardButton(text='Вперед',
                                                   callback_dat=MyCallbackData(
                                                       id=str(uuid.uuid4()),
                                                       action='next',
                                                       bd_id=id,
                                                       kb_number=index // 14,
                                                   ).pack()
                                                   ))

            kb_list.append(inline_but_kb)
            inline_but_kb = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
        else:
            if (len(but_list) % 14) != 0:
                inline_but_kb.add(*but_list[(len(but_list) // 14) * 14:])
                inline_but_kb.row(InlineKeyboardButton(text='Назад',
                                                       callback_data=MyCallbackData(
                                                           id=str(uuid.uuid4()),
                                                           action='back',
                                                           bd_id=id,
                                                           kb_number=(
                                                                   len(but_list) // 14 + 1),
                                                       ).pack()
                                                       ),
                                  InlineKeyboardButton(text='Вперед',
                                                       callback_data=MyCallbackData(
                                                           id=str(uuid.uuid4()),
                                                           action='next',
                                                           bd_id=id,
                                                           kb_number=(
                                                                   len(but_list) // 14 + 1),
                                                       ).pack()
                                                       ))

                kb_list.append(inline_but_kb)

    else:
        inline_but_kb.add(*but_list)
        kb_list.append(inline_but_kb)
    return kb_list


if __name__ == '__main__':
    # print(type(db_mysql_all_products()))
    dad = db_mysql_all_products()
    # print(type(get_product_list_kb(dad)))
