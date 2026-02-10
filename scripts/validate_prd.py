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
    ("Section 1 (Vision & Problem)", re.compile(r"^##\s+1\.\s+", re.M)),
    ("Section 2 (Target Personas)", re.compile(r"^##\s+2\.\s+", re.M)),
    ("Section 3 (Success Metrics)", re.compile(r"^##\s+3\.\s+", re.M)),
    ("Section 4 (Use Cases)", re.compile(r"^##\s+4\.\s+", re.M)),
    ("Section 5 (Scope)", re.compile(r"^##\s+5\.\s+", re.M)),
    ("Section 6 (Out of Scope)", re.compile(r"^##\s+6\.\s+", re.M)),
    ("Section 7 (Milestones)", re.compile(r"^##\s+7\.\s+", re.M)),
    ("Section 8 (Risks/Compliance)", re.compile(r"^##\s+8\.\s+", re.M)),
]

STRICT_FORBIDDEN_SNIPPETS: list[str] = [
    "# [Feature/Epic Name] PRD",
    "- **Status**: [Draft | Review | Approved | Deprecated]",
    "* **Status**: [Draft | Review | Approved | Deprecated]",
    "- **Owner**: [Name]",
    "* **Owner**: [Name]",
    "- **Stakeholders**: [Project Manager, Lead Engineer, Designer, etc.]",
    "* **Stakeholders**: [Project Manager, Lead Engineer, Designer, etc.]",
    "- **Parent Epic**: [Link to Epic PRD] (Optional)",
    "* **Parent Epic**: [Link to Epic PRD] (Optional)",
    "[Provide a 2-3 sentence overview of what this feature is, why it's being built,",
    "* **Vision**: [Provide a one-paragraph vision statement of what this feature",
    '* **Persona 1 ([Name/Role])**: [e.g., "Sarah the Data Scientist"]',
    "* **Pain Point**: [Describe a specific frustration they face today]",
    "* **Goal**: [What does this persona want to achieve with this feature?]",
    "| **REQ-PRD-MET-01** | [e.g., Latency] |",
    "| **REQ-PRD-MET-02** | [e.g., Conversion] |",
    "**As a** [Persona Name]",
    "**I want** [action/feature]",
    "**So that** [value/benefit]",
    "[Requirement Description linked to STORY-XX]",
    "[Requirement Description]",
    "[Items that will NOT be built in this phase]",
    "* **PoC**: [Target Date]",
    "* **MVP**: [Target Date]",
    "* **Beta**: [Target Date]",
    "* **v1.0**: [Target Date]",
    "* **Risks & Mitigation**: [Market, Technical, or Operational risks and blockers]",
    "* **Compliance & Privacy**: [Personal data, GDPR/CCPA, industry regulations]",
    "* **Security Protocols**: [Specific security requirements for this feature]",
    "* **Assumptions**: [What are we assuming to be true? (e.g., Users have X device)]",
    "* **External Dependencies**: [Does this rely on external APIs or other teams?]",
    "| v0.1 | [YYYY-MM-DD] | [Name] | Initial Draft |",
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


def validate_prd(path: Path, *, strict: bool) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if not path.exists():
        return [ValidationError(path, "File does not exist.")]
    if not path.is_file():
        return [ValidationError(path, "Not a file.")]

    text = _read_text(path)

    if not text.lstrip().startswith("# "):
        errors.append(ValidationError(path, "Missing H1 title (expected '# ...')."))

    if not re.search(r"^[*-]\s+\*\*Status\*\*:\s+.*$", text, flags=re.M):
        errors.append(ValidationError(path, "Missing '- **Status**: ...' line."))

    for label, pattern in SECTION_HEADING_PATTERNS:
        if not pattern.search(text):
            errors.append(ValidationError(path, f"Missing {label} heading."))

    if strict:
        status_match = re.search(r"^[*-]\s+\*\*Status\*\*:\s*(.+)\s*$", text, flags=re.M)
        if status_match is None:
            errors.append(ValidationError(path, "Status line missing (strict)."))
        else:
            status_value = status_match.group(1).strip().lower()
            if "approved" not in status_value:
                errors.append(
                    ValidationError(
                        path,
                        "Status must include 'Approved' for strict validation.",
                    )
                )

        for snippet in STRICT_FORBIDDEN_SNIPPETS:
            if snippet in text:
                errors.append(
                    ValidationError(
                        path,
                        f"Unfilled template placeholder found: {snippet!r}",
                    )
                )

        if not re.search(r"\bREQ-PRD-MET-\d+\b", text):
            errors.append(
                ValidationError(
                    path,
                    "Missing success metric IDs (expected 'REQ-PRD-MET-NN').",
                )
            )

        if not re.search(r"\bREQ-PRD-FUN-\d+\b", text):
            errors.append(
                ValidationError(
                    path,
                    "Missing functional requirement IDs (expected 'REQ-PRD-FUN-NN').",
                )
            )

        stories = re.findall(r"\bSTORY-(\d+)\b", text)
        if len(set(stories)) < 3:
            errors.append(
                ValidationError(
                    path,
                    "Missing core use cases (expected at least STORY-01, STORY-02, STORY-03).",
                )
            )

    return errors


def _is_prd_path(path: Path) -> bool:
    normalized = str(path).replace("\\", "/")
    if not (normalized.startswith("docs/prd/") and normalized.endswith(".md")):
        return False
    if Path(normalized).name.lower() == "readme.md":
        return False
    return True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate PRD documents.")
    parser.add_argument(
        "paths",
        nargs="*",
        help="PRD markdown files to validate (docs/prd/*.md).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enforce 'Approved' status and no template placeholders.",
    )
    parser.add_argument(
        "--changed-only",
        action="store_true",
        help="Validate only staged changed PRD files (git).",
    )
    args = parser.parse_args(argv)

    targets: list[Path] = []
    if args.changed_only:
        targets = [p for p in _git_changed_files() if _is_prd_path(p)]
    else:
        targets = [Path(p) for p in args.paths if _is_prd_path(Path(p))]

    if not targets:
        return 0

    all_errors: list[ValidationError] = []
    for target in targets:
        if args.changed_only and not _is_prd_path(target):
            continue
        all_errors.extend(validate_prd(target, strict=args.strict))

    if all_errors:
        for err in all_errors:
            print(f"{err.path}: {err.message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
