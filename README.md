# TMDBX


## Development

### Generate v3 Models

Create patched openapi spec file which is input to the codegen call specified in pyproject.toml:

```shell
uv run python scripts/patch_raw_body.py -i data/tmdb_v3_openapi.json -o data/tmdb_v3_openapi_patched.json
uv run datamodel-codegen
```