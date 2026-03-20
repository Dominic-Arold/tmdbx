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
        description = "Retrieve a list by id.",
    ),
    EndpointDef(
        id             = "list:post",
        method         = HTTPMethod.POST,
        path_template  = "/4/list",
        params         = [],             # no path/query params; payload is a JSON body
    ),
    EndpointDef(
        id            = "list:delete",
        method        = HTTPMethod.DELETE,
        path_template = "/4/list/{list_id}",
        params        = [
            ParamDef(name="list_id", kind=ParamKind.PATH, python_type="int", required=True),
        ],
    ),
    EndpointDef(
        id            = "list.items:post",
        method        = HTTPMethod.POST,
        path_template = "/4/list/{list_id}/items",
        params        = [
            ParamDef(name="list_id", kind=ParamKind.PATH, python_type="int", required=True),
        ],
    ),
    EndpointDef(
        id            = "list:put",
        method        = HTTPMethod.PUT,
        path_template = "/4/list/{list_id}",
        params        = [
            ParamDef(name="list_id", kind=ParamKind.PATH, python_type="int", required=True),
        ],
    ),
]