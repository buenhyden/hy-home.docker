#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

python3 - "$@" <<'PY'
from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys
from dataclasses import dataclass

DEFAULT_PACK = pathlib.Path("docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack")

EXPECTED_REPORTS = [
    "implementation-overview.md",
    "harness-engineering-implementation.md",
    "loop-engineering-implementation.md",
    "provider-harness-loop-implementation.md",
    "workspace-rules-environment-implementation.md",
    "automation-candidates.md",
    "sdlc-quality-formatting-implementation.md",
    "security-framework-maturity.md",
]

EXPECTED_OVERVIEW_CATEGORIES = [
    "Harness engineering",
    "Loop engineering",
    "Claude provider harness/loop",
    "Codex provider harness/loop",
    "Gemini provider harness/loop",
    "Common provider-neutral rules/environment",
    "Automation, pipeline, workflow",
    "Spec-driven SDLC",
    "Docker Compose / infrastructure",
    "CI/CD",
    "QA, formatting, linting, syntax",
    "Security",
]

STATUS_HEADERS = {"status", "current status", "claude", "codex", "gemini"}


@dataclass(frozen=True)
class StatusCell:
    report: pathlib.Path
    row_label: str
    header: str
    raw_status: str
    normalized_status: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Report implementation-status coverage for the agentic engineering "
            "audit pack. Default mode prints an advisory summary; --check fails "
            "only when required reports or overview categories are missing."
        )
    )
    parser.add_argument("--pack", default=str(DEFAULT_PACK), help="Audit pack directory to inspect.")
    parser.add_argument("--check", action="store_true", help="Validate required coverage and exit non-zero on gaps.")
    return parser.parse_args(sys.argv[1:])


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def normalize_status(value: str) -> str:
    value_lower = value.lower()
    if "not implemented" in value_lower or value_lower == "gap" or value_lower.startswith("gap "):
        return "Gap / Not Implemented"
    if "partial" in value_lower or "partially" in value_lower or "fixture" in value_lower or "mapped" in value_lower:
        return "Partially Implemented"
    if "implemented" in value_lower:
        return "Implemented"
    if "unknown" in value_lower or "needs revalidation" in value_lower:
        return "Unknown / Needs Revalidation"
    return "Other"


def iter_tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    lines = text.splitlines()
    tables: list[tuple[list[str], list[list[str]]]] = []
    index = 0
    while index < len(lines) - 1:
        header_line = lines[index]
        separator_line = lines[index + 1]
        if not header_line.startswith("|") or not separator_line.startswith("|") or not is_separator(separator_line):
            index += 1
            continue
        header = split_row(header_line)
        rows: list[list[str]] = []
        index += 2
        while index < len(lines) and lines[index].startswith("|"):
            row = split_row(lines[index])
            if len(row) == len(header):
                rows.append(row)
            index += 1
        tables.append((header, rows))
    return tables


def extract_status_cells(path: pathlib.Path) -> list[StatusCell]:
    text = path.read_text(errors="ignore")
    status_cells: list[StatusCell] = []
    for header, rows in iter_tables(text):
        status_indexes = [
            index
            for index, name in enumerate(header)
            if name.strip().lower() in STATUS_HEADERS
        ]
        if not status_indexes:
            continue
        for row in rows:
            row_label = row[0]
            for index in status_indexes:
                raw_status = row[index]
                if not raw_status or raw_status == "---":
                    continue
                status_cells.append(
                    StatusCell(
                        report=path,
                        row_label=row_label,
                        header=header[index],
                        raw_status=raw_status,
                        normalized_status=normalize_status(raw_status),
                    )
                )
    return status_cells


def extract_overview_categories(path: pathlib.Path) -> dict[str, str]:
    text = path.read_text(errors="ignore")
    categories: dict[str, str] = {}
    for header, rows in iter_tables(text):
        if len(header) >= 2 and header[0] == "Category" and header[1] == "Status":
            for row in rows:
                categories[row[0]] = row[1]
    return categories


def main() -> int:
    args = parse_args()
    pack = pathlib.Path(args.pack)
    failures: list[str] = []

    if not pack.is_dir():
        failures.append(f"missing audit pack directory: {pack}")
        report_paths: list[pathlib.Path] = []
    else:
        report_paths = [pack / name for name in EXPECTED_REPORTS]
        for report in report_paths:
            if not report.is_file():
                failures.append(f"missing required audit report: {report}")

    all_status_cells: list[StatusCell] = []
    per_report_counts: dict[pathlib.Path, int] = {}
    for report in report_paths:
        if not report.is_file():
            continue
        cells = extract_status_cells(report)
        per_report_counts[report] = len(cells)
        all_status_cells.extend(cells)
        if len(cells) == 0:
            failures.append(f"no parseable implementation-status cells in required audit report: {report}")

    overview_path = pack / "implementation-overview.md"
    overview_categories = extract_overview_categories(overview_path) if overview_path.is_file() else {}
    for category in EXPECTED_OVERVIEW_CATEGORIES:
        if category not in overview_categories:
            failures.append(f"missing implementation-overview category: {category}")

    normalized_counts = collections.Counter(cell.normalized_status for cell in all_status_cells)
    raw_counts = collections.Counter(cell.raw_status for cell in all_status_cells)

    print("Audit pack implementation-status coverage")
    print(f"pack={pack}")
    print(f"reports_expected={len(EXPECTED_REPORTS)}")
    print(f"reports_checked={sum(1 for report in report_paths if report.is_file())}")
    print(f"status_cells_total={len(all_status_cells)}")
    print(f"overview_categories_expected={len(EXPECTED_OVERVIEW_CATEGORIES)}")
    print(f"overview_categories_found={len(overview_categories)}")
    print()
    print("Report coverage")
    for report in report_paths:
        print(f"- {report.name}: status_cells={per_report_counts.get(report, 0)}")
    print()
    print("Normalized status counts")
    for status in ["Implemented", "Partially Implemented", "Gap / Not Implemented", "Unknown / Needs Revalidation", "Other"]:
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
