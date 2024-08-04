import json
import string

from aiogram import Dispatcher, Router
from aiogram import F
from aiogram import types

from create_obj import bot
from keybords import kb_client, kb_answer_and_qusetion
from custom_filters import QuestionFilter

# from aiogram.dispatcher.filters import Text

router = Router()


# @dp.message_handler()
async def cenz_filter(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
        message.text.split(' ')}.intersection(
        set(json.load(open('cenz\cenz.json')))) != set():
        await message.reply("Мат запрещен")
        await message.delete()


@router.message(QuestionFilter())
async def answer_and_question(message: types.Message):
    from features.answer_and_question import STR_ANSWER_AND_QUESTION
    if message.text == 'Узнать о боте':
        await message.reply('Инфо', reply_markup=kb_answer_and_qusetion)
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


async def donat_handler(message: types.Message):
    '''Хендоер доната, пошлем клавиатуру со ссылками'''
    from keybords import DONATE_KB
    await message.answer('Донат',
                         reply_markup=DONATE_KB)

async def back_handler(message: types.Message):
    '''Gor back button'''
    await message.reply('Назад', reply_markup=kb_client)


def register_handlers_other(dp: Dispatcher):
    dp.message.register(answer_and_question, F.text.lower() == 'узнать о боте')

    dp.message.register(donat_handler, F.text.lower() == 'поддержать проект')
    dp.message.register(back_handler, F.text.lower() == 'назад')
    dp.include_router(router)

    # dp.message.register(start_mes) пустой


if __name__ == "__main__":
    print()
