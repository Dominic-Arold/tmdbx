from tmdbx.endpoints._def import EndpointDef, ParamKind, ParamDef, HTTPMethod

ENDPOINTS: list[EndpointDef] = [
    EndpointDef(
        id            = "list:get",
        method        = HTTPMethod.GET,
        path_template = "/4/list/{list_id}",
        params        = [
            ParamDef(name="list_id", kind=ParamKind.PATH,  python_type="int", required=True),
            ParamDef(name="page",    kind=ParamKind.QUERY, python_type="int", required=False, default=1),
        ],
        response_model = "ListGetResponse",
        cacheable      = True,
        description = "Retrieve a list by id.",
    ),
    EndpointDef(
        id             = "list:post",
        method         = HTTPMethod.POST,
        path_template  = "/4/list",
        params         = [],             # no path/query params; payload is a JSON body
        request_model  = "ListPostRequest",
        response_model = "ListPostResponse",
        cacheable      = False,
    ),
    EndpointDef(
        id            = "list:delete",
        method        = HTTPMethod.DELETE,
        path_template = "/4/list/{list_id}",
        params        = [
            ParamDef(name="list_id", kind=ParamKind.PATH, python_type="int", required=True),
        ],
        response_model = "ListDeleteResponse",
        cacheable      = False,
    ),
    EndpointDef(
        id            = "list.items:post",
        method        = HTTPMethod.POST,
        path_template = "/4/list/{list_id}/items",
        params        = [
            ParamDef(name="list_id", kind=ParamKind.PATH, python_type="int", required=True),
        ],
        request_model  = "ListItemsRequest",
        response_model = "ListItemsResponse",
        cacheable      = False,
    ),
    EndpointDef(
        id            = "list:put",
        method        = HTTPMethod.PUT,
        path_template = "/4/list/{list_id}",
        params        = [
            ParamDef(name="list_id", kind=ParamKind.PATH, python_type="int", required=True),
        ],
        request_model  = "ListUpdateRequest",
        response_model = "StatusResponse",
        cacheable      = False,
    ),
]