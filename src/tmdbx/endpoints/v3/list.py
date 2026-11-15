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
        method         = HTTPMethod.POST,
        path_template  = '/3/list/{list_id}/add_item',
        params         = [
            ParamDef(
                name        = 'list_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
            ),
        ],
        response_model = 'Field3ListListIdAddItemPostResponse',
        request_model  = 'Field3ListListIdAddItemPostRequest',
        description    = 'Add a movie to a list.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/list/{list_id}/item_status',
        params         = [
            ParamDef(
                name        = 'list_id',
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
                name        = 'movie_id',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
            ),
        ],
        response_model = 'Field3ListListIdItemStatusGetResponse',
        description    = 'Use this method to check if an item has already been added to the list.',
    ),
    EndpointDef(
        method         = HTTPMethod.POST,
        path_template  = '/3/list/{list_id}/clear',
        params         = [
            ParamDef(
                name        = 'list_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
            ),
            ParamDef(
                name        = 'confirm',
                kind        = ParamKind.QUERY,
                python_type = 'bool',
                required    = True,
                default     = False,
            ),
        ],
        response_model = 'Field3ListListIdClearPostResponse',
        description    = 'Clear all items from a list.',
    ),
    EndpointDef(
        method         = HTTPMethod.POST,
        path_template  = '/3/list',
        params         = [
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
            ),
        ],
        response_model = 'Field3ListPostResponse',
        request_model  = 'Field3ListPostRequest',
    ),
    EndpointDef(
        method         = HTTPMethod.DELETE,
        path_template  = '/3/list/{list_id}',
        params         = [
            ParamDef(
                name        = 'list_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
            ),
        ],
        response_model = 'Field3ListListIdDeleteResponse',
        description    = 'Delete a list.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/list/{list_id}',
        params         = [
            ParamDef(
                name        = 'list_id',
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
        ],
        response_model = 'Field3ListListIdGetResponse',
    ),
    EndpointDef(
        method         = HTTPMethod.POST,
        path_template  = '/3/list/{list_id}/remove_item',
        params         = [
            ParamDef(
                name        = 'list_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'session_id',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
            ),
        ],
        response_model = 'Field3ListListIdRemoveItemPostResponse',
        request_model  = 'Field3ListListIdRemoveItemPostRequest',
        description    = 'Remove a movie from a list.',
    ),
]
