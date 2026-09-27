"""Public client for the Link-Shortly providers."""

from __future__ import annotations

import asyncio
import functools
from urllib.parse import urlparse
from typing import Any, Optional

from .errors import ShortlyValueError
from .utils import LinkShortly


class Shortly:
    """Shorten URLs through one of the supported provider APIs.

    ``convert`` can be called synchronously from normal Python code or awaited
    from an already-running asyncio event loop.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        if not isinstance(base_url, str) or not base_url.strip():
            raise ShortlyValueError("base_url must be a non-empty string")

        raw_url = base_url.strip()
        parsed = urlparse(raw_url if "://" in raw_url else f"//{raw_url}")
        self.base_url = (parsed.netloc or parsed.path).rstrip("/").lower()
        if not self.base_url:
            raise ShortlyValueError("base_url must be a non-empty string")

        if self.base_url == "tinyurl.com":
            # The legacy TinyURL endpoint does not require a token.
            self.api_key = api_key.strip() if isinstance(api_key, str) else api_key
        else:
            if not isinstance(api_key, str) or not api_key.strip():
                raise ShortlyValueError(
                    f"api_key must be a non-empty string for {self.base_url}"
                )
            self.api_key = api_key.strip()

    async def _convert_async(
        self,
        link: str,
        alias: Optional[str] = None,
        silently: bool = False,
        timeout: float = 10,
    ) -> str:
        """Convert a long URL into a short URL."""
        if not isinstance(link, str) or not link.strip():
            raise ShortlyValueError("link must be a non-empty string")
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ShortlyValueError("timeout must be a positive number")
        if alias is not None and (not isinstance(alias, str) or not alias.strip()):
            raise ShortlyValueError("alias must be a non-empty string when provided")

        client = LinkShortly(api_key=self.api_key, base_site=self.base_url)
        providers = {
            "tinyurl.com": client.tinyurl_convert,
            "shareus.io": client.shareus_convert,
            "bitly.com": client.bitly_convert,
            "ouo.io": client.ouo_convert,
        }
        converter = providers.get(self.base_url, client.adlinkfy_convert)
        return await converter(link.strip(), alias, silently, timeout)


def async_to_sync(obj: Any, name: str) -> None:
    """Wrap an async method so it works in sync and async callers."""
    function = getattr(obj, name)

    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        coroutine = function(*args, **kwargs)
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coroutine)
        return coroutine

    setattr(obj, name, wrapper)


Shortly.convert = Shortly._convert_async
async_to_sync(Shortly, "convert")
