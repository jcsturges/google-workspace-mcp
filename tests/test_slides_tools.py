"""Tests for Slides tool functions."""

from unittest.mock import AsyncMock, patch

import pytest
from google_workspace_mcp.tools.slides_tools import (
    SlidesBatchUpdateInput,
    SlidesAddSlideInput,
    SlidesCreateInput,
    SlidesDeleteSlideInput,
    SlidesReadInput,
    slides_add_slide,
    slides_batch_update,
    slides_create,
    slides_delete_slide,
    slides_read,
)


@pytest.mark.asyncio
class TestSlidesTools:
    """Test Slides tool functions."""

    @patch("google_workspace_mcp.tools.slides_tools.slides_service")
    async def test_create_presentation(self, mock_service):
        """Test slides_create tool."""
        mock_service.create_presentation = AsyncMock(
            return_value={"presentationId": "pres1", "title": "Test Presentation"}
        )

        result = await slides_create(SlidesCreateInput(title="Test Presentation"))

        assert isinstance(result, str)
        assert "pres1" in result
        mock_service.create_presentation.assert_called_once_with(title="Test Presentation")

    @patch("google_workspace_mcp.tools.slides_tools.slides_service")
    async def test_create_presentation_error(self, mock_service):
        """Test slides_create error handling."""
        mock_service.create_presentation = AsyncMock(side_effect=Exception("API error"))

        result = await slides_create(SlidesCreateInput(title="Test Presentation"))

        assert isinstance(result, str)
        assert "error" in result.lower() or "Error" in result

    @patch("google_workspace_mcp.tools.slides_tools.slides_service")
    async def test_read_presentation(self, mock_service):
        """Test slides_read tool."""
        mock_service.read_presentation = AsyncMock(
            return_value={
                "presentation_id": "pres1",
                "title": "Test Presentation",
                "slide_count": 1,
                "content": "Slide content",
            }
        )

        result = await slides_read(SlidesReadInput(presentation_id="pres1"))

        assert isinstance(result, str)
        mock_service.read_presentation.assert_called_once()

    @patch("google_workspace_mcp.tools.slides_tools.slides_service")
    async def test_add_slide(self, mock_service):
        """Test slides_add_slide tool."""
        mock_service.add_slide = AsyncMock(
            return_value={"replies": [{"createSlide": {"objectId": "new_slide"}}]}
        )

        result = await slides_add_slide(SlidesAddSlideInput(presentation_id="pres1"))

        assert isinstance(result, str)
        mock_service.add_slide.assert_called_once()

    @patch("google_workspace_mcp.tools.slides_tools.slides_service")
    async def test_delete_slide(self, mock_service):
        """Test slides_delete_slide tool."""
        mock_service.delete_slide = AsyncMock(return_value=None)

        result = await slides_delete_slide(
            SlidesDeleteSlideInput(presentation_id="pres1", slide_id="slide1")
        )

        assert isinstance(result, str)
        mock_service.delete_slide.assert_called_once()

    @patch("google_workspace_mcp.tools.slides_tools.slides_service")
    async def test_batch_update(self, mock_service):
        """Test slides_batch_update tool."""
        mock_service.update_slide = AsyncMock(
            return_value={"replies": [{"createSlide": {"objectId": "new_slide"}}]}
        )

        result = await slides_batch_update(
            SlidesBatchUpdateInput(
                presentation_id="pres1",
                requests=[{"createSlide": {"insertionIndex": 1}}],
            )
        )

        assert isinstance(result, str)
        mock_service.update_slide.assert_called_once()
