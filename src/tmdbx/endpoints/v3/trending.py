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
        path_template  = '/3/trending/all/{time_window}',
        params         = [
            ParamDef(
                name        = 'time_window',
                kind        = ParamKind.PATH,
                python_type = 'str',
                required    = True,
                default     = 'day',
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
                description = '`ISO-639-1`-`ISO-3166-1` code',
            ),
        ],
        response_model = 'Field3TrendingAllTimeWindowGetResponse',
        description    = 'Get the trending movies, TV shows and people.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/trending/movie/{time_window}',
        params         = [
            ParamDef(
                name        = 'time_window',
                kind        = ParamKind.PATH,
                python_type = 'str',
                required    = True,
                default     = 'day',
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
                description = '`ISO-639-1`-`ISO-3166-1` code',
            ),
        ],
        response_model = 'Field3TrendingMovieTimeWindowGetResponse',
        description    = 'Get the trending movies on TMDB.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/trending/person/{time_window}',
        params         = [
            ParamDef(
                name        = 'time_window',
                kind        = ParamKind.PATH,
                python_type = 'str',
                required    = True,
                default     = 'day',
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
                description = '`ISO-639-1`-`ISO-3166-1` code',
            ),
        ],
        response_model = 'Field3TrendingPersonTimeWindowGetResponse',
        description    = 'Get the trending people on TMDB.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/trending/tv/{time_window}',
        params         = [
            ParamDef(
                name        = 'time_window',
                kind        = ParamKind.PATH,
                python_type = 'str',
                required    = True,
                default     = 'day',
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
                description = '`ISO-639-1`-`ISO-3166-1` code',
            ),
        ],
        response_model = 'Field3TrendingTvTimeWindowGetResponse',
        description    = 'Get the trending TV shows on TMDB.',
    ),
]
