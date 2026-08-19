#!/usr/bin/env python3
"""Fail when local-only files are tracked by Git."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PRIVATE_EXACT_PATHS = frozenset(
    {
        "CODEGEN_REFERENCE_PROMPT.md",
        "COMPILE_PROMPT.md",
        "LOCAL_WORKFLOW.md",
        "REPOSITORY_WORKFLOWS.md",
        "change_detection.py",
        "config.py",
        "docs/index.json",
        "ingest.py",
        "ingest_v2.py",
        "markdown_source.py",
        "requirements-local.txt",
        "tests/test_change_detection.py",
        "tests/test_markdown_source.py",
        "tests/welcome.md",
    }
)
PRIVATE_PATH_PREFIXES = (
    "docs/_working/",
    "docs/techdocs-akamai-com/",
    "functions/",
)


def find_private_paths(paths: Iterable[str]) -> list[str]:
    """Return sorted tracked paths that belong to the private local workflow."""
    return sorted(
        path
        for path in paths
        if path in PRIVATE_EXACT_PATHS
        or any(path.startswith(prefix) for prefix in PRIVATE_PATH_PREFIXES)
    )


def tracked_paths(project_root: Path = PROJECT_ROOT) -> list[str]:
    """Read the current repository's tracked paths without inspecting history."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=project_root,
            capture_output=True,
            check=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("Git is required to check the public boundary") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"Cannot inspect tracked files: {message}") from exc
    return [
        path.decode("utf-8")
        for path in result.stdout.split(b"\0")
        if path
    ]


def main() -> int:
    try:
        private_paths = find_private_paths(tracked_paths())
    except RuntimeError as exc:
        print(f"Public-boundary check failed: {exc}", file=sys.stderr)
        return 1

    if private_paths:
        print(
            "Public-boundary check failed. Local-only files are tracked:",
            file=sys.stderr,
        )
        for path in private_paths:
            print(f"- {path}", file=sys.stderr)
        print(
            "Remove them from Git's index while keeping the local files, then "
            "run this check again.",
            file=sys.stderr,
        )
        return 1

    print("Public repository boundary is clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
