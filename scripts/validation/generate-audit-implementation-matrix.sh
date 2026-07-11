#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

OUTPUT="docs/90.references/data/governance/audit-implementation-matrix.md"

usage() {
  cat <<'EOF'
Usage: bash scripts/validation/generate-audit-implementation-matrix.sh [--check|--dry-run]

Generate the Stage 90 audit implementation matrix snapshot from tracked audit-pack evidence.

Options:
  --check    Fail when the generated snapshot is stale.
  --dry-run  Print the generated snapshot to stdout without writing it.
  -h, --help Show this help.
EOF
}

mode="write"
case "${1:-}" in
  "")
    ;;
  --check)
    mode="check"
    ;;
  --dry-run)
    mode="dry-run"
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

python3 - "$mode" "$OUTPUT" <<'PY'
from __future__ import annotations

import collections
import os
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass

sys.path.insert(0, str(pathlib.Path("scripts/validation").resolve()))
from audit_criterion_contract import (  # noqa: E402
    AuditCriterionContractError,
    REPORT_PREFIX_COUNTS,
    validate_pack,
)

MODE = sys.argv[1]
OUTPUT = pathlib.Path(sys.argv[2])
PACK = pathlib.Path(os.environ.get("AUDIT_PACK_DIR", "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack"))

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

EXPECTED_CANDIDATES = [f"AEA-AUTO-{index:03d}" for index in range(1, 14)]


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    candidate: str
    disposition: str
    evidence: str


def git_ls_files() -> set[str]:
    result = subprocess.run(["git", "ls-files"], check=True, capture_output=True, text=True)
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


TRACKED = git_ls_files()


def read(path: pathlib.Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(errors="ignore")


def exists(path: pathlib.Path) -> bool:
    return path.is_file()


def file_state(path: pathlib.Path) -> str:
    if exists(path):
        return "present"
    return "missing"


def link(path: pathlib.Path | str, label: str | None = None) -> str:
    path_text = path.as_posix() if isinstance(path, pathlib.Path) else path
    label_text = label or path_text
    return f"[{label_text}](../../../../{path_text})"


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


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


def extract_overview_categories(path: pathlib.Path) -> dict[str, str]:
    categories: dict[str, str] = {}
    for header, rows in iter_tables(read(path)):
        if len(header) >= 2 and header[0] == "Category" and header[1] == "Status":
            for row in rows:
                categories[row[0]] = row[1]
    return categories


def strip_markdown_link(text: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)


def extract_candidates(path: pathlib.Path) -> dict[str, Candidate]:
    candidates: dict[str, Candidate] = {}
    for header, rows in iter_tables(read(path)):
        if len(header) < 3 or header[0] != "Candidate ID":
            continue
        for row in rows:
            candidate_id = row[0]
            if not re.fullmatch(r"AEA-AUTO-[0-9]{3}", candidate_id):
                continue
            detail = " ".join(row[2:])
            if re.search(r"implemented by", detail, flags=re.I):
                disposition = "Closed with evidence"
                if re.search(r"remain|future work|optional future|deferred", detail, flags=re.I):
                    disposition = "Closed with residual gap"
            else:
                disposition = "Open / needs planning"
            candidates[candidate_id] = Candidate(
                candidate_id=candidate_id,
                candidate=strip_markdown_link(row[1]),
                disposition=disposition,
                evidence=detail,
            )
    return candidates


def extract_gap_signals() -> list[str]:
    combined = "\n".join(
        read(path)
        for path in [
            PACK / "implementation-overview.md",
            PACK / "automation-candidates.md",
            PACK / "security-framework-maturity.md",
        ]
    ).lower()
    checks = [
        ("Broader ecosystem/container vulnerability scanning remains future work.", ("broader ecosystem/container vulnerability", "broad ecosystem/container vulnerability")),
        ("SBOM generation remains future work.", ("sbom",)),
        ("Signing, provenance, and attestation automation remain future work.", ("provenance", "attestation", "signing")),
        ("OpenSSF Scorecard automation remains future work.", ("scorecard",)),
    ]
    return [
        label
        for label, terms in checks
        if any(term in combined for term in terms)
    ]


def build_output() -> tuple[str, list[str]]:
    failures: list[str] = []
    contract = validate_pack(PACK)
    report_paths = [PACK / name for name in REPORT_PREFIX_COUNTS]
    all_criteria = list(contract.rows)
    per_report_counts = {
        PACK / report_name: count
        for report_name, count in contract.per_report_counts.items()
    }
    criterion_ids = [criterion.criterion_id for criterion in all_criteria]

    overview_categories = extract_overview_categories(PACK / "implementation-overview.md")
    for category in EXPECTED_OVERVIEW_CATEGORIES:
        if category not in overview_categories:
            failures.append(f"missing implementation-overview category: {category}")

    candidates = extract_candidates(PACK / "automation-candidates.md")
    for candidate_id in EXPECTED_CANDIDATES:
        if candidate_id not in candidates:
            failures.append(f"missing automation candidate row: {candidate_id}")

    normalized_counts = collections.Counter(criterion.normalized_status for criterion in all_criteria)
    raw_counts = collections.Counter(criterion.raw_status for criterion in all_criteria)
    disposition_counts = collections.Counter(candidate.disposition for candidate in candidates.values())
    gap_signals = extract_gap_signals()

    expected_generated_surfaces = [
        ("Audit-pack coverage report", "AEA-AUTO-007", pathlib.Path("scripts/validation/report-audit-pack-coverage.sh"), None),
        ("LLM Wiki stage/category coverage", "AEA-AUTO-008", pathlib.Path("scripts/knowledge/generate-llm-wiki-coverage.sh"), pathlib.Path("docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md")),
        ("Tech-stack version provenance", "AEA-AUTO-009", pathlib.Path("scripts/operations/generate-tech-stack-version-provenance.sh"), pathlib.Path("docs/90.references/data/docker/tech-stack-version-provenance.md")),
        ("Provider hook parity matrix", "AEA-AUTO-010", pathlib.Path("scripts/validation/report-provider-hook-parity.sh"), pathlib.Path("docs/90.references/data/governance/provider-hook-parity-matrix.md")),
        ("Agent-output eval runner", "AEA-AUTO-011", pathlib.Path("scripts/validation/run-agent-output-eval-fixtures.sh"), pathlib.Path("docs/90.references/data/governance/agent-output-eval-fixtures.md")),
        ("Security automation readiness", "AEA-AUTO-012", pathlib.Path("scripts/validation/generate-security-automation-readiness.sh"), pathlib.Path("docs/90.references/data/security/security-automation-readiness.md")),
        ("Audit implementation matrix", "AEA-AUTO-013", pathlib.Path("scripts/validation/generate-audit-implementation-matrix.sh"), OUTPUT),
    ]

    lines: list[str] = [
        "---",
        "status: active",
        "generated_by: scripts/validation/generate-audit-implementation-matrix.sh",
        "---",
        "",
        "<!-- Target: docs/90.references/data/governance/audit-implementation-matrix.md -->",
        "",
        "# Reference: Audit Implementation Matrix",
        "",
        "## Overview",
        "",
        "This generated reference summarizes the implementation-status audit pack,",
        "automation-candidate closure state, and generated evidence surfaces for the",
        "`2026-07-05-agentic-engineering-implementation-audit-pack` audit pack.",
        "",
        "## Purpose",
        "",
        "The purpose is to make audit maintenance repeatable without rewriting audit",
        "conclusions. The snapshot gives maintainers a single generated view of",
        "the complete canonical criterion set, overview categories, automation candidate rows, and",
        "residual gap signals that still require separate Stage 03/04 work.",
        "",
        "## Repository Role",
        "",
        "Use this document as generated audit context only. Active governance remains",
        "in Stage 00, implementation contracts remain in Stage 03, execution evidence",
        "remains in Stage 04, audit conclusions remain in Stage 90 audit reports, and",
        "runtime truth remains in tracked source files such as scripts, workflows,",
        "Compose files, and registry references.",
        "",
        "## Scope",
        "",
        "### In Scope",
        "",
        "- Required criterion-report presence for the agentic engineering implementation audit pack.",
        "- Complete, unique Spec 123 criterion rows and schema/vocabulary validation.",
        "- Required implementation-overview categories.",
        "- `AEA-AUTO-*` automation candidate closure rows.",
        "- Generated evidence surfaces that support audit automation follow-ups.",
        "- Residual gap signals for future Stage 03/04 work.",
        "",
        "### Out of Scope",
        "",
        "- Rewriting audit findings or changing implementation-status conclusions.",
        "- Running security scanners, SBOM tools, Scorecard, signing, attestation, model calls, remote jobs, or CI gates.",
        "- Mutating provider runtime, Docker Compose runtime, branch protection, release assets, secrets, credentials, tokens, raw logs, shell history, or `.env` values.",
        "- Replacing `scripts/validation/report-audit-pack-coverage.sh`; this snapshot complements it with candidate and generated-surface context.",
        "",
        "## Definitions / Facts",
        "",
        f"- **Criterion reports**: {len(REPORT_PREFIX_COUNTS)} criterion-bearing reports are expected under `{PACK}`.",
        "- **Non-criterion pack files**: `README.md` is the index and `implementation-overview.md` is the cross-category overview; neither is counted as a criterion report.",
        "- **Completeness contract**: every expected ID is present exactly once in its declared report/prefix; every row has the exact ten-field schema with non-empty values and allowed state/depth/disposition vocabulary.",
        f"- **Required overview categories**: {len(EXPECTED_OVERVIEW_CATEGORIES)} categories are expected in `implementation-overview.md`.",
        f"- **Required automation candidates**: {len(EXPECTED_CANDIDATES)} `AEA-AUTO-*` rows are expected in `automation-candidates.md`.",
        "- **Closed with residual gap**: candidate has implementation evidence, but its row still names follow-up work that remains outside this generated snapshot.",
        "",
        "## Snapshot Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Criterion reports expected | {len(REPORT_PREFIX_COUNTS)} |",
        f"| Criterion reports present | {sum(1 for report in report_paths if report.is_file())} |",
        "| README indexes | 1 |",
        "| Overview reports | 1 |",
        f"| Criterion rows parsed | {len(all_criteria)} |",
        f"| Unique criterion IDs | {len(set(criterion_ids))} |",
        f"| Overview categories expected | {len(EXPECTED_OVERVIEW_CATEGORIES)} |",
        f"| Overview categories found | {len(overview_categories)} |",
        f"| Automation candidates expected | {len(EXPECTED_CANDIDATES)} |",
        f"| Automation candidates found | {len(candidates)} |",
        f"| Closed candidates with residual gaps | {disposition_counts.get('Closed with residual gap', 0)} |",
        f"| Generator-detected structural failures | {len(failures)} |",
        "",
        "## Implementation Overview Matrix",
        "",
        "| Category | Status |",
        "| --- | --- |",
    ]

    for category in EXPECTED_OVERVIEW_CATEGORIES:
        lines.append(f"| {category} | {overview_categories.get(category, '[missing]')} |")

    lines.extend(
        [
            "",
            "## Audit Report Coverage",
            "",
            "| Criterion Report | File State | Criterion Rows |",
            "| --- | --- | ---: |",
        ]
    )
    for report in report_paths:
        lines.append(f"| {report.name} | {file_state(report)} | {per_report_counts.get(report, 0)} |")

    lines.extend(
        [
            "",
            "## Complete Criterion Matrix",
            "",
            "| Report | Criterion ID | External criterion | Workspace evidence | Status | Depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |",
            "| --- | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |",
        ]
    )

    def escape(value: str) -> str:
        return value.replace("|", "\\|").replace("\n", " ")

    for criterion in all_criteria:
        lines.append(
            "| "
            + " | ".join(
                escape(value)
                for value in [
                    criterion.report.name,
                    criterion.criterion_id,
                    criterion.external_criterion,
                    criterion.workspace_evidence,
                    criterion.raw_status,
                    criterion.enforcement_depth,
                    criterion.disposition,
                    criterion.canonical_owner,
                    criterion.automation_impact,
                    criterion.verification,
                    criterion.confidence,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Normalized Status Counts",
            "",
            "| Normalized Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status in ["Implemented", "Partially Implemented", "Gap / Not Implemented", "Not Applicable", "Unknown / Needs Revalidation", "Other"]:
        lines.append(f"| {status} | {normalized_counts.get(status, 0)} |")

    lines.extend(
        [
            "",
            "## Raw Status Counts",
            "",
            "| Raw Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status, count in sorted(raw_counts.items()):
        lines.append(f"| {status} | {count} |")

    lines.extend(
        [
            "",
            "## Automation Candidate Closure Matrix",
            "",
            "| Candidate ID | Candidate | Disposition |",
            "| --- | --- | --- |",
        ]
    )
    for candidate_id in EXPECTED_CANDIDATES:
        candidate = candidates.get(candidate_id)
        if candidate is None:
            lines.append(f"| {candidate_id} | [missing] | Missing |")
        else:
            lines.append(f"| {candidate.candidate_id} | {candidate.candidate} | {candidate.disposition} |")

    lines.extend(
        [
            "",
            "## Generated Evidence Surface Matrix",
            "",
            "| Surface | Candidate | Script | Output / Evidence | Script State | Output State |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for surface, candidate_id, script_path, output_path in expected_generated_surfaces:
        output_cell = "report-only" if output_path is None else link(output_path)
        output_state = "not-applicable" if output_path is None else file_state(output_path)
        lines.append(
            f"| {surface} | `{candidate_id}` | {link(script_path)} | {output_cell} | "
            f"{file_state(script_path)} | {output_state} |"
        )

    lines.extend(
        [
            "",
            "## Residual Gap Signals",
            "",
            "| Signal | Canonical Routing |",
            "| --- | --- |",
        ]
    )
    if gap_signals:
        for signal in gap_signals:
            lines.append(f"| {signal} | Stage 03 security/QA/automation spec plus Stage 04 plan/task before implementation |")
    else:
        lines.append("| None detected | N/A |")

    lines.extend(
        [
            "",
            "## Source Rules",
            "",
            "- Regenerate this file after changing the agentic engineering implementation audit pack, generated audit/data references, or related automation-candidate evidence.",
            "- Treat this snapshot as consistency evidence, not as the canonical audit conclusion.",
            "- Re-check the underlying audit reports before using this generated summary for prioritization.",
            "- Keep broader vulnerability scanning, SBOM, signing, attestation, Scorecard, and remote jobs in separate approved Stage 03/04 work.",
            "",
            "## Sources",
            "",
            f"- {link(PACK / 'implementation-overview.md', 'implementation overview')} - overview categories and residual cross-category gaps.",
            f"- {link(PACK / 'automation-candidates.md', 'automation candidates')} - `AEA-AUTO-*` candidate rows and closure evidence.",
            f"- {link(PACK / 'security-framework-maturity.md', 'security framework maturity')} - residual security automation gap signals.",
            f"- {link(pathlib.Path('scripts/validation/report-audit-pack-coverage.sh'), 'audit pack coverage report')} - existing implementation-status coverage parser.",
            f"- {link(pathlib.Path('scripts/validation/audit_criterion_contract.py'), 'audit criterion completeness contract')} - shared exact report/ID/schema/cardinality parser used by both audit scripts.",
            f"- {link(pathlib.Path('scripts/validation/generate-audit-implementation-matrix.sh'), 'audit implementation matrix generator')} - generator for this snapshot.",
            "",
            "## Maintenance",
            "",
            "- **Owner**: Documentation Specialist / QA Engineer.",
            "- **Review Cadence**: Review after audit-pack, generated-reference, or automation-candidate changes.",
            "- **Update Trigger**: Run the generator after changing Stage 90 implementation audit reports, generated evidence surfaces, or `AEA-AUTO-*` candidate rows.",
            "",
            "## Related Documents",
            "",
            "- **Governance data index**: [README.md](./README.md)",
            "- **Reference data index**: [../README.md](../README.md)",
            "- **Audit pack index**: [../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)",
            "- **Spec**: [../../../03.specs/118-audit-implementation-matrix-snapshot/spec.md](../../../03.specs/118-audit-implementation-matrix-snapshot/spec.md)",
            "- **Plan**: [../../../04.execution/plans/2026-07-06-audit-implementation-matrix-snapshot.md](../../../04.execution/plans/2026-07-06-audit-implementation-matrix-snapshot.md)",
            "- **Task**: [../../../04.execution/tasks/2026-07-06-audit-implementation-matrix-snapshot.md](../../../04.execution/tasks/2026-07-06-audit-implementation-matrix-snapshot.md)",
            "",
        ]
    )

    return "\n".join(lines), failures


def main() -> int:
    try:
        generated, failures = build_output()
    except AuditCriterionContractError as exc:
        for failure in exc.errors:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    if MODE == "dry-run":
        print(generated, end="")
        return 0

    if MODE == "check":
        if not OUTPUT.is_file():
            print(f"generated audit implementation matrix is missing: {OUTPUT}", file=sys.stderr)
            return 1
        current = OUTPUT.read_text(errors="ignore")
        if current != generated:
            print(f"generated audit implementation matrix is stale: {OUTPUT}", file=sys.stderr)
            return 1
        print("generated audit implementation matrix is fresh")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(generated, encoding="utf-8")
    print(f"wrote {OUTPUT}")
    return 0


raise SystemExit(main())
PY
