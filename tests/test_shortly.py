import asyncio
import unittest
from unittest.mock import patch

from shortly import Shortly, ShortlyValueError


class FakeProvider:
    def __init__(self, *args, **kwargs):
        pass

    async def tinyurl_convert(self, link, alias, silently, timeout):
        return f"tiny:{link}:{timeout}"

    async def shareus_convert(self, link, alias, silently, timeout):
        return f"shareus:{link}"

    async def bitly_convert(self, link, alias, silently, timeout):
        return f"bitly:{link}"

    async def ouo_convert(self, link, alias, silently, timeout):
        return f"ouo:{link}"

    async def adlinkfy_convert(self, link, alias, silently, timeout):
        return f"generic:{link}"


class ShortlyClientTests(unittest.TestCase):
    def test_base_url_normalization_and_tinyurl_without_key(self):
        client = Shortly(base_url="https://TinyURL.com/")
        self.assertEqual(client.base_url, "tinyurl.com")

    def test_non_tiny_provider_requires_api_key(self):
        with self.assertRaises(ShortlyValueError):
            Shortly(base_url="gplinks.com")

    def test_invalid_inputs_are_rejected(self):
        client = Shortly(base_url="tinyurl.com")
        with self.assertRaises(ShortlyValueError):
            client.convert("")
        with self.assertRaises(ShortlyValueError):
            client.convert("https://example.com", timeout=0)

    def test_sync_convert_routes_to_provider(self):
        with patch("shortly.shortly.LinkShortly", FakeProvider):
            client = Shortly(base_url="tinyurl.com")
            self.assertEqual(
                client.convert(" https://example.com ", timeout=4),
                "tiny:https://example.com:4",
            )

    def test_async_convert_returns_awaitable_inside_event_loop(self):
        async def run():
            with patch("shortly.shortly.LinkShortly", FakeProvider):
                client = Shortly(api_key="key", base_url="bitly.com")
                result = client.convert("https://example.com")
                self.assertTrue(asyncio.iscoroutine(result))
                self.assertEqual(await result, "bitly:https://example.com")

        asyncio.run(run())

    def test_silent_mode_returns_original_link(self):
        client = Shortly(base_url="tinyurl.com")
        self.assertEqual(client.convert("https://example.com", silently=True), "https://example.com")


if __name__ == "__main__":
    unittest.main()
