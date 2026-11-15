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
        path_template  = '/3/guest_session/{guest_session_id}/rated/movies',
        params         = [
            ParamDef(
                name        = 'guest_session_id',
                kind        = ParamKind.PATH,
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
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'sort_by',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'created_at.asc',
            ),
        ],
        response_model = 'Field3GuestSessionGuestSessionIdRatedMoviesGetResponse',
        description    = 'Get the rated movies for a guest session.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/guest_session/{guest_session_id}/rated/tv',
        params         = [
            ParamDef(
                name        = 'guest_session_id',
                kind        = ParamKind.PATH,
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
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'sort_by',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'created_at.asc',
            ),
        ],
        response_model = 'Field3GuestSessionGuestSessionIdRatedTvGetResponse',
        description    = 'Get the rated TV shows for a guest session.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/guest_session/{guest_session_id}/rated/tv/episodes',
        params         = [
            ParamDef(
                name        = 'guest_session_id',
                kind        = ParamKind.PATH,
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
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'sort_by',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'created_at.asc',
            ),
        ],
        response_model = 'Field3GuestSessionGuestSessionIdRatedTvEpisodesGetResponse',
        description    = 'Get the rated TV episodes for a guest session.',
    ),
]
