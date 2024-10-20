#from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types
from create_obj import bot

#создание клавиатуры с кнопками
b1 = types.KeyboardButton(text='Узнать о боте')
b2 = types.KeyboardButton(text='Поиск')
b3 = types.KeyboardButton(text='Категории продуктов')
b4 = types.KeyboardButton(text='Список продуктов')
b5 = types.KeyboardButton(text='Поддержать проект')
b6 = types.KeyboardButton(text='Консультации')
b7 = types.KeyboardButton(text='Обратная связь')


search_b1 = types.KeyboardButton(text='Искать')
search_b2 = types.KeyboardButton(text='Выйти из поиска')
#кнопки номера и локации(
# b4 =KeyboardButton('Поделиться номером', request_contact=True)
# b5 =KeyboardButton('Отправить где я', request_location=True)

#настройки клавиатуры
#one_time_keyboard=True для одноразового показа, но клавиатуру можно вернуть для
# полного удаления нужно в хендлере прописать reply_markup=ReplyKeyboardRemove()
kb_client = types.ReplyKeyboardMarkup(
    keyboard=[[b1, b2],
              [b3, b4],
              [b5],
              [b6, b7],
              ],
    resize_keyboard=True,
    input_field_placeholder="Выберите способ подачи",

                                )

kb_search = types.ReplyKeyboardMarkup(
    keyboard=[
        [search_b1],
        [search_b2],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите способ подачи"
                                )

#добавляет кнопку каждый раз с новой строки метод add
#.insert добавляет кнопку если есть место рядом
#.row(but1,but2...) медот добавляет все кнопки в строку

#kb_client.add(b1).add(b2).add(b3).add(b4).add(b5)
#kb_search.add(search_b2)

def get_inline_search_kb(bot_info):
    #KB and butons for search
    #switch_inline_query_current_chat=bot_info.username,
    search_button = types.InlineKeyboardButton(
        text="Поиск",
        switch_inline_query_current_chat='',
    )
    inline_search_kb = types.InlineKeyboardMarkup(inline_keyboard=[[search_button]])
    return inline_search_kb
