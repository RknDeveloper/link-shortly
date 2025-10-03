class ShortlyError(Exception):
    """Base exception for all Shortly (link shortener) errors."""
    pass

class ShortlyInvalidLinkError(ShortlyError):
    """Raised when the provided link is invalid or malformed."""
    pass

class ShortlyLinkNotFoundError(ShortlyError):
    """Raised when the requested short link does not exist or has expired."""
    pass

class ShortlyTimeoutError(ShortlyError):
    """Raised when a request to the Shortly API exceeds the allowed timeout."""
    pass

class ShortlyConnectionError(ShortlyError):
    """Raised when the client cannot connect to the Shortly API server."""
    pass

class ShortlyJsonDecodeError(ShortlyError):
    """Raised when the API response is not valid JSON."""
    pass

class ShortlyValueError(ShortlyError):
    """Raised when invalid input is provided to the Shortly client (e.g., api_key or base_url)."""
    pass