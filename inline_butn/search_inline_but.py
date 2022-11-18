from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



async def inline_button_gen(search_option_list: list):
    '''get list with search options
    :return inline_key_board'''
    inline_but_kb = InlineKeyboardMarkup(row_width=3,resize_keybasrd=True)
    sl = search_option_list
    buttons = []

    for name in sl:
        b = InlineKeyboardButton(text=f'{name}',callback_data='www')
        inline_but_kb.add(b)
    return inline_but_kb
