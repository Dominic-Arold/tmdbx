from tmdbx.endpoints._def import EndpointDef, ParamKind, ParamDef, HTTPMethod

LIST_DETAILS = EndpointDef(
    id            = "list.details",
    method        = HTTPMethod.GET,
    path_template = "/4/list/{list_id}",
    params        = [
        ParamDef(name="list_id", kind=ParamKind.PATH,  python_type="int", required=True),
        ParamDef(name="page",    kind=ParamKind.QUERY, python_type="int", required=False, default=1),
    ],
    response_model = "ListDetailsResponse",
    cacheable      = True,
)

LIST_CREATE = EndpointDef(
    id             = "list.create",
    method         = HTTPMethod.POST,
    path_template  = "/4/list",
    params         = [],             # no path/query params; payload is a JSON body
    request_model  = "ListCreateRequest",
    response_model = "ListCreateResponse",
    cacheable      = False,
    description    = "Create a new list.",
)

LIST_DELETE = EndpointDef(
    id            = "list.delete",
    method        = HTTPMethod.DELETE,
    path_template = "/4/list/{list_id}",
    params        = [
        ParamDef(name="list_id", kind=ParamKind.PATH, python_type="int", required=True),
    ],
    response_model = "StatusResponse",
    cacheable      = False,
)

LIST_ADD_ITEMS = EndpointDef(
    id            = "list.add_items",
    method        = HTTPMethod.POST,
    path_template = "/4/list/{list_id}/items",
    params        = [
        ParamDef(name="list_id", kind=ParamKind.PATH, python_type="int", required=True),
    ],
    request_model  = "ListItemsRequest",
    response_model = "ListItemsResponse",
    cacheable      = False,
)

LIST_UPDATE = EndpointDef(
    id            = "list.update",
    method        = HTTPMethod.PUT,
    path_template = "/4/list/{list_id}",
    params        = [
        ParamDef(name="list_id", kind=ParamKind.PATH, python_type="int", required=True),
    ],
    request_model  = "ListUpdateRequest",
    response_model = "StatusResponse",
    cacheable      = False,
)

LISTS_ENDPOINTS: list[EndpointDef] = [
    LIST_DETAILS, LIST_CREATE, LIST_DELETE, LIST_ADD_ITEMS, LIST_UPDATE,
    # LIST_CLEAR, LIST_ITEM_STATUS, LIST_REMOVE_ITEMS, LIST_UPDATE_ITEMS
]