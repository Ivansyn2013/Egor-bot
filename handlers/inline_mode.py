import io
import json
import logging
import typing
from difflib import get_close_matches

from aiogram import Dispatcher
from aiogram import exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import base64

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
from uuid import uuid4


async def inline_handler(query: types.InlineQuery):
    user = query.from_user
    text = query.query
    logging.info(f'Inline search:: user {user["username"]} search text {text}')
    if len(text) > 2:
        product_dict = await db_mysql_all_products()
        #filtered_product_list = await my_fuzzy_search(list(product_dict.keys()), text)
        filtered_product_list = [name for name in product_dict if name.lower().find(text.lower()) != -1]
        search_dict_ready = {x: product_dict[x] for x in product_dict
                             if x in filtered_product_list}
        responce = []

        for name, product_id in search_dict_ready.items():
            url1=f'https://fodmap.moscow/media/{product_id}.png'
            id_code = str(uuid4())
            result = await db_mysql_request(name) or str('Не найдено')
            product_name = result['Название продукта'][0].replace('(', '\(').replace(')', '\)')
            mark_probe = f"[{product_name}](https://fodmap.moscow/media/{product_id}.png)"
            #вариант через Article
            print(mark_probe) #+ get_answer_str(result))
            responce.append(types.InlineQueryResultArticle(
                id=id_code,
                title=name,
                input_message_content=types.InputTextMessageContent(
                    message_text= mark_probe + get_answer_str(result).replace(product_name, ''),
                    #f"{url1}" + "\n" +
            # get_answer_str(
            # result),
                    parse_mode='MarkdownV2',
                ),
                    #здесь ссылка на картинку
                thumb_url=url1,
                thumb_width=100,  # Set the width of the thumbnail image
                thumb_height=100
            )
            )

            #вариаент через фото
            # responce.append(
            #     types.InlineQueryResultPhoto(
            #         id=id_code + 'f',
            #         photo_url='https://upload.wikimedia.org/wikipedia/commons/3/3f/JPEG_example_flower.jpg',
            #         thumb_url=url1,
            #         ),
            #     )
        await query.answer(responce, cache_time=2, is_personal=False)
        print()
        #await bot.send_photo(query.from_user.id, url1, f'{get_answer_str(result)}', parse_mode='html')

def register_handlers_inline(dp: Dispatcher):
    dp.register_inline_handler(inline_handler)
