"""Tests for Sheets tool functions."""

from unittest.mock import AsyncMock, patch

import pytest
from google_workspace_mcp.tools.sheets_tools import (
    SheetsClearInput,
    SheetsCreateInput,
    SheetsReadInput,
    SheetsWriteInput,
    sheets_clear,
    sheets_create,
    sheets_read,
    sheets_write,
)


@pytest.mark.asyncio
class TestSheetsTools:
    """Test Sheets tool functions."""

    @patch("google_workspace_mcp.tools.sheets_tools.sheets_service")
    async def test_create_spreadsheet(self, mock_service):
        """Test sheets_create tool."""
        mock_service.create_spreadsheet = AsyncMock(
            return_value={
                "spreadsheetId": "sheet1",
                "properties": {"title": "Test Sheet"},
            }
        )

        result = await sheets_create(SheetsCreateInput(title="Test Sheet"))

        assert isinstance(result, str)
        assert "sheet1" in result
        mock_service.create_spreadsheet.assert_called_once_with(title="Test Sheet")

    @patch("google_workspace_mcp.tools.sheets_tools.sheets_service")
    async def test_create_spreadsheet_error(self, mock_service):
        """Test sheets_create error handling."""
        mock_service.create_spreadsheet = AsyncMock(side_effect=Exception("API error"))

        result = await sheets_create(SheetsCreateInput(title="Test Sheet"))

        assert isinstance(result, str)
        assert "error" in result.lower() or "Error" in result

    @patch("google_workspace_mcp.tools.sheets_tools.sheets_service")
    async def test_read_range(self, mock_service):
        """Test sheets_read tool."""
        mock_service.read_range = AsyncMock(
            return_value={
                "range": "Sheet1!A1:B2",
                "values": [["A1", "B1"], ["A2", "B2"]],
            }
        )

        result = await sheets_read(
            SheetsReadInput(spreadsheet_id="sheet1", range_name="Sheet1!A1:B2")
        )

        assert isinstance(result, str)
        mock_service.read_range.assert_called_once()

    @patch("google_workspace_mcp.tools.sheets_tools.sheets_service")
    async def test_read_range_no_data(self, mock_service):
        """Test sheets_read with no data."""
        mock_service.read_range = AsyncMock(return_value={"range": "Sheet1!A1:B2", "values": []})

        result = await sheets_read(
            SheetsReadInput(spreadsheet_id="sheet1", range_name="Sheet1!A1:B2")
        )

        assert isinstance(result, str)
        assert "No data" in result

    @patch("google_workspace_mcp.tools.sheets_tools.sheets_service")
    async def test_write_range(self, mock_service):
        """Test sheets_write tool."""
        mock_service.update_range = AsyncMock(
            return_value={"updatedCells": 4, "updatedRows": 2, "updatedColumns": 2}
        )

        result = await sheets_write(
            SheetsWriteInput(
                spreadsheet_id="sheet1",
                range_name="Sheet1!A1:B2",
                values=[["A1", "B1"], ["A2", "B2"]],
            )
        )

        assert isinstance(result, str)
        mock_service.update_range.assert_called_once()

    @patch("google_workspace_mcp.tools.sheets_tools.sheets_service")
    async def test_clear_range(self, mock_service):
        """Test sheets_clear tool."""
        mock_service.clear_range = AsyncMock(return_value=None)

        result = await sheets_clear(
            SheetsClearInput(spreadsheet_id="sheet1", range_name="Sheet1!A1:B2")
        )

        assert isinstance(result, str)
