from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from features.answer_and_question import STR_ANSWER_AND_QUESTION


b_quit = KeyboardButton(text='Назад')

buttons = []
for quest, answer in STR_ANSWER_AND_QUESTION.items():
    b = KeyboardButton(text=f'{quest}')
    buttons.append(b)

buttons.append(b_quit)

kb_answer_and_qusetion = ReplyKeyboardMarkup(
    keyboard=[buttons],
    row_width=1,
    resize_keyboard=True
)