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
        path_template  = '/3/genre/movie/list',
        params         = [
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en',
            ),
        ],
        response_model = 'Field3GenreMovieListGetResponse',
        description    = 'Get the list of official genres for movies.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/genre/tv/list',
        params         = [
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en',
            ),
        ],
        response_model = 'Field3GenreTvListGetResponse',
        description    = 'Get the list of official genres for TV shows.',
    ),
]
