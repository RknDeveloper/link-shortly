"""Link-Shortly public package API."""

__version__ = "0.0.8"
__author__ = "RknDeveloper"
__license__ = "MIT"
__copyright__ = "Copyright (C) 2025-present RknDeveloper"

from .shortly import Shortly
from .errors import (
    ShortlyConnectionError,
    ShortlyError,
    ShortlyInvalidLinkError,
    ShortlyJsonDecodeError,
    ShortlyLinkNotFoundError,
    ShortlyTimeoutError,
    ShortlyValueError,
)

__all__ = [
    "Shortly",
    "ShortlyError",
    "ShortlyInvalidLinkError",
    "ShortlyLinkNotFoundError",
    "ShortlyTimeoutError",
    "ShortlyConnectionError",
    "ShortlyJsonDecodeError",
    "ShortlyValueError",
]
