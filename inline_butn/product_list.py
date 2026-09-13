from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import uuid
from aiogram.filters.callback_data import CallbackData
from aiogram import types
from acces_reader import db_mysql_all_products
from inline_butn.search_inline_but import MyCallbackData


async def get_product_list_kb(all_product_dict: dict) -> types.InlineKeyboardButton:
    '''

    :param all_product_dict:dict with product name: product id from db
    :return:inline_kb
    '''
    global cd_data

    pd = all_product_dict
    kb_list = []
    but_list = []

    for name, id in sorted(pd.items()):
        b = InlineKeyboardButton(text=f'{name}',
                                 callback_data=MyCallbackData(
                                     id=str(uuid.uuid4()),
                                     action='search_in',
                                     bd_id=str(id),
                                     kb_number=0,
                                     button='',
                                 ).pack(),
                                 )
        but_list.append(b)

    if len(but_list) > 15:

        for index in range(0, len(but_list), 14):
            row = [InlineKeyboardButton(text='Назад',
                                        callback_data=MyCallbackData(
                                            id=str(uuid.uuid4()),
                                            action='back',
                                            bd_id='back',
                                            button='',
                                            kb_number=index // 14,
                                        ).pack()
                                        ),
                   InlineKeyboardButton(text='Вперед',
                                        callback_data=MyCallbackData(
                                            id=str(uuid.uuid4()),
                                            action='next',
                                            bd_id='next',
                                            button='',
                                            kb_number=index // 14,
                                        ).pack()
                                        )]

            # подумать как теперь запихнуть все в листы листов
            but_list_divide = but_list[index:index + 14]
            divided_by_too = [but_list_divide[i:i + 2] for i in range(0, len(but_list_divide), 2)]
            divided_by_too.append(row)
            inline_but_kb = InlineKeyboardMarkup(
                # inline_keyboard=[but_list[index:index + 14], row],
                inline_keyboard=divided_by_too,
                resize_keyboard=True
            )
            # inline_but_kb.add(*but_list[index:index + 14])
            kb_list.append(inline_but_kb)

    elif (len(but_list) % 14) != 0:
        inline_but_kb = []
        inline_but_kb.extend(but_list[(len(but_list) // 14) * 14:])
        inline_but_kb.append(InlineKeyboardButton(text='Назад',
                                                  callback_data=MyCallbackData(
                                                      id=str(uuid.uuid4()),
                                                      action='back',
                                                      bd_id='back',
                                                      button="",
                                                      kb_number=(
                                                              len(but_list) // 14 + 1),
                                                  ).pack()
                                                  ))
        inline_but_kb.append(InlineKeyboardButton(text='Вперед',
                                                  callback_data=MyCallbackData(
                                                      id=str(uuid.uuid4()),
                                                      action='next',
                                                      bd_id='next',
                                                      button="",
                                                      kb_number=(
                                                              len(but_list) // 14 + 1),
                                                  ).pack()
                                                  ))

        kb_instance = InlineKeyboardMarkup(
            inline_keyboard=[inline_but_kb[i:i + 2] for i in range(0, len(inline_but_kb), 2)],
            resize_keyboard=True)
        kb_list.append(kb_instance)

    else:
        inline_but_kb = []
        inline_but_kb.append(*but_list)
        kb_list.append(inline_but_kb)
        kb_list = InlineKeyboardMarkup(inline_keyboard=[inline_but_kb], resize_keyboard=True)

    return kb_list


if __name__ == '__main__':
    # print(type(db_mysql_all_products()))
    dad = db_mysql_all_products()
    # print(type(get_product_list_kb(dad)))
