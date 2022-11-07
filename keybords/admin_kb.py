from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load = KeyboardButton('/Load')
button_delete =KeyboardButton("/Delete")
button_delete =KeyboardButton("/Show")

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True
                                        ).add(button_load)\
                                        .add(button_delete)\
                                        .add(button_delete)
