from pydantic import BaseModel
from tmdbx.models._base import TMDBModel

class ListsItem(BaseModel):
    account_object_id:  str
    adult:              bool    = False
    average_rating:     float   = 0.0
    created_at:         str
    description:        str
    featured:           bool    = False
    id:                 int     = 0
    iso_3166_1:         str
    iso_639_1:          str
    name:               str
    number_of_items:    int     = 0
    public:             bool    = False
    revenue:            int
    runtime:            int     = 0
    sort_by:            int     = 0
    updated_at:         str


class PaginatedList(TMDBModel):
    """Paginated list Response."""
    page:          int
    results:       list
    total_pages:   int
    total_results: int


class AccountListsGetResponse(PaginatedList):
    """Paginated list of the user's custom lists."""
    results:       list[ListsItem]


class AccountMovieFavoritesItem(BaseModel):
    adult: bool
    backdrop_path: str
    genre_ids: list[int]
    id: int
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    release_date: str
    title: str
    video: bool
    vote_average: float
    vote_count: int


class AccountMovieFavoritesGetResponse(PaginatedList):
    results: list[AccountMovieFavoritesItem]


class AccountMovieWatchlistItem(BaseModel):
    adult:             bool         = True
    backdrop_path:     str
    genre_ids:         list[int]
    id:                int          = 0
    original_language: str 
    original_title:    str 
    overview:          str
    popularity:        float        = 0
    poster_path:       str
    release_date:      str
    title:             str
    video:             bool         = True
    vote_average:      float        = 0
    vote_count:        int          = 0


class AccountMovieWatchlistGetResponse(PaginatedList):
    results: list[AccountMovieWatchlistItem]