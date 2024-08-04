import asyncio
import logging
import re
from datetime import datetime

from aiogram import Bot, Dispatcher, html, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile, LinkPreviewOptions
from aiogram.utils.formatting import as_list, as_marked_section, Bold, as_key_value, HashTag
from aiogram.utils.markdown import hide_link
from aiogram.utils.media_group import MediaGroupBuilder



#@dp.message(Command("advanced_example"))
async def cmd_advanced_example(message: Message):
    content = as_list(
        as_marked_section(
            Bold("Success:"),
            "Test 1",
            "Test 3",
            "Test 4",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Failed:"),
            "Test 2",
            marker="❌ ",
        ),
        as_marked_section(
            Bold("Summary:"),
            as_key_value("Total", 4),
            as_key_value("Success", 3),
            as_key_value("Failed", 1),
            marker="  ",
        ),
        HashTag("#test"),
        sep="\n\n",
    )
    await message.answer(**content.as_kwargs())

def register_tmp_handlers(dp: Dispatcher) -> None:
    dp.message.register(cmd_advanced_example, Command("advanced_example"))
