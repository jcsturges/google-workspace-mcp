"""MCP tools for Google Workspace services.

Tools are automatically registered with FastMCP when imported.
Each tool module uses @mcp.tool() decorators for registration.
"""

# Import all tool modules to register their tools with FastMCP
# The @mcp.tool() decorators in each module handle registration
from . import (
    docs_tools,  # noqa: F401
    drive_tools,  # noqa: F401
    forms_tools,  # noqa: F401
    gmail_tools,  # noqa: F401
    sheets_tools,  # noqa: F401
    slides_tools,  # noqa: F401
)

__all__ = [
    "drive_tools",
    "docs_tools",
    "sheets_tools",
    "slides_tools",
    "gmail_tools",
    "forms_tools",
]
