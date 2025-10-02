## Link Shortly

A simple yet powerful async URL shortener library supporting multiple providers (TinyURL, Bitly, Ouo.io, Adlinkfy, Shareus.io, etc).

[![PyPI](https://img.shields.io/pypi/v/link-shortly.svg)](https://pypi.org/project/link-shortly/)
[![License](https://img.shields.io/github/license/RknDeveloper/link-shortly)](LICENSE)
[![Downloads](https://pepy.tech/badge/link-shortly)](https://pepy.tech/project/link-shortly)

## Installation

Install link-shortly with pip
```python
pip install link-shortly
```

To Upgrade
```python
pip install --upgrade link-shortly
```

## Quick Usage Example ( supports sync )
```python
from shortly import Shortly

shortly = Shortly(api_key='<YOUR API KEY>', base_url='<YOUR BASE SITE>')

def main():
    link = shortly.convert("https://example.com/long-url")
    print(link)

if __name__ == "__main__":
    main()
```

## Quick Usage Example ( supports async  )
```python
import asyncio
from shortly import Shortly

# Initialize Shortly
shortly = Shortly(api_key='<YOUR API KEY>', base_url='<YOUR BASE SITE>')

async def main():
    # Async call to convert URL
    link = await shortly.convert("https://example.com/long-url")
    print(link)

if __name__ == "__main__":
    asyncio.run(main())
```

## Error Handling

The library comes with built-in exception handling to manage common errors such as invalid links, not found links, timeouts, or connection issues.
```python
from shortly import Shortly
from shortly.errors import (
    ShortlyInvalidLinkError,
    ShortlyLinkNotFoundError,
    ShortlyTimeoutError,
    ShortlyConnectionError,
    ShortlyJsonDecodeError,
    ShortlyError
)

client = Shortly(api_key="your_api_key", base_url="gplinks.com")
try:
    response = client.convert("https://example.com/long-url")
    print(f"Shortened Link: {response}")
except ShortlyInvalidLinkError:
    print("The provided link is invalid or malformed.")
except ShortlyLinkNotFoundError:
    print("The short link does not exist or has expired.")
except ShortlyTimeoutError:
    print("The request took too long and timed out.")
except ShortlyConnectionError:
    print("Failed to connect to the server.")
except ShortlyJsonDecodeError as e:
    print(f"JSON decoding error: {str(e)}")
except ShortlyError as e:
    print(f"An error occurred: {e}")
```

## Handling Timeout

If the request takes too long and exceeds the specified timeout, a ShortlyTimeoutError will be raised.
```python
from shortly import Shortly
from shortly.errors import ShortlyTimeoutError

client = Shortly(api_key="your_api_key", base_url="gplinks.com")
try:
    link = client.convert("https://example.com/long-url", timeout=5)
    print(f"Shortened Link: {link}")
except ShortlyTimeoutError:
    print("The request took too long and timed out.")
```

## Handling Connection Issues

If there's a problem connecting to the API, a ShortlyConnectionError will be raised.
```python
from shortly import Shortly
from shortly.errors import ShortlyConnectionError

client = Shortly(api_key="your_api_key", base_url="gplinks.com")
try:
    link = client.convert("https://example.com/long-url")
    print(f"Shortened Link: {link}")
except ShortlyConnectionError:
    print("Failed to connect to the server.")
```

## Supported Sites
adlinkfy all sites support 
shareus support 
ouo support 
bitly support 
tinyurl support 
request your shortner sites [Support](https://t.me/RknBots_Support)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
