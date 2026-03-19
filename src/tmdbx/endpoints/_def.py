from __future__ import annotations

from enum import Enum
from typing import Any
from pydantic import BaseModel, field_validator, model_validator


class HTTPMethod(str, Enum):
    GET    = "GET"
    POST   = "POST"
    PUT    = "PUT"
    DELETE = "DELETE"


class ParamKind(str, Enum):
    PATH  = "path"   # injected into URL template:  /4/account/{account_object_id}/lists
    QUERY = "query"  # appended as ?key=value


class ParamDef(BaseModel):
    """Describes a single parameter for an endpoint."""
    name:        str
    kind:        ParamKind
    python_type: str  = "str"    # "str" | "int" | "bool" — kept as string for JSON-serializability
    required:    bool = True
    default:     Any  = None
    description: str  = ""


class EndpointDef(BaseModel):
    """
    Full specification of one TMDB API endpoint.
    Intentionally serializable to JSON so the registry can be
    stored/diffed as plain data (e.g. endpoints.json).
    """
    id:              str           # dot-notation: "account.lists", "list.create"
    method:          HTTPMethod
    path_template:   str           # "/4/account/{account_object_id}/lists"
    params:          list[ParamDef] = []

    # String references keep the registry JSON-serializable.
    # The client resolves these to actual model classes at import time
    # via a MODEL_REGISTRY dict[str, type[BaseModel]].
    request_model:   str | None = None   # e.g. "ListCreateRequest"
    response_model:  str | None = None   # e.g. "AccountListsResponse"

    cacheable:       bool       = False
    # Subset of param names whose values form the cache key.
    # Populated automatically for GET endpoints (all path + query params)
    # but can be overridden per-endpoint.
    cache_key_params: list[str] = []

    description:     str        = ""
    auth_required:   bool       = True

    @model_validator(mode="after")
    def _default_cache_key(self) -> "EndpointDef":
        """Auto-populate cache_key_params for GET endpoints if not explicitly set."""
        if not self.cache_key_params and self.method == HTTPMethod.GET:
            self.cache_key_params = [p.name for p in self.params]
        return self