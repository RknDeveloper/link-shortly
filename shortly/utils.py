"""
Link-Shortly - A simple URL shortening library.

@author:   RknDeveloper
@contact:  https://t.me/RknDeveloperr
@license:  MIT License, see LICENSE file

Copyright (c) 2025-present RknDeveloper
"""

import aiohttp
import asyncio
import json
from .errors import (
    ShortlyError,
    ShortlyInvalidLinkError,
    ShortlyLinkNotFoundError,
    ShortlyTimeoutError,
    ShortlyConnectionError,
    ShortlyJsonDecodeError
)

class LinkShortly:
    def __init__(self, api_key: str = None, base_site: str = None):
        self.api_key = api_key
        self.base_site = base_site

    async def adlinkfy_convert(self, link, alias=None, silently=False, timeout=30):  
        """  
        Shorten a URL using Link Shortly/All Adlinkfy API.  

        Parameters:  
            api_key (str): Your API key for the Shortly/GPLinks service.  
            base_url (str): The domain of the API (e.g., "gplinks.com", etc).  
            link (str): The long URL you want to shorten.  
            alias (str, optional): Custom alias for the short link. Default is None.  
            silently (bool): If True, the function will directly return the original URL without raising errors.  
            timeout (int, optional): Maximum seconds to wait for API response. Default is 30.  

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
        if silently:  
            return link
            
        api_url = f"https://{self.base_site}/api"  
        params = {"api": self.api_key, "url": link}  
     
        if alias:  
            params["alias"] = alias  

        try:  
            async with aiohttp.ClientSession() as session:  
                headers = {  
                    "User-Agent": (  
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "  
                        "AppleWebKit/537.36 (KHTML, like Gecko) "  
                        "Chrome/91.0.4472.124 Safari/537.36"  
                    )  
                }  
                async with session.get(api_url, params=params, headers=headers, timeout=timeout) as response:  
                    if response.status != 200:  
                        raise ShortlyError("Failed to shorten your link (bad response).")  
                    try:  
                        data = await response.json()  
                    except Exception as e:  
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

        except asyncio.TimeoutError:  
            raise ShortlyTimeoutError(f"Request timed out after {timeout} seconds.")  
        except aiohttp.ClientConnectionError:  
            raise ShortlyConnectionError(f"Failed to connect to {self.base_site}.")  
        except Exception as e:  
            raise ShortlyError(f"An unexpected error occurred: {e}")

    async def ouo_convert(self, link, alias=None, silently=False, timeout=30):
        """
        Shorten a URL using ouo.io API.

        Parameters:  
            link (str): Long URL to shorten.  
            alias (str, optional): (Not supported by ouo.io API, ignored).  
            silently (bool): If True, return original link without error.  
            timeout (int, optional): Request timeout.  
        """  
        if silently:  
            return link  

        # API endpoint  
        api_url = f"https://{self.base_site}/api/{self.api_key}"  
        params = {"s": link}  

        try:  
            async with aiohttp.ClientSession() as session:  
                async with session.get(api_url, params=params, timeout=timeout) as response:  
                    if response.status != 200:  
                        raise ShortlyError(f"Failed to shorten (HTTP {response.status})")  
                    
                    # You need to get the response text/content here  
                    short_url = await response.text()  
                    return short_url.strip()  # Return the shortened URL  
                    
        except asyncio.TimeoutError:  
            raise ShortlyTimeoutError(f"Ouo.io request timed out after {timeout} seconds.")  
        except aiohttp.ClientConnectionError:  
            raise ShortlyConnectionError("Failed to connect to ouo.io.")  
        except Exception as e:  
            raise ShortlyError(f"Ouo.io unexpected error: {e}")

    async def shareus_convert(self, link, alias=None, silently=False, timeout=30):
        """
        Shorten a URL using Shareus.io API.

        Parameters:  
            api_key (str): Your API key for the Shareus service.  
            base_url (str): The domain of the API (should be "shareus.io").  
            link (str): The long URL you want to shorten.  
            alias (str, optional): Custom alias for the short link. Default is None.  
            silently (bool): If True, the function will directly return the original URL without raising errors.  
            timeout (int, optional): Maximum seconds to wait for API response. Default is 30.  

        Returns:  
            str: The shortened URL returned by the API.  

        Raises:  
            ShortlyInvalidLinkError: If the provided link is invalid or malformed.  
            ShortlyLinkNotFoundError: If the short link does not exist or has expired.  
            ShortlyTimeoutError: If request exceeds the allowed timeout.  
            ShortlyConnectionError: If cannot connect to API server.  
            ShortlyError: For other API-related errors.  
        """  
        if silently:  
            return link  

        # Shareus.io API configuration  
        api_url = f"https://api.{self.base_site}/easy_api"  
        params = {"key": self.api_key, "link": link}  
        
        if alias:  
            params["alias"] = alias  

        try:  
            async with aiohttp.ClientSession() as session:  
                headers = {  
                    "User-Agent": (  
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "  
                        "AppleWebKit/537.36 (KHTML, like Gecko) "  
                        "Chrome/91.0.4472.124 Safari/537.36"  
                    )  
                }  
                
                async with session.get(api_url, params=params, headers=headers, timeout=timeout) as response:  
                    if response.status != 200:  
                        raise ShortlyError(f"Failed to shorten your link (HTTP {response.status}).")  
                    
                    # Shareus returns plain text response  
                    data_text = await response.text()  
                    
                    if data_text == "settings not saved":  
                        raise ShortlyError("Settings not saved or invalid API key.")  
                    
                    # Check if response looks like an error  
                    if any(error_indicator in data_text.lower() for error_indicator in ["error", "invalid", "not found", "failed"]):  
                        if "invalid" in data_text.lower():  
                            raise ShortlyInvalidLinkError(data_text)  
                        elif "not found" in data_text.lower() or "expired" in data_text.lower():  
                            raise ShortlyLinkNotFoundError(data_text)  
                        else:  
                            raise ShortlyError(data_text)  
                    
                    # If we get here, it's likely a successful shortening  
                    return data_text  

        except asyncio.TimeoutError:  
            raise ShortlyTimeoutError(f"Request timed out after {timeout} seconds.")  
        except aiohttp.ClientConnectionError:  
            raise ShortlyConnectionError(f"Failed to connect to {self.base_site}.")  
        except json.JSONDecodeError as e:  
            # This is expected for Shareus as it returns plain text, not JSON  
            raise ShortlyJsonDecodeError(f"Json Error: {e}")  
        except Exception as e:  
            raise ShortlyError(f"An unexpected error occurred: {e}")

    async def tinyurl_convert(self, link, alias=None, silently=False, timeout=30):
        """
        Shorten a URL using TinyURL API - supports both old (no token) and new (with token) APIs
        """
        if silently:
            return link

        # Check if we have a token to decide which API to use  
        if hasattr(self, 'api_key') and self.api_key:  
            return await self._tinyurl_new_api(link, alias, timeout)  
        else:  
            return await self._tinyurl_old_api(link, alias, timeout)

    async def _tinyurl_old_api(self, link, alias=None, timeout=30):
        """
        Old TinyURL API (no token required)
        Docs: https://tinyurl.com/api-create.php
        """
        api_url = f"https://{self.base_site}/api-create.php"
        params = {"url": link}

        if alias:  
            params["alias"] = alias  

        try:  
            async with aiohttp.ClientSession() as session:  
                async with session.get(api_url, params=params, timeout=timeout) as response:  
                    if response.status != 200:  
                        raise ShortlyError(f"Failed to shorten link (TinyURL error: {response.status}).")  
                    
                    shortened_url = await response.text()  
                    
                    if "Error:" in shortened_url:  
                        raise ShortlyError(f"TinyURL error: {shortened_url}")  
                    
                    return shortened_url.strip()  
                    
        except asyncio.TimeoutError:  
            raise ShortlyTimeoutError(f"TinyURL request timed out after {timeout} seconds.")  
        except aiohttp.ClientConnectionError:  
            raise ShortlyConnectionError("Failed to connect to TinyURL.")  
        except Exception as e:  
            raise ShortlyError(f"TinyURL unexpected error: {e}")

    async def _tinyurl_new_api(self, link, alias=None, timeout=30):
        """
        New TinyURL API (requires token)
        Docs: https://tinyurl.com/app/dev/api
        """

        api_url = f"https://api.{self.base_site}/create"    
        headers = {    
            "Authorization": f"Bearer {self.api_key}",    
            "Content-Type": "application/json"    
        }    
        
        payload = {    
            "url": link,    
            "domain": "tinyurl.com"    
        }    
        
        if alias:    
            payload["alias"] = alias    

        try:    
            async with aiohttp.ClientSession() as session:    
                async with session.post(    
                    api_url,   
                    json=payload,   
                    headers=headers,   
                    timeout=timeout    
                ) as response:  
                    
                    # 🔹 Safe JSON parsing with better error handling  
                    try:    
                        response_data = await response.json(content_type=None)    
                    except Exception:    
                        response_text = await response.text()  
                        response_data = {"raw": response_text}  
                        
                        # Handle case where alias already exists (returns string)  
                        if "alias already exists" in response_text.lower():  
                            raise ShortlyError("Custom alias already exists. Please choose a different one.")  

                    if response.status == 200 and "data" in response_data:    
                        return response_data["data"]["tiny_url"]    

                    elif response.status == 401:    
                        raise ShortlyError("Invalid TinyURL API token.")    

                    elif response.status == 422:    
                        error_msg = "Unknown validation error"    
                        if isinstance(response_data, dict):    
                            errors = response_data.get("errors")    
                            if isinstance(errors, list) and errors:    
                                error_msg = errors[0].get("message", error_msg)    
                        elif isinstance(response_data, str):    
                            error_msg = response_data    
                        raise ShortlyError(f"TinyURL validation error: {error_msg}")    

                    elif response.status == 429:    
                        raise ShortlyError("TinyURL rate limit exceeded. Please try again later.")    

                    else:    
                        # Handle string responses gracefully  
                        if isinstance(response_data, str):  
                            error_message = response_data  
                        elif isinstance(response_data, dict) and "raw" in response_data:  
                            error_message = response_data["raw"]  
                        else:  
                            error_message = str(response_data)  
                        
                        raise ShortlyError(f"TinyURL API error: {response.status} - {error_message}")    
                    
        except asyncio.TimeoutError:    
            raise ShortlyTimeoutError(f"TinyURL request timed out after {timeout} seconds.")  
        except aiohttp.ClientConnectionError:    
            raise ShortlyConnectionError("Failed to connect to TinyURL API.")  
        except Exception as e:    
            raise ShortlyError(f"TinyURL unexpected error: {e}")

    async def bitly_convert(self, link, alias=None, silently=False, timeout=30):
        """
        Bitly API का उपयोग करके URL को छोटा (shorten) करें।
        Docs: https://dev.bitly.com/api-reference
        """
        if silently:
            return link

        api_url = f"https://api-ssl.{self.base_site}/v4/shorten"  
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}  
        payload = {"long_url": link}  
        
        # Correct way to add custom alias  
        if alias:        
            payload["custom_bitlink"] = alias  
            
        try:  
            async with aiohttp.ClientSession() as session:  
                async with session.post(api_url, headers=headers, json=payload, timeout=timeout) as response:  
                    
                    # Different error cases handle करें  
                    if response.status == 401:  
                        raise ShortlyError("Invalid Bitly API key")  
                    elif response.status == 400:  
                        error_text = await response.text()  
                        if "CUSTOM_BITLINK_ALREADY_EXISTS" in error_text:  
                            raise ShortlyError(f"Custom alias '{alias}' already exists on Bitly")  
                        elif "INVALID_CUSTOM_BITLINK" in error_text:  
                            raise ShortlyError(f"Invalid custom alias: {alias}")  
                        else:  
                            raise ShortlyError("Invalid URL provided to Bitly")  
                    elif response.status == 403:  
                        raise ShortlyError("Bitly API permission denied")  
                    elif response.status == 409:  
                        raise ShortlyError("Custom alias already exists")  
                    elif response.status != 200 and response.status != 201:  
                        raise ShortlyError(f"Bitly error: {await response.text()}")  
                    
                    try:  
                        data = await response.json()  
                    except Exception as e:  
                        raise ShortlyJsonDecodeError(f"Invalid JSON from Bitly: {e}")  
                        
                    return data.get("link")  
                    
        except asyncio.TimeoutError:  
            raise ShortlyTimeoutError(f"Bitly request timed out after {timeout} seconds.")  
        except aiohttp.ClientConnectionError:  
            raise ShortlyConnectionError("Failed to connect to Bitly.")  
        except Exception as e:  
            raise ShortlyError(f"Bitly unexpected error: {e}")