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
        path_template  = '/3/authentication',
        params         = [],
        response_model = 'Field3AuthenticationGetResponse',
        description    = "Test your API Key to see if it's valid.",
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/authentication/guest_session/new',
        params         = [],
        response_model = 'Field3AuthenticationGuestSessionNewGetResponse',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/authentication/token/new',
        params         = [],
        response_model = 'Field3AuthenticationTokenNewGetResponse',
    ),
    EndpointDef(
        method         = HTTPMethod.POST,
        path_template  = '/3/authentication/session/new',
        params         = [],
        response_model = 'Field3AuthenticationSessionNewPostResponse',
        request_model  = 'Field3AuthenticationSessionNewPostRequest',
    ),
    EndpointDef(
        method         = HTTPMethod.POST,
        path_template  = '/3/authentication/session/convert/4',
        params         = [],
        response_model = 'Field3AuthenticationSessionConvert4PostResponse',
        request_model  = 'Field3AuthenticationSessionConvert4PostRequest',
    ),
    EndpointDef(
        method         = HTTPMethod.POST,
        path_template  = '/3/authentication/token/validate_with_login',
        params         = [],
        response_model = 'Field3AuthenticationTokenValidateWithLoginPostResponse',
        request_model  = 'Field3AuthenticationTokenValidateWithLoginPostRequest',
        description    = 'This method allows an application to validate a request token by entering a username and password.',
    ),
    EndpointDef(
        method         = HTTPMethod.DELETE,
        path_template  = '/3/authentication/session',
        params         = [],
        response_model = 'Field3AuthenticationSessionDeleteResponse',
    ),
]
