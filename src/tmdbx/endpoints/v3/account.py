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
        path_template  = '/3/account/{account_id}',
        params         = [
            ParamDef(
                name        = 'account_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3AccountAccountIdGetResponse',
        description    = 'Get the public details of an account on TMDB.',
    ),
    EndpointDef(
        method         = HTTPMethod.POST,
        path_template  = '/3/account/{account_id}/favorite',
        params         = [
            ParamDef(
                name        = 'account_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3AccountAccountIdFavoritePostResponse',
        request_model  = 'Field3AccountAccountIdFavoritePostRequest',
        description    = 'Mark a movie or TV show as a favourite.',
    ),
    EndpointDef(
        method         = HTTPMethod.POST,
        path_template  = '/3/account/{account_id}/watchlist',
        params         = [
            ParamDef(
                name        = 'account_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3AccountAccountIdWatchlistPostResponse',
        request_model  = 'Field3AccountAccountIdWatchlistPostRequest',
        description    = 'Add a movie or TV show to your watchlist.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/account/{account_id}/favorite/movies',
        params         = [
            ParamDef(
                name        = 'account_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
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
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'sort_by',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'created_at.asc',
            ),
        ],
        response_model = 'Field3AccountAccountIdFavoriteMoviesGetResponse',
        description    = 'Get a users list of favourite movies.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/account/{account_id}/favorite/tv',
        params         = [
            ParamDef(
                name        = 'account_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
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
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'sort_by',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'created_at.asc',
            ),
        ],
        response_model = 'Field3AccountAccountIdFavoriteTvGetResponse',
        description    = 'Get a users list of favourite TV shows.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/account/{account_id}/lists',
        params         = [
            ParamDef(
                name        = 'account_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3AccountAccountIdListsGetResponse',
        description    = 'Get a users list of custom lists.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/account/{account_id}/rated/movies',
        params         = [
            ParamDef(
                name        = 'account_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
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
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'sort_by',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'created_at.asc',
            ),
        ],
        response_model = 'Field3AccountAccountIdRatedMoviesGetResponse',
        description    = 'Get a users list of rated movies.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/account/{account_id}/rated/tv',
        params         = [
            ParamDef(
                name        = 'account_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
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
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'sort_by',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'created_at.asc',
            ),
        ],
        response_model = 'Field3AccountAccountIdRatedTvGetResponse',
        description    = 'Get a users list of rated TV shows.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/account/{account_id}/rated/tv/episodes',
        params         = [
            ParamDef(
                name        = 'account_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
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
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'sort_by',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'created_at.asc',
            ),
        ],
        response_model = 'Field3AccountAccountIdRatedTvEpisodesGetResponse',
        description    = 'Get a users list of rated TV episodes.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/account/{account_id}/watchlist/movies',
        params         = [
            ParamDef(
                name        = 'account_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
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
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'sort_by',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'created_at.asc',
            ),
        ],
        response_model = 'Field3AccountAccountIdWatchlistMoviesGetResponse',
        description    = 'Get a list of movies added to a users watchlist.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/account/{account_id}/watchlist/tv',
        params         = [
            ParamDef(
                name        = 'account_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
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
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'sort_by',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'created_at.asc',
            ),
        ],
        response_model = 'Field3AccountAccountIdWatchlistTvGetResponse',
        description    = 'Get a list of TV shows added to a users watchlist.',
    ),
]
