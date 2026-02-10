#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ValidationError:
    path: Path
    message: str


SECTION_HEADING_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Context and Problem Statement", re.compile(r"^##\s+Context and Problem Statement\b", re.M)),
]

STRICT_FORBIDDEN_SNIPPETS: list[str] = [
    "# [Short Title of Decision]",
    "* **Status**: [Proposed | Accepted | Deprecated | Superseded]",
    "* **Date**: [YYYY-MM-DD]",
    "* **Authors**: [Name]",
    "* **Deciders**: [List of decision makers] (Optional)",
    "* **Stakeholders**: [Who is affected by this?] (Optional)",
    "* **Consulted**: [Who provided input?] (Optional)",
    "* **Reviewers**: [Who reviewed this record?] (Optional)",
    "[Describe the context and problem statement.",
    "* **[Driver 1]**:",
    "* **[Option 1]**:",
    'Chosen option: "**[Option 1]**", because',
    "* **[Requirement ID]**: [e.g., REQ-FUN-01, REQ-PRD-MET-01]",
]


def _git_changed_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--cached"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return []
    if result.returncode != 0:
        return []
    return [Path(p.strip()) for p in result.stdout.splitlines() if p.strip()]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _is_adr_path(path: Path) -> bool:
    normalized = str(path).replace("\\", "/")
    if not (normalized.startswith("docs/adr/") and normalized.endswith(".md")):
        return False
    if Path(normalized).name.lower() == "readme.md":
        return False
    return True


def validate_adr(path: Path, *, strict: bool) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if not path.exists():
        return [ValidationError(path, "File does not exist.")]
    if not path.is_file():
        return [ValidationError(path, "Not a file.")]

    text = _read_text(path)

    if not text.lstrip().startswith("# "):
        errors.append(ValidationError(path, "Missing H1 title (expected '# ...')."))

    if not re.search(r"^[*-]\s+\*\*Status\*\*:\s+.*$", text, flags=re.M):
        errors.append(ValidationError(path, "Missing '* **Status**: ...' line."))

    if not re.search(r"^[*-]\s+\*\*Date\*\*:\s+.*$", text, flags=re.M):
        errors.append(ValidationError(path, "Missing '* **Date**: ...' line."))

    for label, pattern in SECTION_HEADING_PATTERNS:
        if not pattern.search(text):
            errors.append(ValidationError(path, f"Missing section: {label}."))

    if strict:
        status_match = re.search(r"^[*-]\s+\*\*Status\*\*:\s*(.+)\s*$", text, flags=re.M)
        if status_match is None:
            errors.append(ValidationError(path, "Status line missing (strict)."))
        else:
            status_value = status_match.group(1).strip().lower()
            if "accepted" not in status_value:
                errors.append(ValidationError(path, "Status must include 'Accepted' for strict validation."))

        for snippet in STRICT_FORBIDDEN_SNIPPETS:
            if snippet in text:
                errors.append(ValidationError(path, f"Unfilled template placeholder found: {snippet!r}"))

    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate ADR documents.")
    parser.add_argument("paths", nargs="*", help="ADR markdown files to validate (docs/adr/*.md).")
    parser.add_argument("--strict", action="store_true", help="Enforce 'Accepted' status and no template placeholders.")
    parser.add_argument("--changed-only", action="store_true", help="Validate only staged changed ADR files (git).")
    args = parser.parse_args(argv)

    targets: list[Path] = []
    if args.changed_only:
        targets = [p for p in _git_changed_files() if _is_adr_path(p)]
    else:
        targets = [Path(p) for p in args.paths if _is_adr_path(Path(p))]

    if not targets:
        return 0

    all_errors: list[ValidationError] = []
    for target in targets:
        if args.changed_only and not _is_adr_path(target):
            continue
        all_errors.extend(validate_adr(target, strict=args.strict))

    if all_errors:
        for err in all_errors:
            print(f"{err.path}: {err.message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
