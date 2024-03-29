from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#создание клавиатуры с кнопками
b1 =KeyboardButton('Узнать о боте')
b2 =KeyboardButton('Поиск')
b3 =KeyboardButton('Категории продуктов')
b4 = KeyboardButton('Список продуктов')
b5 = KeyboardButton('Поддержать проект')


search_b1 = KeyboardButton('Искать')
search_b2 = KeyboardButton('Выйти из поиска')
#кнопки номера и локации(
# b4 =KeyboardButton('Поделиться номером', request_contact=True)
# b5 =KeyboardButton('Отправить где я', request_location=True)

#настройки клавиатуры
#one_time_keyboard=True для одноразового показа, но клавиатуру можно вернуть для
# полного удаления нужно в хендлере прописать reply_markup=ReplyKeyboardRemove()
kb_client = ReplyKeyboardMarkup(resize_keyboard=True,
                                #one_time_keyboard=True
                                )

kb_search = ReplyKeyboardMarkup(resize_keyboard=True,
                                )

#добавляет кнопку каждый раз с новой строки метод add
#.insert добавляет кнопку если есть место рядом
#.row(but1,but2...) медот добавляет все кнопки в строку

kb_client.add(b1).add(b2).add(b3).add(b4).add(b5)
kb_search.add(search_b2)
