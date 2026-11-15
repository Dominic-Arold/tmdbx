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
        path_template  = '/3/watch/providers/regions',
        params         = [
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
        ],
        response_model = 'Field3WatchProvidersRegionsGetResponse',
        description    = 'Get the list of the countries we have watch provider (OTT/streaming) data for.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/watch/providers/movie',
        params         = [
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'watch_region',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3WatchProvidersMovieGetResponse',
        description    = 'Get the list of streaming providers we have for movies.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/watch/providers/tv',
        params         = [
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'watch_region',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3WatchProvidersTvGetResponse',
        description    = 'Get the list of streaming providers we have for TV shows.',
    ),
]
