#!/usr/bin/env python3
"""Validate Spec 137 pre-deletion gate 4.

Gate 4 requires zero clickable references to the retiring research pack across
all tracked text outside the retiring directory, and requires every permitted
non-link literal to appear in the reviewed allowlist the Stage 04 Task owns.

The gate was manual until this module existed. A regression introduced on
2026-08-14 survived five days undetected because nothing re-ran the scan.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass

SLUG = "2026-07-05-agentic-research-pack-refresh"
RETIRING_DIR = f"docs/90.references/research/{SLUG}"
TASK_PATH = "docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md"
ALLOWLIST_HEADING = "### Old-path allowlist"

# Generated advisory navigation. Spec 137's generated-artifact inventory closes
# this surface separately and authorizes no refresh, so it is reported rather
# than allowlisted. Never silently dropped: the count is always printed.
GENERATED_PREFIXES = ("graphify-out/",)

CLICKABLE = re.compile(rf"\]\([^)]*{re.escape(SLUG)}/")


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    line: int
    message: str


def _git(root: pathlib.Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def tracked_files(root: pathlib.Path) -> list[str]:
    return [line for line in _git(root, "ls-files").splitlines() if line]


def read_allowlist(root: pathlib.Path) -> set[str]:
    """Return the allowlisted repository paths the Task records."""
    text = (root / TASK_PATH).read_text(encoding="utf-8")
    lines = text.split("\n")
    try:
        start = next(
            index
            for index, line in enumerate(lines)
            if line.startswith(ALLOWLIST_HEADING)
        )
    except StopIteration:
        return set()
    allowed: set[str] = set()
    for line in lines[start + 1 :]:
        if line.startswith("### ") or line.startswith("## "):
            break
        if not line.startswith("| `"):
            continue
        cells = line.split("|")
        if len(cells) < 3:
            continue
        allowed.add(cells[1].strip().strip("`"))
    return allowed


def _is_text(path: pathlib.Path) -> bool:
    try:
        path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return True


def scan(root: pathlib.Path) -> tuple[list[Finding], int]:
    """Return gate-4 findings plus the generated-surface occurrence count."""
    allowed = read_allowlist(root)
    findings: list[Finding] = []
    generated_hits = 0
    for relative in tracked_files(root):
        if relative.startswith(f"{RETIRING_DIR}/"):
            continue
        absolute = root / relative
        if not absolute.is_file() or not _is_text(absolute):
            continue
        for number, line in enumerate(
            absolute.read_text(encoding="utf-8").split("\n"), start=1
        ):
            if SLUG not in line:
                continue
            if relative.startswith(GENERATED_PREFIXES):
                generated_hits += 1
                continue
            if CLICKABLE.search(line):
                findings.append(
                    Finding(
                        "OLD-PATH-CLICKABLE-LINK",
                        relative,
                        number,
                        "clickable link to the retiring pack; gate 4 admits no "
                        "clickable-link exception",
                    )
                )
                continue
            if relative not in allowed:
                findings.append(
                    Finding(
                        "OLD-PATH-UNALLOWLISTED",
                        relative,
                        number,
                        "non-link literal outside the reviewed allowlist",
                    )
                )
    return findings, generated_hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Spec 137 pre-deletion gate 4 (old-path references)"
    )
    parser.add_argument(
        "--root",
        default=".",
        help="repository root to scan (default: current directory)",
    )
    arguments = parser.parse_args(argv)
    root = pathlib.Path(arguments.root).resolve()

    findings, generated_hits = scan(root)
    allowed = read_allowlist(root)

    for finding in sorted(findings, key=lambda item: (item.path, item.line)):
        print(
            f"FAIL [{finding.code}] {finding.path}:{finding.line}: {finding.message}",
            file=sys.stderr,
        )

    clickable = sum(1 for item in findings if item.code == "OLD-PATH-CLICKABLE-LINK")
    unallowlisted = len(findings) - clickable
    print("Old-path gate 4 check")
    print(f"allowlist_rows={len(allowed)}")
    print(f"clickable_links={clickable}")
    print(f"unallowlisted_literals={unallowlisted}")
    print(f"generated_surface_occurrences={generated_hits}")
    print(f"failures={len(findings)}")
    if findings:
        return 1
    print("PASS: no clickable old-pack reference and no unallowlisted literal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
