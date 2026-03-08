"""Tests for Sheets service."""

from unittest.mock import patch

import pytest

from google_workspace_mcp.services.sheets_service import SheetsService


@pytest.mark.asyncio
class TestSheetsService:
    """Test Sheets service operations."""

    @patch("google_workspace_mcp.services.sheets_service.get_oauth_handler")
    async def test_create_spreadsheet(self, mock_get_oauth, mock_sheets_service):
        """Test spreadsheet creation."""
        mock_get_oauth.return_value.get_service.return_value = mock_sheets_service

        service = SheetsService()
        result = await service.create_spreadsheet(title="Test Sheet")

        assert result["spreadsheetId"] == "sheet1"
        assert result["properties"]["title"] == "Test Sheet"
        assert mock_sheets_service.spreadsheets().create.call_count >= 1

    @patch("google_workspace_mcp.services.sheets_service.get_oauth_handler")
    async def test_read_range(self, mock_get_oauth, mock_sheets_service):
        """Test reading a range."""
        mock_get_oauth.return_value.get_service.return_value = mock_sheets_service

        service = SheetsService()
        result = await service.read_range(spreadsheet_id="sheet1", range_name="Sheet1!A1:B2")

        assert "values" in result
        assert result["values"] == [["A1", "B1"], ["A2", "B2"]]

    @patch("google_workspace_mcp.services.sheets_service.get_oauth_handler")
    async def test_update_range(self, mock_get_oauth, mock_sheets_service):
        """Test updating a range."""
        mock_get_oauth.return_value.get_service.return_value = mock_sheets_service

        service = SheetsService()
        result = await service.update_range(
            spreadsheet_id="sheet1",
            range_name="Sheet1!A1:B2",
            values=[["A1", "B1"], ["A2", "B2"]],
        )

        assert result["updatedCells"] == 4
        assert mock_sheets_service.spreadsheets().values().update.call_count >= 1
