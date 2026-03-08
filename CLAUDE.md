# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Model Context Protocol (MCP) server that integrates Claude Code with Google Workspace services (Drive, Docs, Sheets, Slides, Forms, Gmail). The server runs via stdio and tools are registered using FastMCP decorators.

## Commands

### Setup
```bash
poetry install --with dev
```

### Run the server
```bash
poetry run google-workspace-mcp
```

### Authentication
- On first run, a browser opens for OAuth consent
- Tokens are stored at `~/.config/gw-mcp/token.pickle`
- Credentials file must exist at `~/.config/gw-mcp/credentials.json` (copy from `config/credentials.json.example`)
- To reset auth: `rm ~/.config/gw-mcp/token.pickle`
- Config dir can be overridden with `GW_MCP_CONFIG_DIR` env var

### Testing and formatting
```bash
make test          # run pytest with coverage (htmlcov/)
make fmt           # format and auto-fix lint
make fmt-check     # check formatting/lint without modifying files

# Run a specific test or file directly
poetry run pytest tests/test_drive_service.py -v
poetry run pytest tests/test_drive_service.py::TestDriveService::test_search_files -v
```

### Environment variables
```bash
export GW_MCP_CONFIG_DIR=~/.config/gw-mcp  # Config/token directory
export GW_MCP_LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR
```

## Working in this repo

When making changes that affect user-facing behaviour, installation steps, configuration, or architecture, update `README.md` accordingly before considering the task complete.

## Architecture

### Entry point and tool registration
`__main__.py` → imports `google_workspace_mcp/tools/__init__.py` → which imports all `*_tools.py` modules → each module's `@mcp.tool()` decorators register tools on the shared `mcp` instance from `server_fastmcp.py`.

The `mcp` instance in `server_fastmcp.py` is the single FastMCP object. Tool modules import it and decorate functions with `@mcp.tool()`. **Never import tool modules in `server_fastmcp.py`** — that causes circular imports.

### Layer structure
```
tools/*_tools.py     — MCP tool definitions: Pydantic input validation, calls service layer
services/*_service.py — Google API wrappers: business logic, caching, rate limiting
auth/oauth_handler.py — OAuth 2.0: token storage (pickle), credential refresh, service building
utils/               — Shared: error_handler, response_formatter, base_models, cache, rate_limiter, logger
```

### Adding a new tool
1. Define a Pydantic input model extending `BaseMCPInput` (or `BaseListInput` for paginated results) in the relevant `tools/*_tools.py`
2. Add a `@mcp.tool()` decorated async function that validates input and calls the service layer
3. Return strings from tools — use `format_error()` for errors and `create_success_response()` for success
4. Add the corresponding method to the service class in `services/*_service.py`

### Key patterns
- **Input models**: All tool inputs use Pydantic v2 with `extra='forbid'`, `str_strip_whitespace=True`. Base classes in `utils/base_models.py` (`BaseMCPInput`, `BaseListInput`, `FileIdInput`, etc.)
- **Response format**: All list/read tools support `response_format: ResponseFormat` (markdown or json). CHARACTER_LIMIT is 25000 chars; use `truncate_response()` for large outputs.
- **Error handling**: Service methods are decorated with `@with_error_handling` from `utils/error_handler.py`. Custom exceptions: `GoogleWorkspaceError`, `AuthenticationError`, `ResourceNotFoundError`, `RateLimitError`, `PermissionError`.
- **Services**: Each service class lazy-initializes its Google API client via the singleton `OAuthHandler` (`get_oauth_handler()`). Services use `@rate_limited_call` and `@cached_call` decorators from utils.
- **Tests**: All tests use `unittest.mock` with mock service fixtures defined in `tests/conftest.py`. Tests are async (`asyncio_mode = auto` in pytest.ini).
