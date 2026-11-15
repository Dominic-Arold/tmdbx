from tmdbx.endpoints._def import EndpointDef


ENDPOINT_REGISTRY: dict[str, EndpointDef] = {}


def register(ep: EndpointDef) -> EndpointDef:
    """
    Insert *ep* into ENDPOINT_REGISTRY.  Raises on duplicate id.
    Returns the endpoint unchanged so it can be used as a decorator.
    """
    if ep.id in ENDPOINT_REGISTRY:
        raise ValueError(
            f"Duplicate endpoint id {ep.id!r} — "
            f"already registered as {ENDPOINT_REGISTRY[ep.id]!r}"
        )
    ENDPOINT_REGISTRY[ep.id] = ep
    return ep
