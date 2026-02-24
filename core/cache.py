"""
Redis cache utility module for the PMS backend.

Provides reusable methods for caching data with Redis:
- get_cache: Retrieve cached data
- set_cache: Store data with TTL
- delete_cache: Remove specific cache key
- delete_pattern: Remove multiple keys matching a pattern
"""

import json
import logging
from typing import Any, Optional

from django.core.cache import cache

logger = logging.getLogger(__name__)


def get_cache(key: str) -> Optional[Any]:
    """
    Retrieve cached data by key.

    Args:
        key: Cache key to retrieve

    Returns:
        Cached data if found, None otherwise
    """
    try:
        cached_data = cache.get(key)
        if cached_data is not None:
            logger.debug(f"Cache hit for key: {key}")
            return cached_data
        logger.debug(f"Cache miss for key: {key}")
        return None
    except Exception as e:
        logger.error(
            f"Error retrieving cache for key {key}: {str(e)}",
            exc_info=True,
        )
        return None


def set_cache(key: str, value: Any, timeout: int = 7200) -> bool:
    """
    Store data in cache with TTL.

    Args:
        key: Cache key to store
        value: Data to cache (will be JSON serialized if needed)
        timeout: TTL in seconds (default: 7200 = 2 hours)

    Returns:
        True if successful, False otherwise
    """
    try:
        cache.set(key, value, timeout=timeout)
        logger.debug(f"Cache set for key: {key} with timeout: {timeout} seconds")
        return True
    except Exception as e:
        logger.error(
            f"Error setting cache for key {key}: {str(e)}",
            exc_info=True,
        )
        return False


def delete_cache(key: str) -> bool:
    """
    Remove cached data by key.

    Args:
        key: Cache key to delete

    Returns:
        True if successful, False otherwise
    """
    try:
        cache.delete(key)
        logger.debug(f"Cache deleted for key: {key}")
        return True
    except Exception as e:
        logger.error(
            f"Error deleting cache for key {key}: {str(e)}",
            exc_info=True,
        )
        return False


def delete_pattern(pattern: str) -> int:
    """
    Delete multiple cache keys matching a pattern.

    Args:
        pattern: Pattern to match (e.g., "user_*" to delete all user keys)

    Returns:
        Number of keys deleted, -1 on error
    """
    try:
        # Use django-redis specific method for pattern deletion
        deleted_count = cache.delete_pattern(pattern)
        logger.debug(f"Deleted {deleted_count} cache keys matching pattern: {pattern}")
        return deleted_count
    except AttributeError:
        # Fallback if delete_pattern is not available
        logger.warning("delete_pattern not available, cache backend may not support it")
        return -1
    except Exception as e:
        logger.error(
            f"Error deleting cache pattern {pattern}: {str(e)}",
            exc_info=True,
        )
        return -1
