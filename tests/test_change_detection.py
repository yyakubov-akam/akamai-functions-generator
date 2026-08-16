import unittest
from unittest.mock import Mock, patch

import requests

from change_detection import VALIDATOR_ACCEPT, check_response_headers


def make_response(status_code=200, headers=None):
    response = Mock()
    response.status_code = status_code
    response.headers = headers or {}
    if status_code >= 400:
        response.raise_for_status.side_effect = requests.HTTPError(
            f"HTTP {status_code}"
        )
    return response


class CheckResponseHeadersTests(unittest.TestCase):
    @patch("change_detection.requests.head")
    def test_matching_etag_is_unchanged(self, head):
        head.return_value = make_response(headers={"ETag": '"same"'})

        result = check_response_headers("https://example.com/doc", '"same"')

        self.assertEqual(result.outcome, "unchanged")
        head.assert_called_once_with(
            "https://example.com/doc",
            headers={
                "Accept": VALIDATOR_ACCEPT,
                "If-None-Match": '"same"',
            },
            allow_redirects=True,
            timeout=30,
        )

    @patch("change_detection.requests.head")
    def test_changed_etag_is_changed(self, head):
        head.return_value = make_response(headers={"ETag": '"new"'})

        result = check_response_headers("https://example.com/doc", '"old"')

        self.assertEqual(result.outcome, "changed")
        self.assertEqual(result.etag, '"new"')

    @patch("change_detection.requests.head")
    def test_weak_and_strong_versions_of_same_etag_match(self, head):
        head.return_value = make_response(headers={"ETag": '"same"'})

        result = check_response_headers("https://example.com/doc", 'W/"same"')

        self.assertEqual(result.outcome, "unchanged")

    @patch("change_detection.requests.head")
    def test_last_modified_is_used_when_etag_cannot_be_compared(self, head):
        head.return_value = make_response(
            headers={"Last-Modified": "Sun, 16 Aug 2026 07:00:00 GMT"}
        )

        result = check_response_headers(
            "https://example.com/doc",
            old_last_modified="Sun, 16 Aug 2026 07:00:00 GMT",
        )

        self.assertEqual(result.outcome, "unchanged")

    @patch("change_detection.requests.head")
    def test_304_is_unchanged(self, head):
        head.return_value = make_response(status_code=304)

        result = check_response_headers("https://example.com/doc", '"same"')

        self.assertEqual(result.outcome, "unchanged")
        self.assertEqual(result.etag, '"same"')

    @patch("change_detection.requests.head")
    def test_unsupported_head_falls_back(self, head):
        head.return_value = make_response(status_code=405)

        result = check_response_headers("https://example.com/doc", '"old"')

        self.assertEqual(result.outcome, "fallback")
        self.assertFalse(result.headers_received)

    @patch("change_detection.requests.head")
    def test_missing_validator_falls_back(self, head):
        head.return_value = make_response(headers={"Content-Type": "text/html"})

        result = check_response_headers("https://example.com/doc", '"old"')

        self.assertEqual(result.outcome, "fallback")
        self.assertTrue(result.headers_received)


if __name__ == "__main__":
    unittest.main()
