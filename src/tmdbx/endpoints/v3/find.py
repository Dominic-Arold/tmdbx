# GENERATED FILE — do not edit by hand.
# Re-generate with:
#   uv run python scripts/generate_v3_endpoints.py \
#       --spec   data/tmdb_v3_openapi_patched.json \
#       --models src/tmdbx/models/v3.py \
#       --out    src/tmdbx/endpoints/v3
from __future__ import annotations

from tmdbx.endpoints._def import EndpointDef, HTTPMethod, ParamDef, ParamKind

ENDPOINTS: list[EndpointDef] = [
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/find/{external_id}',
        params         = [
            ParamDef(
                name        = 'external_id',
                kind        = ParamKind.PATH,
                python_type = 'str',
                required    = True,
            ),
            ParamDef(
                name        = 'external_source',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
        ],
        response_model = 'Field3FindExternalIdGetResponse',
        description    = "Find data by external ID's.",
    ),
]
