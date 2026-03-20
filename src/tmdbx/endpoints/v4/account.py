from tmdbx.endpoints._def import EndpointDef, HTTPMethod
from .params import *

ENDPOINTS: list[EndpointDef] = [
    EndpointDef(
        id              = "v4.account.lists",
        method          = HTTPMethod.GET,
        path_template   = "/4/account/{account_object_id}/lists",
        params          = [AccountObjectIdDef(), PageDef()],
        response_model  = "AccountListsGetResponse",
        cacheable       = True,
        cache_key_params = ["account_object_id", "page"],
        description     = "Get the custom lists that a user has created.",
    ),
    EndpointDef(
        id              = "v4.account.movie.favorites",
        method          = HTTPMethod.GET,
        path_template   = "/4/account/{account_object_id}/movie/favorites",
        params          = [AccountObjectIdDef(), PageDef(), LanguageDef(), SortByDef()],
        response_model  = "AccountMovieFavoritesGetResponse",
        cacheable       = True,
        description     = "Get a users list of favourite movies.",
    ),
    EndpointDef(
        id="v4.account.tv.favorites",
        method=HTTPMethod.GET,
        path_template="/4/account/{account_object_id}/tv/favorites",
        params=[AccountObjectIdDef(), PageDef(), LanguageDef(), SortByDef()],
        response_model="AccountTvFavoritesGetResponse",
        cacheable=True,
        description="Get a users list of favourite TV shows.",
    ),
    EndpointDef(
        id = "v4.account.movie.watchlist",
        method = HTTPMethod.GET,
        path_template = "/4/account/{account_object_id}/movie/watchlist",
        params = [AccountObjectIdDef(), PageDef(), LanguageDef(), SortByDef()],
        response_model = "AccountMovieWatchlistGetResponse",
        cacheable = True,
        description = "Get a users movie watchlist.",
    ),
]