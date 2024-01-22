from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load = KeyboardButton(text='/Load')
button_delete = KeyboardButton(text="/Delete")
button_show = KeyboardButton(text="/Show")
button_ok = KeyboardButton(text="/OK")
button_notok = KeyboardButton(text="/NOT OK")

buttons = [button_ok, button_delete, button_show, button_notok]
button_case_admin = ReplyKeyboardMarkup(
    keyboard=[buttons],
    resize_keyboard=True,
    one_time_keyboard=True
                                        )

admin_kb_check = ReplyKeyboardMarkup(
    keyboard=[buttons],
    resize_keyboard=True,
    one_time_keyboard=True
                                     )
