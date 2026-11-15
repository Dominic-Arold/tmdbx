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
        method         = HTTPMethod.GET,
        path_template  = '/3/network/{network_id}',
        params         = [
            ParamDef(
                name        = 'network_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3NetworkNetworkIdGetResponse',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/network/{network_id}/alternative_names',
        params         = [
            ParamDef(
                name        = 'network_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3NetworkNetworkIdAlternativeNamesGetResponse',
        description    = 'Get the alternative names of a network.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/network/{network_id}/images',
        params         = [
            ParamDef(
                name        = 'network_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3NetworkNetworkIdImagesGetResponse',
        description    = 'Get the TV network logos by id.',
    ),
]
