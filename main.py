import os

from aiogram.utils import executor
from aiogram.utils.executor import start_webhook
from colorama import Fore, Style
from dotenv import load_dotenv
from create_obj import dp, db_test_connect, bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware

load_dotenv()

DEBUG = os.getenv('DEBUG')
WEBAPP_HOST = os.getenv("WEBAPP_HOST")
WEBAPP_PORT = os.getenv("WEBAPP_PORT")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


async def on_startup(dp):
    print('Бот загрузился')
    print('Соединение с базой', (Fore.GREEN + Style.DIM + str(db_test_connect)) if
    db_test_connect else (Fore.RED + Style.DIM + str(db_test_connect)), Fore.RESET)
    print('Переменная DEBUG =' + str(DEBUG))
    if  DEBUG == False:
        print('set.webhook')
        await bot.set_webhook(WEBHOOK_URL)

    global kb_list


async def on_shutdown(dp):
    # logging.warning('Shutting down..')
    # insert code here to run it before shutdown
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()
    #logging.warning('Bye!')


from handlers import cliet_part, admin, other

cliet_part.register_handlers_client(dp)

admin.register_handlers_admin(dp)

# для записи сообщений которые не ловятся хенжлерами
# пустой хендлер должен быть последним
other.register_handlers_other(dp)

if DEBUG:
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup,
                           on_shutdown=on_shutdown)

else:
    start_webhook(
        dispatcher=dp,
        webhook_path='/',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
