"""
Link-Shortly - A simple URL shortening library.

@author:   RknDeveloper
@contact:  https://t.me/RknDeveloperr
@license:  MIT License, see LICENSE file

Copyright (c) 2025-present RknDeveloper
"""

import asyncio
import functools
from .utils import LinkShortly

from .errors import (
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
        
        self.base_url = (urlparse(base_url).netloc or urlparse(base_url).path).rstrip("/")

        if self.base_url == "tinyurl.com":
            # api_key optional
            self.api_key = api_key
        else:
            # api_key required
            if not api_key or not isinstance(api_key, str):
                raise ShortlyValueError(f"api_key must be a non-empty string for {self.base_url}")
            self.api_key = api_key
            
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
        # LinkShortly instance create 
        shortly_client = LinkShortly(api_key=self.api_key, base_site=self.base_url)
        
        if self.base_url == "tinyurl.com":
            self.shortner = await shortly_client.tinyurl_convert(link, alias, silently, timeout)
        elif self.base_url == "shareus.io":
            self.shortner = await shortly_client.shareus_convert(link, alias, silently, timeout)   
        elif self.base_url == "bitly.com":
            self.shortner = await shortly_client.bitly_convert(link, alias, silently, timeout)
        elif self.base_url == "ouo.io":  
            self.shortner = await shortly_client.ouo_convert(link, alias, silently, timeout)
        else:
            self.shortner = await shortly_client.adlinkfy_convert(link, alias, silently, timeout)
            
        return self.shortner


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