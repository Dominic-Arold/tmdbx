from __future__ import annotations
import json
from pathlib import Path
from tmdbx.endpoints._def import EndpointDef, ParamDef, HTTPMethod, ParamKind


# ── Type mapping ──────────────────────────────────────────────────────────────

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


# ── operationId → dot-notation id ─────────────────────────────────────────────
# TMDB uses kebab-case: "list-add-movie" → "list.add_movie"

def _normalise_id(operation_id: str) -> str:
    parts = operation_id.split("-", 1)          # ["list", "add-movie"]
    if len(parts) == 2:
        prefix, rest = parts
        return f"{prefix}.{rest.replace('-', '_')}"
    return operation_id.replace("-", "_")

# "list-add-movie"  → "list.add_movie"
# "account-lists"   → "account.lists"
# "movie-popular"   → "movie.popular"


# ── Parameter parsing ─────────────────────────────────────────────────────────

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


# ── Response model name ───────────────────────────────────────────────────────
# Convention: PascalCase from operationId, e.g. "list-add-movie" → "ListAddMovieResponse"
# The codegen step produces a class with exactly this name in v3.py.

def _response_model_name(operation_id: str) -> str:
    return "".join(w.capitalize() for w in operation_id.replace("-", " ").split()) + "Response"

def _request_model_name(operation_id: str) -> str:
    return "".join(w.capitalize() for w in operation_id.replace("-", " ").split()) + "Request"


# ── Has body? ─────────────────────────────────────────────────────────────────

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


# ── Single operation → EndpointDef ────────────────────────────────────────────

def _parse_operation(
    path: str,
    http_method: str,
    op: dict,
) -> EndpointDef:
    operation_id = op["operationId"]       # e.g. "list-add-movie"
    endpoint_id  = _normalise_id(operation_id)   # e.g. "list.add_movie"
    method       = HTTPMethod(http_method.upper())
    params       = _parse_parameters(op.get("parameters", []))
    has_body     = _has_request_body(op)

    cacheable = method == HTTPMethod.GET

    return EndpointDef(
        id              = endpoint_id,
        method          = method,
        path_template   = path,            # "/3/list/{list_id}/add_item"
        params          = params,
        request_model   = _request_model_name(operation_id) if has_body else None,
        response_model  = _response_model_name(operation_id),
        cacheable       = cacheable,
        description     = op.get("summary", ""),
        deprecated      = op.get("deprecated", False),
    )


# ── Full spec → REGISTRY ──────────────────────────────────────────────────────

def build_v3_registry(spec_path: Path) -> dict[str, EndpointDef]:
    """
    Parse a TMDB v3 OpenAPI JSON file and return a flat EndpointDef registry.

    Called once at module import:
        V3_REGISTRY = build_v3_registry(Path(__file__).parent / "tmdb_v3_openapi.json")
    """
    spec = json.loads(spec_path.read_text())
    registry: dict[str, EndpointDef] = {}

    for path, path_item in spec.get("paths", {}).items():
        for http_method, op in path_item.items():
            if http_method not in ("get", "post", "put", "delete", "patch"):
                continue
            if op.get("deprecated", False):
                continue  # skip deprecated endpoints (configurable)

            ep = _parse_operation(path, http_method, op)

            if ep.id in registry:
                # Rare: two paths share an operationId — append method suffix
                ep = ep.model_copy(update={"id": f"{ep.id}_{http_method}"})

            registry[ep.id] = ep

    return registry