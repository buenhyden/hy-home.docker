#!/usr/bin/env python3
"""Validate the Spec 137 `carry` remediation-owner requirement.

Spec 137's `Route-3 and disposition-vocabulary amendment` requires every `carry`
record to name the owner of any remediation it does not perform. That requirement
was measured wrongly seven times in a row, each time by a different mechanism and
each time producing output that looked more thorough than the state it replaced:
a count of rows that merely mention an owner; a blanket coverage justification
asserted without per-row evaluation; that same justification propagated to rows
it was never evaluated against; a measurement taken on the ledger while the gate
reads the destination; a resolver that prefixed the governance directory onto
arbitrary tokens; a closure claim that measured field PRESENCE and reported it as
correctness; and a survival sweep whose two halves were a path-token false
positive and a paraphrase-blind zero.

What every one of those attempts lacked was a check that could fail. This module
is that check.

The invariant it enforces is deliberately narrow, because the wide version is not
mechanisable. Deciding which surface a claim's remediation lands on is a semantic
judgement and stays with the author. What a machine CAN verify is that the
judgement, once written, is internally consistent:

    stated_owner == owner_declared_at(cited_scope_file, cited_line)

A record therefore has to cite the File Ownership SSOT row it relies on, and this
module reads that row and compares. It catches a wrong owner written against a
real citation, a citation that points at no ownership row at all, and drift when
a scope table is edited under a record that cites it.

Declared non-coverage, so these are limits rather than silent gaps. This module
does NOT decide whether the cited surface is the right surface for the claim —
that is the judgement it deliberately leaves with the author. It does not check
uniqueness, which Spec 137's `Uniqueness-predicate amendment` defines as survival
after deletion and which needs a reading rather than a scan. Passing here is
necessary, not sufficient.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from dataclasses import dataclass

LEDGER_HEADING = "### Old-claim migration ledger"
DESTINATION_HEADING = "### Gate 3 carried claims"
SCOPES_DIR = "docs/00.agent-governance/scopes"
CODEOWNERS = ".github/CODEOWNERS"
LEDGER_COLUMNS = 11
DISPOSITION_COLUMN = 5
REASON_COLUMN = 9
ANCHOR_COLUMN = 3

OWNERSHIP_HEADING = re.compile(r"^## \d+\. File Ownership")
SCOPE_CITATION = re.compile(r"`scopes/([a-z-]+)\.md:(\d+)`")
CODEOWNERS_CITATION = re.compile(r"`\.github/CODEOWNERS(?::(\d+))?`")
# An owner is a backticked role slug or a backticked @handle introduced by an
# owner phrase. The corpus writes several spellings and interposes wording such
# as "the repository owner" before the backticks, so a bounded run of non-backtick
# text is allowed between the phrase and the name.
OWNER_STATEMENT = re.compile(
    r"[Rr]emediation owner[^`]{0,80}?`(@?[A-Za-z][A-Za-z0-9@_-]*)`"
)
# A destination claim paragraph declares the ledger row it serves with a braced
# marker holding that row's exact Claim anchor cell. A braced form is used rather
# than a sentence-terminated one because several anchors contain a period and a
# period-terminated pattern truncates them; that exact mistake has already been
# made once in this corpus.
LEDGER_ANCHOR_DECLARATION = re.compile(r"\{ledger-anchor:\s*(.+?)\}")


@dataclass(frozen=True)
class Finding:
    code: str
    where: str
    detail: str

    def render(self) -> str:
        return f"FAIL [{self.code}] {self.where}: {self.detail}"


@dataclass(frozen=True)
class Record:
    """One carry record on one surface."""

    surface: str
    where: str
    label: str
    text: str
    keys: tuple[str, ...] = ()

    def owners(self) -> frozenset[str]:
        return frozenset(OWNER_STATEMENT.findall(self.text))

    def operative_owner(self) -> str:
        """The last owner this record names.

        These cells accumulate. A correction appends "Owner re-resolved ... the
        earlier statement is withdrawn" rather than editing the earlier text, so
        a cell routinely names two or three owners of which only the last is
        operative. Comparing the two surfaces by set intersection therefore went
        blind as soon as any cell named more than one: injecting a third,
        disagreeing owner into a synchronised cell produced no finding. The
        operative owner is the last one stated, which is the convention the cells
        already follow in words.
        """

        named = OWNER_STATEMENT.findall(self.text)
        return named[-1] if named else ""


def _read(root: pathlib.Path, relative: str) -> list[str]:
    path = root / relative
    if not path.is_file():
        raise FileNotFoundError(f"required file is missing: {relative}")
    return path.read_text(encoding="utf-8", errors="strict").split("\n")


def _section(lines: list[str], heading: str, stop_prefix: str) -> tuple[int, int]:
    start = None
    for index, line in enumerate(lines):
        if line.startswith(heading):
            start = index
            continue
        if start is not None and index > start and line.startswith(stop_prefix):
            return start, index
    if start is None:
        raise ValueError(f"section not found: {heading}")
    return start, len(lines)


def load_ownership_table(root: pathlib.Path) -> dict[tuple[str, int], str]:
    """Map (scope file stem, 1-based line) -> owner declared on that row."""

    table: dict[tuple[str, int], str] = {}
    scopes = sorted((root / SCOPES_DIR).glob("*.md"))
    for scope in scopes:
        lines = scope.read_text(encoding="utf-8", errors="strict").split("\n")
        inside = False
        for index, line in enumerate(lines):
            if OWNERSHIP_HEADING.match(line):
                inside = True
                continue
            if inside and line.startswith("## "):
                inside = False
            if not inside or not line.startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) < 2 or cells[0].startswith("Path"):
                continue
            if set("".join(cells)) <= set("-: "):
                continue
            owner = cells[1].strip("`").strip()
            if owner:
                table[(scope.stem, index + 1)] = owner
    return table


def load_codeowners_lines(root: pathlib.Path) -> set[int]:
    path = root / CODEOWNERS
    if not path.is_file():
        return set()
    lines = path.read_text(encoding="utf-8", errors="strict").split("\n")
    return {
        index + 1
        for index, line in enumerate(lines)
        if line.strip() and not line.lstrip().startswith("#")
    }


def collect_ledger_records(root: pathlib.Path, task: str) -> list[Record]:
    lines = _read(root, task)
    start, end = _section(lines, LEDGER_HEADING, "### ")
    records: list[Record] = []
    for index in range(start, end):
        line = lines[index]
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != LEDGER_COLUMNS:
            continue
        if cells[DISPOSITION_COLUMN] != "Carry":
            continue
        records.append(
            Record(
                surface="ledger",
                where=f"{task}:{index + 1}",
                label=cells[ANCHOR_COLUMN][:60],
                text=cells[REASON_COLUMN],
                keys=(cells[ANCHOR_COLUMN],),
            )
        )
    return records


def collect_destination_records(root: pathlib.Path, task: str) -> list[Record]:
    """Claim paragraphs in the carried-claims section.

    A claim paragraph opens with a bolded title. Editorial notes in the same
    section open the same way, and nothing in the text distinguishes them, so
    this collector keeps only paragraphs that already carry an owner phrase.

    Corrected 2026-08-19. This docstring previously claimed the caller "sees a
    missing-owner finding either way, which is the safe direction". That was
    false: a paragraph with no owner phrase never becomes a record, so
    CARRY-OWNER-MISSING is unreachable on this surface and the reported
    destination count is a count of owner-bearing paragraphs rather than
    coverage of the carried claims. An independent seat found this. It is the
    same measure-presence-report-correctness move this module's header lists as
    the sixth historical failure, reproduced in the header that lists it.

    The reachability gap is not closed by widening this collector, because an
    editorial note would then be reported as a claim missing an owner. It is
    closed by pairing, which check_pairing below performs: a Carry ledger row
    with no destination paragraph declaring it is reported directly.
    """

    lines = _read(root, task)
    start, end = _section(lines, DESTINATION_HEADING, "### ")
    records: list[Record] = []
    index = start
    while index < end:
        line = lines[index]
        if line.startswith("**") and line.count("**") >= 2:
            title = line.split("**")[1]
            cursor = index + 1
            while cursor < end and lines[cursor].strip() != "":
                cursor += 1
            body = " ".join(lines[index:cursor])
            if OWNER_STATEMENT.search(body):
                declared = tuple(
                    match.strip()
                    for match in LEDGER_ANCHOR_DECLARATION.findall(body)
                )
                records.append(
                    Record(
                        surface="destination",
                        where=f"{task}:{index + 1}",
                        label=title[:60],
                        text=body,
                        keys=declared,
                    )
                )
            index = cursor
            continue
        index += 1
    return records


def check_record(
    record: Record,
    ownership: dict[tuple[str, int], str],
    codeowners_lines: set[int],
) -> list[Finding]:
    findings: list[Finding] = []
    owners = OWNER_STATEMENT.findall(record.text)
    if not owners:
        findings.append(
            Finding(
                "CARRY-OWNER-MISSING", record.where, f"{record.label}: no owner named"
            )
        )
        return findings

    scope_citations = SCOPE_CITATION.findall(record.text)
    codeowners_citations = CODEOWNERS_CITATION.findall(record.text)
    role_owners = [owner for owner in owners if not owner.startswith("@")]
    handle_owners = [owner for owner in owners if owner.startswith("@")]

    # A record may legitimately name two owners when the surface is split across
    # two scope tables. Comparing every owner against every citation would then
    # report a false mismatch, so the test is set-based: each cited ownership row
    # must declare one of the owners the record names, and each named role must be
    # declared by at least one cited row.
    declared_owners: set[str] = set()
    for scope_stem, raw_line in scope_citations:
        line_number = int(raw_line)
        declared = ownership.get((scope_stem, line_number))
        if declared is None:
            findings.append(
                Finding(
                    "CARRY-OWNER-CITATION-UNRESOLVED",
                    record.where,
                    f"{record.label}: cites `scopes/{scope_stem}.md:{line_number}`, "
                    "which is not a File Ownership row",
                )
            )
            continue
        declared_owners.add(declared)

    unbacked = [owner for owner in role_owners if owner not in declared_owners]
    if unbacked and declared_owners:
        findings.append(
            Finding(
                "CARRY-OWNER-MISMATCH",
                record.where,
                f"{record.label}: names {unbacked} but the cited ownership rows "
                f"declare {sorted(declared_owners)}",
            )
        )

    if role_owners and not scope_citations:
        findings.append(
            Finding(
                "CARRY-OWNER-UNCITED",
                record.where,
                f"{record.label}: names role {role_owners} with no "
                "`scopes/<file>.md:<line>` citation to check it against",
            )
        )

    if handle_owners and not codeowners_citations:
        findings.append(
            Finding(
                "CARRY-OWNER-UNCITED",
                record.where,
                f"{record.label}: names {handle_owners} with no `.github/CODEOWNERS` citation",
            )
        )

    for raw_line in codeowners_citations:
        if not raw_line:
            continue
        if int(raw_line) not in codeowners_lines:
            findings.append(
                Finding(
                    "CARRY-OWNER-CITATION-UNRESOLVED",
                    record.where,
                    f"{record.label}: cites `.github/CODEOWNERS:{raw_line}`, "
                    "which is not an active rule line",
                )
            )
    return findings


def check_pairing(records: list[Record]) -> list[Finding]:
    """Pair each Carry ledger row with the destination paragraph that serves it.

    Gate 2 reads the destination, and the two surfaces state the same claim
    twice. Nothing in the data joined them: a ledger row is keyed by its Claim
    anchor and a destination paragraph opens with unrelated prose, so no check
    could compare what the two surfaces say. Every comparison was therefore made
    by eye, and by eye the owner agreed on both surfaces while an independent
    seat found 21 disagreements, 17 of them naming a different owner.

    This function supplies the join. A destination paragraph declares the ledger
    row it serves, and the owners the two surfaces name must then agree.
    """

    ledger = [record for record in records if record.surface == "ledger"]
    destination = [record for record in records if record.surface == "destination"]
    # A paragraph may serve several rows: three rows state one Gemini claim from
    # three old leaves, so the marker is collected as a list rather than a scalar.
    by_key: dict[str, Record] = {}
    for record in destination:
        for key in record.keys:
            by_key[key] = record
    ledger_keys = {key for item in ledger for key in item.keys}

    findings: list[Finding] = []
    for record in destination:
        if not record.keys:
            findings.append(
                Finding(
                    "CARRY-PAIR-UNDECLARED",
                    record.where,
                    f"{record.label}: declares no ledger row; add a "
                    "`{ledger-anchor: <exact Claim anchor cell>}` marker",
                )
            )
            continue
        for key in record.keys:
            if key not in ledger_keys:
                findings.append(
                    Finding(
                        "CARRY-PAIR-ORPHAN",
                        record.where,
                        f"{record.label}: declares ledger anchor {key!r}, "
                        "which matches no Carry row",
                    )
                )

    for record in ledger:
        partner = by_key.get(record.keys[0]) if record.keys else None
        if partner is None:
            findings.append(
                Finding(
                    "CARRY-PAIR-MISSING",
                    record.where,
                    f"{record.label}: no destination paragraph declares this row",
                )
            )
            continue
        # Each surface's operative owner must be named by the other. The test is
        # deliberately not a set intersection: these cells accumulate withdrawn
        # owners, and an intersection passes whenever any historical owner
        # happens to match.
        mine, theirs = record.owners(), partner.owners()
        my_operative, their_operative = record.operative_owner(), partner.operative_owner()
        if my_operative and theirs and my_operative not in theirs:
            findings.append(
                Finding(
                    "CARRY-OWNER-CROSS-SURFACE",
                    record.where,
                    f"{record.label}: the ledger's operative owner {my_operative!r} "
                    f"is named nowhere in the destination at {partner.where}, "
                    f"which names {sorted(theirs)}",
                )
            )
        elif their_operative and mine and their_operative not in mine:
            findings.append(
                Finding(
                    "CARRY-OWNER-CROSS-SURFACE",
                    partner.where,
                    f"{partner.label}: the destination's operative owner "
                    f"{their_operative!r} is named nowhere in the ledger row at "
                    f"{record.where}, which names {sorted(mine)}",
                )
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the Spec 137 carry remediation-owner requirement."
    )
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument(
        "--task",
        default="docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md",
        help="owning Task that holds the ledger and the carried-claims section",
    )
    parser.add_argument(
        "--surface",
        choices=("ledger", "destination", "both"),
        default="both",
        help="which surface to check; the gate reads the destination",
    )
    arguments = parser.parse_args()
    root = pathlib.Path(arguments.root).resolve()

    try:
        ownership = load_ownership_table(root)
        codeowners_lines = load_codeowners_lines(root)
        records: list[Record] = []
        if arguments.surface in ("ledger", "both"):
            records += collect_ledger_records(root, arguments.task)
        if arguments.surface in ("destination", "both"):
            records += collect_destination_records(root, arguments.task)
    except (FileNotFoundError, ValueError) as error:
        print(f"carry-owner: ERROR {error}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    for record in records:
        findings += check_record(record, ownership, codeowners_lines)
    if arguments.surface == "both":
        findings += check_pairing(records)

    for finding in findings:
        print(finding.render())

    ledger_count = sum(1 for record in records if record.surface == "ledger")
    destination_count = len(records) - ledger_count
    print(
        "carry-owner contract\n"
        f"ownership_rows={len(ownership)}\n"
        f"ledger_records={ledger_count}\n"
        f"destination_records={destination_count}\n"
        f"failures={len(findings)}"
    )
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
