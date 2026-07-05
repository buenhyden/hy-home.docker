#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

python3 - "$@" <<'PY'
from __future__ import annotations

import argparse
import pathlib
import re
import sys
from dataclasses import dataclass

PROTOCOL = pathlib.Path("docs/00.agent-governance/rules/documentation-protocol.md")


@dataclass(frozen=True)
class RoutingRow:
    gap_type: str
    owner: str
    rule: str


@dataclass(frozen=True)
class Recommendation:
    label: str
    input_type: str
    display_value: str
    owner: str
    gap_type: str
    rule: str
    confidence: str
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Print advisory canonical-stage routing suggestions for audit, "
            "review, validation, or handoff gaps. This script does not mutate "
            "repository, runtime, remote, or secret state."
        )
    )
    parser.add_argument("--text", action="append", default=[], help="Gap description to classify. May be repeated.")
    parser.add_argument("--stdin", action="store_true", help="Read newline-delimited gap descriptions from stdin.")
    parser.add_argument("--files", nargs="+", default=[], help="File paths related to a gap.")
    parser.add_argument("--list", action="store_true", help="Print the source gap-to-stage routing table.")
    return parser.parse_args(sys.argv[1:])


def read_protocol() -> str:
    if not PROTOCOL.is_file():
        raise SystemExit(f"FAIL: missing routing protocol source: {PROTOCOL}")
    return PROTOCOL.read_text(errors="ignore")


def parse_routing_rows(text: str) -> list[RoutingRow]:
    marker = "### 5.1 Gap-to-Stage Routing"
    if marker not in text:
        raise SystemExit(f"FAIL: missing routing section marker in {PROTOCOL}: {marker}")

    section = text.split(marker, 1)[1]
    rows: list[RoutingRow] = []
    for line in section.splitlines():
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in {"Gap Type", "---"}:
            continue
        if set(cells[0]) == {"-"}:
            continue
        rows.append(RoutingRow(*cells))
    if len(rows) < 10:
        raise SystemExit(f"FAIL: parsed too few routing rows from {PROTOCOL}: {len(rows)}")
    return rows


def row_for_owner(rows: list[RoutingRow], owner_fragment: str) -> RoutingRow:
    for row in rows:
        if owner_fragment in row.owner:
            return row
    raise SystemExit(f"FAIL: routing source missing owner fragment: {owner_fragment}")


def redact_for_display(value: str) -> str:
    sensitive_patterns = [
        r"(?i)(password|passwd|token|secret|private[_-]?key|credential)\s*[:=]\s*\S+",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"\bsk-[A-Za-z0-9_-]{12,}\b",
        r"\bgh[pousr]_[A-Za-z0-9_]{12,}\b",
    ]
    if any(re.search(pattern, value) for pattern in sensitive_patterns):
        return "[redacted-sensitive-input]"
    compact = " ".join(value.split())
    if len(compact) > 160:
        return compact[:157] + "..."
    return compact


PATH_OWNER_RULES: list[tuple[str, str, str]] = [
    ("docs/00.agent-governance/", "docs/00.agent-governance/", "path prefix"),
    ("docs/01.requirements/", "docs/01.requirements/", "path prefix"),
    ("docs/02.architecture/", "docs/02.architecture/", "path prefix"),
    ("docs/03.specs/", "docs/03.specs/", "path prefix"),
    ("docs/04.execution/plans/", "docs/04.execution/plans/", "path prefix"),
    ("docs/04.execution/tasks/", "docs/04.execution/tasks/", "path prefix"),
    ("docs/05.operations/", "docs/05.operations/", "path prefix"),
    ("docs/90.references/", "docs/90.references/", "path prefix"),
    ("docs/98.archive/", "docs/98.archive/", "path prefix"),
    ("docs/99.templates/", "docs/99.templates/", "path prefix"),
    (".github/", "Stage 04 task/audit gap first", "protected CI/remote-adjacent surface"),
    ("infra/", "Stage 04 task/audit gap first", "runtime implementation surface"),
    ("scripts/", "Stage 04 task/audit gap first", "implementation automation surface"),
    ("secrets/", "Stage 04 task/audit gap first", "secret metadata surface"),
    (".claude/", "docs/00.agent-governance/", "provider adapter surface"),
    (".codex/", "docs/00.agent-governance/", "provider adapter surface"),
    (".agents/", "docs/00.agent-governance/", "provider adapter surface"),
]

TEXT_OWNER_RULES: list[tuple[str, tuple[str, ...], str, str]] = [
    ("protected", ("secret", "credential", "token", "private key", "runtime state", "deployment", "remote github", "remote mutation", ".env"), "Stage 04 task/audit gap first", "high"),
    ("governance", ("governance", "provider", "agent", "subagent", "approval", "memory", "model policy", "hook", "permission", "boundary"), "docs/00.agent-governance/", "medium"),
    ("requirements", ("user value", "acceptance criteria", "product intent", "requirement", "prd", "scope gap"), "docs/01.requirements/", "medium"),
    ("architecture", ("architecture", "ard", "adr", "decision", "tradeoff", "quality attribute", "topology"), "docs/02.architecture/", "medium"),
    ("spec", ("interface", "api", "schema", "data model", "service contract", "agent contract", "verification contract", "spec"), "docs/03.specs/", "medium"),
    ("operations", ("operator", "guide", "policy", "runbook", "recovery", "incident", "postmortem", "operational control"), "docs/05.operations/", "medium"),
    ("plan", ("plan", "backlog", "sequencing", "approval gate", "rollback", "milestone", "implementation order"), "docs/04.execution/plans/", "medium"),
    ("task", ("completed work", "validation output", "check result", "deviation", "evidence", "implementation disposition"), "docs/04.execution/tasks/", "medium"),
    ("reference", ("research", "audit", "reference", "glossary", "learning", "llm wiki", "data reference", "snapshot"), "docs/90.references/", "medium"),
    ("archive", ("obsolete", "archive", "tombstone", "implementation-conflicting", "leave the active chain"), "docs/98.archive/", "medium"),
    ("template", ("template", "frontmatter", "lifecycle", "authoring contract", "document shape"), "docs/99.templates/", "medium"),
]


def recommend_path(rows: list[RoutingRow], label: str, path_value: str) -> Recommendation:
    normalized = path_value.removeprefix("./")
    for prefix, owner_fragment, reason in PATH_OWNER_RULES:
        if normalized == prefix.rstrip("/") or normalized.startswith(prefix):
            row = row_for_owner(rows, owner_fragment)
            return Recommendation(
                label=label,
                input_type="path",
                display_value=normalized,
                owner=row.owner,
                gap_type=row.gap_type,
                rule=row.rule,
                confidence="high",
                reason=reason,
            )
    row = row_for_owner(rows, "Stage 04 task/audit gap first")
    return Recommendation(
        label=label,
        input_type="path",
        display_value=normalized,
        owner=row.owner,
        gap_type=row.gap_type,
        rule=row.rule,
        confidence="low",
        reason="unknown path; record an audit/task gap before editing",
    )


def recommend_text(rows: list[RoutingRow], label: str, text_value: str) -> Recommendation:
    normalized = " ".join(text_value.lower().split())
    for _name, keywords, owner_fragment, confidence in TEXT_OWNER_RULES:
        if any(keyword in normalized for keyword in keywords):
            row = row_for_owner(rows, owner_fragment)
            return Recommendation(
                label=label,
                input_type="text",
                display_value=redact_for_display(text_value),
                owner=row.owner,
                gap_type=row.gap_type,
                rule=row.rule,
                confidence=confidence,
                reason="keyword match: " + ", ".join(keyword for keyword in keywords if keyword in normalized),
            )
    row = row_for_owner(rows, "Stage 04 task/audit gap first")
    return Recommendation(
        label=label,
        input_type="text",
        display_value=redact_for_display(text_value),
        owner=row.owner,
        gap_type=row.gap_type,
        rule=row.rule,
        confidence="low",
        reason="ambiguous description; record an audit/task gap before editing",
    )


def print_table(rows: list[RoutingRow]) -> None:
    print("Gap-to-stage routing table")
    print(f"source={PROTOCOL}")
    for index, row in enumerate(rows, start=1):
        print()
        print(f"[{index}] owner={row.owner}")
        print(f"gap_type={row.gap_type}")
        print(f"routing_rule={row.rule}")


def print_recommendations(recommendations: list[Recommendation]) -> None:
    print("Gap routing recommendation")
    print(f"source={PROTOCOL}")
    print(f"inputs_total={len(recommendations)}")
    print("note=Advisory only; update the canonical owner first, then link downstream artifacts.")
    for index, item in enumerate(recommendations, start=1):
        print()
        print(f"[{index}] label={item.label}")
        print(f"input_type={item.input_type}")
        print(f"input={item.display_value}")
        print(f"suggested_owner={item.owner}")
        print(f"matched_gap_type={item.gap_type}")
        print(f"routing_rule={item.rule}")
        print(f"confidence={item.confidence}")
        print(f"reason={item.reason}")


def main() -> int:
    args = parse_args()
    rows = parse_routing_rows(read_protocol())

    if args.list:
        print_table(rows)
        if not args.text and not args.stdin and not args.files:
            return 0

    text_values = list(args.text)
    if args.stdin:
        text_values.extend(line.strip() for line in sys.stdin if line.strip())

    recommendations: list[Recommendation] = []
    for index, value in enumerate(text_values, start=1):
        recommendations.append(recommend_text(rows, f"text-{index}", value))
    for index, value in enumerate(args.files, start=1):
        recommendations.append(recommend_path(rows, f"path-{index}", value))

    if not recommendations:
        if not args.list:
            print("No gap input provided. Use --text, --stdin, --files, or --list.", file=sys.stderr)
            return 2
        return 0

    print_recommendations(recommendations)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
PY
