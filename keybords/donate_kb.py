from aiogram import types
import os


button_data = {
    '100 руб.': os.getenv('PAY_LINK_100'),
    '200 руб.': os.getenv('PAY_LINK_200'),
    '300 руб.': os.getenv('PAY_LINK_300'),
    '400 руб.': os.getenv('PAY_LINK_400'),
    '500 руб.': os.getenv('PAY_LINK_500'),
    '600 руб.': os.getenv('PAY_LINK_600'),
    '5000 руб.': os.getenv('PAY_LINK_5000'),
}

buttons = []
for text, link in button_data.items():
    button = types.InlineKeyboardButton(text=text, url=link)
    buttons.append(button)

DONATE_KB = types.InlineKeyboardMarkup(
    resize_keyboard=True,
    inline_keyboard=[[buttons[x], buttons[x+1]] for x in range(0, len(buttons)-1,2)],
)
