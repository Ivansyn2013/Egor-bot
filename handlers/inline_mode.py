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
    product_dict = await db_mysql_all_products()
    #filtered_product_list = await my_fuzzy_search(list(product_dict.keys()), text)
    filtered_product_list = [name for name in product_dict if name.lower().find(text.lower()) != -1]

    search_dict_ready = {x: product_dict[x] for x in product_dict
                         if x in filtered_product_list}


    print('dfsdf')
    responce = []

    for name, product_id in search_dict_ready.items():
        url1='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQO_DvKa3Xd0JcA1f4zlaNXN78zJ4HvqnH5CohpBQTYUA&s'


        chat = await bot.get_chat(query.from_user.id)

        id_code = str(uuid4())
        result = await db_mysql_request(name) or str('Не найдено')
        if not isinstance(result, str):
            image_bytes = result['image'][0]
            image_IO = io.BytesIO(image_bytes)
            image_file = types.InputFile(image_IO)


            result.pop('image')
            result.pop('Картинка')

        #вариант через Article
        responce.append(types.InlineQueryResultArticle(
            id=id_code,
            title=name,
            #здесь ссылка на картинку
            thumb_url=url1,
            input_message_content=types.InputTextMessageContent(
                message_text=get_answer_str(result),
                parse_mode='html')
        )
        )

        #вариаент через фото
        #types.InputMediaPhoto
        #photo_id = await bot.send_photo(chat_id=query.from_user.id, photo=image)
        # responce.append(
        #     types.InlineQueryResultPhoto(
        #         id=id_code,
        #         title=name,
        #         description=name,
        #         photo_url=url1,
        #         thumb_url=url1,
        #         input_message_content=types.InputTextMessageContent(
        #             message_text=get_answer_str(result),
        #             parse_mode='html',
        #         ),
        #         #parse_mode='html',
        #     )
        # )

    await query.answer(responce, cache_time=2, is_personal=True)

def register_handlers_inline(dp: Dispatcher):
    dp.register_inline_handler(inline_handler)
