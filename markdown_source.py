import re
from urllib.parse import urljoin, urlparse, urlunparse

import requests

from change_detection import VALIDATOR_ACCEPT


DEFAULT_LLMS_INDEX = (
    "https://techdocs.akamai.com/akamai-functions/docs/llms.txt"
)
REQUEST_TIMEOUT_SECONDS = 30
_MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")


def canonicalize_markdown_url(url: str) -> str:
    """Convert a published .md URL to the canonical page URL used by the index."""
    parsed = urlparse(url)
    path = parsed.path[:-3] if parsed.path.lower().endswith(".md") else parsed.path
    return urlunparse(parsed._replace(path=path, fragment=""))


def parse_llms_urls(content: str, llms_url: str) -> list[str]:
    """Extract same-site Markdown page links from an llms.txt document."""
    source_host = urlparse(llms_url).hostname
    urls = []
    seen = set()

    for target in _MARKDOWN_LINK.findall(content):
        absolute_url = urljoin(llms_url, target)
        parsed = urlparse(absolute_url)
        if parsed.scheme not in ("http", "https"):
            continue
        if parsed.hostname != source_host or not parsed.path.lower().endswith(".md"):
            continue

        canonical_url = canonicalize_markdown_url(absolute_url)
        if canonical_url not in seen:
            seen.add(canonical_url)
            urls.append(canonical_url)

    return urls


def fetch_llms_urls(llms_url: str) -> list[str]:
    """Download an llms.txt index and return its canonical documentation URLs."""
    response = requests.get(
        llms_url,
        headers={"Accept": "text/plain"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "").lower()
    if not content_type.startswith(("text/plain", "text/markdown")):
        raise ValueError(f"Unexpected llms.txt content type: {content_type or 'missing'}")

    return parse_llms_urls(response.text, response.url)


def fetch_native_markdown(url: str) -> tuple[str | None, str | None]:
    """Fetch a page's server-provided Markdown representation."""
    try:
        response = requests.get(
            url,
            headers={"Accept": VALIDATOR_ACCEPT},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        return None, f"native Markdown request failed: {exc}"

    content_type = response.headers.get("Content-Type", "").lower()
    if not content_type.startswith("text/markdown"):
        return None, (
            "native Markdown unavailable "
            f"(Content-Type: {content_type or 'missing'})"
        )

    return (response.text, None) if response.text else (None, "Empty Markdown response")
