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
    ("Section 1 (Executive Summary)", re.compile(r"^##\s+1\.\s+", re.M)),
    ("Section 2 (System Overview & Context)", re.compile(r"^##\s+2\.\s+", re.M)),
    ("Section 3 (Component Architecture)", re.compile(r"^##\s+3\.\s+", re.M)),
    ("Section 4 (Data Architecture)", re.compile(r"^##\s+4\.\s+", re.M)),
    ("Section 5 (Security & Compliance)", re.compile(r"^##\s+5\.\s+", re.M)),
    ("Section 6 (Non-Functional Requirements)", re.compile(r"^##\s+6\.\s+", re.M)),
    ("Section 7 (Deployment & Infrastructure)", re.compile(r"^##\s+7\.\s+", re.M)),
    ("Section 8 (Alternatives & Trade-offs)", re.compile(r"^##\s+8\.\s+", re.M)),
]

STRICT_FORBIDDEN_SNIPPETS: list[str] = [
    "# [System/Service Name] Architecture Reference Document (ARD)",
    "- **Status**: [Draft | Review | Approved]",
    "- **Owner**: [Name]",
    "- **ADR References**: [Link to ADRs]",
    "- **PRD Reference**: [Link to PRD]",
    "title [System Name] Context Diagram",
    'System(this_system, "[System Name]")',
    "title [System Name] Container Diagram",
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


def _is_ard_path(path: Path) -> bool:
    normalized = str(path).replace("\\", "/")
    if not (normalized.startswith("docs/ard/") and normalized.endswith(".md")):
        return False
    if Path(normalized).name.lower() == "readme.md":
        return False
    return True


def validate_ard(path: Path, *, strict: bool) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if not path.exists():
        return [ValidationError(path, "File does not exist.")]
    if not path.is_file():
        return [ValidationError(path, "Not a file.")]

    text = _read_text(path)

    if not text.lstrip().startswith("# "):
        errors.append(ValidationError(path, "Missing H1 title (expected '# ...')."))

    if not re.search(r"^- \*\*Status\*\*:\s+.*$", text, flags=re.M):
        errors.append(ValidationError(path, "Missing '- **Status**: ...' line."))
    if not re.search(r"^- \*\*Owner\*\*:\s+.*$", text, flags=re.M):
        errors.append(ValidationError(path, "Missing '- **Owner**: ...' line."))
    if not re.search(r"^- \*\*ADR References\*\*:\s+.*$", text, flags=re.M):
        errors.append(ValidationError(path, "Missing '- **ADR References**: ...' line."))
    if not re.search(r"^- \*\*PRD Reference\*\*:\s+.*$", text, flags=re.M):
        errors.append(ValidationError(path, "Missing '- **PRD Reference**: ...' line."))

    for label, pattern in SECTION_HEADING_PATTERNS:
        if not pattern.search(text):
            errors.append(ValidationError(path, f"Missing {label} heading."))

    if strict:
        status_match = re.search(r"^- \*\*Status\*\*:\s*(.+)\s*$", text, flags=re.M)
        if status_match is None:
            errors.append(ValidationError(path, "Status line missing (strict)."))
        else:
            status_value = status_match.group(1).strip().lower()
            if "approved" not in status_value:
                errors.append(ValidationError(path, "Status must include 'Approved' for strict validation."))

        for snippet in STRICT_FORBIDDEN_SNIPPETS:
            if snippet in text:
                errors.append(ValidationError(path, f"Unfilled template placeholder found: {snippet!r}"))

    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate ARD documents.")
    parser.add_argument("paths", nargs="*", help="ARD markdown files to validate (docs/ard/*.md).")
    parser.add_argument("--strict", action="store_true", help="Enforce 'Approved' status and no template placeholders.")
    parser.add_argument("--changed-only", action="store_true", help="Validate only staged changed ARD files (git).")
    args = parser.parse_args(argv)

    targets: list[Path] = []
    if args.changed_only:
        targets = [p for p in _git_changed_files() if _is_ard_path(p)]
    else:
        targets = [Path(p) for p in args.paths if _is_ard_path(Path(p))]

    if not targets:
        return 0

    all_errors: list[ValidationError] = []
    for target in targets:
        if args.changed_only and not _is_ard_path(target):
            continue
        all_errors.extend(validate_ard(target, strict=args.strict))

    if all_errors:
        for err in all_errors:
            print(f"{err.path}: {err.message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
