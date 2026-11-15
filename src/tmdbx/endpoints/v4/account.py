from tmdbx.endpoints._def import EndpointDef, HTTPMethod
from .params import *

ENDPOINTS: list[EndpointDef] = [
    EndpointDef(
        method          = HTTPMethod.GET,
        path_template   = "/4/account/{account_object_id}/lists",
        params          = [AccountObjectIdDef(), PageDef()],
        description     = "Get the custom lists that a user has created.",
    ),
    EndpointDef(
        method          = HTTPMethod.GET,
        path_template   = "/4/account/{account_object_id}/movie/favorites",
        params          = [AccountObjectIdDef(), PageDef(), LanguageDef(), SortByDef()],
        description     = "Get a users list of favourite movies.",
    ),
    EndpointDef(
        method=HTTPMethod.GET,
        path_template="/4/account/{account_object_id}/tv/favorites",
        params=[AccountObjectIdDef(), PageDef(), LanguageDef(), SortByDef()],
        description="Get a users list of favourite TV shows.",
    ),
    EndpointDef(
        method = HTTPMethod.GET,
        path_template = "/4/account/{account_object_id}/movie/watchlist",
        params = [AccountObjectIdDef(), PageDef(), LanguageDef(), SortByDef()],
        description = "Get a users movie watchlist.",
    ),
]