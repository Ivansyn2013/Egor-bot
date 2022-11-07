from aiogram import types
from aiogram.utils import executor

from create_obj import dp, bot
from sql_bd import sql_start


async def on_startup(_):
    print('Бот загрузился')
    sql_start()


from handlers import cliet_part, admin, other

cliet_part.register_handlers_client(dp)

admin.register_handlers_admin(dp)

# для записи сообщений которые не ловятся хенжлерами
# пустой хендлер должен быть последним
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
