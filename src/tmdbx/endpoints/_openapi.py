from __future__ import annotations
import json
import re
from collections import defaultdict
from pathlib import Path
from tmdbx.endpoints._def import EndpointDef, ParamDef, HTTPMethod, ParamKind
from tmdbx.endpoints._registry import register


_TYPE_MAP: dict[str, str] = {
    "integer": "int",
    "number":  "float",
    "boolean": "bool",
    "array":   "list",
    "object":  "dict",
    "string":  "str",
}

def _oas_type(schema: dict) -> str:
    return _TYPE_MAP.get(schema.get("type", "string"), "str")

_PARAM_SEGMENT = re.compile(r"^\{.+\}$")

def _path_base_id(path: str) -> str:
    segments = [s for s in path.split("/") if s]
    version = f"v{segments[0]}" if segments else "v3"
    rest = [s for s in segments[1:] if not _PARAM_SEGMENT.match(s)]
    return ".".join([version, *rest])


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


def _parse_operation(path: str, http_method: str, op: dict) -> EndpointDef:
    operation_id = op["operationId"]
    method       = HTTPMethod(http_method.upper())
    params       = _parse_parameters(op.get("parameters", []))
    has_body     = _has_request_body(op)
    cacheable    = method == HTTPMethod.GET

    return EndpointDef(
        id             = _path_base_id(path),
        method         = method,
        path_template  = path,
        params         = params,
        request_model  = _request_model_name(operation_id) if has_body else None,
        response_model = _response_model_name(operation_id),
        cacheable      = cacheable,
        description    = op.get("description", ""),
    )


def load_v3_endpoints(spec_path: Path) -> None:
    """
    Parse a TMDB v3 OpenAPI JSON file and register all endpoints into
    ENDPOINT_REGISTRY via register().

    Called once at import time from endpoints/__init__.py:
        load_v3_endpoints(Path(__file__).parent.parent / "data" / "tmdb_v3_openapi_patched.json")
    """
    spec = json.loads(spec_path.read_text())

    # Pass 1 — group by base id to detect method collisions on same path.
    groups: dict[str, list[EndpointDef]] = defaultdict(list)

    for path, path_item in spec.get("paths", {}).items():
        for http_method, op in path_item.items():
            if http_method not in ("get", "post", "put", "delete", "patch"):
                continue
            if op.get("deprecated", False):
                continue
            ep = _parse_operation(path, http_method, op)
            groups[ep.id].append(ep)

    # Pass 2 — assign final ids, adding :<method> suffix on collision, then register.
    for base_id, endpoints in groups.items():
        if len(endpoints) == 1:
            register(endpoints[0])
        else:
            # Collision — suffix ALL methods symmetrically, including GET.
            for ep in endpoints:
                final_id = f"{base_id}:{ep.method.value.lower()}"
                register(ep.model_copy(update={"id": final_id}))