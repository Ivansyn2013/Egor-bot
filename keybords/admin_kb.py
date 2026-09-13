from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load = KeyboardButton(text='/Load')
button_delete = KeyboardButton(text="/Delete")
button_show = KeyboardButton(text="/Show")
button_ok = KeyboardButton(text="/OK")
button_notok = KeyboardButton(text="/NOT OK")

button_send_message = KeyboardButton(text="/Отправить сообщение",)

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

ADMIN_KB_SENDMESSAGE = ReplyKeyboardMarkup(
    keyboard=[[button_send_message]],
    resize_keyboard=True,
    one_time_keyboard=True
)