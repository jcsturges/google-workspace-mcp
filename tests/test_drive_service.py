"""Tests for Drive service."""

from unittest.mock import patch

import pytest
from google_workspace_mcp.services.drive_service import DriveService


@pytest.mark.asyncio
class TestDriveService:
    """Test Drive service operations."""

    @patch("google_workspace_mcp.services.drive_service.get_oauth_handler")
    async def test_search_files(self, mock_get_oauth, mock_drive_service):
        """Test file search functionality."""
        mock_get_oauth.return_value.get_service.return_value = mock_drive_service

        service = DriveService()
        results = await service.search_files(query="test")

        assert len(results) == 1
        assert results[0]["name"] == "test.txt"
        assert mock_drive_service.files().list.call_count >= 1

    @patch("google_workspace_mcp.services.drive_service.get_oauth_handler")
    async def test_search_files_no_query(self, mock_get_oauth, mock_drive_service):
        """Test file search with no query."""
        mock_get_oauth.return_value.get_service.return_value = mock_drive_service

        service = DriveService()
        results = await service.search_files()

        assert isinstance(results, list)

    @patch("google_workspace_mcp.services.drive_service.get_oauth_handler")
    async def test_list_shared_drives(self, mock_get_oauth, mock_drive_service):
        """Test listing shared drives."""
        mock_get_oauth.return_value.get_service.return_value = mock_drive_service

        service = DriveService()
        result = await service.list_shared_drives()

        assert len(result) == 1
        assert result[0]["name"] == "Shared Drive"
        assert mock_drive_service.drives().list.call_count >= 1
