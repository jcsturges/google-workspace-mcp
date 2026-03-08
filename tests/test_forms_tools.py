"""Tests for Forms tool functions."""

from unittest.mock import AsyncMock, patch

import pytest

from google_workspace_mcp.tools.forms_tools import (
    FormsCreateInput,
    FormsDeleteInput,
    FormsGetResponsesInput,
    FormsReadInput,
    FormsUpdateInput,
    forms_create,
    forms_delete,
    forms_get_responses,
    forms_read,
    forms_update,
)


@pytest.mark.asyncio
class TestFormsTools:
    """Test Forms tool functions."""

    @patch("google_workspace_mcp.tools.forms_tools.forms_service")
    async def test_create_form(self, mock_service):
        """Test forms_create tool."""
        mock_service.create_form = AsyncMock(
            return_value={"formId": "form1", "info": {"title": "Test Form"}}
        )

        result = await forms_create(FormsCreateInput(title="Test Form"))

        assert isinstance(result, str)
        assert "form1" in result
        mock_service.create_form.assert_called_once()

    @patch("google_workspace_mcp.tools.forms_tools.forms_service")
    async def test_create_form_error(self, mock_service):
        """Test forms_create error handling."""
        mock_service.create_form = AsyncMock(side_effect=Exception("API error"))

        result = await forms_create(FormsCreateInput(title="Test Form"))

        assert isinstance(result, str)
        assert "error" in result.lower() or "Error" in result

    @patch("google_workspace_mcp.tools.forms_tools.forms_service")
    async def test_read_form(self, mock_service):
        """Test forms_read tool."""
        mock_service.read_form = AsyncMock(
            return_value={
                "form_id": "form1",
                "title": "Test Form",
                "item_count": 0,
                "items": [],
            }
        )

        result = await forms_read(FormsReadInput(form_id="form1"))

        assert isinstance(result, str)
        mock_service.read_form.assert_called_once_with(form_id="form1")

    @patch("google_workspace_mcp.tools.forms_tools.forms_service")
    async def test_update_form(self, mock_service):
        """Test forms_update tool."""
        mock_service.update_form = AsyncMock(return_value=None)

        result = await forms_update(
            FormsUpdateInput(
                form_id="form1",
                requests=[{"createItem": {"item": {"title": "Q1"}, "location": {"index": 0}}}],
            )
        )

        assert isinstance(result, str)
        mock_service.update_form.assert_called_once()

    @patch("google_workspace_mcp.tools.forms_tools.forms_service")
    async def test_delete_form(self, mock_service):
        """Test forms_delete tool."""
        mock_service.delete_form = AsyncMock(return_value=None)

        result = await forms_delete(FormsDeleteInput(form_id="form1"))

        assert isinstance(result, str)
        mock_service.delete_form.assert_called_once_with(form_id="form1")

    @patch("google_workspace_mcp.tools.forms_tools.forms_service")
    async def test_get_responses(self, mock_service):
        """Test forms_get_responses tool."""
        mock_service.get_responses = AsyncMock(
            return_value={"form_id": "form1", "response_count": 0, "responses": []}
        )

        result = await forms_get_responses(FormsGetResponsesInput(form_id="form1"))

        assert isinstance(result, str)
        mock_service.get_responses.assert_called_once_with(form_id="form1")
