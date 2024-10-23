import logging
from datetime import datetime
from typing import Dict, Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.exc import SQLAlchemyError

from models import Subscriber
from models import db

logger = logging.getLogger(__name__)


class CheckUserMiddleware(BaseMiddleware):
    """Work with user data in database"""

    def __init__(self) -> None:
        self.user = None

    async def is_user_in_db(self, user_id: int) -> bool:
        from models import Subscriber
        from models import db

        self.user = (db.query(Subscriber)
                     .filter(Subscriber.user_id == user_id)
                     .one_or_none())
        return self.user is not None

    async def add_user_to_db(self, user_id: int, user_name: str) -> None:
        """
        """
        user = Subscriber(
            user_id=user_id,
            user_name=user_name,
            last_use=datetime.utcnow(),
        )
        try:
            db.add(user)
            db.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error in addintion user in db {e}")
            return None
        self.user = user

    async def update_user_in_db(self, user: Subscriber) -> None:
        user.last_use = datetime.utcnow()
        try:
            db.merge(user)
            db.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error in updating user in db {e}")

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Any,
            data: Dict[str, Any]
    ) -> Any:

        if await self.is_user_in_db(user_id=event.from_user.id):
            await self.update_user_in_db(user=self.user)
        else:
            await self.add_user_to_db(user_id=event.from_user.id,
                                user_name=event.from_user.first_name)

        data['user'] = self.user
        return await handler(event, data)
