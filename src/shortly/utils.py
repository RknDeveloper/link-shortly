"""
link-shortly - A simple URL shortening library.

@author:   RknDeveloper
@contact:  https://t.me/RknDeveloperr
@license:  MIT License, see LICENSE file

Copyright (c) 2025-present RknDeveloper
"""

import requests
import json
from .exceptions import (
    ShortlyError,
    ShortlyInvalidLinkError,
    ShortlyLinkNotFoundError,
    ShortlyTimeoutError,
    ShortlyConnectionError,
    ShortlyJsonDecodeError
)

def convert(self, link, alias=None, timeout=10):
    """
    Shorten a URL using Link Shortly/All Adlinkfy API.

    Parameters:
        api_key (str): Your API key for the Shortly/GPLinks service.
        base_url (str): The domain of the API (e.g., "gplinks.com", etc).
        link (str): The long URL you want to shorten.
        alias (str, optional): Custom alias for the short link. Default is None.
        timeout (int, optional): Maximum seconds to wait for API response. Default is 10.

    Returns:
        str: The shortened URL returned by the API.

    Raises:
        ShortlyInvalidLinkError: If the provided link is invalid or malformed.
        ShortlyLinkNotFoundError: If the short link does not exist or has expired.
        ShortlyTimeoutError: If request exceeds the allowed timeout.
        ShortlyConnectionError: If cannot connect to API server.
        ShortlyJsonDecodeError: If API response is not valid JSON.
        ShortlyError: For other API-related errors.
    """

    api_url = f"https://{self.base_url}/api"
    params = {"api": self.api_key, "url": link}
    if alias:
        params["alias"] = alias

    try:
        # request session started
        with requests.Session() as session:
            session.headers.update({
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
            })

            response = session.get(self.api_url, params=params, timeout=timeout)

            if response.status_code != 200 or not response.text.strip():
                raise ShortlyError("Failed to shorten your link (empty or bad response).")

            try:
                data = response.json()
            except json.JSONDecodeError as e:
                raise ShortlyJsonDecodeError(f"Invalid JSON response: {e}")

            status = data.get("status", "").lower()
            message = data.get("message", "Unknown error")

            if status != "success":
                if "invalid" in message.lower():
                    raise ShortlyInvalidLinkError(message)
                elif "not found" in message.lower() or "expired" in message.lower():
                    raise ShortlyLinkNotFoundError(message)
                else:
                    raise ShortlyError(message)

            return data.get("shortenedUrl")

    except requests.exceptions.Timeout:
        raise ShortlyTimeoutError(f"Request timed out after {timeout} seconds.")
    except requests.exceptions.ConnectionError:
        raise ShortlyConnectionError(f"Failed to connect to {self.base_url}.")
    except requests.exceptions.RequestException as e:
        raise ShortlyError(f"An unexpected error occurred: {e}")
