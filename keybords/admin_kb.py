from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load = KeyboardButton('/Load')
button_delete = KeyboardButton("/Delete")
button_delete = KeyboardButton("/Show")
button_ok = KeyboardButton("/OK")
button_notok = KeyboardButton("/NOT OK")

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True
                                        ).add(button_load) \
    .add(button_delete) \
    .add(button_delete)

admin_kb_check = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True
                                     ).add(button_ok) \
    .add(button_notok)
