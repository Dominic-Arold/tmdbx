import asyncio
import threading
import diskcache
from pathlib import Path
from typing import Any
from tmdbx.endpoints._def import EndpointDef


def build_cache_key(endpoint: EndpointDef, path_params: dict, query_params: dict) -> str:
    """
    Deterministic string key for a specific endpoint call.
    E.g. "account.lists:account_object_id=abc123:page=2"
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


class AsyncCacheManager:
    """
    Async disk cache with per-key double-lock.
    """
    def __init__(self, cache_dir: Path, ttl: float):
        self._cache      = diskcache.Cache(str(cache_dir))
        self._ttl        = ttl
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


class SyncCacheManager:
    """
    Sync version — uses threading.Lock instead of asyncio.Lock.
    Same double-check pattern; threading makes it simpler (no in_flight_lock needed
    because dict operations under GIL are safe for get/set — but we still use one
    for correctness on lock creation).
    """
    def __init__(self, cache_dir: Path, ttl: float):
        self._cache      = diskcache.Cache(str(cache_dir))
        self._ttl        = ttl
        self._in_flight: dict[str, threading.Lock] = {}
        self._in_flight_lock = threading.Lock()

    def get_or_fetch(self, key: str, fetch_fn) -> Any:
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        with self._in_flight_lock:
            if key not in self._in_flight:
                self._in_flight[key] = threading.Lock()
            key_lock = self._in_flight[key]

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