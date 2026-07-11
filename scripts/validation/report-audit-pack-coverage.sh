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

CRITERION_REPORTS = [
    "harness-engineering-implementation.md",
    "loop-engineering-implementation.md",
    "provider-harness-loop-implementation.md",
    "workspace-rules-environment-implementation.md",
    "agent-instructions-catalog-vibe-models.md",
    "automation-candidates.md",
    "sdlc-document-contracts-implementation.md",
    "frontmatter-template-readme-implementation.md",
    "sdlc-quality-formatting-implementation.md",
    "compose-infrastructure-operations-readiness.md",
    "security-framework-maturity.md",
]

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

CRITERION_FIELDS = ["criterion id", "external criterion", "workspace evidence", "implementation state", "enforcement depth", "disposition", "canonical owner", "automation impact", "verification", "confidence"]
VALID_STATES = {"Implemented", "Partial", "Missing", "Not Applicable", "Needs Revalidation"}
VALID_DISPOSITIONS = {"Retain", "Fix", "Improve", "Add", "Remove"}


@dataclass(frozen=True)
class CriterionRow:
    report: pathlib.Path
    criterion_id: str
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
    if value_lower == "missing" or "not implemented" in value_lower or value_lower == "gap" or value_lower.startswith("gap "):
        return "Gap / Not Implemented"
    if value_lower == "not applicable":
        return "Not Applicable"
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


def extract_criterion_rows(path: pathlib.Path) -> tuple[list[CriterionRow], list[str]]:
    text = path.read_text(errors="ignore")
    criteria: list[CriterionRow] = []
    failures: list[str] = []
    for header, rows in iter_tables(text):
        normalized_header = [name.strip().lower() for name in header]
        if not normalized_header or normalized_header[0] != "criterion id":
            continue
        if "status" in normalized_header and "implementation state" not in normalized_header:
            normalized_header[normalized_header.index("status")] = "implementation state"
        if normalized_header != CRITERION_FIELDS:
            failures.append(f"invalid criterion schema in {path}: {' | '.join(header)}")
            continue
        index = {name: position for position, name in enumerate(normalized_header)}
        for row in rows:
            criterion_id = row[index["criterion id"]]
            raw_status = row[index["implementation state"]]
            depth = row[index["enforcement depth"]]
            disposition = row[index["disposition"]]
            if not re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-[0-9]{2}", criterion_id):
                failures.append(f"invalid criterion ID in {path}: {criterion_id}")
            if raw_status not in VALID_STATES:
                failures.append(f"invalid implementation state for {criterion_id}: {raw_status}")
            if not re.match(r"^([0-4])(?:\b|\s)", depth):
                failures.append(f"invalid enforcement depth for {criterion_id}: {depth}")
            if disposition not in VALID_DISPOSITIONS:
                failures.append(f"invalid disposition for {criterion_id}: {disposition}")
            criteria.append(
                CriterionRow(
                    report=path,
                    criterion_id=criterion_id,
                    raw_status=raw_status,
                    normalized_status=normalize_status(raw_status),
                )
            )
    return criteria, failures


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
        report_paths = [pack / name for name in CRITERION_REPORTS]
        for report in report_paths:
            if not report.is_file():
                failures.append(f"missing required audit report: {report}")

    all_criteria: list[CriterionRow] = []
    per_report_counts: dict[pathlib.Path, int] = {}
    for report in report_paths:
        if not report.is_file():
            continue
        criteria, criterion_failures = extract_criterion_rows(report)
        failures.extend(criterion_failures)
        per_report_counts[report] = len(criteria)
        all_criteria.extend(criteria)
        if len(criteria) == 0:
            failures.append(f"no parseable criterion rows in required audit report: {report}")

    criterion_ids = [criterion.criterion_id for criterion in all_criteria]
    for criterion_id, count in sorted(collections.Counter(criterion_ids).items()):
        if count > 1:
            failures.append(f"duplicate criterion ID: {criterion_id}")

    overview_path = pack / "implementation-overview.md"
    overview_categories = extract_overview_categories(overview_path) if overview_path.is_file() else {}
    for category in EXPECTED_OVERVIEW_CATEGORIES:
        if category not in overview_categories:
            failures.append(f"missing implementation-overview category: {category}")

    normalized_counts = collections.Counter(criterion.normalized_status for criterion in all_criteria)
    raw_counts = collections.Counter(criterion.raw_status for criterion in all_criteria)

    print("Audit pack implementation-status coverage")
    print(f"pack={pack}")
    print(f"criterion_reports_expected={len(CRITERION_REPORTS)}")
    print(f"criterion_reports_checked={sum(1 for report in report_paths if report.is_file())}")
    print("readme_indexes=1")
    print("overview_reports=1")
    print(f"criterion_rows_total={len(all_criteria)}")
    print(f"criterion_ids_unique={len(set(criterion_ids))}")
    print(f"overview_categories_expected={len(EXPECTED_OVERVIEW_CATEGORIES)}")
    print(f"overview_categories_found={len(overview_categories)}")
    print()
    print("Report coverage")
    for report in report_paths:
        print(f"- {report.name}: criterion_rows={per_report_counts.get(report, 0)}")
    print()
    print("Normalized status counts")
    for status in ["Implemented", "Partially Implemented", "Gap / Not Implemented", "Not Applicable", "Unknown / Needs Revalidation", "Other"]:
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
