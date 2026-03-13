from tmdbx.endpoints._def import EndpointDef, HTTPMethod, ParamDef, ParamKind
from .params import AccountObjectIdDef, PageDef, SortByDef


ACCOUNT_LISTS = EndpointDef(
    id              = "v4.account.lists",
    method          = HTTPMethod.GET,
    path_template   = "/4/account/{account_object_id}/lists",
    params          = [AccountObjectIdDef(), PageDef()],
    response_model  = "AccountListsResponse",
    cacheable       = True,
    cache_key_params = ["account_object_id", "page"],
    description     = "Get the custom lists that a user has created.",
)

ACCOUNT_FAVORITE_MOVIES = EndpointDef(
    id              = "v4.account.movie.favorites",
    method          = HTTPMethod.GET,
    path_template   = "/4/account/{account_object_id}/movie/favorites",
    params          = [AccountObjectIdDef(), PageDef(), SortByDef()],
    response_model  = "AccountFavoriteMoviesResponse",
    cacheable       = True,
    description     = "Get a users list of favourite movies.",
)



ACCOUNT_WATCHLIST_MOVIES = EndpointDef(
    id = "v4.account.movie.watchlist",
    method = HTTPMethod.GET,
    path_template = "/4/account/{account_object_id}/movie/watchlist",
    params = [AccountObjectIdDef(), PageDef(), SortByDef()],
    response_model = "AccountWatchlistMoviesResponse",
    cacheable = True,
    description = "Get a users movie watchlist.",
)

# ... ACCOUNT_FAVORITE_TV, ACCOUNT_RATED_MOVIES, ACCOUNT_WATCHLIST_MOVIES, etc.
# All follow the same shape — parsed from the docs sidebar.

ACCOUNT_ENDPOINTS: list[EndpointDef] = [
    ACCOUNT_LISTS,
    ACCOUNT_FAVORITE_MOVIES,
    ACCOUNT_WATCHLIST_MOVIES
    # ...
]