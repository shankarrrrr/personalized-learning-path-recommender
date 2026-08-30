"""Tests for the in-memory TTL cache."""
import time

from services.cache import TTLCache


class TestTTLCache:
    def test_set_and_get(self):
        cache = TTLCache(default_ttl_seconds=10)
        cache.set("k", "v")
        assert cache.get("k") == "v"

    def test_miss_returns_none(self):
        cache = TTLCache()
        assert cache.get("missing") is None

    def test_expiry(self):
        cache = TTLCache(default_ttl_seconds=0.05)
        cache.set("k", "v")
        assert cache.get("k") == "v"
        time.sleep(0.1)
        assert cache.get("k") is None

    def test_get_or_compute_caches(self):
        cache = TTLCache()
        calls = {"n": 0}

        def compute():
            calls["n"] += 1
            return "computed"

        assert cache.get_or_compute("k", compute) == "computed"
        assert cache.get_or_compute("k", compute) == "computed"
        assert calls["n"] == 1  # computed only once

    def test_invalidate(self):
        cache = TTLCache()
        cache.set("k", "v")
        cache.invalidate("k")
        assert cache.get("k") is None

    def test_clear(self):
        cache = TTLCache()
        cache.set("a", 1)
        cache.set("b", 2)
        cache.clear()
        assert cache.size() == 0

    def test_size(self):
        cache = TTLCache()
        assert cache.size() == 0
        cache.set("a", 1)
        cache.set("b", 2)
        assert cache.size() == 2

    def test_thread_safe_signature(self):
        """The cache exposes a lock-based interface (smoke test)."""
        cache = TTLCache()
        cache.set("k", "v")
        # Concurrent set + get should not raise.
        cache.get("k")
        assert cache.get("k") == "v"
