from pydantic import BaseModel


class ListSummary(BaseModel):
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


class AccountListsResponse(BaseModel):
    """Paginated list of the user's custom lists."""
    page:          int
    results:       list[ListSummary]
    total_pages:   int
    total_results: int