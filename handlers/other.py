import json
import string

from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink, link

from create_obj import  bot
from keybords import kb_client, kb_answer_and_qusetion
from features.answer_and_question import STR_ANSWER_AND_QUESTION


filter_list = list(STR_ANSWER_AND_QUESTION.keys())
filter_list.append('Узнать о боте')

#@dp.message_handler()
async def cenz_filter(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
        message.text.split(' ')}.intersection(
        set(json.load(open('cenz\cenz.json')))) != set():
        await message.reply("Мат запрещен")
        await message.delete()


async def answer_and_qusetion(message: types.Message):
    if message.text == 'Узнать о боте':
        await message.reply('Инфо', reply_markup=kb_answer_and_qusetion)
    elif message.text == "Назад":
        await message.reply(reply_markup=kb_client)
    if message.text in STR_ANSWER_AND_QUESTION.keys():
        await message.reply(f'{STR_ANSWER_AND_QUESTION[message.text]}',
                            reply_markup=kb_answer_and_qusetion,
                            parse_mode='html')



async def start_mes(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Привет! Меня зовут @ibs_doc_bot. Я помогу тебе '
                           'справиться с повышенным газообразованием ;)\n  При '
                           'помощи поиска, категорий или общего списка ты  '
                           'найдешь информацию по большинству  продуктов -  '
                           'какие из них являются high-FODMAP, а какие '
                           'low-FODMAP, а также сколько можно чего съесть, '
                           'чтобы не вздуло. Если ты не знаешь что такое '
                           'low-FODMAP диета, то посмотри в справке или '
                           'подпишись на телеграм-канал @ibs_doc или '
                           'инстаграм\n https://instagram.com/ibs.doc\n Также '
                           'ты '
                           'можешь помочь в моем развитии, для этого есть удобная кнопка доната ;)'
                           '',
                           reply_markup=kb_client)
    print('Есть сообщение')
    print(message)

# async def get_photo_mes(photo: types.Message.photo):
#     print('есть фото')
#     print(photo)



async def donat_handler(message: types.Message):
    await bot.send_message(message.from_user.id,
                            text=link('Нажми сюда',
                                      'https://donate.stream/jarantat',
                                      ),
                           parse_mode='Markdown',
                           disable_web_page_preview=True)



def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(answer_and_qusetion, Text(equals=filter_list,
                                               ignore_case=True))


    dp.register_message_handler(donat_handler, Text(
                                                    equals=['Поддержать '
                                                            'проект'],
                                               ignore_case=True))

    dp.register_message_handler(start_mes)
#    dp.register_message_handler(get_photo_mes)


if __name__ == "__main__":
    print(filter_list)