#from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types

#создание клавиатуры с кнопками
b1 = types.KeyboardButton(text='Узнать о боте')
b2 = types.KeyboardButton(text='Поиск')
b3 = types.KeyboardButton(text='Категории продуктов')
b4 = types.KeyboardButton(text='Список продуктов')
b5 = types.KeyboardButton(text='Поддержать проект')


search_b1 = types.KeyboardButton(text='Искать')
search_b2 = types.KeyboardButton(text='Выйти из поиска')
#кнопки номера и локации(
# b4 =KeyboardButton('Поделиться номером', request_contact=True)
# b5 =KeyboardButton('Отправить где я', request_location=True)

#настройки клавиатуры
#one_time_keyboard=True для одноразового показа, но клавиатуру можно вернуть для
# полного удаления нужно в хендлере прописать reply_markup=ReplyKeyboardRemove()
kb_client = types.ReplyKeyboardMarkup(
    keyboard=[[b1, b2]],
    resize_keyboard=True,
    input_field_placeholder="Выберите способ подачи"
                                )

kb_search = types.ReplyKeyboardMarkup(
    keyboard=[[search_b1, search_b2]],
    resize_keyboard=True,
    input_field_placeholder="Выберите способ подачи"
                                )

#добавляет кнопку каждый раз с новой строки метод add
#.insert добавляет кнопку если есть место рядом
#.row(but1,but2...) медот добавляет все кнопки в строку

#kb_client.add(b1).add(b2).add(b3).add(b4).add(b5)
#kb_search.add(search_b2)
