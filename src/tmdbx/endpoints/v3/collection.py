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
        path_template  = '/3/collection/{collection_id}',
        params         = [
            ParamDef(
                name        = 'collection_id',
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
        ],
        response_model = 'Field3CollectionCollectionIdGetResponse',
        description    = 'Get collection details by ID.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/collection/{collection_id}/images',
        params         = [
            ParamDef(
                name        = 'collection_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'include_image_language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                description = 'specify a comma separated list of ISO-639-1 values to query, for example: `en-US,null`',
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3CollectionCollectionIdImagesGetResponse',
        description    = 'Get the images that belong to a collection.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/collection/{collection_id}/translations',
        params         = [
            ParamDef(
                name        = 'collection_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3CollectionCollectionIdTranslationsGetResponse',
    ),
]
