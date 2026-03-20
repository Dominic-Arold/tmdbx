import httpx
from pathlib import Path
from typing import Any
from pydantic import BaseModel
from ._base import TMDBClientBase
from tmdbx.cache import AsyncCacheManager, SyncCacheManager, build_cache_key


class AsyncTMDB(TMDBClientBase):

    def __init__(self, access_token: str, cache_dir: Path, cache_ttl: float, timeout: float = 10.0):
        super().__init__(access_token)
        self._http  = httpx.AsyncClient(timeout=timeout, headers=self._headers())
        self.cache = AsyncCacheManager(cache_dir, cache_ttl)

    async def __aenter__(self): return self
    async def __aexit__(self, *_): await self.close()
    async def close(self): await self._http.aclose()

    async def request(
        self,
        endpoint_id: str,
        **kwargs: Any,
    ) -> BaseModel | dict:
        """
        Generic entry point.  kwargs are split automatically into
        path params, query params, and body per the endpoint definition.

        Usage:
            await client.request("account.lists", account_object_id="abc", page=2)
            await client.request("list.create", name="My List", description="...")
        """
        endpoint = self._get_endpoint(endpoint_id)
        path_params, query_params, body_params = self._split_params(endpoint, kwargs)
        url    = self._resolve_url(endpoint, path_params)
        params = self._resolve_query(endpoint, query_params)

        async def _fetch():
            resp = await self._http.request(
                method  = endpoint.method.value,
                url     = url,
                params  = params or None,
                json    = body_params or None,
            )
            resp.raise_for_status()
            return resp.json()

        if endpoint.cacheable:
            key = build_cache_key(endpoint, path_params, query_params)
            raw = await self.cache.get_or_fetch(key, _fetch)
        else:
            raw = await _fetch()

        return self._parse_response(endpoint, raw)


class TMDB(TMDBClientBase):

    def __init__(self, access_token: str, cache_dir: Path, cache_ttl: float, timeout: float = 10.0):
        super().__init__(access_token)
        self._http  = httpx.Client(timeout=timeout, headers=self._headers())
        self.cache = SyncCacheManager(cache_dir, cache_ttl)

    def __enter__(self): return self
    def __exit__(self, *_): self.close()
    def close(self): self._http.close()

    def request(self, endpoint_id: str, **kwargs: Any) -> BaseModel | dict:
        """Sync mirror of AsyncTMDB.request — identical logic, no await."""
        endpoint = self._get_endpoint(endpoint_id)
        path_params, query_params, body_params = self._split_params(endpoint, kwargs)
        url    = self._resolve_url(endpoint, path_params)
        params = self._resolve_query(endpoint, query_params)

        def _fetch():
            resp = self._http.request(
                method = endpoint.method.value,
                url    = url,
                params = params or None,
                json   = body_params or None,
            )
            resp.raise_for_status()
            return resp.json()

        if endpoint.cacheable:
            key = build_cache_key(endpoint, path_params, query_params)
            raw = self.cache.get_or_fetch(key, _fetch)
        else:
            raw = _fetch()

        return self._parse_response(endpoint, raw)
