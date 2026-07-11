#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

python3 - "$@" <<'PY'
from __future__ import annotations

import argparse
import collections
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path("scripts/validation").resolve()))
from audit_criterion_contract import (  # noqa: E402
    AuditCriterionContractError,
    DEFAULT_PACK,
    EXPECTED_PREFIX_COUNTS,
    EXPECTED_TOTAL,
    REPORT_PREFIX_COUNTS,
    is_separator,
    split_row,
    validate_pack,
)

EXPECTED_OVERVIEW_CATEGORIES = [
    "Harness engineering",
    "Loop engineering",
    "Claude provider harness/loop",
    "Codex provider harness/loop",
    "Gemini provider harness/loop",
    "Common provider-neutral rules/environment",
    "Agent instructions, catalogs, vibe coding, and model routing",
    "Automation, pipeline, workflow",
    "Spec-driven SDLC",
    "Frontmatter, templates, and README profiles",
    "Release communication and records",
    "Docker Compose / infrastructure",
    "CI/CD",
    "QA, formatting, linting, syntax",
    "Security",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Report exact criterion coverage for the agentic engineering audit "
            "pack. --check fails on report, schema, field, ID, vocabulary, "
            "cardinality, uniqueness, or overview-category defects."
        )
    )
    parser.add_argument(
        "--pack",
        default=os.environ.get("AUDIT_PACK_DIR", str(DEFAULT_PACK)),
        help="Audit pack directory to inspect.",
    )
    parser.add_argument("--check", action="store_true", help="Print an explicit pass marker.")
    return parser.parse_args(sys.argv[1:])


def iter_tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    lines = text.splitlines()
    tables: list[tuple[list[str], list[list[str]]]] = []
    index = 0
    while index < len(lines) - 1:
        if not lines[index].lstrip().startswith("|") or not lines[index + 1].lstrip().startswith("|"):
            index += 1
            continue
        header = split_row(lines[index])
        separator = split_row(lines[index + 1])
        if len(separator) != len(header) or not is_separator(separator):
            index += 1
            continue
        rows: list[list[str]] = []
        index += 2
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            row = split_row(lines[index])
            if len(row) == len(header):
                rows.append(row)
            index += 1
        tables.append((header, rows))
    return tables


def extract_overview_categories(path: pathlib.Path) -> dict[str, str]:
    categories: dict[str, str] = {}
    if not path.is_file():
        return categories
    for header, rows in iter_tables(path.read_text(encoding="utf-8")):
        if len(header) >= 2 and header[0] == "Category" and header[1] == "Status":
            for row in rows:
                categories[row[0]] = row[1]
    return categories


def main() -> int:
    args = parse_args()
    pack = pathlib.Path(args.pack)
    failures: list[str] = []

    try:
        contract = validate_pack(pack)
    except AuditCriterionContractError as exc:
        for failure in exc.errors:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    overview_categories = extract_overview_categories(pack / "implementation-overview.md")
    for category in EXPECTED_OVERVIEW_CATEGORIES:
        if category not in overview_categories:
            failures.append(f"missing implementation-overview category: {category}")

    normalized_counts = collections.Counter(row.normalized_status for row in contract.rows)
    raw_counts = collections.Counter(row.raw_status for row in contract.rows)
    criterion_ids = {row.criterion_id for row in contract.rows}

    print("Audit pack criterion completeness coverage")
    print(f"pack={pack}")
    print(f"criterion_reports_expected={len(REPORT_PREFIX_COUNTS)}")
    print(f"criterion_reports_checked={len(contract.per_report_counts)}")
    print("readme_indexes=1")
    print("overview_reports=1")
    print(f"criterion_rows_expected={EXPECTED_TOTAL}")
    print(f"criterion_rows_total={len(contract.rows)}")
    print(f"criterion_ids_unique={len(criterion_ids)}")
    print(f"overview_categories_expected={len(EXPECTED_OVERVIEW_CATEGORIES)}")
    print(f"overview_categories_found={len(overview_categories)}")
    print()
    print("Report coverage")
    for report_name in REPORT_PREFIX_COUNTS:
        print(f"- {report_name}: criterion_rows={contract.per_report_counts[report_name]}")
    print()
    print("Prefix coverage")
    for prefix, expected in sorted(EXPECTED_PREFIX_COUNTS.items()):
        print(f"- {prefix}: criterion_rows={contract.per_prefix_counts[prefix]} expected={expected}")
    print()
    print("Normalized status counts")
    for status in [
        "Implemented",
        "Partially Implemented",
        "Gap / Not Implemented",
        "Not Applicable",
        "Unknown / Needs Revalidation",
        "Other",
    ]:
        print(f"- {status}: {normalized_counts.get(status, 0)}")
    print()
    print("Raw status counts")
    for status, count in sorted(raw_counts.items()):
        print(f"- {status}: {count}")
    print()
    print("Overview category statuses")
    for category in EXPECTED_OVERVIEW_CATEGORIES:
        print(f"- {category}: {overview_categories.get(category, '[missing]')}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    if args.check:
        print()
        print("coverage_check=pass")
    return 0


raise SystemExit(main())
PY
