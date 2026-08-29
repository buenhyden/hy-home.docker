#!/usr/bin/env python3
"""Validate the Spec 137 gate-2 claim-review contract.

Ported to the migrated document layout on 2026-08-29 from
`agentic-research-delta-revalidation`, where it lived inside
`carry_owner_contract.py`. That branch diverged before the governance migration
and every document path it names was dissolved, so the branch could not be
merged; this module is the part of it worth keeping, rebased rather than lost.

What it is for. Gate 2 quantifies over the retained, corrected, superseded and
carried claims in the owning Task's `Old-claim migration ledger`, and asks that
each resolve to a reviewed destination. Whether a claim really lands on the
surface it names is a reading, and stays with a review seat. What a machine can
hold is the *evidence* of that reading: which rows were assigned to which seat,
in which round, against which exact bytes, and what verdict came back. This
module enforces that record and nothing wider.

It reads three sections the Task owns -- `Gate 2 review manifest`, its
`evidence envelope`, and its `receipts` -- and checks them as a closed schema:
exact key sets, sorted and unique arrays, canonical JSON digests, git blob OIDs
pinned to a bootstrap commit, and per-record verdict basis. Unknown keys are
rejected rather than ignored, because a record that can carry an unread field is
a record that can carry a forged one.

It FAILS CLOSED when the manifest is absent. That is the current state and it is
the correct one: the sections have never been authored, so the contract has no
subject and says so, rather than reporting a pass over an empty set. This is the
same defect class the gate-4 scanner showed on 2026-08-29, where a scan target
that named nothing read green; a check whose subject is missing must fail, not
pass.

Declared non-coverage. It does not decide whether a destination is the right one
for a claim, does not evaluate the survival predicate, and does not settle a
verdict. Passing here is necessary, not sufficient.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from typing import Any, Callable

TASK_PATH = "docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md"

LEDGER_HEADING = "### Old-claim migration ledger"
DESTINATION_HEADING = "### Gate 3 carried claims"
LEDGER_COLUMNS = 11
DISPOSITION_COLUMN = 5
REASON_COLUMN = 9
ANCHOR_COLUMN = 3

LEDGER_HEADERS = (
    "Old path",
    "Old commit",
    "Old blob",
    "Claim anchor",
    "Claim summary",
    "Disposition",
    "Evidence state",
    "New path",
    "New anchor",
    "Correction / omission reason",
    "Review verdict",
)
SUBJECT_KEYS = (
    "old_path",
    "old_commit",
    "old_blob",
    "claim_anchor",
    "claim_summary",
    "disposition",
    "evidence_state",
    "new_path",
    "new_anchor",
    "correction_or_omission_reason",
)
DISPOSITIONS = frozenset(("Retain", "Supersede", "Correct", "Carry", "Omit"))
GATE2_DISPOSITIONS = frozenset(("Retain", "Correct", "Carry"))
MANIFEST_HEADING = "### Gate 2 review manifest"
ENVELOPE_HEADING = "### Gate 2 review evidence envelope"
RECEIPTS_HEADING = "### Gate 2 review receipts"
BOOTSTRAP_COMMIT = "7fbedcc10a5f5c07bc04d1346c6498ad38bc526f"
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
OID_RE = re.compile(r"^[0-9a-f]{40}$")
RECORD_ID_RE = re.compile(r"^g2r-[0-9]{6}$")
BATCH_ID_RE = re.compile(r"^gate2-batch-v1:[0-9]{3}:sha256:[0-9a-f]{64}$")
SAFE_PATH_RE = re.compile(r"^(?!/)(?!.*(?:^|/)\.\.(?:/|$))(?!.*\\)[^\x00-\x1f]+$")
ASCII_TRIM = "\t\n\v\f\r "

MANIFEST_KEYS = frozenset(("schema", "bootstrap_commit", "records", "identity_transitions"))
MANIFEST_RECORD_KEYS = frozenset(
    ("record_id", "status", "identity_revision", "claim_key_v1", "subject_digest_v1")
)
ASSIGNMENT_KEYS = frozenset(
    ("schema", "review_round", "reviewed_commit", "manifest_digest_v1", "ledger_digest_v1", "population_digest_v1", "batches")
)
BATCH_KEYS = frozenset(("ordinal", "batch_id", "reviewer_identity", "record_ids", "claim_keys"))
ASSIGNMENT_REVIEWER_KEYS = frozenset(("agent_id", "seat", "task_id"))
REPORT_REVIEWER_KEYS = frozenset(("agent_id", "seat", "task_id", "report_path"))
CANDIDATE_KEYS = frozenset(
    (
        "schema", "review_round", "manifest_digest_v1", "ledger_digest_v1", "population_digest_v1",
        "record_id", "identity_revision", "claim_key_v1", "subject_digest_v1",
        "destination", "destination_digest_v1", "reviewer_identity", "reviewed_commit",
        "batch_id", "reviewer_body", "verdict", "basis", "finding_ids",
        "assignment_digest_v1", "candidate_digest_v1",
    )
)
DESTINATION_KEYS = frozenset(("kind", "path", "anchor_locator", "blob_oid", "content_digest_v1"))
BASIS_KEYS = frozenset(
    (
        "source_fidelity", "destination_resolution", "destination_substance",
        "correction_explicit", "correction_evidence", "current_repository_verification",
        "carry_owner_alignment", "carry_survival_predicate", "evidence_freshness",
    )
)
FINAL_KEYS = frozenset(
    ("schema", "review_round", "assignment_digest_v1", "batch_id", "reviewer_identity", "reviewed_commit", "candidates", "batch_verdict", "finding_ids")
)
REPORT_ENTRY_KEYS = frozenset(
    ("report_path", "report_bytes_digest_v1", "reviewer_body_digest_v1", "reviewer_final_digest_v1", "reviewer_final")
)
ENVELOPE_KEYS = frozenset(("schema", "review_round", "assignment", "assignment_digest_v1", "reports", "evidence_envelope_digest_v1"))
SET_ASSIGNMENT_KEYS = frozenset(
    ("schema", "review_round", "reviewed_commit", "row_assignment_digest_v1", "evidence_envelope_digest_v1", "members", "reviewers", "set_assignment_digest_v1")
)
SET_MEMBER_KEYS = frozenset(
    ("batch_id", "report_path", "report_bytes_digest_v1", "reviewer_final_digest_v1", "record_ids", "candidate_digests_v1")
)
SET_REVIEWER_KEYS = frozenset(("review_kind", "agent_id", "role", "seat", "task_id", "report_path"))
ATTESTATION_KEYS = frozenset(
    (
        "schema", "review_round", "review_kind", "reviewer_identity", "reviewed_commit",
        "row_assignment_digest_v1", "evidence_envelope_digest_v1", "set_assignment_digest_v1",
        "members", "reviewer_body", "reviewer_body_digest_v1", "basis", "verdict",
        "critical", "important", "minor", "finding_ids", "attestation_digest_v1",
    )
)
SET_BASIS_KEYS = frozenset(
    ("assignment_integrity", "envelope_integrity", "member_identity", "batch_exact_once", "population_exact_once", "candidate_integrity", "report_integrity", "reviewer_independence")
)
SET_AUTHORITY_KEYS = frozenset(("schema", "review_round", "set_assignment", "set_assignment_digest_v1", "attestations", "set_authority_digest_v1"))
ATTESTATION_WRAPPER_KEYS = frozenset(("review_kind", "report_path", "report_bytes_digest_v1", "attestation"))
RECEIPTS_KEYS = frozenset(("schema", "review_round", "p4_set_authority", "receipts"))
RECEIPT_KEYS = frozenset(
    (
        "schema", "review_round", "manifest_digest_v1", "ledger_digest_v1", "population_digest_v1",
        "record_id", "identity_revision", "claim_key_v1", "subject_digest_v1",
        "destination", "destination_digest_v1", "reviewer_identity", "reviewed_commit",
        "batch_id", "reviewer_body", "verdict", "basis", "finding_ids",
        "assignment_digest_v1", "candidate_digest_v1", "report_bytes_digest_v1",
        "reviewer_body_digest_v1", "reviewer_final_digest_v1", "evidence_envelope_digest_v1",
        "p4_set_authority_digest_v1", "receipt_digest_v1",
    )
)
TERMINAL_VERDICT_RE = re.compile(
    r"^SETTLED \{gate2-receipt=(sha256:[0-9a-f]{64});"
    r"gate2-set-authority=(sha256:[0-9a-f]{64})\}$"
)

# An owner is a backticked role slug or a backticked @handle introduced by an
# owner phrase. The corpus writes several spellings and interposes wording such
# as "the repository owner" before the backticks, so a bounded run of non-backtick
# text is allowed between the phrase and the name.
# Owners are introduced two ways in this corpus. The original phrasing is
# "Remediation owner ... `X`". Superseding corrections were later written as
# "Owner is `X` under the ... rule", and matching only the first phrasing made
# every such correction invisible: `operative_owner()` returned the withdrawn
# owner while the correction sat in the same cell. An independent seat found
# that on two rows in 2026-08-20.
OWNER_STATEMENT = re.compile(
    r"(?:[Rr]emediation owner|\bOwner is)[^`]{0,80}?`(@?[A-Za-z][A-Za-z0-9@_-]*)`"
)
# A destination claim paragraph declares the ledger row it serves with a braced
# marker holding that row's exact Claim anchor cell. A braced form is used rather
# than a sentence-terminated one because several anchors contain a period and a
# period-terminated pattern truncates them; that exact mistake has already been
# made once in this corpus.
# The Uniqueness-predicate amendment defines uniqueness as survival after the
# retiring pack is deleted, and voids the intra-document test outright: whether
# another row in the same ledger, or another paragraph in the same section,
# carries the claim does not bear on the gate. Gate 2 reads the destination, so
# the destination is where the survival verdict has to be stated.


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
    survival: str = ""

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


@dataclass(frozen=True)
class LedgerRow:
    """One strictly decoded migration-ledger row."""

    line_number: int
    values: tuple[str, ...]

    def as_subject(self) -> dict[str, str]:
        return dict(zip(SUBJECT_KEYS, self.values[:10], strict=True))

    @property
    def disposition(self) -> str:
        return self.values[5]

    @property
    def claim_key_v1(self) -> str:
        subject = self.as_subject()
        return canonical_digest(
            {
                "claim_anchor": subject["claim_anchor"],
                "claim_summary": subject["claim_summary"],
                "old_blob": subject["old_blob"],
                "old_commit": subject["old_commit"],
                "old_path": subject["old_path"],
            }
        )

    @property
    def subject_digest_v1(self) -> str:
        return canonical_digest(self.as_subject())


@dataclass(frozen=True)
class Gate2Result:
    ledger_records: int
    population_records: int
    settled: int
    held: int
    findings: tuple[Finding, ...]
    publication_bytes: bytes = b""
    exit_status: int = 1


class Gate2ContractError(ValueError):
    """A fail-closed Gate 2 contract violation."""

    def __init__(self, message: str, *, code: str = "GATE2-CONTRACT") -> None:
        super().__init__(message)
        self.code = code


def _gate2_result(
    task_path: str,
    ledger_records: int,
    population_records: int,
    settled: int,
    held: int,
    findings: tuple[Finding, ...],
) -> Gate2Result:
    """Compose the immutable public result before the final HEAD probe."""
    if findings:
        lines = [finding.render() for finding in findings]
        lines.extend(
            (
                "gate2 claim-review contract",
                f"ledger_records={ledger_records}",
                f"population_records={population_records}",
                f"settled={settled}",
                f"held={held}",
                f"failures={len(findings)}",
            )
        )
        publication = ("\n".join(lines) + "\n").encode("utf-8")
        exit_status = 1
    else:
        publication = (
            "gate2 claim-review contract\n"
            f"ledger_records={ledger_records}\n"
            f"population_records={population_records}\n"
            f"settled={settled}\n"
            f"held={held}\n"
            "failures=0\n"
        ).encode("utf-8")
        exit_status = 0
    return Gate2Result(
        ledger_records,
        population_records,
        settled,
        held,
        findings,
        publication,
        exit_status,
    )


def normalize_cell(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip(ASCII_TRIM))


def canonical_json(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, OverflowError) as error:
        raise Gate2ContractError(f"value is not canonical JSON: {error}") from error


def raw_digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def canonical_digest(value: Any, *, omit: str | None = None) -> str:
    if omit is not None:
        if not isinstance(value, dict) or omit not in value:
            raise Gate2ContractError(f"digest source does not contain {omit!r}")
        value = {key: item for key, item in value.items() if key != omit}
    return raw_digest(canonical_json(value))


def _duplicate_rejecting_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise Gate2ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_object(raw: str) -> dict[str, Any]:
    def reject_constant(value: str) -> None:
        raise Gate2ContractError(f"non-finite JSON number: {value}")

    def reject_nonfinite_float(value: str) -> float:
        parsed = float(value)
        if not math.isfinite(parsed):
            raise Gate2ContractError(f"non-finite JSON number: {value}")
        return parsed

    try:
        decoded = json.loads(
            raw,
            object_pairs_hook=_duplicate_rejecting_object,
            parse_constant=reject_constant,
            parse_float=reject_nonfinite_float,
        )
    except (json.JSONDecodeError, UnicodeError, OverflowError, TypeError, ValueError) as error:
        raise Gate2ContractError(f"invalid JSON: {error}") from error
    if not isinstance(decoded, dict):
        raise Gate2ContractError("canonical JSON block must contain one object")
    if canonical_json(decoded).decode("utf-8") != raw:
        raise Gate2ContractError("JSON object is not compact canonical JSON")
    return decoded


def _assert_exact_keys(value: Any, keys: frozenset[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise Gate2ContractError(f"{label} must be an object")
    actual = frozenset(value)
    if actual != keys:
        raise Gate2ContractError(
            f"{label} keys differ: missing={sorted(keys - actual)} extra={sorted(actual - keys)}"
        )
    return value


def _assert_sorted_unique(values: Any, label: str) -> list[Any]:
    if not isinstance(values, list):
        raise Gate2ContractError(f"{label} must be an array")
    if len({type(item) for item in values}) > 1:
        raise Gate2ContractError(f"{label} contains mixed member types")
    encoded = [canonical_json(item) for item in values]
    if encoded != sorted(encoded):
        raise Gate2ContractError(f"{label} is not canonically ordered")
    if len(values) != len(set(encoded)):
        raise Gate2ContractError(f"{label} contains duplicates")
    return values


def _object_array(values: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        raise Gate2ContractError(f"{label} must be an array")
    if any(not isinstance(item, dict) for item in values):
        raise Gate2ContractError(f"{label} members must be objects")
    return values


def _assert_round(value: Any, label: str) -> int:
    if type(value) is not int or value != 1:
        raise Gate2ContractError(f"{label} must be the non-boolean integer 1")
    return value


def _assert_digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or not DIGEST_RE.fullmatch(value):
        raise Gate2ContractError(f"{label} is not a canonical SHA-256 digest")
    return value


def _assert_string(
    value: Any,
    label: str,
    *,
    pattern: re.Pattern[str] | None = None,
    nonempty: bool = True,
) -> str:
    if not isinstance(value, str) or (nonempty and not value):
        raise Gate2ContractError(f"{label} must be a nonempty string")
    if pattern is not None and pattern.fullmatch(value) is None:
        raise Gate2ContractError(f"{label} has invalid syntax")
    return value


def _assert_string_array(
    values: Any,
    label: str,
    *,
    pattern: re.Pattern[str] | None = None,
    ordered: bool = False,
) -> list[str]:
    if not isinstance(values, list):
        raise Gate2ContractError(f"{label} must be an array")
    if any(not isinstance(item, str) or not item for item in values):
        raise Gate2ContractError(f"{label} members must be nonempty strings")
    if pattern is not None and any(pattern.fullmatch(item) is None for item in values):
        raise Gate2ContractError(f"{label} contains an invalid member")
    if ordered and values != sorted(values):
        raise Gate2ContractError(f"{label} is not canonically ordered")
    if len(values) != len(set(values)):
        raise Gate2ContractError(f"{label} contains duplicates")
    return values


def _fence_mask(lines: list[str]) -> list[bool]:
    mask = [False] * len(lines)
    active: tuple[str, int] | None = None
    for index, line in enumerate(lines):
        if active is None:
            match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
            if match:
                token = match.group(1)
                active = (token[0], len(token))
                mask[index] = True
            continue
        mask[index] = True
        character, width = active
        if re.fullmatch(rf" {{0,3}}{re.escape(character)}{{{width},}} *", line):
            active = None
    if active is not None:
        raise Gate2ContractError("unclosed Markdown fence")
    return mask


def _unique_section(lines: list[str], heading: str) -> tuple[int, int]:
    mask = _fence_mask(lines)
    matches = [index for index, line in enumerate(lines) if not mask[index] and line == heading]
    if len(matches) != 1:
        raise Gate2ContractError(f"expected one {heading!r} heading, found {len(matches)}")
    start = matches[0] + 1
    end = len(lines)
    for index in range(start, len(lines)):
        if not mask[index] and re.match(r"^#{1,3}(?: |$)", lines[index]):
            end = index
            break
    return start, end


def split_gfm_row(line: str) -> list[str]:
    """Decode one GFM row using the Plan's escaped-pipe parity rule."""

    cells: list[str] = []
    current: list[str] = []
    for character in line:
        if character != "|":
            current.append(character)
            continue
        backslashes = 0
        for prior in reversed(current):
            if prior != "\\":
                break
            backslashes += 1
        if backslashes % 2:
            current.pop()
            current.append("|")
        else:
            cells.append("".join(current))
            current = []
    cells.append("".join(current))
    if len(cells) < 3 or normalize_cell(cells[0]) or normalize_cell(cells[-1]):
        raise Gate2ContractError("table row requires unescaped leading/trailing delimiters")
    return [normalize_cell(cell) for cell in cells[1:-1]]


def parse_ledger_text(text: str) -> list[LedgerRow]:
    if "\r" in text:
        raise Gate2ContractError("Task must use LF line endings")
    lines = text.split("\n")
    start, end = _unique_section(lines, LEDGER_HEADING)
    header_matches: list[tuple[int, list[str]]] = []
    for index in range(start, end):
        line = lines[index]
        if not line.startswith("|"):
            continue
        try:
            cells = split_gfm_row(line)
        except Gate2ContractError:
            continue
        if tuple(cells) == LEDGER_HEADERS:
            header_matches.append((index, cells))
    if len(header_matches) != 1:
        raise Gate2ContractError(f"expected one exact ledger header, found {len(header_matches)}")
    header_index, _ = header_matches[0]
    for competing in range(start, header_index):
        if lines[competing].lstrip().startswith("|"):
            raise Gate2ContractError(f"competing table-like line at {competing + 1}")
    if header_index + 1 >= end:
        raise Gate2ContractError("ledger delimiter row is missing")
    delimiter = split_gfm_row(lines[header_index + 1])
    if len(delimiter) != len(LEDGER_HEADERS) or any(
        re.fullmatch(r":?-{3,}:?", cell) is None for cell in delimiter
    ):
        raise Gate2ContractError("ledger delimiter row is malformed")

    records: list[LedgerRow] = []
    index = header_index + 2
    while index < end and lines[index].strip(ASCII_TRIM):
        line = lines[index]
        if not line.startswith("|"):
            raise Gate2ContractError(f"malformed ledger row at line {index + 1}")
        cells = split_gfm_row(line)
        if len(cells) != len(LEDGER_HEADERS):
            raise Gate2ContractError(
                f"ledger row {index + 1} has {len(cells)} cells, expected {len(LEDGER_HEADERS)}"
            )
        if any(not cells[column] for column in (0, 1, 2, 3, 4, 5)):
            raise Gate2ContractError(f"ledger row {index + 1} has an empty identity/disposition cell")
        if cells[5] not in DISPOSITIONS:
            raise Gate2ContractError(f"ledger row {index + 1} has unknown disposition {cells[5]!r}")
        records.append(LedgerRow(index + 1, tuple(cells)))
        index += 1
    for trailing in range(index, end):
        if lines[trailing].lstrip().startswith("|"):
            raise Gate2ContractError(f"competing table-like line at {trailing + 1}")
    if not records:
        raise Gate2ContractError("ledger has no data rows")
    return records


def extract_json_block(text: str, heading: str, schema: str) -> dict[str, Any]:
    lines = text.split("\n")
    start, end = _unique_section(lines, heading)
    openings = [index for index in range(start, end) if lines[index] == "```json"]
    if len(openings) != 1:
        raise Gate2ContractError(f"{heading}: expected one exact JSON fence")
    opening = openings[0]
    closings = [index for index in range(opening + 1, end) if lines[index] == "```"]
    if len(closings) != 1:
        raise Gate2ContractError(f"{heading}: expected one exact closing fence")
    closing = closings[0]
    if any(line.strip() for line in lines[start:opening]) or any(
        line.strip() for line in lines[closing + 1 : end]
    ):
        raise Gate2ContractError(f"{heading}: prefix or suffix content is forbidden")
    if any(re.match(r"^ {0,3}(`{3,}|~{3,})", line) for line in lines[opening + 1 : closing]):
        raise Gate2ContractError(f"{heading}: nested or competing fence")
    raw = "\n".join(lines[opening + 1 : closing])
    value = strict_json_object(raw)
    if value.get("schema") != schema:
        raise Gate2ContractError(f"{heading}: wrong schema")
    occurrences = sum(line.count(schema) for line in lines)
    if occurrences != 1:
        raise Gate2ContractError(f"{heading}: competing schema occurrence")
    return value


def validate_manifest(
    manifest: dict[str, Any], rows: list[LedgerRow], *, enforce_frozen_count: bool = True
) -> tuple[dict[str, dict[str, Any]], str, str, str]:
    _assert_exact_keys(manifest, MANIFEST_KEYS, "manifest")
    if manifest["schema"] != "gate2-review-manifest/v1":
        raise Gate2ContractError("manifest schema mismatch")
    if manifest["bootstrap_commit"] != BOOTSTRAP_COMMIT:
        raise Gate2ContractError("manifest bootstrap commit mismatch")
    if manifest["identity_transitions"] != []:
        raise Gate2ContractError("static v1 requires empty identity_transitions")
    records = _object_array(manifest["records"], "manifest records")
    if enforce_frozen_count and (len(records) != 253 or len(rows) != 253):
        raise Gate2ContractError("static v1 requires exactly 253 manifest and ledger rows")
    for record in records:
        _assert_exact_keys(record, MANIFEST_RECORD_KEYS, "manifest record")
        _assert_string(record["record_id"], "manifest record_id", pattern=RECORD_ID_RE)
        _assert_string(record["status"], "manifest status")
        if type(record["identity_revision"]) is not int:
            raise Gate2ContractError("manifest identity_revision must be an integer")
        _assert_digest(record["claim_key_v1"], "manifest claim key")
        _assert_digest(record["subject_digest_v1"], "manifest subject digest")
    record_ids = [record["record_id"] for record in records]
    if record_ids != sorted(record_ids):
        raise Gate2ContractError("manifest records are not ordered by record_id")
    if len(record_ids) != len(set(record_ids)):
        raise Gate2ContractError("duplicate manifest record_id")
    expected_ids = [f"g2r-{index:06d}" for index in range(1, len(records) + 1)]
    if record_ids != expected_ids:
        raise Gate2ContractError("manifest record IDs are not the contiguous bootstrap sequence")

    live_by_key = {row.claim_key_v1: row for row in rows}
    if len(live_by_key) != len(rows):
        raise Gate2ContractError("ledger claim-key collision")
    by_id: dict[str, dict[str, Any]] = {}
    for record in records:
        record_id = record["record_id"]
        if (
            record["status"] != "ACTIVE"
            or record["identity_revision"] != 1
        ):
            raise Gate2ContractError("static v1 requires ACTIVE revision 1")
        row = live_by_key.get(record["claim_key_v1"])
        if row is None:
            raise Gate2ContractError(f"orphan manifest record {record_id}")
        if record["subject_digest_v1"] != row.subject_digest_v1:
            raise Gate2ContractError(f"stale subject digest for {record_id}")
        by_id[record_id] = record
    if {record["claim_key_v1"] for record in records} != set(live_by_key):
        raise Gate2ContractError("manifest/ledger bijection mismatch")
    expected_key_order = sorted(live_by_key)
    if [record["claim_key_v1"] for record in records] != expected_key_order:
        raise Gate2ContractError("manifest bootstrap ID/key assignment mismatch")

    manifest_digest = canonical_digest(manifest)
    projection = [
        {
            "record_id": record["record_id"],
            "identity_revision": record["identity_revision"],
            "claim_key_v1": record["claim_key_v1"],
            "subject_digest_v1": record["subject_digest_v1"],
        }
        for record in records
    ]
    ledger_digest = canonical_digest(projection)
    disposition_by_key = {row.claim_key_v1: row.disposition for row in rows}
    population_projection = sorted(
        (
            item
            for item in projection
            if disposition_by_key[item["claim_key_v1"]] in GATE2_DISPOSITIONS
        ),
        key=lambda item: item["claim_key_v1"],
    )
    population_digest = canonical_digest(population_projection)
    return by_id, manifest_digest, ledger_digest, population_digest


def _safe_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or not SAFE_PATH_RE.fullmatch(value):
        raise Gate2ContractError(f"{label} is not a safe repository-relative path")
    return value


class _Gate2Git:
    """One shell-free, literal-snapshot Git execution boundary per invocation."""

    def __init__(self, root: pathlib.Path, pinned_head: str) -> None:
        if not OID_RE.fullmatch(pinned_head):
            raise Gate2ContractError("PINNED_HEAD is not a lowercase full commit OID")
        self.root = root
        self.pinned_head = pinned_head
        self.reviewed_commit: str | None = None
        self._cache: dict[tuple[str, str | None, str | None], bytes] = {}

    def bind_reviewed_commit(self, commit: str) -> None:
        if not OID_RE.fullmatch(commit):
            raise Gate2ContractError("reviewed commit is invalid")
        if self.reviewed_commit not in (None, commit):
            raise Gate2ContractError("reviewed commit was reassigned")
        self.reviewed_commit = commit

    @staticmethod
    def _execute(root: pathlib.Path, argv: list[str], operation: str) -> bytes:
        try:
            process = subprocess.Popen(
                argv,
                cwd=root,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
            )
        except OSError as error:
            raise Gate2ContractError(f"Git operation could not start: {operation}") from error
        try:
            stdout, _stderr = process.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.communicate(timeout=1)
            except subprocess.TimeoutExpired:
                if process.poll() is None:
                    process.kill()
                process.communicate()
            raise Gate2ContractError(
                f"GATE2_GIT_TIMEOUT operation={operation}", code="GATE2_GIT_TIMEOUT"
            )
        if process.returncode:
            raise Gate2ContractError(f"Git operation failed: {operation}")
        return stdout

    @classmethod
    def start(cls, root: pathlib.Path) -> "_Gate2Git":
        raw = cls._execute(
            root, ["git", "rev-parse", "--verify", "HEAD^{commit}"], "head-probe-initial"
        )
        try:
            pinned = raw.decode("utf-8", errors="strict").strip()
        except UnicodeDecodeError as error:
            raise Gate2ContractError("initial HEAD probe is not UTF-8") from error
        if not OID_RE.fullmatch(pinned):
            raise Gate2ContractError("initial HEAD probe did not return one full commit OID")
        return cls(root, pinned)

    def probe_head(self, operation: str) -> str:
        raw = self._execute(
            self.root,
            ["git", "rev-parse", "--verify", "HEAD^{commit}"],
            operation,
        )
        try:
            value = raw.decode("utf-8", errors="strict").strip()
        except UnicodeDecodeError as error:
            raise Gate2ContractError("HEAD freshness probe is not UTF-8") from error
        if not OID_RE.fullmatch(value):
            raise Gate2ContractError("HEAD freshness probe did not return one full commit OID")
        return value

    def run(
        self, operation: str, commit: str | None = None, path: str | None = None
    ) -> bytes:
        if commit is not None and not OID_RE.fullmatch(commit):
            raise Gate2ContractError(f"{operation} commit is invalid")
        if path is not None:
            _safe_path(path, f"{operation} path")
        if operation == "ancestor":
            if commit is None or path is not None:
                raise Gate2ContractError("ancestor operation shape is invalid")
            argv = ["git", "merge-base", "--is-ancestor", commit, self.pinned_head]
        elif operation == "show":
            if commit is None or path is None:
                raise Gate2ContractError("show operation shape is invalid")
            if commit not in (self.pinned_head, self.reviewed_commit):
                raise Gate2ContractError("show commit is not a frozen snapshot")
            argv = ["git", "show", commit + ":" + path]
        elif operation == "tracked":
            if commit != self.pinned_head or path is None:
                raise Gate2ContractError("tracked operation requires PINNED_HEAD and path")
            argv = [
                "git", "ls-tree", "-z", "--full-tree", "--name-only",
                self.pinned_head, "--", path,
            ]
        elif operation == "oid":
            if commit is None or path is None:
                raise Gate2ContractError("oid operation shape is invalid")
            if commit not in (self.pinned_head, self.reviewed_commit):
                raise Gate2ContractError("oid commit is not a frozen snapshot")
            argv = ["git", "rev-parse", commit + ":" + path]
        elif operation == "tree":
            if commit is None or path is not None:
                raise Gate2ContractError("tree operation shape is invalid")
            argv = ["git", "rev-parse", commit + "^{tree}"]
        else:
            raise Gate2ContractError(f"unknown Git operation: {operation}")
        key = (operation, commit, path)
        if key not in self._cache:
            self._cache[key] = self._execute(self.root, argv, operation)
        return self._cache[key]


class _Gate2Invocation:
    def __init__(self, root: pathlib.Path, task_path: str, git: _Gate2Git) -> None:
        self.root = root
        self.task_path = _safe_path(task_path, "Task path")
        self.git = git
        self._working_files: dict[str, bytes] = {}
        self._task_states: dict[str, tuple[bytes, str, list[LedgerRow], dict[str, Any] | None, dict[str, bytes]]] = {}
        self._destinations: set[str] = set()

    def working_file(self, path: str) -> bytes:
        path = _safe_path(path, "working-tree path")
        if path not in self._working_files:
            tracked = self.git.run("tracked", self.git.pinned_head, path)
            expected = path.encode("utf-8") + b"\x00"
            if tracked != expected:
                raise Gate2ContractError(f"tracked path query did not return exactly {path}")
            target = self.root / path
            if not target.is_file() or target.is_symlink():
                raise Gate2ContractError(f"tracked path is not a regular file: {path}")
            self._working_files[path] = target.read_bytes()
        return self._working_files[path]

    def task_state(
        self, state: str, commit: str | None
    ) -> tuple[bytes, str, list[LedgerRow], dict[str, Any] | None, dict[str, bytes]]:
        if state not in self._task_states:
            if state == "working":
                raw = self.working_file(self.task_path)
            else:
                if commit is None:
                    raise Gate2ContractError(f"{state} Task commit is missing")
                raw = self.git.run("show", commit, self.task_path)
            try:
                text = raw.decode("utf-8", errors="strict")
            except UnicodeDecodeError as error:
                raise Gate2ContractError(f"{state} Task is not UTF-8") from error
            rows = parse_ledger_text(text)
            try:
                manifest = extract_json_block(text, MANIFEST_HEADING, "gate2-review-manifest/v1")
            except Gate2ContractError:
                manifest = None
            carries = _carried_blocks(raw)
            self._task_states[state] = (raw, text, rows, manifest, carries)
        return self._task_states[state]


# A carried block is introduced by a bolded lead. Stage 00 later required that a
# historical quotation retained in current Markdown be a contiguous blockquote
# opening with an exact sentence
# (`docs/00.agent-governance/policies/documentation-protocol.md:44`), and five
# carried blocks in the owning Task now use it. That wrapper does not stop a
# block being a carried block, and a Stage 00 policy outranks this module's
# assumption about how one starts, so the registered wrapper is accepted -- but
# only that exact wrapper, and only when the quoted lead is itself bolded. Any
# other non-bolded block carrying a marker is still rejected.
HISTORICAL_EVIDENCE_WRAPPER = (
    b"> Historical evidence (not current authority; source: Git history):\n"
)


def _is_carried_block(block: bytes) -> bool:
    """True when the block opens a carried claim, wrapped or bare."""

    if block.startswith(b"**"):
        return True
    if not block.startswith(HISTORICAL_EVIDENCE_WRAPPER):
        return False
    return block[len(HISTORICAL_EVIDENCE_WRAPPER):].startswith(b"> **")


def _carried_blocks(task_bytes: bytes) -> dict[str, bytes]:
    try:
        text = task_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Gate2ContractError("Task is not valid UTF-8") from error
    lines = text.splitlines(keepends=True)
    plain = [line.removesuffix("\n").removesuffix("\r") for line in lines]
    fence_mask = _fence_mask(plain)
    start, end = _unique_section(plain, DESTINATION_HEADING)
    section = b"".join(line.encode("utf-8") for line in lines[start:end])
    raw_markers = re.findall(br"\{ledger-anchor:([^{}\r\n]*)\}", section)
    census: list[str] = []
    for raw_marker in raw_markers:
        try:
            decoded_marker = raw_marker.decode("utf-8", errors="strict")
        except UnicodeDecodeError as error:
            raise Gate2ContractError("Carry marker is not valid UTF-8") from error
        marker = normalize_cell(decoded_marker)
        if not marker or decoded_marker != " " + marker:
            raise Gate2ContractError("Carry marker spacing is not canonical")
        census.append(marker)
    visible_parts: list[bytes] = []
    for index, line in enumerate(lines[start:end], start=start):
        encoded = line.encode("utf-8")
        if fence_mask[index]:
            ending = b"\n" if encoded.endswith(b"\n") else b""
            visible_parts.append(b"x" * (len(encoded) - len(ending)) + ending)
        else:
            visible_parts.append(encoded)
    visible_section = b"".join(visible_parts)
    # The first line after a heading is normally blank. It is a separator, not
    # part of the first carried block. Whitespace-only blank lines separate
    # maximal blocks; content bytes inside each block remain untouched.
    section = re.sub(br"^(?:[ \t]*\r?\n)+", b"", section)
    visible_section = re.sub(br"^(?:[ \t]*\r?\n)+", b"", visible_section)
    blocks = re.split(br"\r?\n(?:[ \t]*\r?\n)+", section)
    visible_blocks = re.split(br"\r?\n(?:[ \t]*\r?\n)+", visible_section)
    if len(blocks) != len(visible_blocks):
        raise Gate2ContractError("Carry fence masking changed block boundaries")
    by_marker: dict[str, bytes] = {}
    for block, visible_block in zip(blocks, visible_blocks, strict=True):
        broad_markers = re.findall(
            br"\{ledger-anchor:([^{}\r\n]*)\}", visible_block
        )
        if not _is_carried_block(block):
            if broad_markers:
                raise Gate2ContractError("Carry marker occurs outside a carried block")
            continue
        if block.endswith(b"\n"):
            block = block[:-1]
        try:
            decoded = visible_block.decode("utf-8")
        except UnicodeDecodeError as error:
            raise Gate2ContractError("carried block is not valid UTF-8") from error
        raw_markers = re.findall(r"\{ledger-anchor:([^{}\r\n]*)\}", decoded)
        markers: list[str] = []
        for raw_marker in raw_markers:
            marker = normalize_cell(raw_marker)
            if not marker or raw_marker != " " + marker:
                raise Gate2ContractError("Carry marker spacing is not canonical")
            markers.append(marker)
        if len(markers) != len(set(markers)):
            raise Gate2ContractError("duplicate Carry marker in Gate 3 section")
        for marker in markers:
            if marker in by_marker:
                raise Gate2ContractError(f"marker occurs in multiple blocks: {marker}")
            by_marker[marker] = block
    if set(census) != set(by_marker):
        raise Gate2ContractError("Carry marker occurs outside a carried block")
    return by_marker


def _validate_destination(
    invocation: _Gate2Invocation,
    row: LedgerRow,
    destination: dict[str, Any],
    reviewed_commit: str,
) -> None:
    _assert_exact_keys(destination, DESTINATION_KEYS, "destination")
    _safe_path(destination["path"], "destination path")
    if not isinstance(destination["anchor_locator"], str) or not destination["anchor_locator"]:
        raise Gate2ContractError("destination anchor_locator must be nonempty")
    _assert_digest(destination["content_digest_v1"], "destination content digest")
    subject = row.as_subject()
    if row.disposition in ("Retain", "Correct"):
        if destination["kind"] != "DOCUMENT_FILE":
            raise Gate2ContractError("Retain/Correct destination kind mismatch")
        if not isinstance(destination["blob_oid"], str) or not OID_RE.fullmatch(destination["blob_oid"]):
            raise Gate2ContractError("document destination requires a full blob OID")
        reviewed = invocation.git.run("show", reviewed_commit, destination["path"])
        pinned = invocation.git.run("show", invocation.git.pinned_head, destination["path"])
        current = invocation.working_file(destination["path"])
        if destination["path"] != subject["new_path"]:
            raise Gate2ContractError("destination path does not match ledger New path")
        if destination["anchor_locator"] != subject["new_anchor"]:
            raise Gate2ContractError("destination locator does not match ledger New anchor")
        if reviewed != pinned or pinned != current:
            raise Gate2ContractError("destination bytes changed since review")
        try:
            oid = invocation.git.run(
                "oid", reviewed_commit, destination["path"]
            ).decode("utf-8", errors="strict").strip()
            pinned_oid = invocation.git.run(
                "oid", invocation.git.pinned_head, destination["path"]
            ).decode("utf-8", errors="strict").strip()
        except UnicodeDecodeError as error:
            raise Gate2ContractError("destination OID is not UTF-8") from error
        if not OID_RE.fullmatch(oid) or pinned_oid != oid:
            raise Gate2ContractError("destination Git OID is invalid or stale")
        if destination["blob_oid"] != oid or destination["content_digest_v1"] != raw_digest(current):
            raise Gate2ContractError("document destination digest/OID mismatch")
        return
    if row.disposition != "Carry":
        raise Gate2ContractError("receipt references a row outside Gate 2")
    marker = "{ledger-anchor: " + subject["claim_anchor"] + "}"
    if destination != {
        "kind": "CARRY_PARAGRAPH",
        "path": invocation.task_path,
        "anchor_locator": marker,
        "blob_oid": None,
        "content_digest_v1": destination["content_digest_v1"],
    }:
        raise Gate2ContractError("Carry destination metadata mismatch")
    current_blocks = invocation.task_state("working", None)[4]
    pinned_blocks = invocation.task_state("pinned", invocation.git.pinned_head)[4]
    reviewed_blocks = invocation.task_state("reviewed", reviewed_commit)[4]
    key = subject["claim_anchor"]
    if key not in current_blocks or key not in pinned_blocks or key not in reviewed_blocks:
        raise Gate2ContractError("Carry marker is unresolved")
    if current_blocks[key] != pinned_blocks[key] or pinned_blocks[key] != reviewed_blocks[key]:
        raise Gate2ContractError("Carry block changed since review")
    if destination["content_digest_v1"] != raw_digest(current_blocks[key]):
        raise Gate2ContractError("Carry block digest mismatch")


def _validate_assignment(
    assignment: dict[str, Any],
    manifest_by_id: dict[str, dict[str, Any]],
    rows_by_key: dict[str, LedgerRow],
    manifest_digest: str,
    ledger_digest: str,
    population_digest: str,
    invocation: _Gate2Invocation,
) -> tuple[str, dict[str, dict[str, Any]]]:
    _assert_exact_keys(assignment, ASSIGNMENT_KEYS, "assignment")
    if assignment["schema"] != "gate2-review-assignment/v1":
        raise Gate2ContractError("assignment schema mismatch")
    _assert_round(assignment["review_round"], "assignment review_round")
    reviewed_commit = assignment["reviewed_commit"]
    if not isinstance(reviewed_commit, str) or not OID_RE.fullmatch(reviewed_commit):
        raise Gate2ContractError("assignment reviewed_commit is invalid")
    for key in ("manifest_digest_v1", "ledger_digest_v1", "population_digest_v1"):
        _assert_digest(assignment[key], f"assignment {key}")
    invocation.git.run("ancestor", reviewed_commit)
    expected_digests = (manifest_digest, ledger_digest, population_digest)
    actual_digests = (
        assignment["manifest_digest_v1"],
        assignment["ledger_digest_v1"],
        assignment["population_digest_v1"],
    )
    if actual_digests != expected_digests:
        raise Gate2ContractError("assignment freshness digest mismatch")

    ids_by_key = {record["claim_key_v1"]: record_id for record_id, record in manifest_by_id.items()}
    population_keys = sorted(
        key for key, row in rows_by_key.items() if row.disposition in GATE2_DISPOSITIONS
    )
    chunks = [population_keys[index : index + 25] for index in range(0, len(population_keys), 25)]
    batches = assignment["batches"]
    if not isinstance(batches, list) or len(batches) != len(chunks):
        raise Gate2ContractError("assignment batch census mismatch")
    if any(not isinstance(batch, dict) for batch in batches):
        raise Gate2ContractError("assignment batches must be objects")
    by_batch: dict[str, dict[str, Any]] = {}
    reviewer_seats: set[str] = set()
    reviewer_tasks: set[str] = set()
    for index, (batch, expected_keys) in enumerate(zip(batches, chunks, strict=True), start=1):
        _assert_exact_keys(batch, BATCH_KEYS, "assignment batch")
        _assert_string(batch["ordinal"], "batch ordinal")
        _assert_string(batch["batch_id"], "batch_id", pattern=BATCH_ID_RE)
        _assert_string_array(
            batch["record_ids"], "batch record_ids", pattern=RECORD_ID_RE
        )
        _assert_string_array(batch["claim_keys"], "batch claim_keys", pattern=DIGEST_RE)
        ordinal = f"{index:03d}"
        if batch["ordinal"] != ordinal or batch["claim_keys"] != expected_keys:
            raise Gate2ContractError("assignment batch order/membership mismatch")
        expected_ids = [ids_by_key[key] for key in expected_keys]
        if batch["record_ids"] != expected_ids:
            raise Gate2ContractError("assignment record/key positional mismatch")
        reviewer = _assert_exact_keys(batch["reviewer_identity"], ASSIGNMENT_REVIEWER_KEYS, "batch reviewer")
        if any(not isinstance(reviewer[key], str) or not reviewer[key] for key in reviewer):
            raise Gate2ContractError("batch reviewer fields must be nonempty strings")
        if reviewer["agent_id"] != "code-reviewer":
            raise Gate2ContractError("row-review implementer must be code-reviewer")
        if reviewer["seat"] in reviewer_seats:
            raise Gate2ContractError("row-review seat is reused")
        if reviewer["task_id"] in reviewer_tasks:
            raise Gate2ContractError("row-review task identity is reused")
        reviewer_seats.add(reviewer["seat"])
        reviewer_tasks.add(reviewer["task_id"])
        expected_batch_id = f"gate2-batch-v1:{ordinal}:{canonical_digest(expected_keys)}"
        if batch["batch_id"] != expected_batch_id:
            raise Gate2ContractError("batch_id digest mismatch")
        by_batch[batch["batch_id"]] = batch
    assignment_digest = canonical_digest(assignment)
    return assignment_digest, by_batch


def _expected_basis(disposition: str) -> dict[str, str]:
    expected = {key: "N/A" for key in BASIS_KEYS}
    for key in ("destination_resolution", "destination_substance", "evidence_freshness"):
        expected[key] = "PASS"
    if disposition in ("Retain", "Correct"):
        expected["source_fidelity"] = "PASS"
    if disposition == "Correct":
        expected["correction_explicit"] = "PASS"
        expected["correction_evidence"] = "PASS"
    if disposition == "Carry":
        expected["current_repository_verification"] = "PASS"
        expected["carry_owner_alignment"] = "PASS"
        expected["carry_survival_predicate"] = "PASS"
    return expected


def _validate_candidate(
    candidate: dict[str, Any],
    *,
    invocation: _Gate2Invocation,
    record: dict[str, Any],
    row: LedgerRow,
    batch: dict[str, Any],
    report_path: str,
    manifest_digest: str,
    ledger_digest: str,
    population_digest: str,
    assignment_digest: str,
) -> None:
    _assert_exact_keys(candidate, CANDIDATE_KEYS, "candidate")
    if candidate["schema"] != "gate2-review-candidate/v1":
        raise Gate2ContractError("candidate schema mismatch")
    _assert_round(candidate["review_round"], "candidate review_round")
    if type(candidate["identity_revision"]) is not int or candidate["identity_revision"] != 1:
        raise Gate2ContractError("candidate identity_revision must be integer 1")
    _assert_string(candidate["record_id"], "candidate record_id", pattern=RECORD_ID_RE)
    _assert_string(candidate["batch_id"], "candidate batch_id", pattern=BATCH_ID_RE)
    _assert_string(candidate["reviewed_commit"], "candidate reviewed_commit", pattern=OID_RE)
    for key in (
        "manifest_digest_v1", "ledger_digest_v1", "population_digest_v1",
        "claim_key_v1", "subject_digest_v1", "destination_digest_v1",
        "assignment_digest_v1", "candidate_digest_v1",
    ):
        _assert_digest(candidate[key], f"candidate {key}")
    for key, expected in (
        ("review_round", 1),
        ("manifest_digest_v1", manifest_digest),
        ("ledger_digest_v1", ledger_digest),
        ("population_digest_v1", population_digest),
        ("record_id", record["record_id"]),
        ("identity_revision", 1),
        ("claim_key_v1", record["claim_key_v1"]),
        ("subject_digest_v1", record["subject_digest_v1"]),
        ("reviewed_commit", batch.get("reviewed_commit", candidate["reviewed_commit"])),
        ("batch_id", batch["batch_id"]),
        ("assignment_digest_v1", assignment_digest),
    ):
        if candidate[key] != expected:
            raise Gate2ContractError(f"candidate {key} mismatch")
    reviewer = _assert_exact_keys(candidate["reviewer_identity"], REPORT_REVIEWER_KEYS, "candidate reviewer")
    for key in REPORT_REVIEWER_KEYS:
        _assert_string(reviewer[key], f"candidate reviewer {key}")
    if {key: reviewer[key] for key in ASSIGNMENT_REVIEWER_KEYS} != batch["reviewer_identity"]:
        raise Gate2ContractError("candidate reviewer substitution")
    if reviewer["report_path"] != report_path:
        raise Gate2ContractError("candidate report path mismatch")
    if not isinstance(candidate["reviewer_body"], str) or not candidate["reviewer_body"]:
        raise Gate2ContractError("candidate reviewer_body must be nonempty")
    basis = _assert_exact_keys(candidate["basis"], BASIS_KEYS, "candidate basis")
    if any(value not in ("PASS", "FAIL", "N/A") for value in basis.values()):
        raise Gate2ContractError("candidate basis has an invalid value")
    finding_ids = _assert_string_array(
        candidate["finding_ids"], "candidate finding_ids", ordered=True
    )
    settled = basis == _expected_basis(row.disposition) and not finding_ids
    if candidate["verdict"] not in ("SETTLED", "HELD"):
        raise Gate2ContractError("candidate verdict is invalid")
    if (candidate["verdict"] == "SETTLED") != settled:
        raise Gate2ContractError("candidate verdict/basis mismatch")
    _assert_exact_keys(candidate["destination"], DESTINATION_KEYS, "candidate destination")
    if candidate["destination_digest_v1"] != canonical_digest(candidate["destination"]):
        raise Gate2ContractError("candidate destination digest mismatch")
    _validate_destination(invocation, row, candidate["destination"], candidate["reviewed_commit"])
    if candidate["candidate_digest_v1"] != canonical_digest(candidate, omit="candidate_digest_v1"):
        raise Gate2ContractError("candidate digest mismatch")


def _assert_unique_destination_locators(
    candidates_by_id: dict[str, dict[str, Any]],
) -> None:
    locator_owners: dict[tuple[str, str], str] = {}
    for record_id, candidate in candidates_by_id.items():
        destination = _assert_exact_keys(
            candidate.get("destination"), DESTINATION_KEYS, "candidate destination"
        )
        locator = (destination["path"], destination["anchor_locator"])
        prior = locator_owners.get(locator)
        if prior is not None:
            raise Gate2ContractError(
                f"destination locator collision between {prior} and {record_id}"
            )
        locator_owners[locator] = record_id


def _validate_envelope(
    envelope: dict[str, Any],
    *,
    invocation: _Gate2Invocation,
    manifest_by_id: dict[str, dict[str, Any]],
    rows_by_key: dict[str, LedgerRow],
    manifest_digest: str,
    ledger_digest: str,
    population_digest: str,
) -> tuple[str, str, dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    _assert_exact_keys(envelope, ENVELOPE_KEYS, "evidence envelope")
    if envelope["schema"] != "gate2-review-evidence-envelope/v1":
        raise Gate2ContractError("evidence envelope schema mismatch")
    _assert_round(envelope["review_round"], "evidence envelope review_round")
    _assert_digest(envelope["assignment_digest_v1"], "envelope assignment digest")
    _assert_digest(
        envelope["evidence_envelope_digest_v1"], "evidence envelope digest"
    )
    assignment = envelope["assignment"]
    assignment_digest, batches = _validate_assignment(
        assignment,
        manifest_by_id,
        rows_by_key,
        manifest_digest,
        ledger_digest,
        population_digest,
        invocation,
    )
    if envelope["assignment_digest_v1"] != assignment_digest:
        raise Gate2ContractError("envelope assignment digest mismatch")
    carry_anchors = {
        rows_by_key[record["claim_key_v1"]].as_subject()["claim_anchor"]
        for record in manifest_by_id.values()
        if rows_by_key[record["claim_key_v1"]].disposition == "Carry"
    }
    for state, commit in (
        ("working", None),
        ("pinned", invocation.git.pinned_head),
        ("reviewed", assignment["reviewed_commit"]),
    ):
        state_markers = set(invocation.task_state(state, commit)[4])
        if state_markers != carry_anchors:
            raise Gate2ContractError(
                "Carry marker population has unknown or unserved rows"
            )
    reports = _object_array(envelope["reports"], "evidence reports")
    if len(reports) != len(batches):
        raise Gate2ContractError("report/batch census mismatch")
    finals_for_order: list[dict[str, Any]] = []
    for report in reports:
        _assert_exact_keys(report, REPORT_ENTRY_KEYS, "report entry")
        final_value = _assert_exact_keys(
            report["reviewer_final"], FINAL_KEYS, "reviewer final"
        )
        _assert_string(final_value["batch_id"], "reviewer final batch_id", pattern=BATCH_ID_RE)
        finals_for_order.append(final_value)
    embedded_batch_ids = [final["batch_id"] for final in finals_for_order]
    if embedded_batch_ids != sorted(embedded_batch_ids) or len(embedded_batch_ids) != len(set(embedded_batch_ids)):
        raise Gate2ContractError("reports are reordered or duplicated")
    candidates_by_id: dict[str, dict[str, Any]] = {}
    reports_by_batch: dict[str, dict[str, Any]] = {}
    for report in reports:
        report_path = _safe_path(report["report_path"], "report path")
        for digest_key in ("report_bytes_digest_v1", "reviewer_body_digest_v1", "reviewer_final_digest_v1"):
            _assert_digest(report[digest_key], f"report {digest_key}")
        final = _assert_exact_keys(report["reviewer_final"], FINAL_KEYS, "reviewer final")
        if final["schema"] != "gate2-review-final/v1":
            raise Gate2ContractError("reviewer final schema mismatch")
        _assert_round(final["review_round"], "reviewer final review_round")
        _assert_digest(final["assignment_digest_v1"], "reviewer final assignment digest")
        _assert_string(final["reviewed_commit"], "reviewer final reviewed_commit", pattern=OID_RE)
        _assert_string(final["batch_verdict"], "reviewer final batch_verdict")
        _assert_string_array(final["finding_ids"], "reviewer final finding_ids", ordered=True)
        batch_id = final["batch_id"]
        batch = batches.get(batch_id)
        if batch is None:
            raise Gate2ContractError("report references an unknown batch")
        expected_report_path = (
            ".superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/"
            f"task-10i-gate2-p4-row-review-{batch['ordinal']}.md"
        )
        if report_path != expected_report_path:
            raise Gate2ContractError("row report path does not match its batch ordinal")
        if final["assignment_digest_v1"] != assignment_digest or final["reviewed_commit"] != assignment["reviewed_commit"]:
            raise Gate2ContractError("reviewer final freshness mismatch")
        reviewer = _assert_exact_keys(final["reviewer_identity"], REPORT_REVIEWER_KEYS, "final reviewer")
        if {key: reviewer[key] for key in ASSIGNMENT_REVIEWER_KEYS} != batch["reviewer_identity"] or reviewer["report_path"] != report_path:
            raise Gate2ContractError("reviewer final identity substitution")
        candidates = _object_array(final["candidates"], "reviewer final candidates")
        for candidate in candidates:
            _assert_exact_keys(candidate, CANDIDATE_KEYS, "candidate")
            _assert_string(candidate["record_id"], "candidate record_id", pattern=RECORD_ID_RE)
        candidate_ids = [item["record_id"] for item in candidates]
        if any(record_id in candidates_by_id for record_id in candidate_ids):
            raise Gate2ContractError("candidate replay/cross-batch duplicate")
        if len(candidate_ids) < len(batch["record_ids"]):
            raise Gate2ContractError("candidate batch gap")
        if len(candidate_ids) > len(batch["record_ids"]):
            raise Gate2ContractError("candidate batch overlap/extra")
        if candidate_ids != sorted(batch["record_ids"]):
            raise Gate2ContractError("candidate membership/order substitution")
        for candidate in candidates:
            record_id = candidate["record_id"]
            if record_id in candidates_by_id:
                raise Gate2ContractError("candidate replay/cross-batch duplicate")
            record = manifest_by_id.get(record_id)
            if record is None:
                raise Gate2ContractError("candidate references an orphan record")
            row = rows_by_key[record["claim_key_v1"]]
            batch_with_commit = {**batch, "reviewed_commit": assignment["reviewed_commit"]}
            _validate_candidate(
                candidate,
                invocation=invocation,
                record=record,
                row=row,
                batch=batch_with_commit,
                report_path=report_path,
                manifest_digest=manifest_digest,
                ledger_digest=ledger_digest,
                population_digest=population_digest,
                assignment_digest=assignment_digest,
            )
            candidates_by_id[record_id] = candidate
        for item in candidates:
            _assert_string_array(item["finding_ids"], "candidate finding_ids", ordered=True)
            _assert_string(item["reviewer_body"], "candidate reviewer_body")
        finding_union = sorted({finding for item in candidates for finding in item["finding_ids"]})
        if final["finding_ids"] != finding_union:
            raise Gate2ContractError("reviewer final finding union mismatch")
        settled = all(item["verdict"] == "SETTLED" for item in candidates) and not finding_union
        if final["batch_verdict"] != ("SETTLED" if settled else "HELD"):
            raise Gate2ContractError("reviewer final batch verdict mismatch")
        bodies = {item["reviewer_body"] for item in candidates}
        if len(bodies) != 1 or report["reviewer_body_digest_v1"] != raw_digest(next(iter(bodies)).encode("utf-8")):
            raise Gate2ContractError("reviewer body digest mismatch")
        if report["reviewer_final_digest_v1"] != canonical_digest(final):
            raise Gate2ContractError("reviewer final digest mismatch")
        reports_by_batch[batch_id] = report
    expected_ids = {
        record_id
        for record_id, record in manifest_by_id.items()
        if rows_by_key[record["claim_key_v1"]].disposition in GATE2_DISPOSITIONS
    }
    if set(candidates_by_id) != expected_ids:
        raise Gate2ContractError("candidate population census mismatch")
    _assert_unique_destination_locators(candidates_by_id)
    envelope_digest = canonical_digest(envelope, omit="evidence_envelope_digest_v1")
    if envelope["evidence_envelope_digest_v1"] != envelope_digest:
        raise Gate2ContractError("evidence envelope digest mismatch")
    return assignment_digest, envelope_digest, candidates_by_id, reports_by_batch


def _validate_set_authority(
    authority: dict[str, Any],
    *,
    assignment_digest: str,
    envelope_digest: str,
    candidates_by_id: dict[str, dict[str, Any]],
    reports_by_batch: dict[str, dict[str, Any]],
    reviewed_commit: str,
) -> str:
    _assert_exact_keys(authority, SET_AUTHORITY_KEYS, "set authority")
    if authority["schema"] != "gate2-review-set-authority/v1":
        raise Gate2ContractError("set authority schema mismatch")
    _assert_round(authority["review_round"], "set authority review_round")
    _assert_digest(authority["set_assignment_digest_v1"], "authority assignment digest")
    _assert_digest(authority["set_authority_digest_v1"], "set authority digest")
    assignment = _assert_exact_keys(authority["set_assignment"], SET_ASSIGNMENT_KEYS, "set assignment")
    if assignment["schema"] != "gate2-review-set-assignment/v1":
        raise Gate2ContractError("set assignment schema mismatch")
    _assert_round(assignment["review_round"], "set assignment review_round")
    _assert_string(assignment["reviewed_commit"], "set reviewed_commit", pattern=OID_RE)
    for key in (
        "row_assignment_digest_v1", "evidence_envelope_digest_v1",
        "set_assignment_digest_v1",
    ):
        _assert_digest(assignment[key], f"set assignment {key}")
    if assignment["reviewed_commit"] != reviewed_commit:
        raise Gate2ContractError("set assignment reviewed commit mismatch")
    if assignment["row_assignment_digest_v1"] != assignment_digest or assignment["evidence_envelope_digest_v1"] != envelope_digest:
        raise Gate2ContractError("set assignment freshness mismatch")
    members = _object_array(assignment["members"], "set members")
    for member in members:
        _assert_exact_keys(member, SET_MEMBER_KEYS, "set member")
        _assert_string(member["batch_id"], "set member batch_id", pattern=BATCH_ID_RE)
        _safe_path(member["report_path"], "set member report_path")
        _assert_digest(member["report_bytes_digest_v1"], "set member report bytes digest")
        _assert_digest(member["reviewer_final_digest_v1"], "set member final digest")
        _assert_string_array(
            member["record_ids"], "set member record_ids", pattern=RECORD_ID_RE, ordered=True
        )
        _assert_string_array(
            member["candidate_digests_v1"], "set member candidate digests",
            pattern=DIGEST_RE, ordered=False,
        )
    if [item["batch_id"] for item in members] != sorted(reports_by_batch):
        raise Gate2ContractError("set members are missing, extra, duplicated, or reordered")
    seen_ids: set[str] = set()
    for member in members:
        member_ids = member["record_ids"]
        overlap = seen_ids.intersection(member_ids)
        if overlap:
            raise Gate2ContractError("set member record overlap")
        seen_ids.update(member_ids)
    if seen_ids != set(candidates_by_id):
        raise Gate2ContractError("set member population gap")
    for member in members:
        report = reports_by_batch.get(member["batch_id"])
        if report is None:
            raise Gate2ContractError("set member references an unknown report")
        final = report["reviewer_final"]
        ids = [candidate["record_id"] for candidate in final["candidates"]]
        digests = [candidate["candidate_digest_v1"] for candidate in final["candidates"]]
        if member != {
            "batch_id": final["batch_id"],
            "report_path": report["report_path"],
            "report_bytes_digest_v1": report["report_bytes_digest_v1"],
            "reviewer_final_digest_v1": report["reviewer_final_digest_v1"],
            "record_ids": ids,
            "candidate_digests_v1": digests,
        }:
            raise Gate2ContractError("set member/report projection mismatch")

    expected_reviewers = (
        (
            "POLICY", "rules-engineer", "SPECIFICATION_POLICY", "p4-set-policy",
            ".superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/task-10i-gate2-p4-set-policy-review.md",
        ),
        (
            "QUALITY_SECURITY", "code-reviewer", "QUALITY_SECURITY", "p4-set-quality-security",
            ".superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/task-10i-gate2-p4-set-quality-security-review.md",
        ),
    )
    reviewers = _object_array(assignment["reviewers"], "set reviewers")
    if len(reviewers) != 2:
        raise Gate2ContractError("set assignment requires two reviewers")
    reviewer_keys: set[tuple[str, str, str, str]] = set()
    for reviewer, expected in zip(reviewers, expected_reviewers, strict=True):
        _assert_exact_keys(reviewer, SET_REVIEWER_KEYS, "set reviewer")
        kind, agent_id, role, seat, path = expected
        if any(not isinstance(reviewer[key], str) or not reviewer[key] for key in reviewer):
            raise Gate2ContractError("set reviewer fields must be nonempty strings")
        if (reviewer["review_kind"], reviewer["agent_id"], reviewer["role"], reviewer["seat"], reviewer["report_path"]) != expected:
            raise Gate2ContractError("set reviewer role/path/seat substitution")
        identity = (reviewer["agent_id"], reviewer["seat"], reviewer["task_id"], reviewer["report_path"])
        if identity in reviewer_keys:
            raise Gate2ContractError("set reviewer identity reused")
        reviewer_keys.add(identity)
    if len({item["task_id"] for item in reviewers}) != 2:
        raise Gate2ContractError("set reviewer task identity reused")
    if len({item["seat"] for item in reviewers}) != 2 or len(
        {item["report_path"] for item in reviewers}
    ) != 2:
        raise Gate2ContractError("set reviewer seat/report identity reused")
    row_seats = {
        candidate["reviewer_identity"]["seat"] for candidate in candidates_by_id.values()
    }
    row_tasks = {
        candidate["reviewer_identity"]["task_id"] for candidate in candidates_by_id.values()
    }
    if row_seats.intersection(item["seat"] for item in reviewers) or row_tasks.intersection(
        item["task_id"] for item in reviewers
    ):
        raise Gate2ContractError("set reviewer identity overlaps a row-review seat")
    set_assignment_digest = canonical_digest(assignment, omit="set_assignment_digest_v1")
    if assignment["set_assignment_digest_v1"] != set_assignment_digest or authority["set_assignment_digest_v1"] != set_assignment_digest:
        raise Gate2ContractError("set assignment digest mismatch")

    wrappers = _object_array(authority["attestations"], "attestation wrappers")
    for wrapper in wrappers:
        _assert_exact_keys(wrapper, ATTESTATION_WRAPPER_KEYS, "attestation wrapper")
        _assert_string(wrapper["review_kind"], "attestation review_kind")
    if [item["review_kind"] for item in wrappers] != ["POLICY", "QUALITY_SECURITY"]:
        raise Gate2ContractError("attestation review kinds missing, duplicated, or reordered")
    for wrapper, reviewer in zip(wrappers, reviewers, strict=True):
        if wrapper["review_kind"] != reviewer["review_kind"] or wrapper["report_path"] != reviewer["report_path"]:
            raise Gate2ContractError("attestation wrapper reviewer mismatch")
        _safe_path(wrapper["report_path"], "attestation report_path")
        _assert_digest(wrapper["report_bytes_digest_v1"], "set report bytes digest")
        attestation = _assert_exact_keys(wrapper["attestation"], ATTESTATION_KEYS, "set attestation")
        if attestation["schema"] != "gate2-review-set-attestation/v1":
            raise Gate2ContractError("set attestation schema mismatch")
        _assert_round(attestation["review_round"], "set attestation review_round")
        _assert_string(attestation["review_kind"], "set attestation review_kind")
        _assert_string(
            attestation["reviewed_commit"], "set attestation reviewed_commit", pattern=OID_RE
        )
        for key in (
            "row_assignment_digest_v1", "evidence_envelope_digest_v1",
            "set_assignment_digest_v1", "reviewer_body_digest_v1",
            "attestation_digest_v1",
        ):
            _assert_digest(attestation[key], f"set attestation {key}")
        attestation_identity = _assert_exact_keys(
            attestation["reviewer_identity"], SET_REVIEWER_KEYS,
            "set attestation reviewer identity",
        )
        for key in SET_REVIEWER_KEYS:
            _assert_string(attestation_identity[key], f"set attestation reviewer {key}")
        expected_identity = {key: reviewer[key] for key in SET_REVIEWER_KEYS}
        for key, expected in (
            ("review_round", assignment["review_round"]),
            ("review_kind", reviewer["review_kind"]),
            ("reviewer_identity", expected_identity),
            ("reviewed_commit", reviewed_commit),
            ("row_assignment_digest_v1", assignment_digest),
            ("evidence_envelope_digest_v1", envelope_digest),
            ("set_assignment_digest_v1", set_assignment_digest),
            ("members", members),
        ):
            if attestation[key] != expected:
                raise Gate2ContractError(f"set attestation {key} mismatch")
        if not isinstance(attestation["reviewer_body"], str) or not attestation["reviewer_body"]:
            raise Gate2ContractError("set reviewer body must be nonempty")
        if attestation["reviewer_body_digest_v1"] != raw_digest(attestation["reviewer_body"].encode("utf-8")):
            raise Gate2ContractError("set reviewer body digest mismatch")
        basis = _assert_exact_keys(attestation["basis"], SET_BASIS_KEYS, "set attestation basis")
        if any(value not in ("PASS", "FAIL") for value in basis.values()):
            raise Gate2ContractError("set attestation basis value is invalid")
        _assert_string_array(
            attestation["finding_ids"], "set attestation finding_ids", ordered=True
        )
        severities_are_zero = all(
            type(attestation[key]) is int and attestation[key] == 0
            for key in ("critical", "important", "minor")
        )
        accepted = (
            all(value == "PASS" for value in basis.values())
            and attestation["verdict"] == "APPROVED"
            and severities_are_zero
            and attestation["finding_ids"] == []
        )
        if not accepted:
            raise Gate2ContractError("set attestation is not APPROVED C0/I0/M0")
        if attestation["attestation_digest_v1"] != canonical_digest(attestation, omit="attestation_digest_v1"):
            raise Gate2ContractError("set attestation digest mismatch")
    authority_digest = canonical_digest(authority, omit="set_authority_digest_v1")
    if authority["set_authority_digest_v1"] != authority_digest:
        raise Gate2ContractError("set authority digest mismatch")
    return authority_digest


def _validate_receipts(
    receipts_top: dict[str, Any],
    *,
    invocation: _Gate2Invocation,
    manifest_by_id: dict[str, dict[str, Any]],
    rows_by_key: dict[str, LedgerRow],
    manifest_digest: str,
    ledger_digest: str,
    population_digest: str,
    assignment_digest: str,
    envelope_digest: str,
    candidates_by_id: dict[str, dict[str, Any]],
    reports_by_batch: dict[str, dict[str, Any]],
    reviewed_commit: str,
) -> tuple[int, int]:
    _assert_exact_keys(receipts_top, RECEIPTS_KEYS, "receipts block")
    if receipts_top["schema"] != "gate2-review-receipts/v1":
        raise Gate2ContractError("receipts schema mismatch")
    _assert_round(receipts_top["review_round"], "receipt-set review_round")
    authority_digest = _validate_set_authority(
        receipts_top["p4_set_authority"],
        assignment_digest=assignment_digest,
        envelope_digest=envelope_digest,
        candidates_by_id=candidates_by_id,
        reports_by_batch=reports_by_batch,
        reviewed_commit=reviewed_commit,
    )
    receipts = _object_array(receipts_top["receipts"], "receipts")
    for receipt in receipts:
        _assert_exact_keys(receipt, RECEIPT_KEYS, "receipt")
        _assert_string(receipt["record_id"], "receipt record_id", pattern=RECORD_ID_RE)
        _assert_string(receipt["batch_id"], "receipt batch_id", pattern=BATCH_ID_RE)
    if [item["record_id"] for item in receipts] != sorted(candidates_by_id):
        raise Gate2ContractError("receipts missing, extra, duplicated, or reordered")
    settled = 0
    held = 0
    seen_digests: set[str] = set()
    for receipt in receipts:
        if receipt["schema"] != "gate2-review-receipt/v1":
            raise Gate2ContractError("receipt schema mismatch")
        _assert_round(receipt["review_round"], "receipt review_round")
        if type(receipt["identity_revision"]) is not int or receipt["identity_revision"] != 1:
            raise Gate2ContractError("receipt identity_revision must be integer 1")
        _assert_string(receipt["reviewed_commit"], "receipt reviewed_commit", pattern=OID_RE)
        _assert_string(receipt["claim_key_v1"], "receipt claim_key", pattern=DIGEST_RE)
        _assert_string(receipt["subject_digest_v1"], "receipt subject digest", pattern=DIGEST_RE)
        _assert_string(receipt["reviewer_body"], "receipt reviewer_body")
        _assert_string(receipt["verdict"], "receipt verdict")
        receipt_reviewer = _assert_exact_keys(
            receipt["reviewer_identity"], REPORT_REVIEWER_KEYS, "receipt reviewer"
        )
        for key in REPORT_REVIEWER_KEYS:
            _assert_string(receipt_reviewer[key], f"receipt reviewer {key}")
        _assert_exact_keys(receipt["destination"], DESTINATION_KEYS, "receipt destination")
        _assert_exact_keys(receipt["basis"], BASIS_KEYS, "receipt basis")
        _assert_string_array(receipt["finding_ids"], "receipt finding_ids", ordered=True)
        for key in (
            "manifest_digest_v1", "ledger_digest_v1", "population_digest_v1",
            "destination_digest_v1", "assignment_digest_v1", "candidate_digest_v1",
            "report_bytes_digest_v1", "reviewer_body_digest_v1",
            "reviewer_final_digest_v1", "evidence_envelope_digest_v1",
            "p4_set_authority_digest_v1", "receipt_digest_v1",
        ):
            _assert_digest(receipt[key], f"receipt {key}")
        record_id = receipt["record_id"]
        candidate = candidates_by_id.get(record_id)
        record = manifest_by_id.get(record_id)
        if candidate is None or record is None:
            raise Gate2ContractError("orphan receipt")
        report = reports_by_batch[candidate["batch_id"]]
        row = rows_by_key[record["claim_key_v1"]]
        projection = {
            key: candidate[key]
            for key in (
                "review_round", "manifest_digest_v1", "ledger_digest_v1", "population_digest_v1",
                "record_id", "identity_revision", "claim_key_v1", "subject_digest_v1",
                "destination", "destination_digest_v1", "reviewer_identity", "reviewed_commit",
                "batch_id", "reviewer_body", "verdict", "basis", "finding_ids",
                "assignment_digest_v1", "candidate_digest_v1",
            )
        }
        for key, expected in projection.items():
            if receipt[key] != expected:
                raise Gate2ContractError(f"receipt/candidate {key} mismatch")
        for key, expected in (
            ("manifest_digest_v1", manifest_digest),
            ("ledger_digest_v1", ledger_digest),
            ("population_digest_v1", population_digest),
            ("assignment_digest_v1", assignment_digest),
            ("report_bytes_digest_v1", report["report_bytes_digest_v1"]),
            ("reviewer_body_digest_v1", report["reviewer_body_digest_v1"]),
            ("reviewer_final_digest_v1", report["reviewer_final_digest_v1"]),
            ("evidence_envelope_digest_v1", envelope_digest),
            ("p4_set_authority_digest_v1", authority_digest),
        ):
            if receipt[key] != expected:
                raise Gate2ContractError(f"receipt {key} mismatch")
        digest = canonical_digest(receipt, omit="receipt_digest_v1")
        if receipt["receipt_digest_v1"] != digest or digest in seen_digests:
            raise Gate2ContractError("receipt digest mismatch or replay")
        seen_digests.add(digest)
        if receipt["verdict"] == "SETTLED":
            terminal = normalize_cell(row.values[10])
            match = TERMINAL_VERDICT_RE.fullmatch(terminal)
            if match is None:
                raise Gate2ContractError(
                    f"Review verdict marker is missing or malformed for {record_id}"
                )
            if match.groups() != (digest, authority_digest):
                raise Gate2ContractError(
                    f"Review verdict marker digest binding mismatch for {record_id}"
                )
            settled += 1
        else:
            held += 1
    if len(receipts) != len(candidates_by_id):
        raise Gate2ContractError("receipt population census mismatch")
    return settled, held


def validate_gate2_contract(
    root: pathlib.Path,
    task_path: str,
    *,
    enforce_frozen_count: bool = True,
) -> Gate2Result:
    try:
        git = _Gate2Git.start(root)
        invocation = _Gate2Invocation(root, task_path, git)
        task_bytes, task_text, rows, manifest, _working_carries = invocation.task_state(
            "working", None
        )
        pinned_bytes, _pinned_text, pinned_rows, pinned_manifest, _pinned_carries = (
            invocation.task_state("pinned", git.pinned_head)
        )
        if task_bytes != pinned_bytes:
            raise Gate2ContractError("working-tree Task bytes differ from PINNED_HEAD")
        if [(row.claim_key_v1, row.subject_digest_v1) for row in pinned_rows] != [
            (row.claim_key_v1, row.subject_digest_v1) for row in rows
        ]:
            raise Gate2ContractError("PINNED_HEAD Task ledger projection differs")
        tree = git.run("tree", git.pinned_head)
        if not OID_RE.fullmatch(tree.decode("utf-8", errors="strict").strip()):
            raise Gate2ContractError("PINNED_HEAD tree OID is invalid")
    except (Gate2ContractError, KeyError, TypeError, ValueError) as error:
        code = error.code if isinstance(error, Gate2ContractError) else "GATE2-CONTRACT"
        finding = Finding(code, task_path, str(error))
        return _gate2_result(task_path, 0, 0, 0, 0, (finding,))
    population = [row for row in rows if row.disposition in GATE2_DISPOSITIONS]
    try:
        if manifest is None or pinned_manifest is None:
            raise Gate2ContractError("current committed Task lacks the canonical manifest")
        manifest_by_id, manifest_digest, ledger_digest, population_digest = validate_manifest(
            manifest, rows, enforce_frozen_count=enforce_frozen_count
        )
        pinned_projection = validate_manifest(
            pinned_manifest, pinned_rows, enforce_frozen_count=enforce_frozen_count
        )[1:]
        if pinned_projection != (manifest_digest, ledger_digest, population_digest):
            raise Gate2ContractError("PINNED_HEAD manifest projection differs")
        rows_by_key = {row.claim_key_v1: row for row in rows}
        envelope = extract_json_block(
            task_text, ENVELOPE_HEADING, "gate2-review-evidence-envelope/v1"
        )
        _assert_exact_keys(envelope, ENVELOPE_KEYS, "evidence envelope")
        _assert_string(envelope["schema"], "evidence envelope schema")
        _assert_round(envelope["review_round"], "evidence envelope review_round")
        _assert_digest(
            envelope["assignment_digest_v1"], "envelope assignment digest"
        )
        _object_array(envelope["reports"], "evidence reports")
        _assert_digest(
            envelope["evidence_envelope_digest_v1"], "evidence envelope digest"
        )
        assignment_preview = _assert_exact_keys(
            envelope["assignment"], ASSIGNMENT_KEYS, "assignment"
        )
        reviewed_commit = assignment_preview["reviewed_commit"]
        if not isinstance(reviewed_commit, str) or not OID_RE.fullmatch(reviewed_commit):
            raise Gate2ContractError("assignment reviewed_commit is invalid")
        git.bind_reviewed_commit(reviewed_commit)
        git.run("ancestor", reviewed_commit)
        reviewed_bytes, reviewed_text, reviewed_rows, reviewed_manifest, _reviewed_carries = (
            invocation.task_state("reviewed", reviewed_commit)
        )
        if reviewed_manifest is None:
            raise Gate2ContractError("reviewed_commit predates the canonical manifest")
        if ENVELOPE_HEADING in reviewed_text or RECEIPTS_HEADING in reviewed_text:
            raise Gate2ContractError("reviewed_commit is not a P3-shaped Task snapshot")
        if any(
            normalize_cell(row.values[10]) != "Not Run"
            for row in reviewed_rows
            if row.disposition in GATE2_DISPOSITIONS
        ):
            raise Gate2ContractError("reviewed P3 snapshot has a terminal review verdict")
        reviewed_projection = validate_manifest(
            reviewed_manifest, reviewed_rows, enforce_frozen_count=enforce_frozen_count
        )[1:]
        if reviewed_projection != (manifest_digest, ledger_digest, population_digest):
            raise Gate2ContractError("reviewed P3 manifest/ledger/population projection differs")
        assignment_digest, envelope_digest, candidates_by_id, reports_by_batch = _validate_envelope(
            envelope,
            invocation=invocation,
            manifest_by_id=manifest_by_id,
            rows_by_key=rows_by_key,
            manifest_digest=manifest_digest,
            ledger_digest=ledger_digest,
            population_digest=population_digest,
        )
        receipts = extract_json_block(task_text, RECEIPTS_HEADING, "gate2-review-receipts/v1")
        settled, held = _validate_receipts(
            receipts,
            invocation=invocation,
            manifest_by_id=manifest_by_id,
            rows_by_key=rows_by_key,
            manifest_digest=manifest_digest,
            ledger_digest=ledger_digest,
            population_digest=population_digest,
            assignment_digest=assignment_digest,
            envelope_digest=envelope_digest,
            candidates_by_id=candidates_by_id,
            reports_by_batch=reports_by_batch,
            reviewed_commit=reviewed_commit,
        )
        if settled != len(population) or held:
            raise Gate2ContractError("Gate 2 requires settled == population and held == 0")
        if git.probe_head("head-probe-pre-success") != git.pinned_head:
            raise Gate2ContractError("HEAD moved before success", code="GATE2_HEAD_DRIFT")
        success = _gate2_result(
            task_path, len(rows), len(population), settled, held, ()
        )
        final_drift = _gate2_result(
            task_path,
            len(rows),
            len(population),
            0,
            len(population),
            (Finding("GATE2_HEAD_DRIFT", task_path, "HEAD moved after pre-success probe"),),
        )
        pinned_head = git.pinned_head
        final_head = git.probe_head("head-probe-final")
        return success if final_head == pinned_head else final_drift
    except (Gate2ContractError, KeyError, TypeError, ValueError) as error:
        code = error.code if isinstance(error, Gate2ContractError) else "GATE2-CONTRACT"
        return _gate2_result(
            task_path,
            len(rows),
            len(population),
            0,
            len(population),
            (Finding(code, task_path, str(error)),),
        )


def _run_gate2(root: pathlib.Path, task_path: str) -> int:
    canonical_task = TASK_PATH
    result = validate_gate2_contract(
        root,
        task_path,
        enforce_frozen_count=task_path == canonical_task,
    )
    publication_bytes = result.publication_bytes
    exit_status = result.exit_status
    sys.stdout.buffer.write(publication_bytes)
    return exit_status


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


def main() -> int:
    """Run the gate-2 claim-review contract over the owning Task."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument(
        "--task",
        default=TASK_PATH,
        help="owning Task that holds the ledger and the gate-2 evidence sections",
    )
    arguments = parser.parse_args()
    return _run_gate2(pathlib.Path(arguments.root).resolve(), arguments.task)


if __name__ == "__main__":
    raise SystemExit(main())
