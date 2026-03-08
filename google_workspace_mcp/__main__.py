"""Entry point for running the Google Workspace MCP server as a module."""

import asyncio
from google_workspace_mcp.server_fastmcp import mcp


def main():
    """Entry point for console script."""
    # Import all tool modules to register their tools
    from google_workspace_mcp import tools  # noqa: F401

    # Authenticate eagerly so the browser OAuth flow completes before the
    # stdio server starts. On subsequent runs the saved token is loaded/refreshed
    # silently and mcp.run() proceeds immediately.
    from google_workspace_mcp.auth.oauth_handler import get_oauth_handler
    get_oauth_handler().authenticate()

    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    main()
