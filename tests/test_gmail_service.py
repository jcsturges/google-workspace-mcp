"""Tests for Gmail service."""

from unittest.mock import patch

import pytest

from google_workspace_mcp.services.gmail_service import GmailService


@pytest.mark.asyncio
class TestGmailService:
    """Test Gmail service operations."""

    @patch("google_workspace_mcp.services.gmail_service.get_oauth_handler")
    async def test_search_messages(self, mock_get_oauth, mock_gmail_service):
        """Test message search."""
        mock_get_oauth.return_value.get_service.return_value = mock_gmail_service

        service = GmailService()
        results = await service.search_messages(query="test")

        assert len(results) >= 1
        assert mock_gmail_service.users().messages().list.call_count >= 1

    @patch("google_workspace_mcp.services.gmail_service.get_oauth_handler")
    async def test_read_message(self, mock_get_oauth, mock_gmail_service):
        """Test reading a message."""
        mock_get_oauth.return_value.get_service.return_value = mock_gmail_service

        service = GmailService()
        result = await service.read_message(message_id="msg1")

        assert "message_id" in result
        assert result["message_id"] == "msg1"

    @patch("google_workspace_mcp.services.gmail_service.get_oauth_handler")
    async def test_list_labels(self, mock_get_oauth, mock_gmail_service):
        """Test listing labels."""
        mock_get_oauth.return_value.get_service.return_value = mock_gmail_service

        service = GmailService()
        result = await service.list_labels()

        assert len(result) == 2
        assert result[0]["id"] == "INBOX"
        assert mock_gmail_service.users().labels().list.call_count >= 1
