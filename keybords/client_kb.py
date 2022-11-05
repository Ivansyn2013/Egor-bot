from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#создание клавиатуры с кнопками
b1 =KeyboardButton('/Старт')
b2 =KeyboardButton('/Поиск')
b3 =KeyboardButton('/Авторизация')
#кнопки номера и локации(
# b4 =KeyboardButton('Поделиться номером', request_contact=True)
# b5 =KeyboardButton('Отправить где я', request_location=True)

#настройки клавиатуры
#one_time_keyboard=True для одноразового показа, но клавиатуру можно вернуть для
# полного удаления нужно в хендлере прописать reply_markup=ReplyKeyboardRemove()
kb_client = ReplyKeyboardMarkup(resize_keyboard=True,
                                #one_time_keyboard=True
                                )

#добавляет кнопку каждый раз с новой строки метод add
#.insert добавляет кнопку если есть место рядом
#.row(but1,but2...) медот добавляет все кнопки в строку
kb_client.add(b1).add(b2).add(b3)