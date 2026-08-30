"""
Simple in-memory TTL cache for expensive, read-only endpoint responses.

This is intentionally dependency-free (no Redis) to keep the MVP lightweight.
It is process-local, so each uvicorn worker has its own cache — fine for the
single-worker dev deployment. For multi-worker production, swap this for a
Redis-backed cache with the same interface.
"""
from __future__ import annotations

import time
import threading
from typing import Any, Callable, Dict, Optional, Tuple


class TTLCache:
    """Thread-safe in-memory cache with per-entry time-to-live."""

    def __init__(self, default_ttl_seconds: float = 300.0):
        self.default_ttl = default_ttl_seconds
        self._store: Dict[str, Tuple[float, Any]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """Return the cached value if present and not expired, else None."""
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            expires_at, value = entry
            if time.monotonic() > expires_at:
                # Lazy eviction.
                self._store.pop(key, None)
                return None
            return value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Store a value with the given TTL (defaults to the cache default)."""
        ttl = self.default_ttl if ttl is None else ttl
        expires_at = time.monotonic() + ttl
        with self._lock:
            self._store[key] = (expires_at, value)

    def get_or_compute(self, key: str, compute: Callable[[], Any], ttl: Optional[float] = None) -> Any:
        """Return the cached value, or compute + cache it."""
        cached = self.get(key)
        if cached is not None:
            return cached
        value = compute()
        self.set(key, value, ttl=ttl)
        return value

    def invalidate(self, key: str) -> None:
        """Drop a single key (call when underlying data changes)."""
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        """Drop everything (used by tests)."""
        with self._lock:
            self._store.clear()

    def size(self) -> int:
        with self._lock:
            return len(self._store)


# Shared singleton caches.
# - response_cache: for read-heavy API responses (careers list, stats, course details)
# - embedding_query_cache is already on EmbeddingService; this one is for HTTP-level payloads.
response_cache = TTLCache(default_ttl_seconds=300.0)
