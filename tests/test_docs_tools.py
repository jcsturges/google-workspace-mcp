"""Tests for Docs tool functions."""

from unittest.mock import AsyncMock, patch

import pytest
from google_workspace_mcp.tools.docs_tools import (
    DocsCreateInput,
    DocsDeleteInput,
    DocsReadInput,
    DocsUpdateInput,
    docs_create,
    docs_delete,
    docs_read,
    docs_update,
)


@pytest.mark.asyncio
class TestDocsTools:
    """Test Docs tool functions."""

    @patch("google_workspace_mcp.tools.docs_tools.docs_service")
    async def test_create_document(self, mock_service):
        """Test docs_create tool."""
        mock_service.create_document = AsyncMock(
            return_value={"documentId": "doc1", "title": "Test Doc"}
        )

        result = await docs_create(DocsCreateInput(title="Test Doc"))

        assert isinstance(result, str)
        assert "doc1" in result
        mock_service.create_document.assert_called_once_with(title="Test Doc")

    @patch("google_workspace_mcp.tools.docs_tools.docs_service")
    async def test_create_document_error(self, mock_service):
        """Test docs_create error handling."""
        mock_service.create_document = AsyncMock(side_effect=Exception("API error"))

        result = await docs_create(DocsCreateInput(title="Test Doc"))

        assert isinstance(result, str)
        assert "error" in result.lower() or "Error" in result

    @patch("google_workspace_mcp.tools.docs_tools.docs_service")
    async def test_read_document(self, mock_service):
        """Test docs_read tool."""
        mock_service.read_document = AsyncMock(
            return_value={
                "document_id": "doc1",
                "title": "Test Doc",
                "content": "Hello world",
            }
        )

        result = await docs_read(
            DocsReadInput(file_id="doc1", document_id="doc1")
        )

        assert isinstance(result, str)
        mock_service.read_document.assert_called_once()

    @patch("google_workspace_mcp.tools.docs_tools.docs_service")
    async def test_update_document(self, mock_service):
        """Test docs_update tool."""
        mock_service.update_document = AsyncMock(return_value=None)

        result = await docs_update(
            DocsUpdateInput(file_id="doc1", document_id="doc1", text="New content")
        )

        assert isinstance(result, str)
        mock_service.update_document.assert_called_once()

    @patch("google_workspace_mcp.tools.docs_tools.docs_service")
    async def test_delete_document(self, mock_service):
        """Test docs_delete tool."""
        mock_service.delete_document = AsyncMock(return_value=None)

        result = await docs_delete(
            DocsDeleteInput(file_id="doc1", document_id="doc1")
        )

        assert isinstance(result, str)
        mock_service.delete_document.assert_called_once_with(document_id="doc1")
