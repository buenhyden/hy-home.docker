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


STRICT_FORBIDDEN_SNIPPETS: list[str] = [
    "# [Component Name] Technical Specification",
    "- **PRD Reference**: [Link to PRD]",
    "| **[REQ-SPC-001]** | [Functional logic] | High | REQ-PRD-FUN-01 |",
    "- **[VAL-SPC-001]** Unit Test: [Description]",
    "- **[VAL-SPC-002]** Integration Test: [Description]",
    "- **[VAL-SPC-003]** Coverage: [Target numbers + how measured]",
    "- **[VAL-SPC-004]** E2E (Optional): [If applicable]",
    "- **[VAL-SPC-005]** Load (Optional): [If applicable]",
    "- **Component/Module Boundary**: [What this component owns and what it must NOT own]",
    "- **Backend**: [Language / framework / key libs (web, ORM, auth, etc.)]",
    "- **Frontend**: [Framework / state mgmt / build tool]",
    "- **Approach**: [None | In-process queue | Background worker | Kafka | RabbitMQ | SQS | ...]",
]

REQUIRED_HEADINGS: list[tuple[str, re.Pattern[str]]] = [
    (
        "Architecture/Tech Stack checklist",
        re.compile(r"^##\s+0\.\s+Architecture\s+/\s+Tech\s+Stack\s+Checklist\b", re.M),
    ),
    (
        "Quality/Testing/Security checklist",
        re.compile(r"^##\s+0\.\s+Quality\s+/\s+Testing\s+/\s+Security\s+Checklist\b", re.M),
    ),
    (
        "Operations/Deployment/Monitoring checklist",
        re.compile(
            r"^##\s+0\.\s+Operations\s+/\s+Deployment\s+/\s+Monitoring\s+Checklist\b",
            re.M,
        ),
    ),
    ("Technical overview", re.compile(r"^##\s+1\.\s+", re.M)),
    ("Traceability table", re.compile(r"^##\s+2\.\s+", re.M)),
    ("Data modeling", re.compile(r"^##\s+3\.\s+", re.M)),
    ("Interfaces", re.compile(r"^##\s+4\.\s+", re.M)),
    ("NFRs", re.compile(r"^##\s+5\.\s+", re.M)),
    ("Scalability/Infra", re.compile(r"^##\s+6\.\s+", re.M)),
    ("Verification plan", re.compile(r"^##\s+7\.\s+", re.M)),
    ("Ops/Observability", re.compile(r"^##\s+9\.\s+", re.M)),
]


def _extract_local_prd_path_from_reference(value: str) -> str | None:
    """
    Extract a local docs/prd/*.md path from a PRD Reference value.

    Supported formats:
    - docs/prd/my-feature-prd.md
    - `docs/prd/my-feature-prd.md`
    - [PRD](docs/prd/my-feature-prd.md)

    Returns the normalized path using forward slashes, or None if no local path found.
    """
    raw = value.strip().strip("`").strip()

    # Markdown link: [text](path)
    link_match = re.search(r"\((docs/prd/[^)]+\.md)\)", raw)
    if link_match:
        return link_match.group(1).strip()

    # Plain path anywhere in the value.
    path_match = re.search(r"\b(docs/prd/[^\s)]+\.md)\b", raw)
    if path_match:
        return path_match.group(1).strip()

    return None


def _validate_prd_approved(prd_path: Path) -> str | None:
    if not prd_path.exists():
        return f"PRD Reference target does not exist: {prd_path}"
    if not prd_path.is_file():
        return f"PRD Reference target is not a file: {prd_path}"

    text = _read_text(prd_path)
    status_match = re.search(r"^[*-]\s+\*\*Status\*\*:\s*(.+)\s*$", text, flags=re.M)
    if status_match is None:
        return f"PRD is missing a Status line: {prd_path}"

    status_value = status_match.group(1).strip().lower()
    if "approved" not in status_value:
        return f"PRD Status must include 'Approved' in strict mode: {prd_path}"

    return None


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


def validate_spec(path: Path, *, strict: bool) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if not path.exists():
        return [ValidationError(path, "File does not exist.")]
    if not path.is_file():
        return [ValidationError(path, "Not a file.")]

    text = _read_text(path)

    if not text.lstrip().startswith("# "):
        errors.append(ValidationError(path, "Missing H1 title (expected '# ...')."))

    for label, pattern in REQUIRED_HEADINGS:
        if not pattern.search(text):
            errors.append(ValidationError(path, f"Missing section: {label}."))

    arch_ref = re.search(
        r"^- \*\*Architecture Reference\*\*:\s*(.+)\s*$",
        text,
        flags=re.M,
    )
    if arch_ref is None:
        errors.append(
            ValidationError(path, "Missing '- **Architecture Reference**: ...' line.")
        )

    prd_ref = re.search(r"^- \*\*PRD Reference\*\*:\s*(.+)\s*$", text, flags=re.M)
    if prd_ref is None:
        errors.append(ValidationError(path, "Missing '- **PRD Reference**: ...' line."))
    elif strict:
        value = prd_ref.group(1).strip()
        if value == "[Link to PRD]":
            errors.append(
                ValidationError(
                    path,
                    "PRD Reference is still the template placeholder (strict).",
                )
            )
        else:
            prd_rel = _extract_local_prd_path_from_reference(value)
            if prd_rel is None:
                errors.append(
                    ValidationError(
                        path,
                        "PRD Reference must point to a local file under docs/prd/*.md (strict).",
                    )
                )
            else:
                prd_file = Path(prd_rel)
                prd_error = _validate_prd_approved(prd_file)
                if prd_error is not None:
                    errors.append(ValidationError(path, prd_error))

    if not re.search(r"\bREQ-SPC-\d+\b", text):
        errors.append(ValidationError(path, "Missing spec requirement IDs (REQ-SPC-NNN)."))

    if not re.search(r"\bREQ-PRD-FUN-\d+\b", text):
        errors.append(
            ValidationError(path, "Missing traceability to PRD requirements (REQ-PRD-FUN-NN).")
        )

    if not re.search(r"\bVAL-SPC-\d+\b", text):
        errors.append(ValidationError(path, "Missing verification IDs (VAL-SPC-NNN)."))

    if strict:
        for snippet in STRICT_FORBIDDEN_SNIPPETS:
            if snippet in text:
                errors.append(
                    ValidationError(
                        path,
                        f"Unfilled template placeholder found: {snippet!r}",
                    )
                )

    return errors


def _is_spec_path(path: Path) -> bool:
    normalized = str(path).replace("\\", "/")
    if not (normalized.startswith("specs/") and normalized.endswith(".md")):
        return False
    name = Path(normalized).name.lower()
    if name in {"readme.md", "plan.md"}:
        return False
    return True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate Technical Specification documents.")
    parser.add_argument("paths", nargs="*", help="Spec markdown files to validate (specs/**/*.md).")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Disallow template placeholders and require PRD Reference to exist and be Approved.",
    )
    parser.add_argument(
        "--changed-only",
        action="store_true",
        help="Validate only staged changed spec markdown files (git).",
    )
    args = parser.parse_args(argv)

    targets: list[Path] = []
    if args.changed_only:
        targets = [p for p in _git_changed_files() if _is_spec_path(p)]
    else:
        targets = [Path(p) for p in args.paths if _is_spec_path(Path(p))]

    if not targets:
        return 0

    all_errors: list[ValidationError] = []
    for target in targets:
        if args.changed_only and not _is_spec_path(target):
            continue
        all_errors.extend(validate_spec(target, strict=args.strict))

    if all_errors:
        for err in all_errors:
            print(f"{err.path}: {err.message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
