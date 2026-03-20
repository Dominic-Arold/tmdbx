"""
Importing this package populates ENDPOINT_REGISTRY with all known endpoints:
"""
from tmdbx.endpoints._registry import register
from tmdbx.endpoints.v4 import account
from tmdbx.endpoints.v4 import lists

for ep in account.ENDPOINTS + lists.ENDPOINTS:
    register(ep)

from tmdbx.endpoints._registry import ENDPOINT_REGISTRY