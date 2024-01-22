import io
import json
import logging
import typing
from difflib import get_close_matches

from aiogram import Dispatcher
from aiogram import types
from acces_reader import db_mysql_request, db_mysql_all_products, \
    db_mysql_category_request
from create_obj import bot
from features import get_answer_str
from uuid import uuid4
from PIL import Image
from io import BytesIO
from keybords.other_kb import kb_answer_and_qusetion
from aiogram.types.link_preview_options import LinkPreviewOptions


async def upload_file_totg(user_id, photo):
    '''функция для рабоэты через кеш фото'''
    chat_id = await bot.get_chat(user_id)

    #image = Image.open(BytesIO(photo))
    try:
        photo_message = await bot.send_photo(chat_id=chat_id.id, photo=photo)
        file_id = photo_message.photo[-1].file_id
        print(file_id)
    except Exception as e:
        print(e)
        file_id = 'AgACAgIAAxkDAAIUoWWaikNnMNoFnR_ZHFsLiz4sylLPAAIC1TEb-bvZSBqzbm4xjodvAQADAgADeAADNAQ'
    return file_id

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
            url_thumb=f'https://fodmap.moscow/media/thumbnails/{product_id}.png'
            id_code = str(uuid4())
            result = await db_mysql_request(name) or str('Не найдено')
            product_name = result['Название продукта'][0].replace('(', '\(').replace(')', '\)')
            mark_probe = f"[{product_name}](https://fodmap.moscow/media/{product_id}.png)"
            image_url = f'https://fodmap.moscow/media/{product_id}.png'
            thumb_url = f'https://fodmap.moscow/media/thumbnails/{product_id}.png'
            #вариант через Article
#            print(mark_probe) #+ get_answer_str(result))


            responce.append(types.InlineQueryResultArticle(
                id=id_code,
                title=name,
                description=name,
                input_message_content=types.InputTextMessageContent(
                    message_text=mark_probe + get_answer_str(result).replace(product_name, ''),
                    #f"{url1} + \n + {get_answer_str(result)}",
                    parse_mode='Markdown',
                    link_preview_options=LinkPreviewOptions(
                        show_above_text=True
                    )

                ),
                    #здесь ссылка на картинку
                thumb_url=url_thumb,
                thumb_width=128,  # Set the width of the thumbnail image
                thumb_height=128,



            ))


            #вариаент через фото
            # responce.append(
            #     types.InlineQueryResultPhoto(
            #         id=id_code,
            #         title='name',
            #         description='Это дескриптион',
            #         photo_url=f"https://fodmap.moscow/media/{product_id}.png",
            #         thumb_url=url_thumb,
            #         caption='Inline Title: Your Photo Title',
            #         parse_mode='html',
            #                             ),
            #     )
            ###Вариант со своим классом


        await query.answer(responce, cache_time=2, is_personal=True)





# async def get_user_inline_choseen(chosen_result: types.ChosenInlineResult):
#
#     '''Перехват инлайна в особом режиме бота'''
#     user_id = chosen_result.from_user.id
#     result = types.InlineQueryResult(
#         id=chosen_result.result_id,
#     )
#     await bot.send_message(user_id, 'fdfdf')
#     await bot.s
#     print(chosen_result)
#     pass

def register_handlers_inline(dp: Dispatcher):
    #dp.message.register(get_user_inline_choseen)
    dp.inline_query.register(inline_handler)

