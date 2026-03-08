"""Integration tests - utility modules and service instantiation."""

import pytest
from google_workspace_mcp.utils.cache import AsyncCache
from google_workspace_mcp.utils.error_handler import (
    GoogleWorkspaceError,
    handle_google_api_error,
)
from google_workspace_mcp.utils.logger import setup_logger
from google_workspace_mcp.utils.rate_limiter import RateLimiter


class TestUtilities:
    """Test utility modules."""

    def test_logger_setup(self):
        """Test logger configuration."""
        logger = setup_logger("test")
        assert logger.name == "test"
        assert logger.level is not None

    def test_error_types(self):
        """Test custom error types."""
        error = GoogleWorkspaceError("Test error", {"key": "value"})
        assert error.message == "Test error"
        assert error.details == {"key": "value"}

        error_dict = error.to_dict()
        assert error_dict["error"]["message"] == "Test error"
        assert error_dict["error"]["type"] == "GoogleWorkspaceError"

    def test_error_handler_conversion(self):
        """Test error handler converts generic exceptions."""
        generic_error = Exception("Generic error")
        converted = handle_google_api_error(generic_error)
        assert isinstance(converted, GoogleWorkspaceError)

    def test_rate_limiter_init(self):
        """Test rate limiter initialization."""
        limiter = RateLimiter(max_requests=10, time_window=60)
        assert limiter.max_requests == 10
        assert limiter.time_window == 60

    @pytest.mark.asyncio
    async def test_cache_basic(self):
        """Test async cache basic operations."""
        cache = AsyncCache(maxsize=100, ttl=300)
        stats = cache.get_stats()
        assert "size" in stats
        assert "hits" in stats
        assert "misses" in stats
        assert "hit_rate" in stats

    @pytest.mark.asyncio
    async def test_cache_set_and_get(self):
        """Test cache set and get operations."""
        cache = AsyncCache(maxsize=100, ttl=300)
        await cache.set("key1", "value1")
        value = await cache.get("key1")
        assert value == "value1"

    @pytest.mark.asyncio
    async def test_cache_miss(self):
        """Test cache returns None for missing keys."""
        cache = AsyncCache(maxsize=100, ttl=300)
        value = await cache.get("nonexistent")
        assert value is None
