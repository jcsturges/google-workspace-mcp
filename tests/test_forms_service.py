"""Tests for Forms service."""

from unittest.mock import patch

import pytest

from google_workspace_mcp.services.forms_service import FormsService


@pytest.mark.asyncio
class TestFormsService:
    """Test Forms service operations."""

    @patch("google_workspace_mcp.services.forms_service.get_oauth_handler")
    async def test_create_form(self, mock_get_oauth, mock_forms_service):
        """Test form creation."""
        mock_get_oauth.return_value.get_service.return_value = mock_forms_service

        service = FormsService()
        result = await service.create_form(title="Test Form")

        assert result["formId"] == "form1"
        assert result["info"]["title"] == "Test Form"
        assert mock_forms_service.forms().create.call_count >= 1

    @patch("google_workspace_mcp.services.forms_service.get_oauth_handler")
    async def test_read_form(self, mock_get_oauth, mock_forms_service):
        """Test reading a form."""
        mock_get_oauth.return_value.get_service.return_value = mock_forms_service

        service = FormsService()
        result = await service.read_form(form_id="form1")

        assert "form_id" in result
        assert result["form_id"] == "form1"

    @patch("google_workspace_mcp.services.forms_service.get_oauth_handler")
    async def test_get_responses(self, mock_get_oauth, mock_forms_service):
        """Test getting form responses."""
        mock_get_oauth.return_value.get_service.return_value = mock_forms_service

        service = FormsService()
        result = await service.get_responses(form_id="form1")

        assert "form_id" in result
        assert mock_forms_service.forms().responses().list.call_count >= 1
