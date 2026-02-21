import logging
import os
import asyncio
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, \
    setup_application
from aiohttp import web
import aiohttp_cors
from colorama import Fore, Style
from dotenv import load_dotenv

from create_obj import bot, db_test_connect, dp

load_dotenv()

DEBUG = os.getenv("DEBUG")

WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = os.getenv("WEB_SERVER_PORT")

WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PORT = os.getenv("WEBHOOK_PORT")
WEBHOOK_SSL_CERT = os.getenv("WEBHOOK_SSL_CERT")
WEBHOOK_SSL_PRIV = os.getenv("WEBHOOK_SSL_PRIV")

logger = logging.getLogger(__name__)


async def on_startup():
    global kb_list

    logger.info("Бот загрузился")
    logger.info(
        "Соединение с базой" + f"{Fore.GREEN}{Style.DIM}{str(db_test_connect)}"
        if db_test_connect
        else f"{Fore.RED}{Style.DIM}{str(db_test_connect)}" + Fore.RESET
    )
    logger.debug("Переменная DEBUG =" + str(DEBUG))

    # dp.outer_middleware.setup(CheckUserMiddleware())
    if DEBUG == "False":
        logger.info("Webhook mode start set.webhook")
        logger.info(f"Set webhook: {WEBHOOK_URL}:{WEBHOOK_PORT}{WEBHOOK_PATH}")
        await bot.set_webhook(
            f"{WEBHOOK_URL}:{WEBHOOK_PORT}{WEBHOOK_PATH}",
            secret_token=WEBHOOK_SECRET,
            drop_pending_updates=True,
        )


async def on_shutdown():
    logging.info("Shutting down..")
    # insert code here to run it before shutdown
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.info("Bye!")


from handlers import admin, cliet_part, inline_mode, other
from acces_reader.mysql_connet_connector import db_mysql_all_products, db_mysql_category_request

async def api_get_products(request):
    products_dict = await db_mysql_all_products()
    if products_dict is None:
        return web.json_response({"error": "Failed to fetch products"}, status=500)
    
    # Transform dict {name: id} to list of objects for frontend compatibility
    # Frontend expects: { id, name, category, status, description, image, ... }
    # For now, we provide what we have and let frontend handle it or expand later.
    products_list = []
    # Fetch categories to map them
    categories_map = await db_mysql_category_request() or {}
    # categories_map is {category_name: [product_id1, product_id2, ...]}
    
    # Inverse map for easy lookup: {product_id: category_name}
    id_to_cat = {}
    for cat_name, ids in categories_map.items():
        clean_cat_name = str(cat_name).replace("\t", "").strip()
        for pid in ids:
            id_to_cat[pid] = clean_cat_name

    # We also need fodmap status for the frontend
    # Since we can't easily get it for all products with existing functions without many queries,
    # we use a default for now. Ideally, we should add a specialized function to mysql_connet_connector.py
    for name, product_id in products_dict.items():
        products_list.append({
            "id": str(product_id), # Ensure string for comparison
            "name": name,
            "category": id_to_cat.get(product_id, "Other"),
            "status": "low" # Default to 'low' for visual testing, or 'unknown'
        })
    return web.json_response(products_list)

async def api_get_categories(request):
    categories = await db_mysql_category_request()
    if categories is None:
        return web.json_response({"error": "Failed to fetch categories"}, status=500)
    return web.json_response(categories)

cliet_part.register_handlers_client(dp)

admin.register_handlers_admin(dp)

inline_mode.register_handlers_inline(dp)

# для записи сообщений которые не ловятся хенжлерами
# пустой хендлер должен быть последним
other.register_handlers_other(dp)


# tmp.register_tmp_handlers(dp)


async def main():
    if DEBUG != "False":
        logging.basicConfig(level=logging.DEBUG)
        logging.warning("Режим pollong")
        
        # Start a separate web server for API in polling mode
        app = web.Application()
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })
        resource_products = cors.add(app.router.add_resource("/api/products"))
        cors.add(resource_products.add_route("GET", api_get_products))
        resource_categories = cors.add(app.router.add_resource("/api/categories"))
        cors.add(resource_categories.add_route("GET", api_get_categories))
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 8080)
        await site.start()
        logging.info("API server started on http://0.0.0.0:8080")

        await dp.start_polling(
            bot,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown
        )
    else:
        logging.basicConfig(level=logging.INFO)
        logging.warning("Режим webhook")

        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        app = web.Application()

        # Configure CORS
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        # Register API routes
        resource_products = cors.add(app.router.add_resource("/api/products"))
        cors.add(resource_products.add_route("GET", api_get_products))
        
        resource_categories = cors.add(app.router.add_resource("/api/categories"))
        cors.add(resource_categories.add_route("GET", api_get_categories))

        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET
        )
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        try:
            web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
        except Exception as e:
            logger.error(e)
            logger.error(f" host={WEB_SERVER_HOST}")
            logger.error(f" port{WEB_SERVER_PORT}")
            logger.error(f" path={WEBHOOK_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
