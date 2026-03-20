from __future__ import annotations

from pydantic import BaseModel

# Maps model class names to their classes.
# Populated automatically when any TMDBModel subclass is defined,
# filtered to names that look like response/request models.
MODEL_REGISTRY: dict[str, type["TMDBModel"]] = {}

# Prefixes/suffixes used to decide which subclasses to register.
# Hand-authored models (account.py etc.) use plain readable names like
# "AccountListsResponse" — these are caught by the suffix check alone.
# Generated v3 models use "Field3...Response" / "Field3...Request".
_REGISTER_SUFFIXES = ("Response", "Request")


class TMDBModel(BaseModel):
    """
    Base class for all TMDB response and request models.

    Subclasses whose names end with 'Response' or 'Request' are
    automatically inserted into MODEL_REGISTRY on class definition,
    making them available to the client without any manual wiring.

    Intermediate shared models (e.g. Genre, SpokenLanguage) are not
    registered — they are never looked up by name in the client.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if cls.__name__.endswith(_REGISTER_SUFFIXES):
            if cls.__name__ in MODEL_REGISTRY:
                raise ValueError(
                    f"Duplicate model name {cls.__name__!r} — "
                    f"already registered as {MODEL_REGISTRY[cls.__name__]!r}"
                )
            MODEL_REGISTRY[cls.__name__] = cls