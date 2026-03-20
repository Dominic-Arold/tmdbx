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
        path_template  = '/3/company/{company_id}',
        params         = [
            ParamDef(
                name        = 'company_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3CompanyCompanyIdGetResponse',
        description    = 'Get the company details by ID.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/company/{company_id}/alternative_names',
        params         = [
            ParamDef(
                name        = 'company_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3CompanyCompanyIdAlternativeNamesGetResponse',
        description    = 'Get the company details by ID.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/company/{company_id}/images',
        params         = [
            ParamDef(
                name        = 'company_id',
                kind        = ParamKind.PATH,
                python_type = 'int',
                required    = True,
            ),
        ],
        response_model = 'Field3CompanyCompanyIdImagesGetResponse',
        description    = 'Get the company logos by id.',
    ),
]
