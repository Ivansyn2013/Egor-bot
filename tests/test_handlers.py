import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from handlers.cliet_part import command_start


@pytest.mark.asyncio
async def test_command_start():
    # Mock message
    message = AsyncMock()
    message.from_user.id = 12345
    message.delete = AsyncMock()

    # Mock bot and MAIN_MENU_ANSWERS
    with (
        patch("handlers.cliet_part.bot") as mock_bot,
        patch("handlers.cliet_part.MAIN_MENU_ANSWERS", {"Start message": "Hello!"}),
        patch("handlers.cliet_part.kb_client", MagicMock()) as mock_kb,
    ):
        mock_bot.send_message = AsyncMock()

        # Call the handler
        await command_start(message)

        # Check if bot.send_message was called with correct parameters
        mock_bot.send_message.assert_called_once_with(
            12345, "Hello!", reply_markup=mock_kb
        )
        # Check if message.delete was called
        message.delete.assert_called_once()


@pytest.mark.asyncio
async def test_command_start_exception():
    # Mock message
    message = AsyncMock()
    message.from_user.id = 12345
    message.reply = AsyncMock()

    # Mock bot to raise an exception
    with patch("handlers.cliet_part.bot") as mock_bot:
        mock_bot.send_message.side_effect = Exception("Bot blocked")

        # Call the handler
        await command_start(message)

        # Check if message.reply was called as a fallback
        message.reply.assert_called_once_with("Напишите боту в ЛС")
