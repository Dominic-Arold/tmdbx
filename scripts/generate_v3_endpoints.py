"""
scripts/generate_v3_endpoints.py
=================================
Generates static Python endpoint-definition files under
src/tmdbx/endpoints/v3/ from the patched TMDB v3 OpenAPI spec.

Each top-level path segment (e.g. "authentication", "movie", "account")
gets its own file:

    src/tmdbx/endpoints/v3/authentication.py
    src/tmdbx/endpoints/v3/movie.py
    ...

Each file contains an ``ENDPOINTS: list[EndpointDef]`` list that is
registered in ``endpoints/__init__.py`` exactly like the v4 hand-authored
endpoints.

Model-name derivation
---------------------
Names are derived purely from the path + HTTP method:

    /3/authentication                      GET  → Field3AuthenticationGetResponse
    /3/account/{account_id}                GET  → Field3AccountAccountIdGetResponse
    /3/account/{account_id}/favorite       POST → Field3AccountAccountIdFavoritePostRequest
                                                  Field3AccountAccountIdFavoritePostResponse
    /3/movie/{movie_id}/watch/providers    GET  → Field3MovieMovieIdWatchProvidersGetResponse

Rule:
  1. Start with "Field" + version digit ("3")
  2. For each path segment after the version digit:
       - plain segment  (e.g. "favorite")   → capitalise each _-separated word → "Favorite"
       - param segment  (e.g. "{movie_id}") → strip braces, capitalise words   → "MovieId"
  3. Append the capitalised HTTP method and "Response" / "Request"

Every derived name is validated against the set of classes that actually
exist in the generated src/tmdbx/models/v3.py.  Mismatches are reported
as warnings and the endpoint is emitted with response_model=False (raw
dict fallback).

Usage
-----
uv run python scripts/generate_v3_endpoints.py \
    --spec   data/tmdb_v3_openapi_patched.json \
    --models src/tmdbx/models/v3.py \
    --out    src/tmdbx/endpoints/v3

After generation, run your formatter:

    uv run ruff format src/tmdbx/endpoints/v3/
    uv run ruff check  src/tmdbx/endpoints/v3/ --fix
"""

from __future__ import annotations

import argparse
import ast
import json
import keyword
import logging
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)


# ── Model-name derivation ─────────────────────────────────────────────────────

_PARAM_SEG = re.compile(r"^\{(.+)\}$")
_WORD_SEP   = re.compile(r"[_\-]+")


def _seg_to_pascal(seg: str) -> str:
    """
    Convert one URL path segment to its PascalCase contribution.

    Plain:  "favorite_movies" → "FavoriteMovies"
    Param:  "{movie_id}"      → "MovieId"
    """
    m = _PARAM_SEG.match(seg)
    inner = m.group(1) if m else seg
    return "".join(w.capitalize() for w in _WORD_SEP.split(inner) if w)


def _model_name(path: str, method: str, suffix: str) -> str:
    """
    Derive the model class name for a given path + HTTP method + suffix.

    suffix is either "Response" or "Request".

    Examples
    --------
    /3/authentication                   GET  Response → Field3AuthenticationGetResponse
    /3/account/{account_id}/favorite    POST Request  → Field3AccountAccountIdFavoritePostRequest
    /3/movie/{movie_id}/watch/providers GET  Response → Field3MovieMovieIdWatchProvidersGetResponse
    """
    segs          = [s for s in path.split("/") if s]
    version_digit = segs[0]                                    # "3"
    rest          = segs[1:]                                   # everything after the version
    pascal_path   = "".join(_seg_to_pascal(s) for s in rest)
    method_pascal = method.capitalize()                        # "Get" / "Post" / …
    return f"Field{version_digit}{pascal_path}{method_pascal}{suffix}"


# ── Path helpers ──────────────────────────────────────────────────────────────

def _group_key(path: str) -> str:
    """Return the first non-version, non-param path segment (module name)."""
    segs = [s for s in path.split("/") if s]
    for seg in segs[1:]:          # skip version digit
        if not _PARAM_SEG.match(seg):
            return seg
    return "misc"


# ── OAS type mapping ──────────────────────────────────────────────────────────

_OAS_TYPE_MAP: dict[str, str] = {
    "integer": "int",
    "number":  "float",
    "boolean": "bool",
    "array":   "list",
    "object":  "dict",
    "string":  "str",
}


def _py_type(schema: dict) -> str:
    return _OAS_TYPE_MAP.get(schema.get("type", "string"), "str")


# ── Spec parsing ──────────────────────────────────────────────────────────────

def _parse_params(raw: list[dict]) -> list[dict]:
    result = []
    for p in raw:
        kind   = "PATH" if p["in"] == "path" else "QUERY"
        schema = p.get("schema", {})
        result.append(
            {
                "name":        p["name"],
                "kind":        kind,
                "python_type": _py_type(schema),
                "required":    p.get("required", False),
                "default":     schema.get("default", None),
                "description": p.get("description", ""),
            }
        )
    return result


def _has_body(op: dict) -> bool:
    rb = op.get("requestBody", {})
    if not rb:
        return False
    content = rb.get("content", {}).get("application/json", {})
    schema  = content.get("schema", {})
    props   = schema.get("properties", {})
    # RAW_BODY placeholder still counts as a body
    return bool(props) or bool(schema)


def _load_operations(spec: dict) -> list[dict]:
    """Return a flat list of operation dicts."""
    http_methods = {"get", "post", "put", "delete", "patch"}
    ops = []
    for path, path_item in spec.get("paths", {}).items():
        for method, op in path_item.items():
            if method not in http_methods:
                continue
            if not isinstance(op, dict):
                continue
            if op.get("deprecated", False):
                continue
            ops.append(
                {
                    "path":        path,
                    "method":      method.upper(),
                    "params":      _parse_params(op.get("parameters", [])),
                    "has_body":    _has_body(op),
                    "description": op.get("description", ""),
                }
            )
    return ops


# ── Model-name validation ─────────────────────────────────────────────────────

def _collect_class_names(models_path: Path) -> set[str]:
    """Parse the generated v3.py and return all top-level class names."""
    src  = models_path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}


def _validated(
    name: str,
    known: set[str],
    path: str,
    method: str,
    label: str,
) -> str | None:
    """Return name if found in known (or known is empty), else warn and return None."""
    if not known or name in known:
        return name
    log.warning(
        "Model %r not found in v3.py  (%s %s, %s) — endpoint will use raw dict",
        name, method, path, label,
    )
    return None


# ── Code generation ───────────────────────────────────────────────────────────

def _repr(value: Any) -> str:
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (int, float)):
        return repr(value)
    return repr(str(value))


def _render_endpoint(op: dict) -> str:
    lines = [
        "    EndpointDef(",
        f"        method         = HTTPMethod.{op['method']},",
        f"        path_template  = {_repr(op['path'])},",
    ]

    if op["params"]:
        lines.append("        params         = [")
        for p in op["params"]:
            lines.append("            ParamDef(")
            lines.append(f"                name        = {_repr(p['name'])},")
            lines.append(f"                kind        = ParamKind.{p['kind']},")
            lines.append(f"                python_type = {_repr(p['python_type'])},")
            lines.append(f"                required    = {_repr(p['required'])},")
            if p["default"] is not None:
                lines.append(f"                default     = {_repr(p['default'])},")
            if p["description"]:
                desc = p["description"].replace('"', "'")[:120]
                lines.append(f"                description = {_repr(desc)},")
            lines.append("            ),")
        lines.append("        ],")
    else:
        lines.append("        params         = [],")

    if op.get("response_model"):
        lines.append(f"        response_model = {_repr(op['response_model'])},")
    else:
        lines.append("        response_model = False,")

    if op.get("request_model"):
        lines.append(f"        request_model  = {_repr(op['request_model'])},")

    if op.get("description"):
        desc = op["description"].replace('"', "'").replace("\n", " ")[:200]
        lines.append(f"        description    = {_repr(desc)},")

    lines.append("    ),")
    return "\n".join(lines)


_FILE_HEADER = """\
# GENERATED FILE — do not edit by hand.
# Re-generate with:
#   uv run python scripts/generate_v3_endpoints.py \\
#       --spec   data/tmdb_v3_openapi_patched.json \\
#       --models src/tmdbx/models/v3.py \\
#       --out    src/tmdbx/endpoints/v3
from __future__ import annotations

from tmdbx.endpoints._def import EndpointDef, HTTPMethod, ParamDef, ParamKind

ENDPOINTS: list[EndpointDef] = [
"""

_FILE_FOOTER = "]\n"


def _safe_module_name(segment: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9_]", "_", segment).lower()
    if keyword.iskeyword(name) or (name and name[0].isdigit()):
        name = f"_{name}"
    return name


def _render_v3_init(module_names: list[str]) -> str:
    lines = [
        "# GENERATED FILE — do not edit by hand.",
        "from __future__ import annotations",
        "",
    ]
    for mod in sorted(module_names):
        lines.append(f"from tmdbx.endpoints.v3 import {mod}")
    lines += [
        "",
        "V3_ENDPOINTS = [",
    ]
    for mod in sorted(module_names):
        lines.append(f"    *{mod}.ENDPOINTS,")
    lines += [
        "]",
        "",
    ]
    return "\n".join(lines) + "\n"


# ── Main ──────────────────────────────────────────────────────────────────────

def generate(spec_path: Path, models_path: Path | None, out_dir: Path) -> None:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    known_classes: set[str] = set()
    if models_path and models_path.exists():
        known_classes = _collect_class_names(models_path)
        log.info("Loaded %d class names from %s", len(known_classes), models_path)
    else:
        log.warning(
            "--models not provided or file missing — skipping model-name validation"
        )

    ops = _load_operations(spec)

    body_methods = {"POST", "PUT", "PATCH"}

    for op in ops:
        path   = op["path"]
        method = op["method"]

        resp_raw = _model_name(path, method, "Response")
        op["response_model"] = _validated(
            resp_raw, known_classes, path, method, "response"
        )

        if method in body_methods and op["has_body"]:
            req_raw = _model_name(path, method, "Request")
            op["request_model"] = _validated(
                req_raw, known_classes, path, method, "request"
            )
        else:
            op["request_model"] = None

    # Group by first non-version path segment → one file each
    by_group: dict[str, list[dict]] = defaultdict(list)
    for op in ops:
        by_group[_group_key(op["path"])].append(op)

    out_dir.mkdir(parents=True, exist_ok=True)

    module_names: list[str] = []
    total_eps = 0
    for group_seg, group_ops in sorted(by_group.items()):
        mod_name  = _safe_module_name(group_seg)
        file_path = out_dir / f"{mod_name}.py"
        module_names.append(mod_name)

        body = _FILE_HEADER
        for op in group_ops:
            body += _render_endpoint(op) + "\n"
        body += _FILE_FOOTER

        file_path.write_text(body, encoding="utf-8")
        log.info("Wrote %-55s  (%d endpoints)", str(file_path), len(group_ops))
        total_eps += len(group_ops)

    # v3/__init__.py
    init_path = out_dir / "__init__.py"
    init_path.write_text(_render_v3_init(module_names), encoding="utf-8")
    log.info("Wrote %s", init_path)

    log.info("Done — %d endpoints across %d module(s)", total_eps, len(module_names))

    # Summary of validation failures
    no_resp = [op for op in ops if op.get("response_model") is None]
    no_req  = [
        op for op in ops
        if op["method"] in body_methods
        and op["has_body"]
        and op.get("request_model") is None
    ]
    if no_resp:
        log.warning(
            "%d endpoint(s) with unresolved response model (raw dict fallback):",
            len(no_resp),
        )
        for op in no_resp:
            log.warning("  %s  %s", op["method"], op["path"])
    if no_req:
        log.warning(
            "%d endpoint(s) with unresolved request model:", len(no_req)
        )
        for op in no_req:
            log.warning("  %s  %s", op["method"], op["path"])


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate static v3 endpoint definition files from the "
            "patched TMDB v3 OpenAPI spec."
        ),
    )
    parser.add_argument(
        "--spec", "-s",
        required=True,
        type=Path,
        metavar="FILE",
        help="Patched TMDB v3 OpenAPI JSON (data/tmdb_v3_openapi_patched.json)",
    )
    parser.add_argument(
        "--models", "-m",
        type=Path,
        metavar="FILE",
        default=None,
        help="Generated src/tmdbx/models/v3.py — used to validate model names",
    )
    parser.add_argument(
        "--out", "-o",
        required=True,
        type=Path,
        metavar="DIR",
        help="Output directory (src/tmdbx/endpoints/v3)",
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s  %(message)s",
    )
    generate(args.spec, args.models, args.out)


if __name__ == "__main__":
    main()
