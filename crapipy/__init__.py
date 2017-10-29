"""
Clash Royale wrapper for cr-api.com
"""
__version__ = "0.15"

from .client import Client
from .client_async import AsyncClient
from .exceptions import APITimeoutError, APIClientResponseError, APIError
# from .models_legacy import Clan, Tag, Player, Constants
from .url import APIURL
