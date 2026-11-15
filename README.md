# tmdbx

[![tests](https://github.com/Dominic-Arold/tmdbx/actions/workflows/tests.yml/badge.svg)](https://github.com/Dominic-Arold/tmdbx/actions/workflows/tests.yml)

A typed Python client for [The Movie Database (TMDB)](https://www.themoviedb.org/) API, covering both **v3** and **v4**.

- **Sync and async**: `TMDB` and `AsyncTMDB` share one request-building core and differ only in I/O.
- **Typed responses**: JSON is parsed into Pydantic v2 models. The v3 models are generated from TMDB's OpenAPI spec and the v4 models are written explicitely.
- **Disk caching**: GET responses are cached with [`diskcache`](https://grantjenks.com/docs/diskcache/). A per-key lock means concurrent identical requests hit the network only once.
- **Predictable addressing**: you call an endpoint by the same path that appears in the TMDB docs, so you don't need to learn a separate method name for it.

> **Status: work in progress.** The core works: request building, caching, response parsing, and all 150+ v3 endpoints are registered. The public API is not stable yet and v4 coverage is partial. See [Current state](#current-state).

## Installation

Requires Python 3.12+. The package is not published on PyPI yet, so install it from GitHub:

```bash
pip install git+https://github.com/Dominic-Arold/tmdbx
```

You need a TMDB API **Read Access Token** (Settings → API on themoviedb.org). The same bearer token works for both v3 and v4.

## Quickstart

```python
from tmdbx import TMDB

with TMDB(access_token="<token>", cache_dir="~/.cache/tmdbx", cache_ttl=3600) as tmdb:
    movie = tmdb.request("/3/movie/{movie_id}", movie_id=9343)
    print(movie.title, movie.release_date, movie.runtime)   # Fitzcarraldo 1982-03-02 157

    results = tmdb.request("/3/search/movie", query="Arrival")
    lists = tmdb.request("/4/account/{account_object_id}/lists", account_object_id="<id>")
```

Async, with many requests in parallel:

```python
import asyncio
from tmdbx import AsyncTMDB

async def main():
    async with AsyncTMDB(access_token="<token>", cache_dir="~/.cache/tmdbx", cache_ttl=3600) as tmdb:
        movies = await asyncio.gather(*(
            tmdb.request("/3/movie/{movie_id}", movie_id=i) for i in (9343, 6404, 2000)
        ))

asyncio.run(main())
```

### How requests work

`request(path, method="get", **kwargs)` looks up the endpoint definition for `path` + `method`. Each keyword argument is then sent as a **path**, **query** or **JSON body** parameter, according to that definition. Query parameters you leave out get the documented defaults (e.g. `language="en-US"`, `page=1`). Leaving out a required parameter raises an error before any request is sent.

If no model exists for an endpoint, the response is returned as a plain `dict`. HTTP errors raise `httpx.HTTPStatusError`.

### Caching

Only GET endpoints are cached. The cache key is the endpoint id plus its parameter values, e.g. `/3/movie/{movie_id}:get:movie_id=550:append_to_response=None:language=en-US`. To manage entries:

```python
tmdb.cache.invalidate("/3/movie/{movie_id}:get", movie_id=550)  # entries matching these params
tmdb.cache.invalidate("/3/movie/{movie_id}:get")                # every entry for the endpoint
tmdb.cache.clear()                                              # everything
```

## Design

```
TMDB OpenAPI spec ──patch_raw_body.py──▶ patched spec ──datamodel-codegen──▶ models/v3.py
                                                     └─generate_v3_endpoints.py─▶ endpoints/v3/*.py
hand-written ───────────────────────────────────────────────────────────────▶ endpoints/v4, models/account.py
```

**Generating code from the spec for v3.** TMDB publishes an OpenAPI spec for v3, but it is incomplete in an awkward way. Many request bodies are declared as a `RAW_BODY` string placeholder, and their real field shapes appear only in the `examples` block. [`scripts/patch_raw_body.py`](scripts/patch_raw_body.py) finds this pattern, infers a JSON Schema from the examples, and writes a patched spec. That patched spec feeds two generators:
- `datamodel-code-generator` produces `models/v3.py`, with about 1,100 Pydantic models.
- [`scripts/generate_v3_endpoints.py`](scripts/generate_v3_endpoints.py) produces one endpoint-definition module per API section, under `src/tmdbx/endpoints/v3/`.

The generated files are committed. That keeps them reviewable and diffable, and importing the package costs nothing extra.

**Hand-written v4.** There seeems to be no usable spec for v4, so its endpoints and models are written by hand. 

**Registries.** Every endpoint is an `EndpointDef`, a Pydantic model whose id has the form `"{path}:{method}"`. It derives its cacheability, response/request model names and cache-key parameters itself. Response models register themselves in `MODEL_REGISTRY` through `__init_subclass__`. The client therefore only looks up a model by name, and adding an endpoint takes no extra wiring.

```
src/tmdbx/
├── client/       TMDBClientBase (no I/O) → TMDB / AsyncTMDB (httpx)
├── cache.py      diskcache wrapper, sync + async managers with per-key locking
├── endpoints/    EndpointDef/ParamDef, registry, v3 (generated) and v4 (hand-written)
└── models/       TMDBModel base + MODEL_REGISTRY, v3 (generated), v4 account models
scripts/          spec patcher and v3 endpoint generator
tests/            pytest suite
```

## Current state

What works:
- All v3 endpoints from the spec are registered (161 endpoints in total).
- Sync and async clients with disk caching.
- Typed responses for nearly every endpoint.

Still in progress:
- **v4 coverage** is limited to the account lists, favorites and watchlist endpoints, plus list CRUD. Some v4 endpoints don't have response models yet and return dicts.
- **Request bodies** are sent as given. They are not validated against the generated request models yet.
- **Tests** currently cover the spec patcher only. Client and cache tests are still to come.

## Development

```bash
uv sync
uv run pytest
```

To regenerate the v3 models and endpoints after updating `data/tmdb_v3_openapi.json`:

```bash
uv run python scripts/patch_raw_body.py -i data/tmdb_v3_openapi.json -o data/tmdb_v3_openapi_patched.json
uv run datamodel-codegen      # settings in [tool.datamodel-codegen] in pyproject.toml
uv run python scripts/generate_v3_endpoints.py \
    --spec   data/tmdb_v3_openapi_patched.json \
    --models src/tmdbx/models/v3.py \
    --out    src/tmdbx/endpoints/v3
```

---

This project uses the TMDB API but is not endorsed or certified by TMDB.
