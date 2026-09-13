import json
import string

from aiogram import Dispatcher, Router
from aiogram import F
from aiogram import types

from create_obj import bot
from keybords import kb_client, kb_answer_and_qusetion
from custom_filters import QuestionFilter
from features.answer_and_question import MAIN_MENU_ANSWERS

# from aiogram.dispatcher.filters import Text

router = Router()

@router.message(QuestionFilter())
async def answer_and_question(message: types.Message):
    from features.answer_and_question import STR_ANSWER_AND_QUESTION
    if message.text == 'Узнать о боте':
        await message.reply(MAIN_MENU_ANSWERS['Start message'], reply_markup=kb_answer_and_qusetion)
    if message.text in STR_ANSWER_AND_QUESTION.keys():
        await message.reply(f'{STR_ANSWER_AND_QUESTION[message.text]}',
                            reply_markup=kb_answer_and_qusetion,
                            parse_mode='html')


async def donat_handler(message: types.Message):
    """Хендолер доната, пошлем клавиатуру со ссылками"""
    from keybords import DONATE_KB
    await message.answer('Донат',
                         reply_markup=DONATE_KB)

async def back_handler(message: types.Message):
    """Gor back button"""
    await message.reply('Назад', reply_markup=kb_client)

@router.message(F.text.in_(list(MAIN_MENU_ANSWERS.keys())))
async def consultations_handler(message: types.Message):
    await message.reply(MAIN_MENU_ANSWERS[message.text],
                        reply_markup=kb_client)

def register_handlers_other(dp: Dispatcher):
    dp.message.register(answer_and_question, F.text.lower() == 'узнать о боте')
    dp.message.register(donat_handler, F.text.lower() == 'поддержать проект')
    dp.message.register(back_handler, F.text.lower() == 'назад')
    dp.include_router(router)

