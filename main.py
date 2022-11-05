from aiogram.utils import executor
from create_obj import dp, bot

async def on_startup():
    print('Бот загрузился')





executor.start_polling(dp, skip_updates=True)