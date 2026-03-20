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
        path_template  = '/3/configuration',
        params         = [],
        response_model = 'Field3ConfigurationGetResponse',
        description    = 'Query the API configuration details.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/configuration/countries',
        params         = [
            ParamDef(
                name        = 'language',
                kind        = ParamKind.QUERY,
                python_type = 'str',
                required    = False,
                default     = 'en-US',
            ),
        ],
        response_model = 'Field3ConfigurationCountriesGetResponse',
        description    = 'Get the list of countries (ISO 3166-1 tags) used throughout TMDB.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/configuration/jobs',
        params         = [],
        response_model = 'Field3ConfigurationJobsGetResponse',
        description    = 'Get the list of the jobs and departments we use on TMDB.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/configuration/languages',
        params         = [],
        response_model = 'Field3ConfigurationLanguagesGetResponse',
        description    = 'Get the list of languages (ISO 639-1 tags) used throughout TMDB.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/configuration/primary_translations',
        params         = [],
        response_model = 'Field3ConfigurationPrimaryTranslationsGetResponse',
        description    = 'Get a list of the officially supported translations on TMDB.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/configuration/timezones',
        params         = [],
        response_model = 'Field3ConfigurationTimezonesGetResponse',
        description    = 'Get the list of timezones used throughout TMDB.',
    ),
]
