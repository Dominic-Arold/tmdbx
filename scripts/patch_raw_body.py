"""
scripts/patch_raw_body.py
=========================
Pre-processing step that must be run BEFORE datamodel-code-generator.

Problem
-------
TMDB's v3 OpenAPI spec uses a lazy placeholder for some request bodies:

    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              RAW_BODY:
                type: string
                format: json          # ← meaningless to code-generators
          examples:
            Request Example:
              value:
                media_id: 18          # ← actual shape lives here

datamodel-code-generator sees the schema and generates a useless model:

    class ListAddMovieRequest(BaseModel):
        raw_body: Optional[str] = None

This script replaces every RAW_BODY schema with a proper JSON Schema
inferred from the example value, producing a patched spec that
datamodel-code-generator can handle correctly.

Usage
-----
    python scripts/patch_raw_body.py \
        --input  data/tmdb_v3_openapi.json \
        --output data/tmdb_v3_openapi_patched.json

    # then run codegen on the patched file:
    datamodel-codegen \
        --input  data/tmdb_v3_openapi_patched.json \
        --input-file-type openapi \
        --output tmdb/models/generated/v3.py \
        --output-model-type pydantic_v2.BaseModel \
        --snake-case-field \
        --use-annotated \
        --reuse-model \
        --collapse-root-models
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# JSON Schema inference
# ─────────────────────────────────────────────────────────────────────────────

def _infer_schema(value: Any, *, field_name: str = "field") -> dict:
    """
    Recursively infer a JSON Schema fragment from a concrete example value.

    Examples
    --------
    18            → {"type": "integer"}
    "en"          → {"type": "string"}
    True          → {"type": "boolean"}
    3.14          → {"type": "number"}
    None          → {}                           # no type constraint — any
    [1, 2]        → {"type": "array", "items": {"type": "integer"}}
    {"id": 1}     → {"type": "object", "properties": {"id": {"type": "integer"}}, ...}
    """
    if value is None:
        # nullable — don't constrain the type
        return {}

    if isinstance(value, bool):
        # bool check MUST come before int (bool is a subclass of int in Python)
        return {"type": "boolean"}

    if isinstance(value, int):
        return {"type": "integer"}

    if isinstance(value, float):
        return {"type": "number"}

    if isinstance(value, str):
        return {"type": "string"}

    if isinstance(value, list):
        if not value:
            return {"type": "array", "items": {}}
        # Infer from the first element; for heterogeneous lists fall back to {}
        first_schema = _infer_schema(value[0])
        if all(_infer_schema(v) == first_schema for v in value[1:]):
            return {"type": "array", "items": first_schema}
        return {"type": "array", "items": {}}   # anyOf would be over-engineering here

    if isinstance(value, dict):
        properties: dict[str, dict] = {}
        required: list[str] = []
        for k, v in value.items():
            properties[k] = _infer_schema(v, field_name=k)
            if v is not None:
                # If the example provides a non-null value, treat the field as required.
                # This is conservative — real required-ness is unknown from examples alone
                # but it produces better Pydantic models than making everything Optional.
                required.append(k)

        schema: dict = {
            "type": "object",
            "properties": properties,
        }
        if required:
            schema["required"] = required
        return schema

    # fallback — should not normally be reached with well-formed JSON
    log.warning("Unexpected type %s for field %r, defaulting to {}", type(value), field_name)
    return {}


def _merge_example_schemas(schemas: list[dict]) -> dict:
    """
    Merge multiple inferred schemas (one per named example) into one.

    Strategy:
    - All non-null properties across all examples are collected.
    - A property is required only if it appears in EVERY example.
    - Type conflicts on the same key → fall back to {} (no constraint).
    """
    if not schemas:
        return {}
    if len(schemas) == 1:
        return schemas[0]

    # Collect all property names
    all_keys: set[str] = set()
    for s in schemas:
        all_keys.update(s.get("properties", {}).keys())

    merged_props: dict[str, dict] = {}
    for key in all_keys:
        key_schemas = [
            s["properties"][key]
            for s in schemas
            if "properties" in s and key in s["properties"]
        ]
        if not key_schemas:
            merged_props[key] = {}
            continue

        # If all examples agree on the type, keep it; otherwise drop the constraint
        first = key_schemas[0]
        merged_props[key] = first if all(ks == first for ks in key_schemas[1:]) else {}

    # Only require fields present in every example
    required = [
        k for k in all_keys
        if all("properties" in s and k in s.get("required", []) for s in schemas)
    ]

    result: dict = {"type": "object", "properties": merged_props}
    if required:
        result["required"] = required
    return result


# ─────────────────────────────────────────────────────────────────────────────
# RAW_BODY detection + replacement
# ─────────────────────────────────────────────────────────────────────────────

def _is_raw_body_schema(schema: dict) -> bool:
    """Return True if this schema is the TMDB RAW_BODY placeholder."""
    props = schema.get("properties", {})
    return (
        schema.get("type") == "object"
        and set(props.keys()) == {"RAW_BODY"}
        and props["RAW_BODY"].get("format") == "json"
    )


def _extract_example_values(media_type_obj: dict) -> list[Any]:
    """
    Extract all concrete example values from an OAS media-type object.

    Handles both:
      examples:                         # map of named Example Objects
        "Request Example":
          value: {media_id: 18}
      example:                          # single inline example
        media_id: 18
    """
    values: list[Any] = []

    # Named examples (OAS 3.x Example Object map)
    for ex in media_type_obj.get("examples", {}).values():
        if isinstance(ex, dict) and "value" in ex:
            raw_value = ex["value"]
            # TMDB sometimes serialises the example value as a JSON string
            if isinstance(raw_value, str):
                try:
                    raw_value = json.loads(raw_value)
                except json.JSONDecodeError:
                    pass
            values.append(raw_value)

    # Inline example
    if "example" in media_type_obj:
        values.append(media_type_obj["example"])

    return values


def _build_replacement_schema(media_type_obj: dict, operation_id: str) -> dict:
    """
    Build the replacement JSON Schema for one RAW_BODY occurrence.
    Falls back to a plain `{"type": "object"}` if no usable examples exist.
    """
    example_values = _extract_example_values(media_type_obj)
    if not example_values:
        log.warning(
            "[%s] RAW_BODY has no examples — falling back to bare object schema",
            operation_id,
        )
        return {"type": "object"}

    inferred = [_infer_schema(v) for v in example_values if v is not None]
    # Filter down to only object schemas (non-objects can't become request body models)
    object_schemas = [s for s in inferred if s.get("type") == "object"]

    if not object_schemas:
        log.warning(
            "[%s] RAW_BODY examples did not yield object schemas (got %r) — bare object",
            operation_id,
            inferred,
        )
        return {"type": "object"}

    merged = _merge_example_schemas(object_schemas)
    log.debug("[%s] Inferred schema: %s", operation_id, json.dumps(merged))
    return merged


# ─────────────────────────────────────────────────────────────────────────────
# Walk the spec
# ─────────────────────────────────────────────────────────────────────────────

def patch_spec(spec: dict) -> tuple[dict, int]:
    """
    Return a deep-copied, patched spec and a count of replacements made.

    Modifies:
      spec["paths"][path][method]["requestBody"]["content"]["application/json"]["schema"]
      when the schema is a RAW_BODY placeholder.
    """
    import copy
    patched = copy.deepcopy(spec)
    count = 0

    for path, path_item in patched.get("paths", {}).items():
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            if not isinstance(operation, dict):
                continue

            operation_id = operation.get("operationId", f"{method}:{path}")
            request_body = operation.get("requestBody", {})
            content = request_body.get("content", {})
            media_type_obj = content.get("application/json", {})
            schema = media_type_obj.get("schema", {})

            if not _is_raw_body_schema(schema):
                continue

            replacement = _build_replacement_schema(media_type_obj, operation_id)
            media_type_obj["schema"] = replacement
            count += 1
            log.info(
                "[%s] %s %s — replaced RAW_BODY with: %s",
                operation_id, method.upper(), path,
                json.dumps(replacement, separators=(",", ":")),
            )

    return patched, count


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Patch TMDB OpenAPI spec: replace RAW_BODY schemas with proper definitions.",
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        type=Path,
        metavar="FILE",
        help="Path to the raw TMDB OpenAPI JSON spec (e.g. data/tmdb_v3_openapi.json)",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        type=Path,
        metavar="FILE",
        help="Destination path for the patched spec (e.g. data/tmdb_v3_openapi_patched.json)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s  %(message)s",
    )

    log.info("Loading spec from %s", args.input)
    spec = json.loads(args.input.read_text(encoding="utf-8"))

    patched_spec, n_replaced = patch_spec(spec)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(patched_spec, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    log.info(
        "Done — %d RAW_BODY schema(s) patched. Patched spec written to %s",
        n_replaced, args.output,
    )


if __name__ == "__main__":
    main()
