"""
Link-Shortly - A simple URL shortening library.

@author:   RknDeveloper
@contact:  https://t.me/RknDeveloperr
@license:  MIT License, see LICENSE file

Copyright (c) 2025-present RknDeveloper
"""

import asyncio
import functools
from .utils import convert as _utils_convert
from .exceptions import (
    ShortlyValueError
)
from urllib.parse import urlparse

class Shortly:
    def __init__(self, api_key=None, base_url=None):
        """
        Initialize Shortly instance.
        
        Input:
            api_key (str)  -> API key for authentication
            base_url (str) -> Base API URL of the shortening service
        
        Output:
            Stores api_key and base_url in the object
            
        Raises:
            ShortlyValueError: api_key & base_url must be a non-empty string
        
        """
        if not base_url or not isinstance(base_url, str):
            raise ShortlyValueError("base_url must be a non-empty string")
        if not api_key or not isinstance(api_key, str):
            raise ShortlyValueError("api_key must be a non-empty string")
            
        self.api_key = api_key
        self.base_url = (urlparse(base_url).netloc or urlparse(base_url).path).rstrip("/")

    # Internal async method calling utils.convert
    async def _convert_async(self, link, alias=None, silently=False, timeout=10):
        """
        Convert a long link into a short one using alias.

        Input:
            link (str)    -> The long URL to shorten
            alias (str)   -> Custom alias for the shortened URL
            silently (bool) -> If True, the function will directly return the original URL without raising errors.
            timeout (int) -> Request timeout in seconds (default: 10)

        Output:
            Returns shortened link or error response from utils.convert
        """
        return await _utils_convert(self, link, alias, silently, timeout)


# -------------------------------
# Wrapper to support sync + async
# -------------------------------
def async_to_sync(obj, name):
    function = getattr(obj, name)

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        coroutine = function(*args, **kwargs)
        try:
            # Async context → return coroutine
            asyncio.get_running_loop()
            return coroutine
        except RuntimeError:
            # Sync context → internally run
            return asyncio.run(coroutine)

    setattr(obj, name, wrapper)


# -------------------------------
# Apply wrapper to Shortly.convert
# -------------------------------
Shortly.convert = Shortly._convert_async   # temporary assign
async_to_sync(Shortly, "convert")         # convert() now supports sync + async