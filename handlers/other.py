import json
import string

from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

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



async def test_mes(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Привет! Егор большой борец за здоровье нас и нашей планеты, '
                           'он попросил меня помочь ему снизить выделение парниковых '
                           'газов!\nВот что я могу:\n'
                           'Список продуктов: покажет продукты, о которых я знаю\n'
                           'Поиск по продуктам: нажми поиск и отправь название '
                           'продукта, что бы получить информацию, если я сразу не '
                           'пойму, что это, то предложу что-нибудь \n'
                           'Набери "отмена" в любом меню, что бы вернуться в главное \n'
                           ' \n'
                           '',
                           reply_markup=kb_client)
    print('Есть сообщение')
    print(message.text)
    with open("log.txt", 'a+', encoding='utf-8') as f:
        f.write(message.date.ctime())
        f.write(message.from_user.username)
        f.write(f': {message.text}')
        f.write('\n')


# @dp.message_handler() эхо
# async def echo_send(message: types.Message):
#     await message.answer(message.text)
#     await message.reply(message.text)
#     await bot.send_message(message.from_user.id, message.text)

#dp.register_message_handler(test_mes)

def register_handlers_other(dp: Dispatcher):
    # dp.register_message_handler(echo_send)
    dp.register_message_handler(answer_and_qusetion, Text(equals=filter_list,
                                               ignore_case=True))

    dp.register_message_handler(test_mes)


if __name__ == "__main__":
    print(filter_list)