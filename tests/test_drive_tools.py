"""Tests for Drive tool functions."""

from unittest.mock import AsyncMock, patch

import pytest

from google_workspace_mcp.tools.drive_tools import (
    DriveCreateFileInput,
    DriveDeleteFileInput,
    DriveDownloadFileInput,
    DriveListSharedDrivesInput,
    DriveReadFileInput,
    DriveSearchInput,
    DriveUpdateFileInput,
    DriveUploadFileInput,
    drive_create_file,
    drive_delete_file,
    drive_download_file,
    drive_list_shared_drives,
    drive_read_file,
    drive_search_files,
    drive_update_file,
    drive_upload_file,
)


@pytest.mark.asyncio
class TestDriveTools:
    """Test Drive tool functions."""

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_search_files(self, mock_service):
        """Test drive_search_files tool."""
        mock_service.search_files = AsyncMock(
            return_value=[{"id": "file1", "name": "test.txt", "mimeType": "text/plain"}]
        )

        result = await drive_search_files(DriveSearchInput(query="test"))

        assert isinstance(result, str)
        mock_service.search_files.assert_called_once()

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_search_files_no_results(self, mock_service):
        """Test drive_search_files with no results."""
        mock_service.search_files = AsyncMock(return_value=[])

        result = await drive_search_files(DriveSearchInput(query="nonexistent"))

        assert isinstance(result, str)
        assert "No files found" in result

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_search_files_error(self, mock_service):
        """Test drive_search_files error handling."""
        mock_service.search_files = AsyncMock(side_effect=Exception("API error"))

        result = await drive_search_files(DriveSearchInput(query="test"))

        assert isinstance(result, str)
        assert "error" in result.lower() or "Error" in result

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_read_file(self, mock_service):
        """Test drive_read_file tool."""
        mock_service.read_file = AsyncMock(
            return_value={
                "metadata": {"id": "file1", "name": "test.txt", "mimeType": "text/plain"},
                "content": "Test content",
            }
        )

        result = await drive_read_file(DriveReadFileInput(file_id="file1"))

        assert isinstance(result, str)
        mock_service.read_file.assert_called_once()

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_create_file(self, mock_service):
        """Test drive_create_file tool."""
        mock_service.create_file = AsyncMock(
            return_value={"id": "new_file", "name": "new.txt", "mimeType": "text/plain"}
        )

        result = await drive_create_file(DriveCreateFileInput(name="new.txt", content="content"))

        assert isinstance(result, str)
        mock_service.create_file.assert_called_once()

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_update_file(self, mock_service):
        """Test drive_update_file tool."""
        mock_service.update_file = AsyncMock(return_value={"id": "file1", "name": "updated.txt"})

        result = await drive_update_file(
            DriveUpdateFileInput(file_id="file1", content="new content")
        )

        assert isinstance(result, str)
        mock_service.update_file.assert_called_once()

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_update_file_no_content_or_name(self, mock_service):
        """Test drive_update_file with no content or name returns error."""
        result = await drive_update_file(DriveUpdateFileInput(file_id="file1"))

        assert isinstance(result, str)
        assert "error" in result.lower() or "Error" in result

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_delete_file(self, mock_service):
        """Test drive_delete_file tool."""
        mock_service.delete_file = AsyncMock(return_value=None)

        result = await drive_delete_file(DriveDeleteFileInput(file_id="file1"))

        assert isinstance(result, str)
        mock_service.delete_file.assert_called_once_with("file1")

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_upload_file(self, mock_service):
        """Test drive_upload_file tool."""
        mock_service.upload_file = AsyncMock(
            return_value={"id": "uploaded1", "name": "test.pdf", "size": "1024"}
        )

        result = await drive_upload_file(DriveUploadFileInput(local_path="/tmp/test.pdf"))

        assert isinstance(result, str)
        mock_service.upload_file.assert_called_once()

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_download_file(self, mock_service):
        """Test drive_download_file tool."""
        mock_service.download_file = AsyncMock(return_value={"size": 1024})

        result = await drive_download_file(
            DriveDownloadFileInput(file_id="file1", local_path="/tmp/test.txt")
        )

        assert isinstance(result, str)
        mock_service.download_file.assert_called_once()

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_list_shared_drives(self, mock_service):
        """Test drive_list_shared_drives tool."""
        mock_service.list_shared_drives = AsyncMock(
            return_value=[{"id": "drive1", "name": "Shared Drive"}]
        )

        result = await drive_list_shared_drives(DriveListSharedDrivesInput())

        assert isinstance(result, str)
        mock_service.list_shared_drives.assert_called_once()

    @patch("google_workspace_mcp.tools.drive_tools.drive_service")
    async def test_list_shared_drives_empty(self, mock_service):
        """Test drive_list_shared_drives with no drives."""
        mock_service.list_shared_drives = AsyncMock(return_value=[])

        result = await drive_list_shared_drives(DriveListSharedDrivesInput())

        assert isinstance(result, str)
        assert "No shared drives" in result
