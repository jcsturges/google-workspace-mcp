"""Tests for Gmail tool functions."""

from unittest.mock import AsyncMock, patch

import pytest

from google_workspace_mcp.tools.gmail_tools import (
    GmailListLabelsInput,
    GmailModifyLabelsInput,
    GmailReadInput,
    GmailReplyInput,
    GmailSearchInput,
    GmailSendInput,
    gmail_list_labels,
    gmail_modify_labels,
    gmail_read_message,
    gmail_reply_message,
    gmail_search_messages,
    gmail_send_message,
)


@pytest.mark.asyncio
class TestGmailTools:
    """Test Gmail tool functions."""

    @patch("google_workspace_mcp.tools.gmail_tools.gmail_service")
    async def test_search_messages(self, mock_service):
        """Test gmail_search_messages tool."""
        mock_service.search_messages = AsyncMock(
            return_value=[
                {
                    "id": "msg1",
                    "threadId": "thread1",
                    "payload": {
                        "headers": [
                            {"name": "From", "value": "test@example.com"},
                            {"name": "Subject", "value": "Test Subject"},
                            {"name": "Date", "value": "2024-01-01"},
                        ]
                    },
                    "snippet": "Test snippet",
                }
            ]
        )

        result = await gmail_search_messages(GmailSearchInput(query="test"))

        assert isinstance(result, str)
        assert "msg1" in result
        mock_service.search_messages.assert_called_once()

    @patch("google_workspace_mcp.tools.gmail_tools.gmail_service")
    async def test_search_messages_no_results(self, mock_service):
        """Test gmail_search_messages with no results."""
        mock_service.search_messages = AsyncMock(return_value=[])

        result = await gmail_search_messages(GmailSearchInput(query="nonexistent"))

        assert isinstance(result, str)
        assert "No messages found" in result

    @patch("google_workspace_mcp.tools.gmail_tools.gmail_service")
    async def test_search_messages_error(self, mock_service):
        """Test gmail_search_messages error handling."""
        mock_service.search_messages = AsyncMock(side_effect=Exception("API error"))

        result = await gmail_search_messages(GmailSearchInput())

        assert isinstance(result, str)
        assert "error" in result.lower() or "Error" in result

    @patch("google_workspace_mcp.tools.gmail_tools.gmail_service")
    async def test_read_message(self, mock_service):
        """Test gmail_read_message tool."""
        mock_service.read_message = AsyncMock(
            return_value={
                "message_id": "msg1",
                "thread_id": "thread1",
                "headers": {
                    "From": "test@example.com",
                    "Subject": "Test Subject",
                    "Date": "2024-01-01",
                },
                "body": "Test body content",
                "labels": ["INBOX"],
            }
        )

        result = await gmail_read_message(GmailReadInput(message_id="msg1"))

        assert isinstance(result, str)
        mock_service.read_message.assert_called_once_with(message_id="msg1")

    @patch("google_workspace_mcp.tools.gmail_tools.gmail_service")
    async def test_send_message(self, mock_service):
        """Test gmail_send_message tool."""
        mock_service.send_message = AsyncMock(return_value={"id": "sent1", "threadId": "thread1"})

        result = await gmail_send_message(
            GmailSendInput(
                to="user@example.com",
                subject="Hello",
                body="Test message body",
            )
        )

        assert isinstance(result, str)
        mock_service.send_message.assert_called_once()

    @patch("google_workspace_mcp.tools.gmail_tools.gmail_service")
    async def test_reply_message(self, mock_service):
        """Test gmail_reply_message tool."""
        mock_service.reply_message = AsyncMock(return_value={"id": "reply1", "threadId": "thread1"})

        result = await gmail_reply_message(
            GmailReplyInput(message_id="msg1", body="Thanks for your email")
        )

        assert isinstance(result, str)
        mock_service.reply_message.assert_called_once()

    @patch("google_workspace_mcp.tools.gmail_tools.gmail_service")
    async def test_list_labels(self, mock_service):
        """Test gmail_list_labels tool."""
        mock_service.list_labels = AsyncMock(
            return_value=[
                {"id": "INBOX", "name": "INBOX"},
                {"id": "SENT", "name": "SENT"},
            ]
        )

        result = await gmail_list_labels(GmailListLabelsInput())

        assert isinstance(result, str)
        mock_service.list_labels.assert_called_once()

    @patch("google_workspace_mcp.tools.gmail_tools.gmail_service")
    async def test_modify_labels_add(self, mock_service):
        """Test gmail_modify_labels tool with add labels."""
        mock_service.modify_labels = AsyncMock(
            return_value={"id": "msg1", "labelIds": ["INBOX", "STARRED"]}
        )

        result = await gmail_modify_labels(
            GmailModifyLabelsInput(message_id="msg1", add_labels=["STARRED"])
        )

        assert isinstance(result, str)
        mock_service.modify_labels.assert_called_once()

    @patch("google_workspace_mcp.tools.gmail_tools.gmail_service")
    async def test_modify_labels_no_labels_error(self, mock_service):
        """Test gmail_modify_labels with no labels specified returns error."""
        result = await gmail_modify_labels(GmailModifyLabelsInput(message_id="msg1"))

        assert isinstance(result, str)
        assert "error" in result.lower() or "Error" in result
