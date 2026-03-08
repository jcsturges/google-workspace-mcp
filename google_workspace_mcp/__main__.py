"""Entry point for running the Google Workspace MCP server as a module."""

import os
import signal
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

    # mcp.run() uses asyncio.run() internally. On Ctrl+C, asyncio tries to
    # cancel all pending tasks before exiting, but the stdio reader task blocks
    # at the OS level on stdin and never cancels cleanly — causing a hang.
    # os._exit() bypasses asyncio cleanup entirely, which is safe here because
    # there is no in-flight state to flush (token already saved, API calls are
    # stateless HTTP).
    signal.signal(signal.SIGINT, lambda *_: os._exit(0))
    signal.signal(signal.SIGTERM, lambda *_: os._exit(0))

    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    main()
