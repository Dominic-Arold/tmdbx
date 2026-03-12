from pydantic import BaseModel
from .account import *


# Maps the string names stored in EndpointDef.response_model / .request_model
# to the actual Pydantic classes.  Populated once at import time.
MODEL_REGISTRY: dict[str, type[BaseModel]] = {
    "AccountListsResponse":        AccountListsResponse,
    # "ListDetailsResponse":       ListDetailsResponse,
    # "ListCreateRequest":         ListCreateRequest,
    # ...
}