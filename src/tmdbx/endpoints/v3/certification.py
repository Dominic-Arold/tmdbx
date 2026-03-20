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
        path_template  = '/3/certification/movie/list',
        params         = [],
        response_model = 'Field3CertificationMovieListGetResponse',
        description    = 'Get an up to date list of the officially supported movie certifications on TMDB.',
    ),
    EndpointDef(
        method         = HTTPMethod.GET,
        path_template  = '/3/certification/tv/list',
        params         = [],
        response_model = 'Field3CertificationTvListGetResponse',
    ),
]
