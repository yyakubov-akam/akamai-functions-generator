#!/usr/bin/env python3
"""Synchronize generated AI-agent instruction compatibility files."""

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "AGENTS.md"
COPILOT_DESTINATION = PROJECT_ROOT / ".github" / "copilot-instructions.md"


def sync_copilot_instructions(check: bool = False) -> int:
    expected = SOURCE.read_text(encoding="utf-8")
    actual = (
        COPILOT_DESTINATION.read_text(encoding="utf-8")
        if COPILOT_DESTINATION.exists()
        else None
    )

    if actual == expected:
        print("Copilot instructions are up to date.")
        return 0

    if check:
        print(
            "Copilot instructions are stale. Run "
            "`python scripts/sync_agent_instructions.py`.",
            file=sys.stderr,
        )
        return 1

    COPILOT_DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    COPILOT_DESTINATION.write_text(expected, encoding="utf-8")
    print(f"Updated {COPILOT_DESTINATION.relative_to(PROJECT_ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check for drift without modifying files",
    )
    args = parser.parse_args()
    return sync_copilot_instructions(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
