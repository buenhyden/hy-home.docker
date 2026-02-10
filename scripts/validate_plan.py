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


REQUIRED_FRONT_MATTER_KEYS = {
    "goal",
    "version",
    "date_created",
    "last_updated",
    "owner",
    "status",
    "tags",
    "stack",
}

STRICT_FORBIDDEN_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\bTBD\b", re.I),
    re.compile(r"\[TBD[^\]]*\]", re.I),
    re.compile(r"\bYYYY-MM-DD\b"),
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


def _is_plan_path(path: Path) -> bool:
    normalized = str(path).replace("\\", "/").lstrip("./")
    return bool(re.match(r"^specs/[^/]+/plan\.md$", normalized))


def _parse_front_matter(text: str) -> tuple[dict[str, str], str] | None:
    """
    Parse YAML front matter (very small subset) and return (kv, body_text).

    Rules:
    - Must start with '---' on the first line.
    - Ends at the next line that is exactly '---'.
    - Supports top-level 'key: value' and 'key:' (multi-line values allowed but ignored).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None

    kv: dict[str, str] = {}
    for raw in lines[1:end_idx]:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key = m.group(1)
        value = m.group(2).strip()
        if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
            value = value[1:-1]
        kv[key] = value

    body = "\n".join(lines[end_idx + 1 :]).lstrip()
    return kv, body


def validate_plan(path: Path, *, strict: bool) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if not path.exists():
        return [ValidationError(path, "File does not exist.")]
    if not path.is_file():
        return [ValidationError(path, "Not a file.")]

    text = _read_text(path)

    if not _is_plan_path(path):
        errors.append(ValidationError(path, "Plan must be located at specs/<feature>/plan.md."))

    parsed = _parse_front_matter(text)
    if parsed is None:
        errors.append(ValidationError(path, "Missing or invalid YAML front matter (--- ... ---)."))
        return errors

    kv, body = parsed

    missing = sorted(REQUIRED_FRONT_MATTER_KEYS - set(kv.keys()))
    if missing:
        errors.append(
            ValidationError(
                path,
                f"Missing required front matter key(s): {', '.join(missing)}.",
            )
        )

    stack = (kv.get("stack") or "").strip().lower()
    if stack and stack not in {"node", "python"}:
        errors.append(ValidationError(path, "Front matter 'stack' must be 'node' or 'python'."))
    if "stack" in kv and not stack:
        errors.append(ValidationError(path, "Front matter 'stack' must not be empty."))

    if not re.search(r"^#\s+.+$", body, flags=re.M):
        errors.append(ValidationError(path, "Missing H1 title after front matter (expected '# ...')."))

    if strict:
        for pat in STRICT_FORBIDDEN_PATTERNS:
            m = pat.search(text)
            if m:
                errors.append(
                    ValidationError(
                        path,
                        f"Unfilled placeholder found (strict): {m.group(0)!r}.",
                    )
                )
                break

    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate implementation plan documents.")
    parser.add_argument("paths", nargs="*", help="Plan markdown files to validate (specs/**/plan.md).")
    parser.add_argument("--strict", action="store_true", help="Disallow template placeholders (TBD, YYYY-MM-DD).")
    parser.add_argument(
        "--changed-only",
        action="store_true",
        help="Validate only staged changed plan files (git).",
    )
    args = parser.parse_args(argv)

    targets: list[Path]
    if args.changed_only:
        targets = [p for p in _git_changed_files() if _is_plan_path(p)]
    else:
        targets = [Path(p) for p in args.paths if _is_plan_path(Path(p))]

    if not targets:
        return 0

    all_errors: list[ValidationError] = []
    for target in targets:
        if args.changed_only and not _is_plan_path(target):
            continue
        all_errors.extend(validate_plan(target, strict=args.strict))

    if all_errors:
        for err in all_errors:
            print(f"{err.path}: {err.message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
