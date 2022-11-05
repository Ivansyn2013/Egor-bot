from aiogram.utils import executor
from create_obj import dp, bot

async def on_startup(_):
    print('Бот загрузился')

from handlers import cliet_part, admin, other

cliet_part.register_handlers_client(dp)

#пустой хендлер должен быть последним
#other.register_handlers_other(dp)




executor.start_polling(dp, skip_updates=True)