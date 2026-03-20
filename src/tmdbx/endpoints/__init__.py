"""
Importing this package populates ENDPOINT_REGISTRY with all known endpoints:
"""
from tmdbx.endpoints._registry import register
from tmdbx.endpoints.v3 import V3_ENDPOINTS
from tmdbx.endpoints.v4 import V4_ENDPOINTS

for ep in V3_ENDPOINTS + V4_ENDPOINTS:
    register(ep)

from tmdbx.endpoints._registry import ENDPOINT_REGISTRY