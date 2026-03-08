"""Tests for Slides service."""

from unittest.mock import patch

import pytest
from google_workspace_mcp.services.slides_service import SlidesService


@pytest.mark.asyncio
class TestSlidesService:
    """Test Slides service operations."""

    @patch("google_workspace_mcp.services.slides_service.get_oauth_handler")
    async def test_create_presentation(self, mock_get_oauth, mock_slides_service):
        """Test presentation creation."""
        mock_get_oauth.return_value.get_service.return_value = mock_slides_service

        service = SlidesService()
        result = await service.create_presentation(title="Test Presentation")

        assert result["presentationId"] == "pres1"
        assert mock_slides_service.presentations().create.call_count >= 1

    @patch("google_workspace_mcp.services.slides_service.get_oauth_handler")
    async def test_read_presentation(self, mock_get_oauth, mock_slides_service):
        """Test reading a presentation."""
        mock_get_oauth.return_value.get_service.return_value = mock_slides_service

        service = SlidesService()
        result = await service.read_presentation(presentation_id="pres1")

        assert "presentation_id" in result
        assert result["presentation_id"] == "pres1"

    @patch("google_workspace_mcp.services.slides_service.get_oauth_handler")
    async def test_add_slide(self, mock_get_oauth, mock_slides_service):
        """Test adding a slide."""
        mock_get_oauth.return_value.get_service.return_value = mock_slides_service

        service = SlidesService()
        result = await service.add_slide(presentation_id="pres1")

        assert "replies" in result
        assert mock_slides_service.presentations().batchUpdate.call_count >= 1
