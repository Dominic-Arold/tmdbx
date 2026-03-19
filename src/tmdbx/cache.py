import asyncio
import threading
import diskcache
from pathlib import Path
from typing import Any
from tmdbx.endpoints._def import EndpointDef


def build_cache_key(endpoint: EndpointDef, path_params: dict, query_params: dict) -> str:
    """
    Deterministic string key for a specific endpoint call.
    E.g. "v4.account.lists:account_object_id=abc123:page=2"
    """
    parts = [endpoint.id]
    for name in endpoint.cache_key_params:
        val = path_params.get(name) or query_params.get(name) or endpoint_default(endpoint, name)
        parts.append(f"{name}={val}")
    return ":".join(parts)


def endpoint_default(endpoint: EndpointDef, param_name: str) -> Any:
    for p in endpoint.params:
        if p.name == param_name:
            return p.default
    return None


class CacheManagerBase:
    """
    Shared state and cache-management operations for both sync and async managers.
    Does not contain any I/O or locking logic — subclasses own get_or_fetch.
    """

    def __init__(self, cache_dir: Path, ttl: float) -> None:
        self._cache = diskcache.Cache(str(cache_dir))
        self._ttl   = ttl

    # ── Cache management ──────────────────────────────────────────────────────

    def clear(self) -> None:
        """Wipe the entire disk cache."""
        self._cache.clear()

    def invalidate(self, endpoint_id: str, **kwargs: Any) -> int:
        """
        Remove cache entries for a given endpoint, optionally filtered by params.

        With no kwargs, all entries for the endpoint are removed:
            cache.invalidate("v4.account.lists")

        With kwargs, only entries whose key contains every supplied param=value
        segment are removed:
            cache.invalidate("v4.account.lists", account_object_id="abc")
            cache.invalidate("v4.account.lists", account_object_id="abc", page=2)

        Returns the number of entries deleted.
        """
        # Keys for this endpoint always start with "<endpoint_id>:"
        # (or equal endpoint_id exactly, though in practice cacheable endpoints
        # always have at least one cache_key_param).
        prefix = f"{endpoint_id}:"

        # Build the set of "param=value" substrings that every matching key must contain.
        required_segments: list[str] = [f"{k}={v}" for k, v in kwargs.items()]

        deleted = 0
        # diskcache supports iteration over all stored keys.
        for key in list(self._cache.iterkeys()):
            if not isinstance(key, str):
                continue
            if not key.startswith(prefix):
                continue
            if all(seg in key for seg in required_segments):
                self._cache.delete(key)
                deleted += 1

        return deleted


class AsyncCacheManager(CacheManagerBase):
    """
    Async disk cache with per-key double-lock pattern.
    """

    def __init__(self, cache_dir: Path, ttl: float) -> None:
        super().__init__(cache_dir, ttl)
        self._in_flight: dict[str, asyncio.Lock] = {}
        self._in_flight_lock = asyncio.Lock()  # guards _in_flight dict itself

    async def get_or_fetch(self, key: str, fetch_coro) -> Any:
        # 1. Fast path — check cache before acquiring any lock
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        # 2. Get/create per-key lock (guarded by the global in-flight lock)
        async with self._in_flight_lock:
            if key not in self._in_flight:
                self._in_flight[key] = asyncio.Lock()
            key_lock = self._in_flight[key]

        # 3. Only one coroutine fetches; late-comers re-check cache after waiting
        async with key_lock:
            cached = self._cache.get(key)
            if cached is not None:
                return cached
            try:
                result = await fetch_coro()
                self._cache.set(key, result, expire=self._ttl)
                return result
            finally:
                async with self._in_flight_lock:
                    self._in_flight.pop(key, None)


class SyncCacheManager(CacheManagerBase):
    """
    Sync disk cache with per-key double-lock pattern.
    Uses threading.Lock instead of asyncio.Lock; otherwise mirrors AsyncCacheManager.
    """

    def __init__(self, cache_dir: Path, ttl: float) -> None:
        super().__init__(cache_dir, ttl)
        self._in_flight: dict[str, threading.Lock] = {}
        self._in_flight_lock = threading.Lock()  # guards _in_flight dict itself

    def get_or_fetch(self, key: str, fetch_fn) -> Any:
        # 1. Fast path
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        # 2. Get/create per-key lock
        with self._in_flight_lock:
            if key not in self._in_flight:
                self._in_flight[key] = threading.Lock()
            key_lock = self._in_flight[key]

        # 3. Only one thread fetches; late-comers re-check cache after waiting
        with key_lock:
            cached = self._cache.get(key)
            if cached is not None:
                return cached
            try:
                result = fetch_fn()
                self._cache.set(key, result, expire=self._ttl)
                return result
            finally:
                with self._in_flight_lock:
                    self._in_flight.pop(key, None)