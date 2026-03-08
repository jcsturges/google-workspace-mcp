"""Tests for Docs service."""

from unittest.mock import patch

import pytest
from google_workspace_mcp.services.docs_service import DocsService


@pytest.mark.asyncio
class TestDocsService:
    """Test Docs service operations."""

    @patch("google_workspace_mcp.services.docs_service.get_oauth_handler")
    async def test_create_document(self, mock_get_oauth, mock_docs_service):
        """Test document creation."""
        mock_get_oauth.return_value.get_service.return_value = mock_docs_service

        service = DocsService()
        result = await service.create_document(title="Test Document")

        assert result["documentId"] == "doc1"
        assert result["title"] == "Test Document"
        assert mock_docs_service.documents().create.call_count >= 1

    @patch("google_workspace_mcp.services.docs_service.get_oauth_handler")
    async def test_read_document(self, mock_get_oauth, mock_docs_service):
        """Test document reading."""
        mock_get_oauth.return_value.get_service.return_value = mock_docs_service

        service = DocsService()
        result = await service.read_document(document_id="doc1")

        assert result["document_id"] == "doc1"
        assert result["title"] == "Test Document"
        assert "content" in result

    @patch("google_workspace_mcp.services.docs_service.get_oauth_handler")
    async def test_update_document(self, mock_get_oauth, mock_docs_service):
        """Test document update."""
        mock_get_oauth.return_value.get_service.return_value = mock_docs_service

        service = DocsService()
        await service.update_document(document_id="doc1", text="New content", index=1)

        assert mock_docs_service.documents().batchUpdate.call_count >= 1
