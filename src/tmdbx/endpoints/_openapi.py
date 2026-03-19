from __future__ import annotations
import json
import re
from collections import defaultdict
from importlib.metadata import requires
from pathlib import Path
from tmdbx.endpoints._def import EndpointDef, ParamDef, HTTPMethod, ParamKind


_TYPE_MAP: dict[str, str] = {
    "integer": "int",
    "number":  "float",
    "boolean": "bool",
    "array":   "list",
    "object":  "dict",
    "string":  "str",   # default / fallback
}

def _oas_type(schema: dict) -> str:
    return _TYPE_MAP.get(schema.get("type", "string"), "str")


# ── path → dot-notation id (without method suffix) ───────────────────────────
# Derived purely from the URL path.
#
# Rules:
#   1. Detect version from the first segment: /3/ → "v3", /4/ → "v4"
#   2. Drop all {param} segments
#   3. Join remaining segments with ".", prepend version prefix
#
# Examples:
#   /3/account/{account_id}/lists  →  "v3.account.lists"
#   /3/list/{list_id}/add_item     →  "v3.list.add_item"
#   /3/movie/popular               →  "v3.movie.popular"

_PARAM_SEGMENT = re.compile(r"^\{.+\}$")

def _path_base_id(path: str) -> str:
    segments = [s for s in path.split("/") if s]   # drop empty strings from leading "/"
    # First segment is the version number ("3", "4", …)
    version = f"v{segments[0]}" if segments else "v3"
    # Keep only non-param segments after the version
    rest = [s for s in segments[1:] if not _PARAM_SEGMENT.match(s)]
    return ".".join([version, *rest])


# ── Response / request model names ───────────────────────────────────────────
# Convention: PascalCase from operationId, e.g. "list-add-movie" → "ListAddMovieResponse"
# The codegen step produces a class with exactly this name in v3.py.

def _response_model_name(operation_id: str) -> str:
    return "".join(w.capitalize() for w in operation_id.replace("-", " ").split()) + "Response"

def _request_model_name(operation_id: str) -> str:
    return "".join(w.capitalize() for w in operation_id.replace("-", " ").split()) + "Request"


def _has_request_body(op: dict) -> bool:
    rb = op.get("requestBody", {})
    content = rb.get("content", {}).get("application/json", {})
    schema = content.get("schema", {})
    # TMDB v3 sometimes uses RAW_BODY as a placeholder — treat as no typed body
    props = schema.get("properties", {})
    if list(props.keys()) == ["RAW_BODY"]:
        # Extract real shape from the example instead
        # (handled separately in the codegen step — at runtime we just flag it)
        return True   # there IS a body, but it's loosely typed
    return bool(props) or bool(rb)


def _parse_parameters(raw_params: list[dict]) -> list[ParamDef]:
    result = []
    for p in raw_params:
        kind = ParamKind.PATH if p["in"] == "path" else ParamKind.QUERY
        result.append(ParamDef(
            name        = p["name"],
            kind        = kind,
            python_type = _oas_type(p.get("schema", {})),
            required    = p.get("required", False),
            default     = p.get("schema", {}).get("default", None),
            description = p.get("description", ""),
        ))
    return result


def _parse_operation(
    path: str,
    http_method: str,
    op: dict,
) -> EndpointDef:
    operation_id = op["operationId"]
    method       = HTTPMethod(http_method.upper())
    params       = _parse_parameters(op.get("parameters", []))
    has_body     = _has_request_body(op)
    cacheable    = method == HTTPMethod.GET

    # id is a temporary placeholder — the registry builder assigns the final id
    # after resolving collisions across all operations on the same path.
    return EndpointDef(
        id              = _path_base_id(path),   # may be refined with :<method> suffix
        method          = method,
        path_template   = path,
        params          = params,
        request_model   = _request_model_name(operation_id) if has_body else None,
        response_model  = _response_model_name(operation_id),
        cacheable       = cacheable,
        description     = op.get("description", ""),
    )


def build_v3_registry(spec_path: Path) -> dict[str, EndpointDef]:
    """
    Parse a TMDB v3 OpenAPI JSON file and return a flat EndpointDef registry.

    Endpoint ids are derived from the URL path, not the operationId:
        /3/account/{account_id}/lists  →  "v3.account.lists"
        /3/list/{list_id}/items  GET   →  "v3.list.items:get"
        /3/list/{list_id}/items  POST  →  "v3.list.items:post"

    When multiple HTTP methods share the same path, ALL of them receive a
    ":<method>" suffix (including GET) so the collision is always explicit.

    Called once at module import:
        V3_REGISTRY = build_v3_registry(Path(__file__).parent / "tmdb_v3_openapi.json")
    """
    spec = json.loads(spec_path.read_text())

    # Pass 1 — parse every operation; group by base id to detect collisions.
    # groups: base_id → list of EndpointDef (one per HTTP method on that path)
    groups: dict[str, list[EndpointDef]] = defaultdict(list)

    for path, path_item in spec.get("paths", {}).items():
        for http_method, op in path_item.items():
            if http_method not in ("get", "post", "put", "delete", "patch"):
                continue
            if op.get("deprecated", False):
                continue

            ep = _parse_operation(path, http_method, op)
            groups[ep.id].append(ep)

    # Pass 2 — assign final ids, adding :<method> suffix wherever there is a collision.
    registry: dict[str, EndpointDef] = {}

    for base_id, endpoints in groups.items():
        if len(endpoints) == 1:
            # No collision — use the base id as-is.
            ep = endpoints[0]
        else:
            # Collision — suffix ALL methods, including GET.
            for ep in endpoints:
                final_id = f"{base_id}:{ep.method.value.lower()}"
                registry[final_id] = ep.model_copy(update={"id": final_id})
            continue   # already inserted above; skip the single-ep insertion below

        registry[base_id] = ep

    return registry