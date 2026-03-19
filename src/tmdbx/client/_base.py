from pydantic import BaseModel
from typing import Any
from tmdbx.endpoints._def import EndpointDef, ParamKind
from tmdbx.endpoints.registry import REGISTRY
from tmdbx.models._registry import MODEL_REGISTRY


class TMDBClientBase:
    """
    Shared request-construction logic.
    Contains NO httpx client and performs NO I/O — both sync and async
    subclasses call these helpers to build their requests.
    """

    BASE_URL = "https://api.themoviedb.org"

    def __init__(self, access_token: str):
        self._token = access_token
        # subclasses add self._http (httpx.Client or httpx.AsyncClient)
        # subclasses add self.cache (SyncCacheManager or AsyncCacheManager)

    def _resolve_url(self, endpoint: EndpointDef, path_params: dict[str, Any]) -> str:
        path = endpoint.path_template.format(**path_params)
        return f"{self.BASE_URL}{path}"

    def _resolve_query(self, endpoint: EndpointDef, query_params: dict[str, Any]) -> dict:
        """Merge caller-supplied values with endpoint defaults."""
        resolved = {}
        for p in endpoint.params:
            if p.kind != ParamKind.QUERY:
                continue
            val = query_params.get(p.name, p.default)
            if val is None and p.required:
                raise ValueError(f"Missing required query param: {p.name}")
            if val is not None:
                resolved[p.name] = val
        return resolved

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Accept":        "application/json",
        }

    def _split_params(
        self,
        endpoint: EndpointDef,
        kwargs: dict[str, Any],
    ) -> tuple[dict, dict, dict]:
        """Split kwargs into (path_params, query_params, body_params)."""
        path_names = {p.name for p in endpoint.params if p.kind == ParamKind.PATH}
        query_names = {p.name for p in endpoint.params if p.kind == ParamKind.QUERY}
        path_params  = {k: v for k, v in kwargs.items() if k in path_names}
        query_params = {k: v for k, v in kwargs.items() if k in query_names}
        body_params  = {k: v for k, v in kwargs.items() if k not in path_names | query_names}
        return path_params, query_params, body_params

    def _get_endpoint(self, endpoint_id: str) -> EndpointDef:
        try:
            return REGISTRY[endpoint_id]
        except KeyError:
            raise ValueError(f"Unknown endpoint: {endpoint_id!r}")

    def _parse_response(self, endpoint: EndpointDef, raw: dict) -> BaseModel | dict:
        if endpoint.response_model and (cls := MODEL_REGISTRY.get(endpoint.response_model)):
            return cls.model_validate(raw)
        return raw   # fall back to plain dict if no model defined yet
