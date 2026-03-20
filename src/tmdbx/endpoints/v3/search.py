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
        path_template  = '/3/search/collection',
        params         = [
            ParamDef(
                name        = 'query',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
            ),
            ParamDef(
                name        = 'include_adult',
                kind        = ParamKind.QUERY,
                python_type = 'bool',
                required    = False,
                default     = False,
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
            ParamDef(
                name        = 'region',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3SearchCollectionGetResponse',
        description    = 'Search for collections by their original, translated and alternative names.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/search/company',
        params         = [
            ParamDef(
                name        = 'query',
                kind        = ParamKind.QUERY,
                python_type = 'str',
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
        response_model = 'Field3SearchCompanyGetResponse',
        description    = 'Search for companies by their original and alternative names.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/search/keyword',
        params         = [
            ParamDef(
                name        = 'query',
                kind        = ParamKind.QUERY,
                python_type = 'str',
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
        response_model = 'Field3SearchKeywordGetResponse',
        description    = 'Search for keywords by their name.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/search/movie',
        params         = [
            ParamDef(
                name        = 'query',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
            ),
            ParamDef(
                name        = 'include_adult',
                kind        = ParamKind.QUERY,
                python_type = 'bool',
                required    = False,
                default     = False,
            ),
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
            ParamDef(
                name        = 'primary_release_year',
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
                name        = 'region',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
            ParamDef(
                name        = 'year',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
            ),
        ],
        response_model = 'Field3SearchMovieGetResponse',
        description    = 'Search for movies by their original, translated and alternative titles.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/search/multi',
        params         = [
            ParamDef(
                name        = 'query',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
            ),
            ParamDef(
                name        = 'include_adult',
                kind        = ParamKind.QUERY,
                python_type = 'bool',
                required    = False,
                default     = False,
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
        response_model = 'Field3SearchMultiGetResponse',
        description    = 'Use multi search when you want to search for movies, TV shows and people in a single request.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/search/person',
        params         = [
            ParamDef(
                name        = 'query',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
            ),
            ParamDef(
                name        = 'include_adult',
                kind        = ParamKind.QUERY,
                python_type = 'bool',
                required    = False,
                default     = False,
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
        response_model = 'Field3SearchPersonGetResponse',
        description    = 'Search for people by their name and also known as names.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/search/tv',
        params         = [
            ParamDef(
                name        = 'query',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = True,
            ),
            ParamDef(
                name        = 'first_air_date_year',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                description = 'Search only the first air date. Valid values are: 1000..9999',
            ),
            ParamDef(
                name        = 'include_adult',
                kind        = ParamKind.QUERY,
                python_type = 'bool',
                required    = False,
                default     = False,
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
            ParamDef(
                name        = 'year',
                kind        = ParamKind.QUERY,
                python_type = 'int',
                required    = False,
                description = 'Search the first air date and all episode air dates. Valid values are: 1000..9999',
            ),
        ],
        response_model = 'Field3SearchTvGetResponse',
        description    = 'Search for TV shows by their original, translated and also known as names.',
    ),
]
