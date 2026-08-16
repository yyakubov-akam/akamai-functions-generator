import unittest
from unittest.mock import Mock, patch

from change_detection import VALIDATOR_ACCEPT
from markdown_source import (
    canonicalize_markdown_url,
    fetch_llms_urls,
    fetch_native_markdown,
    parse_llms_urls,
)


def make_response(text, content_type, url="https://example.com/docs/llms.txt"):
    response = Mock()
    response.text = text
    response.url = url
    response.headers = {"Content-Type": content_type}
    return response


class MarkdownSourceTests(unittest.TestCase):
    def test_canonicalize_markdown_url(self):
        self.assertEqual(
            canonicalize_markdown_url("https://example.com/docs/quickstart.md#top"),
            "https://example.com/docs/quickstart",
        )

    def test_parse_llms_urls_keeps_unique_same_site_markdown_pages(self):
        content = """
- [Page one](https://example.com/docs/one.md)
- [Duplicate](https://example.com/docs/one.md)
- [Relative page](two.md)
- [Section index](https://example.com/docs/category/llms.txt)
- [External page](https://other.example/docs/three.md)
"""

        self.assertEqual(
            parse_llms_urls(content, "https://example.com/docs/llms.txt"),
            ["https://example.com/docs/one", "https://example.com/docs/two"],
        )

    @patch("markdown_source.requests.get")
    def test_fetch_llms_urls_requests_plain_text(self, get):
        get.return_value = make_response(
            "- [Page](https://example.com/docs/page.md)",
            "text/plain; charset=utf-8",
        )

        urls = fetch_llms_urls("https://example.com/docs/llms.txt")

        self.assertEqual(urls, ["https://example.com/docs/page"])
        get.assert_called_once_with(
            "https://example.com/docs/llms.txt",
            headers={"Accept": "text/plain"},
            timeout=30,
        )

    @patch("markdown_source.requests.get")
    def test_native_markdown_fetch_uses_validator_representation(self, get):
        get.return_value = make_response(
            "# Documentation\n",
            "text/markdown; charset=utf-8",
            url="https://example.com/docs/page",
        )

        content, error = fetch_native_markdown("https://example.com/docs/page")

        self.assertEqual(content, "# Documentation\n")
        self.assertIsNone(error)
        get.assert_called_once_with(
            "https://example.com/docs/page",
            headers={"Accept": VALIDATOR_ACCEPT},
            timeout=30,
        )

    @patch("markdown_source.requests.get")
    def test_native_markdown_rejects_html(self, get):
        get.return_value = make_response("<html></html>", "text/html")

        content, error = fetch_native_markdown("https://example.com/docs/page")

        self.assertIsNone(content)
        self.assertIn("native Markdown unavailable", error)


if __name__ == "__main__":
    unittest.main()
