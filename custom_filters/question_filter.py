from aiogram.filters import BaseFilter
from aiogram.types import Message

class QuestionFilter(BaseFilter):
    """Filter for handling info about bot"""
    from features.answer_and_question import STR_ANSWER_AND_QUESTION

    async def __call__(self, message: Message) -> bool:
        return message.text in self.STR_ANSWER_AND_QUESTION
