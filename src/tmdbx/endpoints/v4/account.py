from tmdbx.endpoints._def import EndpointDef, HTTPMethod, ParamDef, ParamKind


ACCOUNT_LISTS = EndpointDef(
    id              = "account.lists",
    method          = HTTPMethod.GET,
    path_template   = "/4/account/{account_object_id}/lists",
    params          = [
        ParamDef(
            name        = "account_object_id",
            kind        = ParamKind.PATH,
            python_type = "str",
            required    = True,
            description = "The v4 account object ID",
        ),
        ParamDef(
            name        = "page",
            kind        = ParamKind.QUERY,
            python_type = "int",
            required    = False,
            default     = 1,
            description = "Page number",
        ),
    ],
    response_model  = "AccountListsResponse",
    cacheable       = True,
    cache_key_params = ["account_object_id", "page"],
    description     = "Get the custom lists that a user has created.",
)

ACCOUNT_FAVORITE_MOVIES = EndpointDef(
    id              = "account.favorite_movies",
    method          = HTTPMethod.GET,
    path_template   = "/4/account/{account_object_id}/movie/favorites",
    params          = [
        ParamDef(name="account_object_id", kind=ParamKind.PATH,  python_type="str", required=True),
        ParamDef(name="page",              kind=ParamKind.QUERY, python_type="int", required=False, default=1),
    ],
    response_model  = "AccountFavoriteMoviesResponse",
    cacheable       = True,
    description     = "Get the list of movies a user has favourited.",
)

# ... ACCOUNT_FAVORITE_TV, ACCOUNT_RATED_MOVIES, ACCOUNT_WATCHLIST_MOVIES, etc.
# All follow the same shape — parsed from the docs sidebar.

ACCOUNT_ENDPOINTS: list[EndpointDef] = [
    ACCOUNT_LISTS,
    ACCOUNT_FAVORITE_MOVIES,
    # ...
]