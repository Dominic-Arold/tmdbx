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
        path_template  = '/3/keyword/{keyword_id}',
        params         = [
            ParamDef(
                name        = 'keyword_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3KeywordKeywordIdGetResponse',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/keyword/{keyword_id}/movies',
        params         = [
            ParamDef(
                name        = 'keyword_id',
                kind        = ParamKind.PATH,
                python_type = 'str',
                required    = True,
            ),
            ParamDef(
                name        = 'include_adult',
                kind        = ParamKind.QUERY,
                python_type = 'bool',
                required    = False,
                default     = False,
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
        ],
        response_model = 'Field3KeywordKeywordIdMoviesGetResponse',
    ),
]
