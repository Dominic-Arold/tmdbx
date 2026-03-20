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
        path_template  = '/3/person/changes',
        params         = [
            ParamDef(
                name        = 'end_date',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'start_date',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3PersonChangesGetResponse',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/person/popular',
        params         = [
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
        response_model = 'Field3PersonPopularGetResponse',
        description    = 'Get a list of people ordered by popularity.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/person/{person_id}',
        params         = [
            ParamDef(
                name        = 'person_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'append_to_response',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                description = 'comma separated list of endpoints within this namespace, 20 items max',
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
        ],
        response_model = 'Field3PersonPersonIdGetResponse',
        description    = 'Query the top level details of a person.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/person/{person_id}/changes',
        params         = [
            ParamDef(
                name        = 'person_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'end_date',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
            ParamDef(
                name        = 'start_date',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3PersonPersonIdChangesGetResponse',
        description    = 'Get the recent changes for a person.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/person/{person_id}/combined_credits',
        params         = [
            ParamDef(
                name        = 'person_id',
                kind        = ParamKind.PATH,
                python_type = 'str',
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
        response_model = 'Field3PersonPersonIdCombinedCreditsGetResponse',
        description    = 'Get the combined movie and TV credits that belong to a person.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/person/{person_id}/external_ids',
        params         = [
            ParamDef(
                name        = 'person_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3PersonPersonIdExternalIdsGetResponse',
        description    = "Get the external ID's that belong to a person.",
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/person/{person_id}/images',
        params         = [
            ParamDef(
                name        = 'person_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3PersonPersonIdImagesGetResponse',
        description    = 'Get the profile images that belong to a person.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/person/latest',
        params         = [],
        response_model = 'Field3PersonLatestGetResponse',
        description    = 'Get the newest created person. This is a live response and will continuously change.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/person/{person_id}/movie_credits',
        params         = [
            ParamDef(
                name        = 'person_id',
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
        response_model = 'Field3PersonPersonIdMovieCreditsGetResponse',
        description    = 'Get the movie credits for a person.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/person/{person_id}/tv_credits',
        params         = [
            ParamDef(
                name        = 'person_id',
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
        response_model = 'Field3PersonPersonIdTvCreditsGetResponse',
        description    = 'Get the TV credits that belong to a person.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/person/{person_id}/tagged_images',
        params         = [
            ParamDef(
                name        = 'person_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
            ParamDef(
                name        = 'page',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                default     = 1,
            ),
        ],
        response_model = 'Field3PersonPersonIdTaggedImagesGetResponse',
        description    = 'Get the tagged images for a person.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/person/{person_id}/translations',
        params         = [
            ParamDef(
                name        = 'person_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3PersonPersonIdTranslationsGetResponse',
        description    = 'Get the translations that belong to a person.',
    ),
]
