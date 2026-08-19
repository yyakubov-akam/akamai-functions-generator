#!/usr/bin/env python3
"""Synchronize exact Akamai Functions Markdown sources without an LLM.

The workflow discovers native Markdown through ``llms.txt``, stores exact
source bytes, and maintains hashes that let an agent determine whether the
compiled reference is current. It uses only Python's standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
import sys
import tempfile
import time
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LLMS_URL = "https://techdocs.akamai.com/akamai-functions/docs/llms.txt"
DEFAULT_SOURCE_DIR = PROJECT_ROOT / "docs" / "_source"
DEFAULT_MANIFEST = PROJECT_ROOT / "docs" / "reference-manifest.json"
DEFAULT_REFERENCE = PROJECT_ROOT / "docs" / "_compiled" / "functions-reference.md"
DEFAULT_CONTRACT = PROJECT_ROOT / "REFERENCE_COMPILATION.md"
DEFAULT_METADATA = (
    PROJECT_ROOT / "docs" / "_compiled" / "functions-reference.meta.json"
)

MANIFEST_SCHEMA_VERSION = 1
METADATA_SCHEMA_VERSION = 2
REQUEST_TIMEOUT_SECONDS = 30
MAX_RETRIES = 3
USER_AGENT = "aka-functions-reference-sync/1.0"
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")
SAFE_PATH_PART = re.compile(r"[^a-z0-9]+")
TRANSIENT_HTTP_STATUSES = {408, 429, 500, 502, 503, 504}
SOURCE_CONTENT_TYPES = {"text/markdown", "text/plain"}
REQUIRED_REFERENCE_HEADINGS = (
    "## 1. Runtime Prohibitions",
    "## 2. Import Rules",
    "## 3. Event Handler Reference",
    "## 4. API Reference",
    "## 5. Cross-Reference",
    "## 6. Known Failure Patterns",
)
SOURCE_COVERAGE_HEADING = "### Source Coverage"
COVERAGE_ROW = re.compile(
    r"^\|\s*\[[^\]]+\]\(([^)]+)\)\s*\|\s*(Included|Excluded)\s*\|\s*(.*?)\s*\|\s*$"
)
NUMBERED_SUBSECTION_HEADING = re.compile(r"^###\s+(\d+\.\d+)\b", re.MULTILINE)
SECTION_REFERENCE = re.compile(r"§(\d+\.\d+)\b")


class ReferenceSyncError(RuntimeError):
    """A source-discovery, synchronization, or verification failure."""


@dataclass(frozen=True)
class HttpResult:
    status: int
    body: bytes
    headers: Mapping[str, str]
    final_url: str


@dataclass
class ChangeReport:
    added: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    reactivated: list[str] = field(default_factory=list)
    repaired: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    index_changed: bool = False

    @property
    def has_changes(self) -> bool:
        return bool(
            self.added
            or self.changed
            or self.removed
            or self.reactivated
            or self.repaired
            or self.index_changed
        )

    def to_dict(self) -> dict:
        return {
            "has_changes": self.has_changes,
            "index_changed": self.index_changed,
            "added": self.added,
            "changed": self.changed,
            "removed": self.removed,
            "reactivated": self.reactivated,
            "repaired": self.repaired,
            "unchanged": self.unchanged,
            "counts": {
                "added": len(self.added),
                "changed": len(self.changed),
                "removed": len(self.removed),
                "reactivated": len(self.reactivated),
                "repaired": len(self.repaired),
                "unchanged": len(self.unchanged),
            },
        }


OpenUrl = Callable[[str, Mapping[str, str], int], HttpResult]


def create_tls_context() -> ssl.SSLContext:
    """Create a verified TLS context, including common OS CA-bundle paths.

    Python.org macOS installations can have no configured OpenSSL CA file even
    when macOS provides a current bundle at ``/etc/ssl/cert.pem``. Loading that
    bundle preserves certificate verification without adding a package such as
    certifi or weakening TLS checks.
    """
    context = ssl.create_default_context()
    verify_paths = ssl.get_default_verify_paths()
    if verify_paths.cafile or verify_paths.capath:
        return context

    candidates = (
        Path("/etc/ssl/cert.pem"),
        Path("/etc/ssl/certs/ca-certificates.crt"),
        Path("/etc/pki/tls/certs/ca-bundle.crt"),
    )
    for candidate in candidates:
        if candidate.is_file():
            context.load_verify_locations(cafile=candidate)
            break
    return context


TLS_CONTEXT = create_tls_context()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _headers_to_dict(headers: Mapping[str, str]) -> dict[str, str]:
    return {str(key).lower(): str(value) for key, value in headers.items()}


def open_url(
    url: str,
    headers: Mapping[str, str],
    timeout: int = REQUEST_TIMEOUT_SECONDS,
) -> HttpResult:
    """Fetch a URL with bounded retries and return response bytes."""
    request_headers = {"User-Agent": USER_AGENT, **headers}
    last_error: Exception | None = None

    for attempt in range(MAX_RETRIES):
        request = Request(url, headers=request_headers)
        try:
            with urlopen(request, timeout=timeout, context=TLS_CONTEXT) as response:
                return HttpResult(
                    status=response.getcode(),
                    body=response.read(),
                    headers=_headers_to_dict(response.headers),
                    final_url=response.geturl(),
                )
        except HTTPError as exc:
            if exc.code == 304:
                return HttpResult(
                    status=304,
                    body=b"",
                    headers=_headers_to_dict(exc.headers or {}),
                    final_url=exc.geturl(),
                )
            last_error = exc
            if exc.code not in TRANSIENT_HTTP_STATUSES or attempt == MAX_RETRIES - 1:
                break
        except URLError as exc:
            last_error = exc
            if attempt == MAX_RETRIES - 1:
                break

        time.sleep(2**attempt)

    raise ReferenceSyncError(f"Failed to fetch {url}: {last_error}")


def _content_type(headers: Mapping[str, str]) -> str:
    return headers.get("content-type", "").split(";", 1)[0].strip().lower()


def _decode_text(body: bytes, headers: Mapping[str, str], source: str) -> str:
    content_type = headers.get("content-type", "")
    charset_match = re.search(r"charset=([^;\s]+)", content_type, re.IGNORECASE)
    charset = charset_match.group(1).strip('"\'') if charset_match else "utf-8"
    try:
        return body.decode(charset)
    except (LookupError, UnicodeDecodeError) as exc:
        raise ReferenceSyncError(f"Cannot decode {source} as {charset}: {exc}") from exc


def canonicalize_markdown_url(url: str) -> str:
    parsed = urlsplit(url)
    path = parsed.path[:-3] if parsed.path.lower().endswith(".md") else parsed.path
    return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, ""))


def parse_llms_sources(content: str, llms_url: str) -> list[tuple[str, str]]:
    """Return unique ``(canonical URL, Markdown URL)`` pairs from llms.txt."""
    source_host = urlsplit(llms_url).hostname
    sources: list[tuple[str, str]] = []
    seen: set[str] = set()

    for target in MARKDOWN_LINK.findall(content):
        absolute = urljoin(llms_url, target)
        parsed = urlsplit(absolute)
        if (
            parsed.scheme not in {"http", "https"}
            or parsed.hostname != source_host
            or not parsed.path.lower().endswith(".md")
        ):
            continue

        markdown_url = urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path, parsed.query, "")
        )
        canonical_url = canonicalize_markdown_url(markdown_url)
        if canonical_url not in seen:
            seen.add(canonical_url)
            sources.append((canonical_url, markdown_url))

    if not sources:
        raise ReferenceSyncError(f"No same-site Markdown links found in {llms_url}")
    return sources


def discover_sources(
    llms_url: str,
    opener: OpenUrl = open_url,
    timeout: int = REQUEST_TIMEOUT_SECONDS,
) -> list[tuple[str, str]]:
    response = opener(
        llms_url,
        {"Accept": "text/plain, text/markdown;q=0.9"},
        timeout,
    )
    if response.status != 200:
        raise ReferenceSyncError(
            f"Documentation index returned HTTP {response.status}: {llms_url}"
        )
    content_type = _content_type(response.headers)
    if content_type not in SOURCE_CONTENT_TYPES:
        raise ReferenceSyncError(
            f"Unexpected documentation-index content type: {content_type or 'missing'}"
        )
    return parse_llms_sources(
        _decode_text(response.body, response.headers, llms_url), response.final_url
    )


def _safe_slug(value: str, fallback: str) -> str:
    slug = SAFE_PATH_PART.sub("-", value.lower()).strip("-")
    return slug or fallback


def source_relative_path(canonical_url: str, source_dir: Path) -> Path:
    parsed = urlsplit(canonical_url)
    host = _safe_slug(parsed.hostname or "", "unknown-host")
    path_parts = [part for part in parsed.path.split("/") if part]
    leaf = _safe_slug(path_parts[-1] if path_parts else "index", "index")
    return source_dir / host / f"{leaf}.md"


def _project_relative(path: Path, project_root: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(project_root.resolve()).as_posix()
    except ValueError as exc:
        raise ReferenceSyncError(
            f"Path must be inside the project root: {resolved}"
        ) from exc


def _resolve_manifest_path(relative_path: str, project_root: Path) -> Path:
    candidate = (project_root / relative_path).resolve()
    try:
        candidate.relative_to(project_root.resolve())
    except ValueError as exc:
        raise ReferenceSyncError(
            f"Manifest path escapes the project root: {relative_path}"
        ) from exc
    return candidate


def empty_manifest(llms_url: str) -> dict:
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "source_index": llms_url,
        "sources": {},
    }


def validate_manifest(manifest: dict) -> None:
    if manifest.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise ReferenceSyncError(
            "Unsupported reference-manifest schema version: "
            f"{manifest.get('schema_version')!r}"
        )
    if not isinstance(manifest.get("source_index"), str):
        raise ReferenceSyncError("Manifest source_index must be a string")
    if not isinstance(manifest.get("sources"), dict):
        raise ReferenceSyncError("Manifest sources must be an object")

    for url, entry in manifest["sources"].items():
        if not isinstance(url, str) or not isinstance(entry, dict):
            raise ReferenceSyncError("Manifest source entries must be URL/object pairs")
        for key in ("source_url", "filepath", "content_sha256", "active"):
            if key not in entry:
                raise ReferenceSyncError(f"Manifest entry {url} is missing {key}")


def load_manifest(path: Path, llms_url: str) -> dict:
    if not path.exists():
        return empty_manifest(llms_url)
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReferenceSyncError(f"Cannot read manifest {path}: {exc}") from exc
    validate_manifest(manifest)
    return manifest


def _local_source_matches(
    entry: dict | None, project_root: Path
) -> tuple[bool, Path | None]:
    if not entry:
        return False, None
    path = _resolve_manifest_path(entry["filepath"], project_root)
    if not path.is_file():
        return False, path
    return sha256_file(path) == entry["content_sha256"], path


def _fetch_markdown(
    source_url: str,
    old_entry: dict | None,
    opener: OpenUrl,
    timeout: int,
    conditional: bool = True,
) -> HttpResult:
    headers = {"Accept": "text/markdown, text/plain;q=0.9"}
    if conditional and old_entry:
        if old_entry.get("etag"):
            headers["If-None-Match"] = old_entry["etag"]
        if old_entry.get("last_modified"):
            headers["If-Modified-Since"] = old_entry["last_modified"]

    response = opener(source_url, headers, timeout)
    if response.status not in {200, 304}:
        raise ReferenceSyncError(
            f"Source returned HTTP {response.status}: {source_url}"
        )
    if response.status == 200:
        content_type = _content_type(response.headers)
        if content_type not in SOURCE_CONTENT_TYPES:
            raise ReferenceSyncError(
                f"Expected Markdown from {source_url}, got "
                f"{content_type or 'a missing content type'}"
            )
    return response


def inspect_upstream(
    *,
    llms_url: str,
    manifest_path: Path,
    source_dir: Path,
    project_root: Path,
    opener: OpenUrl = open_url,
    timeout: int = REQUEST_TIMEOUT_SECONDS,
) -> tuple[dict, ChangeReport, dict[Path, bytes]]:
    """Inspect upstream state without writing and return a proposed sync."""
    manifest = load_manifest(manifest_path, llms_url)
    proposed = deepcopy(manifest)
    report = ChangeReport(index_changed=manifest["source_index"] != llms_url)
    proposed["source_index"] = llms_url
    downloads: dict[Path, bytes] = {}
    discovered = discover_sources(llms_url, opener=opener, timeout=timeout)
    discovered_urls = {canonical for canonical, _ in discovered}
    assigned_paths: dict[str, str] = {}
    for existing_url, existing_entry in manifest["sources"].items():
        existing_path = existing_entry["filepath"]
        conflicting_url = assigned_paths.get(existing_path)
        if conflicting_url and conflicting_url != existing_url:
            raise ReferenceSyncError(
                f"Manifest source-path collision between {conflicting_url} and "
                f"{existing_url}: {existing_path}"
            )
        assigned_paths[existing_path] = existing_url

    for canonical_url, source_url in discovered:
        old_entry = manifest["sources"].get(canonical_url)
        relative_path = _project_relative(
            source_relative_path(canonical_url, source_dir), project_root
        )
        existing_url = assigned_paths.get(relative_path)
        if existing_url and existing_url != canonical_url:
            raise ReferenceSyncError(
                f"Source-path collision between {existing_url} and {canonical_url}: "
                f"{relative_path}"
            )
        assigned_paths[relative_path] = canonical_url

        local_matches, local_path = _local_source_matches(old_entry, project_root)
        response = _fetch_markdown(
            source_url, old_entry, opener, timeout, conditional=True
        )
        if response.status == 304 and not local_matches:
            response = _fetch_markdown(
                source_url, old_entry, opener, timeout, conditional=False
            )
        if response.status == 304:
            if old_entry and not old_entry.get("active", True):
                proposed["sources"][canonical_url] = {
                    **old_entry,
                    "source_url": source_url,
                    "active": True,
                }
                report.reactivated.append(canonical_url)
            else:
                report.unchanged.append(canonical_url)
            continue

        digest = sha256_bytes(response.body)
        new_entry = {
            "source_url": source_url,
            "filepath": relative_path,
            "content_sha256": digest,
            "etag": response.headers.get("etag"),
            "last_modified": response.headers.get("last-modified"),
            "active": True,
        }
        target_path = _resolve_manifest_path(relative_path, project_root)

        if old_entry is None:
            report.added.append(canonical_url)
        elif not old_entry.get("active", True):
            report.reactivated.append(canonical_url)
        elif (
            old_entry["content_sha256"] != digest
            or old_entry["source_url"] != source_url
            or old_entry["filepath"] != relative_path
        ):
            report.changed.append(canonical_url)
        elif not local_matches:
            report.repaired.append(canonical_url)
        else:
            report.unchanged.append(canonical_url)
            continue

        proposed["sources"][canonical_url] = new_entry
        downloads[target_path] = response.body

    for canonical_url, old_entry in manifest["sources"].items():
        if canonical_url in discovered_urls or not old_entry.get("active", True):
            continue
        proposed["sources"][canonical_url] = {**old_entry, "active": False}
        report.removed.append(canonical_url)

    for values in (
        report.added,
        report.changed,
        report.removed,
        report.reactivated,
        report.repaired,
        report.unchanged,
    ):
        values.sort()

    return proposed, report, downloads


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            temporary_path = Path(handle.name)
        os.replace(temporary_path, path)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def apply_sync(
    manifest: dict,
    manifest_path: Path,
    downloads: Mapping[Path, bytes],
) -> None:
    for path, content in sorted(downloads.items(), key=lambda item: str(item[0])):
        if not path.exists() or path.read_bytes() != content:
            _atomic_write(path, content)
    serialized = _json_bytes(manifest)
    if not manifest_path.exists() or manifest_path.read_bytes() != serialized:
        _atomic_write(manifest_path, serialized)


def source_set_digest(manifest: dict) -> str:
    active_sources = [
        {
            "canonical_url": url,
            "source_url": entry["source_url"],
            "filepath": entry["filepath"],
            "content_sha256": entry["content_sha256"],
        }
        for url, entry in sorted(manifest["sources"].items())
        if entry.get("active", True)
    ]
    payload = {
        "source_index": manifest["source_index"],
        "sources": active_sources,
    }
    return sha256_bytes(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )


def verify_source_archive(manifest_path: Path, project_root: Path) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    if not manifest_path.is_file():
        return None, [f"Missing source manifest: {_display_path(manifest_path, project_root)}"]
    try:
        manifest = load_manifest(manifest_path, DEFAULT_LLMS_URL)
    except ReferenceSyncError as exc:
        return None, [str(exc)]

    active_count = 0
    for url, entry in sorted(manifest["sources"].items()):
        if entry.get("active", True):
            active_count += 1
        try:
            source_path = _resolve_manifest_path(entry["filepath"], project_root)
        except ReferenceSyncError as exc:
            errors.append(str(exc))
            continue
        if not source_path.is_file():
            errors.append(f"Missing source snapshot for {url}: {entry['filepath']}")
            continue
        actual_hash = sha256_file(source_path)
        if actual_hash != entry["content_sha256"]:
            errors.append(
                f"Source snapshot hash mismatch for {url}: {entry['filepath']}"
            )

    if active_count == 0:
        errors.append("The source manifest contains no active documentation pages")
    return manifest, errors


def _relative_reference_target(
    source_path: Path, reference_path: Path
) -> str:
    return Path(
        os.path.relpath(source_path.resolve(), reference_path.parent.resolve())
    ).as_posix()


def validate_reference(
    reference_path: Path,
    *,
    manifest: dict | None = None,
    project_root: Path = PROJECT_ROOT,
) -> list[str]:
    if not reference_path.is_file():
        return [f"Missing compiled reference: {reference_path}"]
    content = reference_path.read_text(encoding="utf-8")
    errors: list[str] = []
    actual_headings = [
        line for line in content.splitlines() if line.startswith("## ")
    ]
    if actual_headings != list(REQUIRED_REFERENCE_HEADINGS):
        errors.append(
            "Compiled reference top-level headings must appear exactly once in "
            "the required order"
        )
    if content.count("```") % 2:
        errors.append("Compiled reference contains an unbalanced fenced code block")

    link_targets = MARKDOWN_LINK.findall(content)
    source_link_targets: list[str] = []
    for target in link_targets:
        path_target = target.split("#", 1)[0]
        if "_source/" not in path_target:
            continue
        if not path_target.startswith("../_source/"):
            errors.append(
                f"Exact-source link must be relative to the compiled file: {target}"
            )
            continue
        source_link_targets.append(path_target)
        resolved = (reference_path.parent / path_target).resolve()
        try:
            resolved.relative_to(project_root.resolve())
        except ValueError:
            errors.append(f"Exact-source link escapes the project root: {target}")
            continue
        if not resolved.is_file():
            errors.append(f"Broken exact-source link in compiled reference: {target}")

    if manifest is None:
        return errors

    active_targets: dict[str, str] = {}
    for url, entry in sorted(manifest["sources"].items()):
        if not entry.get("active", True):
            continue
        source_path = _resolve_manifest_path(entry["filepath"], project_root)
        target = _relative_reference_target(source_path, reference_path)
        if target in active_targets:
            errors.append(
                "Active manifest entries share a compiled-reference target: "
                f"{target}"
            )
        active_targets[target] = url

    lines = content.splitlines()
    try:
        coverage_start = lines.index(SOURCE_COVERAGE_HEADING) + 1
    except ValueError:
        errors.append("Compiled reference is missing the Source Coverage table")
        return errors

    coverage_rows: list[tuple[str, str, str]] = []
    for line in lines[coverage_start:]:
        if line.startswith("## ") or line.strip() == "---":
            break
        match = COVERAGE_ROW.match(line)
        if match:
            target, status, detail = match.groups()
            coverage_rows.append((target.split("#", 1)[0], status, detail.strip()))

    row_counts: dict[str, int] = {}
    available_sections = set(NUMBERED_SUBSECTION_HEADING.findall(content))
    for target, status, detail in coverage_rows:
        row_counts[target] = row_counts.get(target, 0) + 1
        if target not in active_targets:
            errors.append(f"Source Coverage contains a non-active source: {target}")
            continue
        if status == "Included":
            referenced_sections = SECTION_REFERENCE.findall(detail)
            if not referenced_sections:
                errors.append(
                    f"Included source has no compiled subsection reference: {target}"
                )
            for section in referenced_sections:
                if section not in available_sections:
                    errors.append(
                        f"Source Coverage references a missing subsection §{section}: "
                        f"{target}"
                    )
            if source_link_targets.count(target) < 2:
                errors.append(
                    "Included source is not attributed outside Source Coverage: "
                    f"{target}"
                )
        elif not detail:
            errors.append(f"Excluded source has no source-specific reason: {target}")

    for target in active_targets:
        count = row_counts.get(target, 0)
        if count == 0:
            errors.append(f"Active source is missing from Source Coverage: {target}")
        elif count > 1:
            errors.append(f"Active source has duplicate Source Coverage rows: {target}")
    return errors


def finalize_reference(
    *,
    manifest_path: Path,
    reference_path: Path,
    contract_path: Path,
    metadata_path: Path,
    project_root: Path,
) -> dict:
    """Validate and record a publishable reference from any compiler workflow."""
    manifest, errors = verify_source_archive(manifest_path, project_root)
    errors.extend(
        validate_reference(
            reference_path,
            manifest=manifest,
            project_root=project_root,
        )
    )
    if not contract_path.is_file():
        errors.append(f"Missing publication contract: {contract_path}")
    if errors:
        raise ReferenceSyncError("Cannot finalize reference:\n- " + "\n- ".join(errors))
    assert manifest is not None

    metadata = {
        "schema_version": METADATA_SCHEMA_VERSION,
        "source_count": sum(
            1 for entry in manifest["sources"].values() if entry.get("active", True)
        ),
        "source_set_sha256": source_set_digest(manifest),
        "publication_contract": _project_relative(contract_path, project_root),
        "publication_contract_sha256": sha256_file(contract_path),
        "compiled_reference": _project_relative(reference_path, project_root),
        "compiled_reference_sha256": sha256_file(reference_path),
    }
    _atomic_write(metadata_path, _json_bytes(metadata))
    return metadata


def verify_reference(
    *,
    manifest_path: Path,
    reference_path: Path,
    contract_path: Path,
    metadata_path: Path,
    project_root: Path,
) -> list[str]:
    manifest, errors = verify_source_archive(manifest_path, project_root)
    errors.extend(
        validate_reference(
            reference_path,
            manifest=manifest,
            project_root=project_root,
        )
    )
    if not contract_path.is_file():
        errors.append(f"Missing publication contract: {contract_path}")
    if not metadata_path.is_file():
        errors.append(
            f"Missing compiled-reference metadata: {_display_path(metadata_path, project_root)}; "
            "run the finalize command after recompiling"
        )
        return errors

    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Cannot read compiled-reference metadata: {exc}")
        return errors
    if metadata.get("schema_version") != METADATA_SCHEMA_VERSION:
        errors.append("Unsupported compiled-reference metadata schema version")
        return errors

    if manifest is not None:
        expected_source_digest = source_set_digest(manifest)
        if metadata.get("source_set_sha256") != expected_source_digest:
            errors.append(
                "Compiled reference is stale: the synchronized source set has changed"
            )
        expected_count = sum(
            1 for entry in manifest["sources"].values() if entry.get("active", True)
        )
        if metadata.get("source_count") != expected_count:
            errors.append("Compiled-reference source count does not match the manifest")
    if contract_path.is_file() and metadata.get(
        "publication_contract_sha256"
    ) != sha256_file(contract_path):
        errors.append("Compiled reference is stale: publication contract has changed")
    if reference_path.is_file() and metadata.get("compiled_reference_sha256") != sha256_file(
        reference_path
    ):
        errors.append("Compiled reference changed after it was finalized")
    return errors


def _display_path(path: Path, project_root: Path = PROJECT_ROOT) -> str:
    try:
        return path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return str(path)


def print_report(report: ChangeReport, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
        return

    if not report.has_changes:
        print(f"Reference sources are current ({len(report.unchanged)} unchanged).")
        return

    labels = (
        ("Added", report.added),
        ("Changed", report.changed),
        ("Removed from index (snapshot retained)", report.removed),
        ("Reactivated", report.reactivated),
        ("Repaired local snapshot", report.repaired),
    )
    if report.index_changed:
        print("Documentation index URL changed.")
    for label, urls in labels:
        if urls:
            print(f"{label} ({len(urls)}):")
            for url in urls:
                print(f"  - {url}")
    print(f"Unchanged: {len(report.unchanged)}")


def _add_sync_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--llms-url", default=DEFAULT_LLMS_URL)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--timeout", type=int, default=REQUEST_TIMEOUT_SECONDS)
    parser.add_argument("--json", action="store_true", help="Print a JSON change report")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser(
        "check", help="Check upstream sources without modifying local files"
    )
    _add_sync_arguments(check_parser)
    check_parser.add_argument(
        "--fail-on-changes",
        action="store_true",
        help="Exit with status 3 when synchronization would change files",
    )

    sync_parser = subparsers.add_parser(
        "sync", help="Synchronize exact upstream Markdown and the source manifest"
    )
    _add_sync_arguments(sync_parser)

    finalize_parser = subparsers.add_parser(
        "finalize",
        help="Validate and record a publishable compiled reference",
    )
    finalize_parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    finalize_parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    finalize_parser.add_argument(
        "--contract",
        "--prompt",
        dest="contract",
        type=Path,
        default=DEFAULT_CONTRACT,
        help="Publication contract; --prompt is retained as a compatibility alias",
    )
    finalize_parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)

    verify_parser = subparsers.add_parser(
        "verify", help="Verify source snapshots and compiled-reference freshness offline"
    )
    verify_parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    verify_parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    verify_parser.add_argument(
        "--contract",
        "--prompt",
        dest="contract",
        type=Path,
        default=DEFAULT_CONTRACT,
        help="Publication contract; --prompt is retained as a compatibility alias",
    )
    verify_parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command in {"check", "sync"}:
            manifest_path = args.manifest.resolve()
            source_dir = args.source_dir.resolve()
            proposed, report, downloads = inspect_upstream(
                llms_url=args.llms_url,
                manifest_path=manifest_path,
                source_dir=source_dir,
                project_root=PROJECT_ROOT,
                timeout=args.timeout,
            )
            if args.command == "sync":
                apply_sync(proposed, manifest_path, downloads)
            print_report(report, args.json)
            if args.command == "check" and args.fail_on_changes and report.has_changes:
                return 3
            return 0

        if args.command == "finalize":
            metadata = finalize_reference(
                manifest_path=args.manifest.resolve(),
                reference_path=args.reference.resolve(),
                contract_path=args.contract.resolve(),
                metadata_path=args.metadata.resolve(),
                project_root=PROJECT_ROOT,
            )
            print(
                "Finalized compiled reference for "
                f"{metadata['source_count']} active source pages."
            )
            return 0

        errors = verify_reference(
            manifest_path=args.manifest.resolve(),
            reference_path=args.reference.resolve(),
            contract_path=args.contract.resolve(),
            metadata_path=args.metadata.resolve(),
            project_root=PROJECT_ROOT,
        )
        if errors:
            print("Reference verification failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Reference sources and compiled output are current.")
        return 0
    except (ReferenceSyncError, OSError) as exc:
        print(f"Reference synchronization failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
