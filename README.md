## Link Shortly

Shortly is a simple Python library to shorten links using the Shortly API or compatible services (like Adlinkfy, GPLinks, etc).

## Installation

Install link-shortly with pip
```python
pip install link-shortly
```

To Upgrade
```python
pip install --upgrade link-shortly
```

## Quick Usage Example
```python
from shortly import Shortly

shortly = Shortly(api_key='<YOUR API KEY>', base_url='<YOUR BASE SITE>')

def main():
    link = shortly.convert("https://example.com/long-url")
    print(link)

if __name__ == "__main__":
    main()
```

## Error Handling

The library comes with built-in exception handling to manage common errors such as invalid links, not found links, timeouts, or connection issues.
```python
from shortly import Shortly
from shortly.exceptions import (
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
from shortly.exceptions import ShortlyTimeoutError

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
from shortly.exceptions import ShortlyConnectionError

client = Shortly(api_key="your_api_key", base_url="gplinks.com")
try:
    link = client.convert("https://example.com/long-url")
    print(f"Shortened Link: {link}")
except ShortlyConnectionError:
    print("Failed to connect to the server.")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
