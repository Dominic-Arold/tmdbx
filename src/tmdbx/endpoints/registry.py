from .v4.account import ACCOUNT_ENDPOINTS
# from .auth    import AUTH_ENDPOINTS
from .v4.lists   import LISTS_ENDPOINTS
from ._def import EndpointDef


# Flat lookup by dot-notation id.  Built at import time, fails fast on duplicates.
REGISTRY: dict[str, EndpointDef] = {}

for _ep in [*ACCOUNT_ENDPOINTS, *LISTS_ENDPOINTS]:  # + AUTH_ENDPOINTS, etc.
    assert _ep.id not in REGISTRY, f"Duplicate endpoint id: {_ep.id}"
    REGISTRY[_ep.id] = _ep


