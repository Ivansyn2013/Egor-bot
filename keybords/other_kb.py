from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from features.answer_and_question import STR_ANSWER_AND_QUESTION

kb_answer_and_qusetion = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
b_quit = KeyboardButton('Назад')

for quest, answer in STR_ANSWER_AND_QUESTION.items():
    b = KeyboardButton(f'{quest}')
    kb_answer_and_qusetion.add(b)

kb_answer_and_qusetion.add(b_quit)