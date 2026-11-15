"""
Run with:  pytest tests/test_patch_raw_body.py -v
"""

import json
import pytest

from scripts.patch_raw_body import (
    _infer_schema,
    _merge_example_schemas,
    _is_raw_body_schema,
    _extract_example_values,
    _build_replacement_schema,
    patch_spec,
)


# ─────────────────────────────────────────────────────────────────────────────
# _infer_schema
# ─────────────────────────────────────────────────────────────────────────────

class TestInferSchema:
    def test_integer(self):
        assert _infer_schema(18) == {"type": "integer"}

    def test_float(self):
        assert _infer_schema(3.14) == {"type": "number"}

    def test_string(self):
        assert _infer_schema("en") == {"type": "string"}

    def test_bool_true(self):
        # bool must resolve before int (bool subclasses int)
        assert _infer_schema(True) == {"type": "boolean"}

    def test_bool_false(self):
        assert _infer_schema(False) == {"type": "boolean"}

    def test_none(self):
        # None → no type constraint
        assert _infer_schema(None) == {}

    def test_empty_list(self):
        assert _infer_schema([]) == {"type": "array", "items": {}}

    def test_homogeneous_list_of_ints(self):
        assert _infer_schema([1, 2, 3]) == {"type": "array", "items": {"type": "integer"}}

    def test_homogeneous_list_of_strings(self):
        assert _infer_schema(["a", "b"]) == {"type": "array", "items": {"type": "string"}}

    def test_heterogeneous_list_falls_back(self):
        # mixed types → items: {}
        assert _infer_schema([1, "a"]) == {"type": "array", "items": {}}

    def test_flat_object(self):
        result = _infer_schema({"media_id": 18})
        assert result["type"] == "object"
        assert result["properties"] == {"media_id": {"type": "integer"}}
        assert result["required"] == ["media_id"]

    def test_object_with_nullable_field_not_required(self):
        result = _infer_schema({"id": 1, "note": None})
        assert "id" in result["required"]
        assert "note" not in result.get("required", [])

    def test_nested_object(self):
        result = _infer_schema({"outer": {"inner": True}})
        assert result["type"] == "object"
        inner_schema = result["properties"]["outer"]
        assert inner_schema["type"] == "object"
        assert inner_schema["properties"]["inner"] == {"type": "boolean"}

    def test_object_with_list_field(self):
        result = _infer_schema({"items": [{"id": 1}, {"id": 2}]})
        items_schema = result["properties"]["items"]
        assert items_schema["type"] == "array"


# ─────────────────────────────────────────────────────────────────────────────
# _merge_example_schemas
# ─────────────────────────────────────────────────────────────────────────────

class TestMergeExampleSchemas:
    def test_empty_list(self):
        assert _merge_example_schemas([]) == {}

    def test_single_schema_returned_as_is(self):
        s = {"type": "object", "properties": {"id": {"type": "integer"}}, "required": ["id"]}
        assert _merge_example_schemas([s]) == s

    def test_all_agree_on_type(self):
        s1 = {"type": "object", "properties": {"id": {"type": "integer"}}, "required": ["id"]}
        s2 = {"type": "object", "properties": {"id": {"type": "integer"}}, "required": ["id"]}
        merged = _merge_example_schemas([s1, s2])
        assert merged["properties"]["id"] == {"type": "integer"}
        assert "id" in merged["required"]

    def test_type_conflict_produces_unconstrained_field(self):
        s1 = {"type": "object", "properties": {"val": {"type": "integer"}}, "required": ["val"]}
        s2 = {"type": "object", "properties": {"val": {"type": "string"}},  "required": ["val"]}
        merged = _merge_example_schemas([s1, s2])
        # Conflicting types → {} (no constraint)
        assert merged["properties"]["val"] == {}

    def test_required_only_if_present_in_all(self):
        s1 = {"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "string"}},
              "required": ["a", "b"]}
        s2 = {"type": "object", "properties": {"a": {"type": "integer"}},
              "required": ["a"]}
        merged = _merge_example_schemas([s1, s2])
        assert "a" in merged["required"]
        assert "b" not in merged.get("required", [])

    def test_union_of_all_keys_in_properties(self):
        s1 = {"type": "object", "properties": {"x": {"type": "integer"}}, "required": ["x"]}
        s2 = {"type": "object", "properties": {"y": {"type": "string"}},  "required": ["y"]}
        merged = _merge_example_schemas([s1, s2])
        assert "x" in merged["properties"]
        assert "y" in merged["properties"]
        # Neither appears in all examples → neither required
        assert merged.get("required", []) == []


# ─────────────────────────────────────────────────────────────────────────────
# _is_raw_body_schema
# ─────────────────────────────────────────────────────────────────────────────

class TestIsRawBodySchema:
    RAW_BODY_SCHEMA = {
        "type": "object",
        "properties": {
            "RAW_BODY": {"type": "string", "format": "json"}
        }
    }

    def test_detects_raw_body(self):
        assert _is_raw_body_schema(self.RAW_BODY_SCHEMA) is True

    def test_proper_schema_not_detected(self):
        assert _is_raw_body_schema({
            "type": "object",
            "properties": {"media_id": {"type": "integer"}}
        }) is False

    def test_empty_schema_not_detected(self):
        assert _is_raw_body_schema({}) is False

    def test_missing_json_format_not_detected(self):
        # RAW_BODY key present but without format: json → not a match
        assert _is_raw_body_schema({
            "type": "object",
            "properties": {"RAW_BODY": {"type": "string"}}
        }) is False

    def test_extra_properties_not_detected(self):
        # RAW_BODY alongside another property → not the placeholder pattern
        assert _is_raw_body_schema({
            "type": "object",
            "properties": {
                "RAW_BODY": {"type": "string", "format": "json"},
                "other":    {"type": "integer"},
            }
        }) is False


# ─────────────────────────────────────────────────────────────────────────────
# _extract_example_values
# ─────────────────────────────────────────────────────────────────────────────

class TestExtractExampleValues:
    def test_named_example_object(self):
        media_type_obj = {
            "examples": {
                "Request Example": {"value": {"media_id": 18}}
            }
        }
        values = _extract_example_values(media_type_obj)
        assert values == [{"media_id": 18}]

    def test_inline_example(self):
        media_type_obj = {"example": {"media_id": 99}}
        values = _extract_example_values(media_type_obj)
        assert values == [{"media_id": 99}]

    def test_json_string_value_is_decoded(self):
        # TMDB sometimes serialises the example as a JSON string
        media_type_obj = {
            "examples": {
                "Result": {"value": '{"status_code": 12, "status_message": "ok"}'}
            }
        }
        values = _extract_example_values(media_type_obj)
        assert values == [{"status_code": 12, "status_message": "ok"}]

    def test_multiple_named_examples(self):
        media_type_obj = {
            "examples": {
                "Ex1": {"value": {"id": 1}},
                "Ex2": {"value": {"id": 2, "name": "test"}},
            }
        }
        values = _extract_example_values(media_type_obj)
        assert len(values) == 2

    def test_empty_returns_empty_list(self):
        assert _extract_example_values({}) == []

    def test_example_without_value_key_ignored(self):
        media_type_obj = {
            "examples": {
                "Broken": {"summary": "no value key here"}
            }
        }
        assert _extract_example_values(media_type_obj) == []


# ─────────────────────────────────────────────────────────────────────────────
# _build_replacement_schema
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildReplacementSchema:
    def _make_media_type_obj(self, example_value):
        return {
            "schema": {
                "type": "object",
                "properties": {"RAW_BODY": {"type": "string", "format": "json"}}
            },
            "examples": {
                "Request Example": {"value": example_value}
            }
        }

    def test_simple_flat_body(self):
        obj = self._make_media_type_obj({"media_id": 18})
        schema = _build_replacement_schema(obj, "list-add-movie")
        assert schema["type"] == "object"
        assert schema["properties"]["media_id"] == {"type": "integer"}

    def test_no_examples_falls_back_to_bare_object(self):
        obj = {
            "schema": {
                "type": "object",
                "properties": {"RAW_BODY": {"type": "string", "format": "json"}}
            }
        }
        schema = _build_replacement_schema(obj, "some-operation")
        assert schema == {"type": "object"}

    def test_non_object_example_falls_back(self):
        # An example that is a plain string — can't be a request body model
        obj = {
            "schema": {"type": "object", "properties": {"RAW_BODY": {"type": "string", "format": "json"}}},
            "examples": {"Ex": {"value": "just a string"}}
        }
        schema = _build_replacement_schema(obj, "weird-op")
        assert schema == {"type": "object"}

    def test_multiple_examples_merged(self):
        obj = {
            "schema": {"type": "object", "properties": {"RAW_BODY": {"type": "string", "format": "json"}}},
            "examples": {
                "Ex1": {"value": {"session_id": "abc", "movie_id": 1}},
                "Ex2": {"value": {"session_id": "xyz", "movie_id": 2}},
            }
        }
        schema = _build_replacement_schema(obj, "rate-movie")
        assert "session_id" in schema["properties"]
        assert "movie_id"   in schema["properties"]
        assert "session_id" in schema["required"]
        assert "movie_id"   in schema["required"]


# ─────────────────────────────────────────────────────────────────────────────
# patch_spec  (integration-level: full spec dict → patched spec dict)
# ─────────────────────────────────────────────────────────────────────────────

def _make_minimal_spec(path: str, method: str, operation: dict) -> dict:
    return {
        "openapi": "3.1.0",
        "info": {"title": "TMDB test", "version": "3"},
        "paths": {path: {method: operation}},
    }


RAW_BODY_OPERATION = {
    "operationId": "list-add-movie",
    "summary": "Add Movie",
    "parameters": [
        {"name": "list_id",    "in": "path",  "required": True,  "schema": {"type": "integer"}},
        {"name": "session_id", "in": "query", "required": True,  "schema": {"type": "string"}},
    ],
    "requestBody": {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {"RAW_BODY": {"type": "string", "format": "json"}}
                },
                "examples": {
                    "Request Example": {"value": {"media_id": 18}}
                }
            }
        }
    },
    "responses": {
        "200": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status_code":    {"type": "integer", "default": 0},
                            "status_message": {"type": "string"},
                        }
                    }
                }
            }
        }
    },
    "deprecated": False,
}


class TestPatchSpec:
    def test_raw_body_is_replaced(self):
        spec = _make_minimal_spec("/3/list/{list_id}/add_item", "post", RAW_BODY_OPERATION)
        patched, count = patch_spec(spec)
        assert count == 1
        schema = (
            patched["paths"]["/3/list/{list_id}/add_item"]["post"]
            ["requestBody"]["content"]["application/json"]["schema"]
        )
        assert schema["type"] == "object"
        assert "RAW_BODY" not in schema.get("properties", {})
        assert "media_id" in schema["properties"]

    def test_original_spec_not_mutated(self):
        spec = _make_minimal_spec("/3/list/{list_id}/add_item", "post", RAW_BODY_OPERATION)
        original_schema_id = id(
            spec["paths"]["/3/list/{list_id}/add_item"]["post"]
            ["requestBody"]["content"]["application/json"]["schema"]
        )
        patch_spec(spec)
        # patch_spec deep-copies, so original must be unchanged
        original_props = (
            spec["paths"]["/3/list/{list_id}/add_item"]["post"]
            ["requestBody"]["content"]["application/json"]["schema"]["properties"]
        )
        assert "RAW_BODY" in original_props

    def test_count_reflects_number_of_patches(self):
        op_a = {
            "operationId": "op-a",
            "requestBody": {"content": {"application/json": {
                "schema": {"type": "object", "properties": {"RAW_BODY": {"type": "string", "format": "json"}}},
                "examples": {"Ex": {"value": {"x": 1}}}
            }}},
        }
        op_b = {
            "operationId": "op-b",
            "requestBody": {"content": {"application/json": {
                "schema": {"type": "object", "properties": {"RAW_BODY": {"type": "string", "format": "json"}}},
                "examples": {"Ex": {"value": {"y": "hello"}}}
            }}},
        }
        spec = {
            "paths": {
                "/a": {"post": op_a},
                "/b": {"post": op_b},
            }
        }
        _, count = patch_spec(spec)
        assert count == 2

    def test_clean_schema_not_touched(self):
        clean_op = {
            "operationId": "movie-details",
            "parameters": [{"name": "movie_id", "in": "path", "required": True, "schema": {"type": "integer"}}],
            "responses": {"200": {"content": {"application/json": {"schema": {"type": "object"}}}}},
        }
        spec = _make_minimal_spec("/3/movie/{movie_id}", "get", clean_op)
        _, count = patch_spec(spec)
        assert count == 0

    def test_deprecated_operations_are_skipped(self):
        deprecated_op = {**RAW_BODY_OPERATION, "deprecated": True}
        spec = _make_minimal_spec("/3/list/{list_id}/add_item", "post", deprecated_op)
        # deprecated flag is handled in the registry builder, not patch_spec
        # patch_spec patches regardless of deprecated flag (codegen may need it)
        _, count = patch_spec(spec)
        assert count == 1  # patch_spec does not filter deprecated — that's _openapi.py's job

    def test_response_schema_untouched(self):
        spec = _make_minimal_spec("/3/list/{list_id}/add_item", "post", RAW_BODY_OPERATION)
        patched, _ = patch_spec(spec)
        response_schema = (
            patched["paths"]["/3/list/{list_id}/add_item"]["post"]
            ["responses"]["200"]["content"]["application/json"]["schema"]
        )
        # Response schema had proper properties and should be unchanged
        assert "status_code"    in response_schema["properties"]
        assert "status_message" in response_schema["properties"]

    def test_patch_produces_valid_json(self):
        spec = _make_minimal_spec("/3/list/{list_id}/add_item", "post", RAW_BODY_OPERATION)
        patched, _ = patch_spec(spec)
        # Must round-trip through JSON without error
        dumped   = json.dumps(patched)
        reloaded = json.loads(dumped)
        assert reloaded["paths"]["/3/list/{list_id}/add_item"]["post"] \
                       ["requestBody"]["content"]["application/json"] \
                       ["schema"]["type"] == "object"
