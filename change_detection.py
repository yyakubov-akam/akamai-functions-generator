from dataclasses import dataclass
from typing import Literal

import requests


VALIDATOR_ACCEPT = "text/markdown, text/html;q=0.9"
HEAD_TIMEOUT_SECONDS = 30


@dataclass(frozen=True)
class HeaderCheckResult:
    outcome: Literal["changed", "unchanged", "fallback"]
    etag: str | None
    last_modified: str | None
    headers_received: bool
    reason: str


def etags_match(left: str, right: str) -> bool:
    """Compare entity tags using HTTP's weak comparison semantics."""
    normalized = []
    for value in (left, right):
        value = value.strip()
        normalized.append(value[2:] if value.startswith("W/") else value)
    return normalized[0] == normalized[1]


def check_response_headers(
    url: str,
    old_etag: str | None = None,
    old_last_modified: str | None = None,
) -> HeaderCheckResult:
    """Check a URL's validators with HEAD without downloading its response body.

    Markdown is preferred because documentation sites may generate volatile HTML
    shells while exposing stable validators for their Markdown representation.
    """
    request_headers = {"Accept": VALIDATOR_ACCEPT}
    if old_etag:
        request_headers["If-None-Match"] = old_etag
    if old_last_modified:
        request_headers["If-Modified-Since"] = old_last_modified

    try:
        response = requests.head(
            url,
            headers=request_headers,
            allow_redirects=True,
            timeout=HEAD_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        return HeaderCheckResult(
            outcome="fallback",
            etag=None,
            last_modified=None,
            headers_received=False,
            reason=f"HEAD request failed: {exc}",
        )

    current_etag = response.headers.get("ETag")
    current_last_modified = response.headers.get("Last-Modified")

    if response.status_code == 304:
        return HeaderCheckResult(
            outcome="unchanged",
            etag=current_etag or old_etag,
            last_modified=current_last_modified or old_last_modified,
            headers_received=True,
            reason="server returned 304 Not Modified",
        )

    if response.status_code in (405, 501):
        return HeaderCheckResult(
            outcome="fallback",
            etag=None,
            last_modified=None,
            headers_received=False,
            reason=f"HEAD is not supported (HTTP {response.status_code})",
        )

    try:
        response.raise_for_status()
    except requests.RequestException as exc:
        return HeaderCheckResult(
            outcome="fallback",
            etag=None,
            last_modified=None,
            headers_received=False,
            reason=f"HEAD request failed: {exc}",
        )

    if old_etag and current_etag:
        outcome = "unchanged" if etags_match(current_etag, old_etag) else "changed"
        return HeaderCheckResult(
            outcome=outcome,
            etag=current_etag,
            last_modified=current_last_modified,
            headers_received=True,
            reason=f"ETag {'matches' if outcome == 'unchanged' else 'changed'}",
        )

    if old_last_modified and current_last_modified:
        outcome = (
            "unchanged"
            if current_last_modified == old_last_modified
            else "changed"
        )
        return HeaderCheckResult(
            outcome=outcome,
            etag=current_etag,
            last_modified=current_last_modified,
            headers_received=True,
            reason=(
                "Last-Modified matches"
                if outcome == "unchanged"
                else "Last-Modified changed"
            ),
        )

    if current_etag or current_last_modified:
        reason = "no stored validator is available for comparison"
    else:
        reason = "HEAD returned no ETag or Last-Modified header"

    return HeaderCheckResult(
        outcome="fallback",
        etag=current_etag,
        last_modified=current_last_modified,
        headers_received=True,
        reason=reason,
    )
