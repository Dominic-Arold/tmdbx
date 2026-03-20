from __future__ import annotations

import re
from enum import Enum
from typing import Any
from pydantic import BaseModel, model_validator


class HTTPMethod(str, Enum):
    GET    = "GET"
    POST   = "POST"
    PUT    = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class ParamKind(str, Enum):
    PATH  = "path"
    QUERY = "query"


class ParamDef(BaseModel):
    """Describes a single parameter for an endpoint."""
    name:        str
    kind:        ParamKind
    python_type: str  = "str"
    required:    bool = True
    default:     Any  = None
    description: str  = ""


# ── Name derivation ───────────────────────────────────────────────────────────

_PARAM_SEGMENT = re.compile(r"^\{.+\}$")
_WORD_BOUNDARY = re.compile(r"[_\-]+")


def _segment_to_pascal(segment: str) -> str:
    return "".join(w.capitalize() for w in _WORD_BOUNDARY.split(segment))


def _derive_model_name(path_template: str, method: HTTPMethod, suffix: str) -> str:
    """
    /4/account/{account_object_id}/lists  GET  → AccountListsGetResponse
    /4/list/{list_id}/items              POST  → ListItemsPostRequest
    /4/list                              POST  → ListPostResponse
    """
    segments = [s for s in path_template.split("/") if s]
    if segments and segments[0].isdigit():
        segments = segments[1:]
    segments = [s for s in segments if not _PARAM_SEGMENT.match(s)]
    pascal = "".join(_segment_to_pascal(s) for s in segments)
    return f"{pascal}{method.value.title()}{suffix}"


# ── EndpointDef ───────────────────────────────────────────────────────────────

_BODY_METHODS = {HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH}


class EndpointDef(BaseModel):
    """
    Full specification of one TMDB API endpoint.

    Auto-derived unless overridden:
      cacheable       None  → True for GET, False otherwise
      response_model  None  → derived from path + method, e.g. "AccountListsGetResponse"
                      False → no response model (opt-out)
                      str   → use as-is
      request_model   None  → derived for POST/PUT/PATCH, None for GET/DELETE
                      False → no request model (opt-out)
                      str   → use as-is
    """
    id:              str
    method:          HTTPMethod
    path_template:   str
    params:          list[ParamDef] = []

    cacheable:       bool | None        = None
    response_model:  str | bool | None  = None
    request_model:   str | bool | None  = None

    cache_key_params: list[str] = []
    description:      str       = ""
    auth_required:    bool      = True

    @model_validator(mode="after")
    def _auto_derive(self) -> "EndpointDef":
        if self.cacheable is None:
            self.cacheable = (self.method == HTTPMethod.GET)

        if self.response_model is None:
            self.response_model = _derive_model_name(self.path_template, self.method, "Response")
        elif self.response_model is False:
            self.response_model = None

        if self.request_model is None:
            if self.method in _BODY_METHODS:
                self.request_model = _derive_model_name(self.path_template, self.method, "Request")
        elif self.request_model is False:
            self.request_model = None

        if not self.cache_key_params and self.cacheable:
            self.cache_key_params = [p.name for p in self.params]

        return self