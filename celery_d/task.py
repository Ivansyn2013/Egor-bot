from logging import getLogger
import asyncio

from lazy_object_proxy.utils import await_

from celery_app import app
from create_obj import bot

logger = getLogger(__name__)


async def send_message_to_user(user_id: int, message: str):
    try:
        await bot.send_message(chat_id=user_id, text=message)
        return True
    except Exception as e:
        logger.warning(f"Failed to send to {user_id}: {e}")
        return False


@app.task
async def broadcast_message(user_ids: list, message: str):
    loop = asyncio.get_event_loop()
    results = []
    for user_id in user_ids:
        result = loop.run_until_complete(send_message_to_user(user_id, message))
        results.append(result)
        await asyncio.sleep(0.2)  # Задержка между отправками, чтобы не спамить
    return results
