#!/usr/bin/env python3
"""Shared completeness contract for the canonical implementation audit pack."""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
from dataclasses import dataclass


DEFAULT_PACK = pathlib.Path(
    "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack"
)

# Ordered manifest: report -> expected criterion prefix -> exact row count.
REPORT_PREFIX_COUNTS: dict[str, dict[str, int]] = {
    "harness-engineering-implementation.md": {"HAR": 7},
    "loop-engineering-implementation.md": {"LOOP": 6},
    "provider-harness-loop-implementation.md": {"PIC": 17},
    "workspace-rules-environment-implementation.md": {"WRE": 10},
    "agent-instructions-catalog-vibe-models.md": {"AIV": 16, "AIC": 7, "AMS": 7},
    "automation-candidates.md": {"AUT": 11},
    "sdlc-document-contracts-implementation.md": {"SDLC": 22},
    "frontmatter-template-readme-implementation.md": {"DML": 14},
    "sdlc-quality-formatting-implementation.md": {"QAF": 16},
    "compose-infrastructure-operations-readiness.md": {"CIO": 14},
    "security-framework-maturity.md": {"SEC": 14},
}

NON_CRITERION_FILES = {
    "README.md",
    "implementation-overview.md",
    "frontmatter-semantic-inventory.md",
}
EXPECTED_PACK_FILES = NON_CRITERION_FILES | set(REPORT_PREFIX_COUNTS)
EXPECTED_TOTAL = sum(
    count for prefix_counts in REPORT_PREFIX_COUNTS.values() for count in prefix_counts.values()
)
EXPECTED_PREFIX_COUNTS = collections.Counter(
    {
        prefix: count
        for prefix_counts in REPORT_PREFIX_COUNTS.values()
        for prefix, count in prefix_counts.items()
    }
)

SCHEMA = (
    "criterion id",
    "external criterion",
    "workspace evidence",
    "implementation state",
    "enforcement depth",
    "disposition",
    "canonical owner",
    "automation impact",
    "verification",
    "confidence",
)
VALID_STATE_HEADERS = {"status", "implementation state"}
VALID_STATES = {"Implemented", "Partial", "Missing", "Not Applicable", "Needs Revalidation"}
VALID_DISPOSITIONS = {"Retain", "Fix", "Improve", "Add", "Remove"}
ID_RE = re.compile(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-[0-9]{2}")
DEPTH_RE = re.compile(r"([0-4])(?:\b|\s)")
SEPARATOR_RE = re.compile(r":?-{3,}:?")


@dataclass(frozen=True)
class CriterionRow:
    report: pathlib.Path
    criterion_id: str
    external_criterion: str
    workspace_evidence: str
    raw_status: str
    normalized_status: str
    enforcement_depth: str
    disposition: str
    canonical_owner: str
    automation_impact: str
    verification: str
    confidence: str


@dataclass(frozen=True)
class AuditCriterionContract:
    pack: pathlib.Path
    rows: tuple[CriterionRow, ...]
    per_report_counts: dict[str, int]
    per_prefix_counts: dict[str, int]


class AuditCriterionContractError(ValueError):
    def __init__(self, errors: list[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(errors))


def split_row(line: str) -> list[str]:
    """Split a Markdown table row while preserving escaped pipes."""

    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|") and not stripped.endswith(r"\|"):
        stripped = stripped[:-1]
    return [cell.replace(r"\|", "|").strip() for cell in re.split(r"(?<!\\)\|", stripped)]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(SEPARATOR_RE.fullmatch(cell) for cell in cells)


def normalize_status(value: str) -> str:
    if value == "Implemented":
        return "Implemented"
    if value == "Partial":
        return "Partially Implemented"
    if value == "Missing":
        return "Gap / Not Implemented"
    if value == "Not Applicable":
        return "Not Applicable"
    if value == "Needs Revalidation":
        return "Unknown / Needs Revalidation"
    return "Other"


def criterion_prefix(criterion_id: str) -> str:
    return criterion_id.rsplit("-", 1)[0]


def expected_ids(prefix: str, count: int) -> set[str]:
    return {f"{prefix}-{index:02d}" for index in range(1, count + 1)}


def _parse_report(path: pathlib.Path, prefix_counts: dict[str, int]) -> tuple[list[CriterionRow], list[str]]:
    errors: list[str] = []
    rows: list[CriterionRow] = []
    lines = path.read_text(encoding="utf-8", errors="strict").splitlines()
    table_count = 0
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.lstrip().startswith("|"):
            index += 1
            continue
        header = split_row(line)
        if not header or header[0].strip().lower() != "criterion id":
            index += 1
            continue

        table_count += 1
        normalized_header = [cell.lower() for cell in header]
        if len(normalized_header) != len(SCHEMA):
            errors.append(
                f"{path}: criterion header has {len(normalized_header)} fields; expected {len(SCHEMA)}"
            )
        elif normalized_header[3] not in VALID_STATE_HEADERS:
            errors.append(
                f"{path}: field 4 must be Status or Implementation state; found {header[3]}"
            )
        else:
            normalized_header[3] = "implementation state"
            if tuple(normalized_header) != SCHEMA:
                errors.append(f"{path}: invalid criterion header order/schema: {' | '.join(header)}")

        if index + 1 >= len(lines) or not lines[index + 1].lstrip().startswith("|"):
            errors.append(f"{path}: criterion table is missing its separator row")
            index += 1
            continue
        separator = split_row(lines[index + 1])
        if len(separator) != len(SCHEMA) or not is_separator(separator):
            errors.append(f"{path}: malformed criterion table separator")

        index += 2
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            raw_line = lines[index]
            cells = split_row(raw_line)
            if is_separator(cells):
                errors.append(f"{path}:{index + 1}: unexpected separator inside criterion rows")
                index += 1
                continue
            if len(cells) != len(SCHEMA):
                errors.append(
                    f"{path}:{index + 1}: malformed criterion row has {len(cells)} fields; expected {len(SCHEMA)}"
                )
                index += 1
                continue
            empty_fields = [SCHEMA[position] for position, cell in enumerate(cells) if not cell.strip()]
            if empty_fields:
                errors.append(
                    f"{path}:{index + 1}: empty criterion fields: {', '.join(empty_fields)}"
                )
                index += 1
                continue

            criterion_id = cells[0]
            raw_status = cells[3]
            depth = cells[4]
            disposition = cells[5]
            prefix = criterion_prefix(criterion_id) if ID_RE.fullmatch(criterion_id) else "[invalid]"

            if not ID_RE.fullmatch(criterion_id):
                errors.append(f"{path}:{index + 1}: invalid criterion ID: {criterion_id}")
            if prefix not in prefix_counts:
                errors.append(
                    f"{path}:{index + 1}: criterion prefix {prefix} is not allowed in {path.name}"
                )
            if raw_status not in VALID_STATES:
                errors.append(
                    f"{path}:{index + 1}: invalid implementation state for {criterion_id}: {raw_status}"
                )
            depth_match = DEPTH_RE.match(depth)
            if not depth_match:
                errors.append(
                    f"{path}:{index + 1}: invalid enforcement depth for {criterion_id}: {depth}"
                )
            if disposition not in VALID_DISPOSITIONS:
                errors.append(
                    f"{path}:{index + 1}: invalid disposition for {criterion_id}: {disposition}"
                )

            rows.append(
                CriterionRow(
                    report=path,
                    criterion_id=criterion_id,
                    external_criterion=cells[1],
                    workspace_evidence=cells[2],
                    raw_status=raw_status,
                    normalized_status=normalize_status(raw_status),
                    enforcement_depth=depth_match.group(1) if depth_match else depth,
                    disposition=disposition,
                    canonical_owner=cells[6],
                    automation_impact=cells[7],
                    verification=cells[8],
                    confidence=cells[9],
                )
            )
            index += 1

    expected_table_count = len(prefix_counts)
    if table_count != expected_table_count:
        errors.append(
            f"{path}: expected exactly {expected_table_count} criterion table(s); found {table_count}"
        )

    report_ids = {row.criterion_id for row in rows}
    expected_report_ids = {
        criterion_id
        for prefix, count in prefix_counts.items()
        for criterion_id in expected_ids(prefix, count)
    }
    missing_ids = sorted(expected_report_ids - report_ids)
    unexpected_ids = sorted(report_ids - expected_report_ids)
    if missing_ids:
        errors.append(f"{path}: missing criterion IDs: {', '.join(missing_ids)}")
    if unexpected_ids:
        errors.append(f"{path}: unexpected criterion IDs: {', '.join(unexpected_ids)}")
    expected_report_count = sum(prefix_counts.values())
    if len(rows) != expected_report_count:
        errors.append(
            f"{path}: criterion row count {len(rows)} does not equal expected {expected_report_count}"
        )

    return rows, errors


def validate_pack(pack: pathlib.Path | str = DEFAULT_PACK) -> AuditCriterionContract:
    pack_path = pathlib.Path(pack)
    errors: list[str] = []
    all_rows: list[CriterionRow] = []
    per_report_counts: dict[str, int] = {}

    if not pack_path.is_dir():
        raise AuditCriterionContractError([f"missing audit pack directory: {pack_path}"])

    actual_files = {path.name for path in pack_path.glob("*.md")}
    for missing in sorted(EXPECTED_PACK_FILES - actual_files):
        errors.append(f"{pack_path}: missing expected Markdown file: {missing}")
    for unexpected in sorted(actual_files - EXPECTED_PACK_FILES):
        errors.append(f"{pack_path}: unexpected Markdown file: {unexpected}")

    for report_name, prefix_counts in REPORT_PREFIX_COUNTS.items():
        report_path = pack_path / report_name
        if not report_path.is_file():
            per_report_counts[report_name] = 0
            continue
        report_rows, report_errors = _parse_report(report_path, prefix_counts)
        all_rows.extend(report_rows)
        per_report_counts[report_name] = len(report_rows)
        errors.extend(report_errors)

    id_counts = collections.Counter(row.criterion_id for row in all_rows)
    duplicates = sorted(criterion_id for criterion_id, count in id_counts.items() if count > 1)
    if duplicates:
        errors.append(f"duplicate criterion IDs: {', '.join(duplicates)}")

    prefix_counts = collections.Counter(criterion_prefix(row.criterion_id) for row in all_rows)
    for prefix in sorted(set(EXPECTED_PREFIX_COUNTS) | set(prefix_counts)):
        actual = prefix_counts.get(prefix, 0)
        expected = EXPECTED_PREFIX_COUNTS.get(prefix, 0)
        if actual != expected:
            errors.append(f"criterion prefix {prefix}: row count {actual} does not equal expected {expected}")

    if len(all_rows) != EXPECTED_TOTAL:
        errors.append(f"criterion row total {len(all_rows)} does not equal expected {EXPECTED_TOTAL}")

    if errors:
        raise AuditCriterionContractError(errors)

    return AuditCriterionContract(
        pack=pack_path,
        rows=tuple(all_rows),
        per_report_counts=per_report_counts,
        per_prefix_counts=dict(prefix_counts),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", type=pathlib.Path, default=DEFAULT_PACK)
    args = parser.parse_args()
    try:
        contract = validate_pack(args.pack)
    except AuditCriterionContractError as exc:
        for error in exc.errors:
            print(f"FAIL: {error}")
        return 1

    print(f"criterion_reports={len(REPORT_PREFIX_COUNTS)}")
    print(f"criterion_rows={len(contract.rows)}")
    print(f"criterion_ids_unique={len({row.criterion_id for row in contract.rows})}")
    print("criterion_contract=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
