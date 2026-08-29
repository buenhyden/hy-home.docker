"""Focused contract tests for the Gate 2 claim-review validator.

Ported to the migrated document layout on 2026-08-29 with the module it
covers. Four things changed and nothing else: the import, the two hard-coded
Task paths, and the public-CLI helper, which no longer passes `--contract
gate2` because the gate-2 validator is now its own module and that flag chose
between two contracts that no longer share one. Every assertion is the
branch's, so a behaviour difference here is a real one and not an artefact of
the move.
"""

from __future__ import annotations

import ast
import copy
import builtins
import inspect
import math
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(
    0,
    str(pathlib.Path(__file__).resolve().parents[2] / "scripts" / "validation"),
)

import gate2_claim_review_contract as contract  # noqa: E402


HEADERS = contract.LEDGER_HEADERS


def _ledger(*rows: tuple[str, ...]) -> str:
    header = "| " + " | ".join(HEADERS) + " |"
    delimiter = "| " + " | ".join("---" for _ in HEADERS) + " |"
    body = "\n".join("| " + " | ".join(row) + " |" for row in rows)
    return f"### Old-claim migration ledger\n\n{header}\n{delimiter}\n{body}\n\n"


def _row(
    claim: str = "claim-a",
    disposition: str = "Retain",
    destination: str = "destination.md",
    review_verdict: str = "Not Run",
) -> tuple[str, ...]:
    return (
        "old.md", "a" * 40, "b" * 40, claim, "summary", disposition,
        "SOURCE-VERIFIED", destination, "anchor-a", "reason", review_verdict,
    )


def _block(heading: str, value: dict[str, object]) -> str:
    raw = contract.canonical_json(value).decode("utf-8")
    return f"{heading}\n\n```json\n{raw}\n```\n\n"


def _digest_placeholder() -> str:
    return "sha256:" + "0" * 64


class Gate2LedgerParserTests(unittest.TestCase):
    def test_strict_parser_decodes_escaped_pipe_parity(self) -> None:
        self.assertEqual(contract.split_gfm_row(r"| a\|b |"), ["a|b"])
        self.assertEqual(contract.split_gfm_row(r"| a\\| b |"), [r"a\\", "b"])
        self.assertEqual(contract.split_gfm_row(r"| a\\\|b |"), [r"a\\|b"])
        self.assertEqual(contract.split_gfm_row(r"| a\\\\| b |"), [r"a\\\\", "b"])

    def test_live_task_strictly_derives_253_and_dynamic_150(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        task = root / contract.TASK_PATH
        rows = contract.parse_ledger_text(task.read_text(encoding="utf-8"))
        self.assertEqual(len(rows), 253)
        self.assertEqual(
            sum(row.disposition in contract.GATE2_DISPOSITIONS for row in rows), 150
        )

    def test_duplicate_heading_fails(self) -> None:
        with self.assertRaisesRegex(contract.Gate2ContractError, "heading"):
            contract.parse_ledger_text(_ledger(_row()) + _ledger(_row("claim-b")))

    def test_duplicate_header_fails(self) -> None:
        text = _ledger(_row())
        header = "| " + " | ".join(HEADERS) + " |"
        text = text.replace(header, header + "\n" + header, 1)
        with self.assertRaises(contract.Gate2ContractError):
            contract.parse_ledger_text(text)

    def test_wrong_row_width_fails(self) -> None:
        text = _ledger(_row()).replace(" | Not Run |", " |")
        with self.assertRaisesRegex(contract.Gate2ContractError, "cells"):
            contract.parse_ledger_text(text)

    def test_table_like_line_after_gap_fails(self) -> None:
        with self.assertRaisesRegex(contract.Gate2ContractError, "competing"):
            contract.parse_ledger_text(_ledger(_row()) + "| unexpected |\n")

    def test_fenced_fake_heading_is_ignored_and_unclosed_fence_fails(self) -> None:
        text = "```md\n### Old-claim migration ledger\n```\n" + _ledger(_row())
        self.assertEqual(len(contract.parse_ledger_text(text)), 1)
        with self.assertRaisesRegex(contract.Gate2ContractError, "unclosed"):
            contract.parse_ledger_text("```md\n" + _ledger(_row()))


class CanonicalBlockTests(unittest.TestCase):
    def test_duplicate_json_key_nan_and_noncanonical_json_fail(self) -> None:
        with self.assertRaisesRegex(contract.Gate2ContractError, "duplicate"):
            contract.strict_json_object('{"a":1,"a":2}')
        with self.assertRaisesRegex(contract.Gate2ContractError, "non-finite"):
            contract.strict_json_object('{"a":NaN}')
        with self.assertRaisesRegex(contract.Gate2ContractError, "canonical"):
            contract.strict_json_object('{"a": 1}')

    def test_nonfinite_and_mixed_arrays_fail_as_controlled_contract_errors(self) -> None:
        with self.assertRaisesRegex(contract.Gate2ContractError, "non-finite"):
            contract.strict_json_object('{"a":1e400}')
        for values in (["a", 1], [{"a": 1}, 7], [math.inf]):
            with self.subTest(values=values), self.assertRaises(contract.Gate2ContractError):
                contract._assert_sorted_unique(values, "mixed")

    def test_duplicate_heading_fence_and_schema_occurrence_fail(self) -> None:
        value = {"schema": "example/v1"}
        text = _block("### X", value)
        self.assertEqual(contract.extract_json_block(text, "### X", "example/v1"), value)
        for mutant in (
            text + text,
            text.replace("```\n", "```\n```\n", 1),
            text + "example/v1\n",
        ):
            with self.assertRaises(contract.Gate2ContractError):
                contract.extract_json_block(mutant, "### X", "example/v1")

    def test_canonical_array_reordering_and_duplicates_fail(self) -> None:
        for values in (["b", "a"], ["a", "a"]):
            with self.assertRaises(contract.Gate2ContractError):
                contract._assert_sorted_unique(values, "fixture array")


class StaticManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = contract.parse_ledger_text(_ledger(_row()))
        record = {
            "record_id": "g2r-000001", "status": "ACTIVE", "identity_revision": 1,
            "claim_key_v1": self.rows[0].claim_key_v1,
            "subject_digest_v1": self.rows[0].subject_digest_v1,
        }
        self.manifest = {
            "schema": "gate2-review-manifest/v1",
            "bootstrap_commit": contract.BOOTSTRAP_COMMIT,
            "records": [record], "identity_transitions": [],
        }

    def test_complete_static_fixture_passes(self) -> None:
        by_id, *digests = contract.validate_manifest(
            self.manifest, self.rows, enforce_frozen_count=False
        )
        self.assertEqual(list(by_id), ["g2r-000001"])
        self.assertTrue(all(contract.DIGEST_RE.fullmatch(item) for item in digests))

    def test_static_state_mutants_fail_closed(self) -> None:
        mutations = (
            ("record", "status", "RETIRED"),
            ("record", "identity_revision", 2),
            ("record", "claim_key_v1", _digest_placeholder()),
            ("record", "subject_digest_v1", _digest_placeholder()),
            ("manifest", "identity_transitions", [{"from": 1}]),
        )
        for target, key, value in mutations:
            with self.subTest(target=target, key=key):
                mutant = copy.deepcopy(self.manifest)
                (mutant["records"][0] if target == "record" else mutant)[key] = value
                with self.assertRaises(contract.Gate2ContractError):
                    contract.validate_manifest(mutant, self.rows, enforce_frozen_count=False)

    def test_first_ten_field_and_disposition_drift_fail(self) -> None:
        for column in range(10):
            values = list(_row())
            values[column] = "Correct" if column == 5 else values[column] + "-drift"
            drifted = contract.parse_ledger_text(_ledger(tuple(values)))
            with self.subTest(column=column), self.assertRaises(contract.Gate2ContractError):
                contract.validate_manifest(self.manifest, drifted, enforce_frozen_count=False)


class CarryBlockBindingTests(unittest.TestCase):
    def test_three_shared_markers_bind_the_same_complete_block(self) -> None:
        block = (
            "**Claim.** Prefix owner. {ledger-anchor: A} {ledger-anchor: B} "
            "{ledger-anchor: C} suffix."
        )
        task = f"### Gate 3 carried claims\n\n{block}\n\n### Next\n".encode()
        blocks = contract._carried_blocks(task)
        self.assertEqual(set(blocks), {"A", "B", "C"})
        self.assertEqual(len({contract.raw_digest(item) for item in blocks.values()}), 1)
        prefix = task.replace(b"Prefix", b"Changed prefix")
        owner = task.replace(b"owner", b"changed-owner")
        suffix = task.replace(b"suffix", b"changed suffix")
        self.assertNotEqual(
            contract.raw_digest(blocks["A"]),
            contract.raw_digest(contract._carried_blocks(prefix)["A"]),
        )
        self.assertNotEqual(
            contract.raw_digest(blocks["A"]),
            contract.raw_digest(contract._carried_blocks(owner)["A"]),
        )
        self.assertNotEqual(
            contract.raw_digest(blocks["A"]),
            contract.raw_digest(contract._carried_blocks(suffix)["A"]),
        )

    def test_duplicate_and_multi_block_markers_fail(self) -> None:
        duplicate = b"### Gate 3 carried claims\n\n**A.** {ledger-anchor: A} {ledger-anchor: A}\n"
        split = b"### Gate 3 carried claims\n\n**A.** {ledger-anchor: A}\n\n**B.** {ledger-anchor: A}\n"
        for task in (duplicate, split):
            with self.assertRaises(contract.Gate2ContractError):
                contract._carried_blocks(task)

    def test_complete_section_scan_rejects_plain_unknown_and_noncanonical_markers(self) -> None:
        tasks = (
            b"### Gate 3 carried claims\n\nplain {ledger-anchor: A}\n\n**A.** {ledger-anchor: A}\n",
            b"### Gate 3 carried claims\n\nplain {ledger-anchor: UNKNOWN}\n\n**A.** {ledger-anchor: A}\n",
            b"### Gate 3 carried claims\n\n**A.** {ledger-anchor: A   }\n",
        )
        for task in tasks:
            with self.subTest(task=task), self.assertRaises(contract.Gate2ContractError):
                contract._carried_blocks(task)

    def test_fenced_marker_is_censused_and_rejected(self) -> None:
        task = (
            b"### Gate 3 carried claims\n\n```text\n{ledger-anchor: UNKNOWN}\n```\n\n"
            b"**A.** {ledger-anchor: A}\n"
        )
        with self.assertRaisesRegex(contract.Gate2ContractError, "outside a carried block"):
            contract._carried_blocks(task)


class CompleteDynamicFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temporary.name)
        subprocess.run(("git", "init", "-q"), cwd=self.root, check=True)
        subprocess.run(("git", "config", "user.email", "gate2@example.invalid"), cwd=self.root, check=True)
        subprocess.run(("git", "config", "user.name", "Gate2 Fixture"), cwd=self.root, check=True)
        (self.root / "destination.md").write_text(
            "# Destination\n\n## anchor-a\n\nclaim\n", encoding="utf-8"
        )
        self.task_path = "task.md"
        (self.root / self.task_path).write_text(
            _ledger(_row()) + "### Gate 3 carried claims\n\n", encoding="utf-8"
        )
        subprocess.run(("git", "add", "destination.md", self.task_path), cwd=self.root, check=True)
        subprocess.run(("git", "commit", "-qm", "fixture"), cwd=self.root, check=True)
        initial_commit = subprocess.run(
            ("git", "rev-parse", "HEAD"), cwd=self.root, check=True, text=True, capture_output=True
        ).stdout.strip()
        self.reviewed_commit = initial_commit
        self._commit_p3_and_p5()

    def _commit_p3_and_p5(self, p3_verdict: str = "Not Run") -> None:
        """Lay down a P3 snapshot and the P5 evidence commit that reviews it.

        `p3_verdict` is the pre-review contents of the `Review verdict` column
        in the P3 snapshot. It is a parameter because the corpus writes
        provenance beside the words rather than the bare token.
        """

        self.bundle = self._build_bundle()
        self._write_p3(self.bundle, review_verdict=p3_verdict)
        subprocess.run(("git", "add", self.task_path), cwd=self.root, check=True)
        subprocess.run(("git", "commit", "-qm", "p3 reviewed snapshot"), cwd=self.root, check=True)
        self.reviewed_commit = subprocess.run(
            ("git", "rev-parse", "HEAD"), cwd=self.root, check=True, text=True, capture_output=True
        ).stdout.strip()
        self.bundle = self._build_bundle()
        self._write_bundle(self.bundle)
        subprocess.run(("git", "add", self.task_path), cwd=self.root, check=True)
        subprocess.run(("git", "commit", "-qm", "p5 evidence snapshot"), cwd=self.root, check=True)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _build_bundle(self) -> dict[str, object]:
        rows = contract.parse_ledger_text(_ledger(_row()))
        row = rows[0]
        record = {
            "record_id": "g2r-000001", "status": "ACTIVE", "identity_revision": 1,
            "claim_key_v1": row.claim_key_v1, "subject_digest_v1": row.subject_digest_v1,
        }
        manifest = {
            "schema": "gate2-review-manifest/v1", "bootstrap_commit": contract.BOOTSTRAP_COMMIT,
            "records": [record], "identity_transitions": [],
        }
        _, manifest_digest, ledger_digest, population_digest = contract.validate_manifest(
            manifest, rows, enforce_frozen_count=False
        )
        reviewer = {"agent_id": "code-reviewer", "seat": "row-001", "task_id": "row-task-001"}
        claim_keys = [row.claim_key_v1]
        batch_id = f"gate2-batch-v1:001:{contract.canonical_digest(claim_keys)}"
        assignment = {
            "schema": "gate2-review-assignment/v1", "review_round": 1,
            "reviewed_commit": self.reviewed_commit,
            "manifest_digest_v1": manifest_digest, "ledger_digest_v1": ledger_digest,
            "population_digest_v1": population_digest,
            "batches": [{
                "ordinal": "001", "batch_id": batch_id, "reviewer_identity": reviewer,
                "record_ids": [record["record_id"]], "claim_keys": claim_keys,
            }],
        }
        assignment_digest = contract.canonical_digest(assignment)
        report_path = ".superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/task-10i-gate2-p4-row-review-001.md"
        reviewer4 = {**reviewer, "report_path": report_path}
        destination_bytes = (self.root / "destination.md").read_bytes()
        blob_oid = subprocess.run(
            ("git", "rev-parse", f"{self.reviewed_commit}:destination.md"),
            cwd=self.root, check=True, text=True, capture_output=True,
        ).stdout.strip()
        destination = {
            "kind": "DOCUMENT_FILE", "path": "destination.md", "anchor_locator": "anchor-a",
            "blob_oid": blob_oid, "content_digest_v1": contract.raw_digest(destination_bytes),
        }
        body = "reviewed row one"
        candidate = {
            "schema": "gate2-review-candidate/v1", "review_round": 1,
            "manifest_digest_v1": manifest_digest,
            "ledger_digest_v1": ledger_digest, "population_digest_v1": population_digest,
            "record_id": record["record_id"], "identity_revision": 1,
            "claim_key_v1": row.claim_key_v1, "subject_digest_v1": row.subject_digest_v1,
            "destination": destination, "destination_digest_v1": contract.canonical_digest(destination),
            "reviewer_identity": reviewer4, "reviewed_commit": self.reviewed_commit,
            "batch_id": batch_id, "reviewer_body": body, "verdict": "SETTLED",
            "basis": contract._expected_basis("Retain"), "finding_ids": [],
            "assignment_digest_v1": assignment_digest, "candidate_digest_v1": _digest_placeholder(),
        }
        candidate["candidate_digest_v1"] = contract.canonical_digest(candidate, omit="candidate_digest_v1")
        final = {
            "schema": "gate2-review-final/v1", "review_round": 1,
            "assignment_digest_v1": assignment_digest,
            "batch_id": batch_id, "reviewer_identity": reviewer4,
            "reviewed_commit": self.reviewed_commit, "candidates": [candidate],
            "batch_verdict": "SETTLED", "finding_ids": [],
        }
        report = {
            "report_path": report_path, "report_bytes_digest_v1": contract.raw_digest(b"row report"),
            "reviewer_body_digest_v1": contract.raw_digest(body.encode()),
            "reviewer_final_digest_v1": contract.canonical_digest(final), "reviewer_final": final,
        }
        envelope = {
            "schema": "gate2-review-evidence-envelope/v1", "review_round": 1,
            "assignment": assignment,
            "assignment_digest_v1": assignment_digest, "reports": [report],
            "evidence_envelope_digest_v1": _digest_placeholder(),
        }
        envelope["evidence_envelope_digest_v1"] = contract.canonical_digest(
            envelope, omit="evidence_envelope_digest_v1"
        )
        member = {
            "batch_id": batch_id, "report_path": report_path,
            "report_bytes_digest_v1": report["report_bytes_digest_v1"],
            "reviewer_final_digest_v1": report["reviewer_final_digest_v1"],
            "record_ids": [record["record_id"]],
            "candidate_digests_v1": [candidate["candidate_digest_v1"]],
        }
        policy = {
            "review_kind": "POLICY", "agent_id": "rules-engineer", "role": "SPECIFICATION_POLICY",
            "seat": "p4-set-policy", "task_id": "set-policy-task",
            "report_path": ".superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/task-10i-gate2-p4-set-policy-review.md",
        }
        quality = {
            "review_kind": "QUALITY_SECURITY", "agent_id": "code-reviewer", "role": "QUALITY_SECURITY",
            "seat": "p4-set-quality-security", "task_id": "set-quality-task",
            "report_path": ".superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/task-10i-gate2-p4-set-quality-security-review.md",
        }
        set_assignment = {
            "schema": "gate2-review-set-assignment/v1", "review_round": 1,
            "reviewed_commit": self.reviewed_commit, "row_assignment_digest_v1": assignment_digest,
            "evidence_envelope_digest_v1": envelope["evidence_envelope_digest_v1"],
            "members": [member], "reviewers": [policy, quality],
            "set_assignment_digest_v1": _digest_placeholder(),
        }
        set_assignment["set_assignment_digest_v1"] = contract.canonical_digest(
            set_assignment, omit="set_assignment_digest_v1"
        )
        set_basis = {key: "PASS" for key in contract.SET_BASIS_KEYS}
        wrappers = []
        for reviewer_item in (policy, quality):
            attestation = {
                "schema": "gate2-review-set-attestation/v1", "review_round": 1,
                "review_kind": reviewer_item["review_kind"], "reviewer_identity": reviewer_item,
                "reviewed_commit": self.reviewed_commit, "row_assignment_digest_v1": assignment_digest,
                "evidence_envelope_digest_v1": envelope["evidence_envelope_digest_v1"],
                "set_assignment_digest_v1": set_assignment["set_assignment_digest_v1"],
                "members": [member], "reviewer_body": "set reviewed",
                "reviewer_body_digest_v1": contract.raw_digest(b"set reviewed"), "basis": set_basis,
                "verdict": "APPROVED", "critical": 0, "important": 0, "minor": 0,
                "finding_ids": [], "attestation_digest_v1": _digest_placeholder(),
            }
            attestation["attestation_digest_v1"] = contract.canonical_digest(
                attestation, omit="attestation_digest_v1"
            )
            wrappers.append({
                "review_kind": reviewer_item["review_kind"], "report_path": reviewer_item["report_path"],
                "report_bytes_digest_v1": contract.raw_digest(reviewer_item["review_kind"].encode()),
                "attestation": attestation,
            })
        authority = {
            "schema": "gate2-review-set-authority/v1", "review_round": 1,
            "set_assignment": set_assignment,
            "set_assignment_digest_v1": set_assignment["set_assignment_digest_v1"],
            "attestations": wrappers, "set_authority_digest_v1": _digest_placeholder(),
        }
        authority["set_authority_digest_v1"] = contract.canonical_digest(
            authority, omit="set_authority_digest_v1"
        )
        receipt = {
            **{key: candidate[key] for key in (
                "manifest_digest_v1", "ledger_digest_v1", "population_digest_v1", "record_id",
                "identity_revision", "claim_key_v1", "subject_digest_v1", "destination",
                "destination_digest_v1", "reviewer_identity", "reviewed_commit", "batch_id",
                "reviewer_body", "verdict", "basis", "finding_ids", "assignment_digest_v1",
                "candidate_digest_v1",
            )},
            "schema": "gate2-review-receipt/v1", "review_round": 1,
            "report_bytes_digest_v1": report["report_bytes_digest_v1"],
            "reviewer_body_digest_v1": report["reviewer_body_digest_v1"],
            "reviewer_final_digest_v1": report["reviewer_final_digest_v1"],
            "evidence_envelope_digest_v1": envelope["evidence_envelope_digest_v1"],
            "p4_set_authority_digest_v1": authority["set_authority_digest_v1"],
            "receipt_digest_v1": _digest_placeholder(),
        }
        receipt["receipt_digest_v1"] = contract.canonical_digest(receipt, omit="receipt_digest_v1")
        receipts = {
            "schema": "gate2-review-receipts/v1", "review_round": 1,
            "p4_set_authority": authority, "receipts": [receipt],
        }
        return {"manifest": manifest, "envelope": envelope, "receipts": receipts}

    def _rehash_bundle(self, bundle: dict[str, object]) -> None:
        envelope = bundle["envelope"]
        assignment = envelope["assignment"]
        assignment_digest = contract.canonical_digest(assignment)
        envelope["assignment_digest_v1"] = assignment_digest
        report = envelope["reports"][0]
        final = report["reviewer_final"]
        candidate = final["candidates"][0]
        candidate["assignment_digest_v1"] = assignment_digest
        candidate["destination_digest_v1"] = contract.canonical_digest(
            candidate["destination"]
        )
        candidate["candidate_digest_v1"] = contract.canonical_digest(
            candidate, omit="candidate_digest_v1"
        )
        final["assignment_digest_v1"] = assignment_digest
        final["reviewer_identity"] = copy.deepcopy(candidate["reviewer_identity"])
        report["reviewer_final_digest_v1"] = contract.canonical_digest(final)
        envelope["evidence_envelope_digest_v1"] = contract.canonical_digest(
            envelope, omit="evidence_envelope_digest_v1"
        )
        authority = bundle["receipts"]["p4_set_authority"]
        set_assignment = authority["set_assignment"]
        member = set_assignment["members"][0]
        member.update({
            "reviewer_final_digest_v1": report["reviewer_final_digest_v1"],
            "candidate_digests_v1": [candidate["candidate_digest_v1"]],
        })
        set_assignment["row_assignment_digest_v1"] = assignment_digest
        set_assignment["evidence_envelope_digest_v1"] = envelope["evidence_envelope_digest_v1"]
        set_assignment["set_assignment_digest_v1"] = contract.canonical_digest(
            set_assignment, omit="set_assignment_digest_v1"
        )
        authority["set_assignment_digest_v1"] = set_assignment["set_assignment_digest_v1"]
        for wrapper, reviewer in zip(
            authority["attestations"], set_assignment["reviewers"], strict=True
        ):
            attestation = wrapper["attestation"]
            attestation.update({
                "reviewer_identity": copy.deepcopy(reviewer),
                "row_assignment_digest_v1": assignment_digest,
                "evidence_envelope_digest_v1": envelope["evidence_envelope_digest_v1"],
                "set_assignment_digest_v1": set_assignment["set_assignment_digest_v1"],
                "members": copy.deepcopy(set_assignment["members"]),
            })
            attestation["attestation_digest_v1"] = contract.canonical_digest(
                attestation, omit="attestation_digest_v1"
            )
        authority["set_authority_digest_v1"] = contract.canonical_digest(
            authority, omit="set_authority_digest_v1"
        )
        receipt = bundle["receipts"]["receipts"][0]
        for key in (
            "review_round", "manifest_digest_v1", "ledger_digest_v1", "population_digest_v1",
            "record_id", "identity_revision", "claim_key_v1", "subject_digest_v1",
            "destination", "destination_digest_v1", "reviewer_identity", "reviewed_commit",
            "batch_id", "reviewer_body", "verdict", "basis", "finding_ids",
            "assignment_digest_v1", "candidate_digest_v1",
        ):
            receipt[key] = copy.deepcopy(candidate[key])
        receipt.update({
            "reviewer_final_digest_v1": report["reviewer_final_digest_v1"],
            "evidence_envelope_digest_v1": envelope["evidence_envelope_digest_v1"],
            "p4_set_authority_digest_v1": authority["set_authority_digest_v1"],
        })
        receipt["receipt_digest_v1"] = contract.canonical_digest(
            receipt, omit="receipt_digest_v1"
        )

    def _write_p3(
        self, bundle: dict[str, object], review_verdict: str = "Not Run"
    ) -> None:
        text = _ledger(_row(review_verdict=review_verdict)) + "### Gate 3 carried claims\n\n"
        text += _block(contract.MANIFEST_HEADING, bundle["manifest"])
        (self.root / self.task_path).write_text(text, encoding="utf-8")

    def _write_bundle(self, bundle: dict[str, object]) -> None:
        try:
            receipt = bundle["receipts"]["receipts"][0]
            authority = bundle["receipts"]["p4_set_authority"]
            verdict = (
                "SETTLED {gate2-receipt=" + receipt["receipt_digest_v1"]
                + ";gate2-set-authority=" + authority["set_authority_digest_v1"] + "}"
            )
        except (IndexError, KeyError, TypeError):
            verdict = "Not Run"
        text = _ledger(_row(review_verdict=verdict))
        text += "### Gate 3 carried claims\n\n"
        text += _block(contract.MANIFEST_HEADING, bundle["manifest"])
        text += _block(contract.ENVELOPE_HEADING, bundle["envelope"])
        text += _block(contract.RECEIPTS_HEADING, bundle["receipts"])
        (self.root / self.task_path).write_text(text, encoding="utf-8")

    def _validate(self, bundle: dict[str, object]) -> contract.Gate2Result:
        self._write_bundle(bundle)
        self._commit_task_if_changed()
        return contract.validate_gate2_contract(
            self.root, self.task_path, enforce_frozen_count=False
        )

    def _commit_task_if_changed(self) -> None:
        if subprocess.run(
            ("git", "diff", "--quiet", "--", self.task_path), cwd=self.root
        ).returncode:
            subprocess.run(("git", "add", self.task_path), cwd=self.root, check=True)
            subprocess.run(("git", "commit", "-qm", "fixture mutation"), cwd=self.root, check=True)

    def _run_public_cli(self) -> subprocess.CompletedProcess[bytes]:
        script = pathlib.Path(contract.__file__).resolve()
        return subprocess.run(
            (
                sys.executable,
                str(script),
                "--root",
                str(self.root),
                "--task",
                self.task_path,
            ),
            check=False,
            capture_output=True,
        )

    def _assert_public_contract_failure(self, detail: str) -> None:
        result = contract.validate_gate2_contract(
            self.root, self.task_path, enforce_frozen_count=False
        )
        self._assert_contract_detail(result, detail)
        completed = self._run_public_cli()
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stderr, b"")
        self.assertEqual(completed.stdout.count(b"FAIL [GATE2-CONTRACT]"), 1)
        self.assertIn(detail.encode(), completed.stdout)
        self.assertNotIn(b"Traceback", completed.stdout + completed.stderr)

    def _assert_contract_detail(
        self, result: contract.Gate2Result, detail: str
    ) -> None:
        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0].code, "GATE2-CONTRACT")
        self.assertEqual(result.findings[0].detail, detail)

    def test_missing_assignment_is_one_exact_public_contract_finding(self) -> None:
        mutant = copy.deepcopy(self.bundle)
        del mutant["envelope"]["assignment"]
        mutant["envelope"]["evidence_envelope_digest_v1"] = contract.canonical_digest(
            mutant["envelope"], omit="evidence_envelope_digest_v1"
        )
        self._write_bundle(mutant)
        self._commit_task_if_changed()
        self._assert_public_contract_failure(
            "evidence envelope keys differ: missing=['assignment'] extra=[]"
        )

    def test_mixed_candidate_finding_ids_fail_before_sorting(self) -> None:
        mutant = copy.deepcopy(self.bundle)
        candidate = mutant["envelope"]["reports"][0]["reviewer_final"]["candidates"][0]
        candidate["finding_ids"] = ["ROW_HELD", {}]
        self._write_bundle(mutant)
        self._commit_task_if_changed()
        self._assert_public_contract_failure(
            "candidate finding_ids members must be nonempty strings"
        )

    def test_missing_document_destination_fails_through_public_chain(self) -> None:
        mutant = copy.deepcopy(self.bundle)
        candidate = mutant["envelope"]["reports"][0]["reviewer_final"]["candidates"][0]
        candidate["destination"]["path"] = "missing.md"
        self._rehash_bundle(mutant)
        self._write_bundle(mutant)
        self._commit_task_if_changed()
        self._assert_public_contract_failure("Git operation failed: show")

    def test_complete_dynamic_fixture_passes(self) -> None:
        result = self._validate(self.bundle)
        self.assertEqual(result.findings, ())
        self.assertEqual(
            (result.ledger_records, result.population_records, result.settled, result.held),
            (1, 1, 1, 0),
        )

    def test_p3_admits_a_pre_review_verdict_that_carries_provenance(self) -> None:
        """`Not Run; <provenance>` is not a verdict, and P3 must admit it.

        The predicate demanded the cell equal exactly `Not Run`. Across all 18
        commits that have ever touched the real Task, the best any commit
        achieved was 0 of 150 rows, so the gate could not pass however much
        review was done. The contract's own definition of a terminal verdict
        is `TERMINAL_VERDICT_RE`, and that is what P3 must exclude.
        """

        for verdict in (
            "Not Run",
            "Not Run; destination supplied 2026-08-19",
            "Not Run; carried from gate 1",
            "SATISFIED (prose, pre-contract)",
        ):
            with self.subTest(verdict=verdict):
                self._commit_p3_and_p5(p3_verdict=verdict)
                result = self._validate(self.bundle)
                self.assertEqual(result.findings, ())

    def test_p3_still_rejects_a_settled_terminal_marker(self) -> None:
        """The guard the predicate exists for must keep firing."""

        marker = (
            "SETTLED {gate2-receipt=sha256:" + "0" * 64
            + ";gate2-set-authority=sha256:" + "1" * 64 + "}"
        )
        self.assertIsNotNone(contract.TERMINAL_VERDICT_RE.fullmatch(marker))
        self._commit_p3_and_p5(p3_verdict=marker)
        self._assert_contract_detail(
            self._validate(self.bundle),
            "reviewed P3 snapshot has a terminal review verdict",
        )

    def test_dependency_consistent_ancestor_substitution_fails(self) -> None:
        mutant = copy.deepcopy(self.bundle)
        ancestor = subprocess.run(
            ("git", "rev-list", "--max-parents=0", "HEAD"), cwd=self.root,
            check=True, text=True, capture_output=True,
        ).stdout.strip()
        mutant["envelope"]["assignment"]["reviewed_commit"] = ancestor
        self._assert_contract_detail(
            self._validate(mutant),
            "reviewed_commit predates the canonical manifest",
        )

    def test_review_round_is_exactly_nonboolean_one_at_every_layer(self) -> None:
        paths = (
            ("envelope", "review_round"),
            ("envelope", "assignment", "review_round"),
            ("envelope", "reports", 0, "reviewer_final", "review_round"),
            ("envelope", "reports", 0, "reviewer_final", "candidates", 0, "review_round"),
            ("receipts", "review_round"),
            ("receipts", "p4_set_authority", "review_round"),
            ("receipts", "p4_set_authority", "set_assignment", "review_round"),
            ("receipts", "p4_set_authority", "attestations", 0, "attestation", "review_round"),
            ("receipts", "receipts", 0, "review_round"),
        )
        labels = {
            paths[0]: "evidence envelope",
            paths[1]: "assignment",
            paths[2]: "reviewer final",
            paths[3]: "candidate",
            paths[4]: "receipts block",
            paths[5]: "set authority",
            paths[6]: "set assignment",
            paths[7]: "set attestation",
            paths[8]: "receipt",
        }
        round_labels = {
            paths[0]: "evidence envelope review_round",
            paths[1]: "assignment review_round",
            paths[2]: "reviewer final review_round",
            paths[3]: "candidate review_round",
            paths[4]: "receipt-set review_round",
            paths[5]: "set authority review_round",
            paths[6]: "set assignment review_round",
            paths[7]: "set attestation review_round",
            paths[8]: "receipt review_round",
        }
        for path in paths:
            for invalid in (None, False, 0, 2):
                with self.subTest(path=path, invalid=invalid):
                    mutant = copy.deepcopy(self.bundle)
                    cursor = mutant
                    for component in path[:-1]:
                        cursor = cursor[component]
                    if invalid is None:
                        del cursor[path[-1]]
                        expected = (
                            f"{labels[path]} keys differ: "
                            "missing=['review_round'] extra=[]"
                        )
                    else:
                        cursor[path[-1]] = invalid
                        expected = (
                            f"{round_labels[path]} must be the non-boolean integer 1"
                        )
                    self._assert_contract_detail(self._validate(mutant), expected)

    def test_dependency_consistent_round_two_and_boolean_retry_fail_closed(self) -> None:
        paths = (
            ("envelope", "review_round"),
            ("envelope", "assignment", "review_round"),
            ("envelope", "reports", 0, "reviewer_final", "review_round"),
            ("envelope", "reports", 0, "reviewer_final", "candidates", 0, "review_round"),
            ("receipts", "review_round"),
            ("receipts", "p4_set_authority", "review_round"),
            ("receipts", "p4_set_authority", "set_assignment", "review_round"),
            ("receipts", "p4_set_authority", "attestations", 0, "attestation", "review_round"),
            ("receipts", "p4_set_authority", "attestations", 1, "attestation", "review_round"),
            ("receipts", "receipts", 0, "review_round"),
        )
        for invalid in (False, 2):
            mutant = copy.deepcopy(self.bundle)
            for path in paths:
                cursor = mutant
                for component in path[:-1]:
                    cursor = cursor[component]
                cursor[path[-1]] = invalid
            self._rehash_bundle(mutant)
            result = self._validate(mutant)
            self._assert_contract_detail(
                result,
                "evidence envelope review_round must be the non-boolean integer 1",
            )

    def test_terminal_verdict_grammar_and_digest_binding(self) -> None:
        valid = (self.root / self.task_path).read_text(encoding="utf-8")
        marker = contract.parse_ledger_text(valid)[0].values[10]
        matched = contract.TERMINAL_VERDICT_RE.fullmatch(marker)
        self.assertIsNotNone(matched)
        receipt_digest, authority_digest = matched.groups()
        malformed = "Review verdict marker is missing or malformed for g2r-000001"
        binding = "Review verdict marker digest binding mismatch for g2r-000001"
        mutants = (
            ("Not Run", malformed),
            ("", malformed),
            (marker.replace("sha256:", "SHA256:", 1), malformed),
            (marker.replace("gate2-receipt=", "gate2-receipt ="), malformed),
            (marker.replace(receipt_digest, _digest_placeholder(), 1), binding),
            (marker.replace(authority_digest, _digest_placeholder(), 1), binding),
            (
                "SETTLED {gate2-receipt=" + authority_digest
                + ";gate2-set-authority=" + receipt_digest + "}",
                binding,
            ),
            (marker + marker, malformed),
        )
        for value, expected in mutants:
            with self.subTest(value=value):
                text = valid.replace(marker, value, 1)
                (self.root / self.task_path).write_text(text, encoding="utf-8")
                self._commit_task_if_changed()
                self._assert_contract_detail(
                    contract.validate_gate2_contract(
                        self.root, self.task_path, enforce_frozen_count=False
                    ),
                    expected,
                )
        (self.root / self.task_path).write_text(valid, encoding="utf-8")

    def test_held_receipt_cannot_close_gate2(self) -> None:
        mutant = copy.deepcopy(self.bundle)
        final = mutant["envelope"]["reports"][0]["reviewer_final"]
        candidate = final["candidates"][0]
        candidate["basis"]["source_fidelity"] = "FAIL"
        candidate["finding_ids"] = ["ROW_HELD"]
        candidate["verdict"] = "HELD"
        final["finding_ids"] = ["ROW_HELD"]
        final["batch_verdict"] = "HELD"
        self._rehash_bundle(mutant)
        result = self._validate(mutant)
        self._assert_contract_detail(
            result, "Gate 2 requires settled == population and held == 0"
        )
        self.assertEqual((result.settled, result.held), (0, 1))

    def test_public_validator_contains_malformed_types_without_traceback(self) -> None:
        mutants = (
            (
                lambda b: b["manifest"].__setitem__("records", [7]),
                "manifest records members must be objects",
            ),
            (
                lambda b: b["envelope"].__setitem__("reports", [7]),
                "evidence reports members must be objects",
            ),
            (
                lambda b: b["receipts"].__setitem__("receipts", [7]),
                "receipts members must be objects",
            ),
            (
                lambda b: b["receipts"]["p4_set_authority"]["attestations"][0]["attestation"].__setitem__("critical", False),
                "set attestation is not APPROVED C0/I0/M0",
            ),
        )
        for mutate, expected in mutants:
            mutant = copy.deepcopy(self.bundle)
            mutate(mutant)
            result = self._validate(mutant)
            self._assert_contract_detail(result, expected)
            self.assertNotIn("Traceback", "\n".join(item.detail for item in result.findings))

    def test_public_boundary_contains_residual_value_and_type_errors(self) -> None:
        for error in (TypeError("unhashable nested identifier"), ValueError("numeric overflow")):
            with self.subTest(error=type(error).__name__), mock.patch.object(
                contract, "validate_manifest", side_effect=error
            ):
                result = contract.validate_gate2_contract(
                    self.root, self.task_path, enforce_frozen_count=False
                )
            self.assertEqual(result.findings[0].code, "GATE2-CONTRACT")
            self.assertNotIn("Traceback", result.findings[0].detail)

    def test_unhashable_and_mixed_identifiers_are_controlled_findings(self) -> None:
        mutations = (
            (
                lambda b: b["manifest"]["records"][0].__setitem__("record_id", []),
                "manifest record_id must be a nonempty string",
            ),
            (
                lambda b: b["manifest"]["records"][0].__setitem__("identity_revision", True),
                "manifest identity_revision must be an integer",
            ),
            (
                lambda b: b["envelope"]["assignment"]["batches"][0].__setitem__(
                    "record_ids", ["g2r-000001", 7]
                ),
                "batch record_ids members must be nonempty strings",
            ),
            (
                lambda b: b["envelope"]["assignment"]["batches"][0].__setitem__(
                    "batch_id", {}
                ),
                "batch_id must be a nonempty string",
            ),
            (
                lambda b: b["envelope"]["assignment"]["batches"][0]["reviewer_identity"].__setitem__(
                    "seat", []
                ),
                "batch reviewer fields must be nonempty strings",
            ),
            (
                lambda b: b["envelope"]["reports"][0]["reviewer_final"]["candidates"][0].__setitem__(
                    "batch_id", []
                ),
                "candidate batch_id must be a nonempty string",
            ),
            (
                lambda b: b["envelope"]["reports"][0]["reviewer_final"]["candidates"][0].__delitem__(
                    "record_id"
                ),
                "candidate keys differ: missing=['record_id'] extra=[]",
            ),
            (
                lambda b: b["envelope"]["reports"][0]["reviewer_final"]["reviewer_identity"].__setitem__(
                    "task_id", {}
                ),
                "reviewer final identity substitution",
            ),
            (
                lambda b: b["receipts"]["p4_set_authority"]["set_assignment"]["members"][0].__setitem__(
                    "batch_id", []
                ),
                "set member batch_id must be a nonempty string",
            ),
            (
                lambda b: b["receipts"]["p4_set_authority"]["set_assignment"]["reviewers"][0].__setitem__(
                    "task_id", {}
                ),
                "set reviewer fields must be nonempty strings",
            ),
            (
                lambda b: b["receipts"]["receipts"][0].__setitem__("record_id", {}),
                "receipt record_id must be a nonempty string",
            ),
            (
                lambda b: b["receipts"]["receipts"][0].__delitem__("batch_id"),
                "receipt keys differ: missing=['batch_id'] extra=[]",
            ),
        )
        for mutate, expected in mutations:
            with self.subTest(mutate=mutate):
                mutant = copy.deepcopy(self.bundle)
                mutate(mutant)
                result = self._validate(mutant)
                self._assert_contract_detail(result, expected)
                self.assertNotIn("Traceback", "\n".join(item.detail for item in result.findings))

    def test_public_boundary_rejects_nonfinite_json_number_without_traceback(self) -> None:
        task = self.root / self.task_path
        text = task.read_text(encoding="utf-8")
        self.assertIn('"review_round":1', text)
        task.write_text(
            text.replace('"review_round":1', '"review_round":1e400', 1),
            encoding="utf-8",
        )
        self._commit_task_if_changed()
        result = contract.validate_gate2_contract(
            self.root, self.task_path, enforce_frozen_count=False
        )
        self._assert_contract_detail(
            result, "invalid JSON: non-finite JSON number: 1e400"
        )
        self.assertNotIn("Traceback", result.findings[0].detail)

    def test_zero_carry_population_requires_exactly_empty_markers_in_every_state(self) -> None:
        git = contract._Gate2Git.start(self.root)
        git.bind_reviewed_commit(self.reviewed_commit)
        invocation = contract._Gate2Invocation(self.root, self.task_path, git)
        for state, commit in (
            ("working", None),
            ("pinned", git.pinned_head),
            ("reviewed", self.reviewed_commit),
        ):
            with self.subTest(state=state):
                raw, _text, _rows, _manifest, carries = invocation.task_state(
                    state, commit
                )
                self.assertEqual(
                    raw.count(b"### Gate 3 carried claims"), 1
                )
                self.assertEqual(carries, {})

        valid = (self.root / self.task_path).read_text(encoding="utf-8")
        for replacement, count in (
            ("", 0),
            (
                "### Gate 3 carried claims\n\n### Gate 3 carried claims\n\n",
                2,
            ),
        ):
            with self.subTest(malformed_heading_count=count):
                (self.root / self.task_path).write_text(
                    valid.replace("### Gate 3 carried claims\n\n", replacement, 1),
                    encoding="utf-8",
                )
                self._commit_task_if_changed()
                self._assert_public_contract_failure(
                    "expected one '### Gate 3 carried claims' heading, "
                    f"found {count}"
                )
                (self.root / self.task_path).write_text(valid, encoding="utf-8")
                self._commit_task_if_changed()

    def test_row_identity_dimensions_and_row_to_set_reuse_fail(self) -> None:
        # Prove both set seats without relying on their necessarily different
        # report paths. POLICY agent reuse is independently rejected by the row
        # role rule; seat/task reuse remains the load-bearing overlap predicate.
        for seat, task_id in (
            ("p4-set-policy", "set-policy-task"),
            ("p4-set-quality-security", "set-quality-task"),
        ):
            mutant = copy.deepcopy(self.bundle)
            row_identity = mutant["envelope"]["assignment"]["batches"][0]["reviewer_identity"]
            row_identity.update({"agent_id": "code-reviewer", "seat": seat, "task_id": task_id})
            reviewer4 = {
                **row_identity,
                "report_path": mutant["envelope"]["reports"][0]["report_path"],
            }
            candidate = mutant["envelope"]["reports"][0]["reviewer_final"]["candidates"][0]
            candidate["reviewer_identity"] = reviewer4
            self._rehash_bundle(mutant)
            result = self._validate(mutant)
            self._assert_contract_detail(
                result, "set reviewer identity overlaps a row-review seat"
            )
    def test_git_runner_uses_shell_free_argv_and_timeout_reaps_child(self) -> None:
        process = mock.Mock()
        process.communicate.side_effect = [subprocess.TimeoutExpired("git", 30),
                                           subprocess.TimeoutExpired("git", 1),
                                           (b"", b"")]
        process.poll.return_value = None
        with mock.patch.object(contract.subprocess, "Popen", return_value=process) as popen:
            with self.assertRaisesRegex(contract.Gate2ContractError, "GATE2_GIT_TIMEOUT"):
                contract._Gate2Git(pathlib.Path("."), "a" * 40).run("tree", "a" * 40)
        self.assertEqual(popen.call_args.args[0], ["git", "rev-parse", ("a" * 40) + "^{tree}"])
        self.assertIs(popen.call_args.kwargs["stdin"], subprocess.DEVNULL)
        self.assertFalse(popen.call_args.kwargs["shell"])
        process.terminate.assert_called_once_with()
        process.kill.assert_called_once_with()
        self.assertEqual(process.communicate.call_args_list[0].kwargs, {"timeout": 30})
        self.assertEqual(process.communicate.call_args_list[1].kwargs, {"timeout": 1})
        self.assertEqual(process.communicate.call_args_list[2].kwargs, {})

    def test_git_argv_cache_and_task_parse_counts_are_deterministic(self) -> None:
        original_popen = subprocess.Popen
        argv_log: list[tuple[str, ...]] = []

        def popen_spy(argv, **kwargs):
            argv_log.append(tuple(argv))
            self.assertFalse(kwargs["shell"])
            self.assertIs(kwargs["stdin"], subprocess.DEVNULL)
            return original_popen(argv, **kwargs)

        with mock.patch.object(contract.subprocess, "Popen", side_effect=popen_spy), \
             mock.patch.object(contract, "parse_ledger_text", wraps=contract.parse_ledger_text) as ledger_parse, \
             mock.patch.object(contract, "_carried_blocks", wraps=contract._carried_blocks) as carry_parse:
            result = contract.validate_gate2_contract(
                self.root, self.task_path, enforce_frozen_count=False
            )
        self.assertEqual(result.findings, ())
        head = ("git", "rev-parse", "--verify", "HEAD^{commit}")
        self.assertEqual(argv_log.count(head), 3)
        non_probes = [argv for argv in argv_log if argv != head]
        pinned = subprocess.run(
            ("git", "rev-parse", "HEAD"), cwd=self.root, check=True,
            text=True, capture_output=True,
        ).stdout.strip()
        expected_non_probes = {
            ("git", "ls-tree", "-z", "--full-tree", "--name-only", pinned, "--", self.task_path),
            ("git", "show", pinned + ":" + self.task_path),
            ("git", "rev-parse", pinned + "^{tree}"),
            ("git", "merge-base", "--is-ancestor", self.reviewed_commit, pinned),
            ("git", "show", self.reviewed_commit + ":" + self.task_path),
            ("git", "show", self.reviewed_commit + ":destination.md"),
            ("git", "show", pinned + ":destination.md"),
            ("git", "ls-tree", "-z", "--full-tree", "--name-only", pinned, "--", "destination.md"),
            ("git", "rev-parse", self.reviewed_commit + ":destination.md"),
            ("git", "rev-parse", pinned + ":destination.md"),
        }
        self.assertEqual(set(non_probes), expected_non_probes)
        self.assertEqual(len(non_probes), len(expected_non_probes))
        self.assertEqual(ledger_parse.call_count, 3)
        self.assertEqual(carry_parse.call_count, 3)

    def test_final_probe_dominates_an_immediate_local_only_return(self) -> None:
        tree = ast.parse(inspect.getsource(contract.validate_gate2_contract))
        function = tree.body[0]
        statements = function.body[-1].body
        final_probe_index = next(
            index
            for index, statement in enumerate(statements)
            if isinstance(statement, ast.Assign)
            and isinstance(statement.value, ast.Call)
            and isinstance(statement.value.func, ast.Attribute)
            and statement.value.func.attr == "probe_head"
            and ast.literal_eval(statement.value.args[0]) == "head-probe-final"
        )
        self.assertEqual(len(statements), final_probe_index + 2)
        final_return = statements[final_probe_index + 1]
        self.assertIsInstance(final_return, ast.Return)
        self.assertIsInstance(final_return.value, ast.IfExp)
        self.assertEqual(
            {node.id for node in ast.walk(final_return) if isinstance(node, ast.Name)},
            {"final_head", "pinned_head", "success", "final_drift"},
        )

    def test_caller_publishes_only_precomposed_result_bytes_once(self) -> None:
        success = contract._gate2_result("task.md", 1, 1, 1, 0, ())
        drift = contract._gate2_result(
            "task.md", 1, 1, 0, 1,
            (contract.Finding("GATE2_HEAD_DRIFT", "task.md", "final drift"),),
        )
        for returned in (success, drift):
            with self.subTest(exit_status=returned.exit_status):
                output = mock.Mock()
                stdout = mock.Mock(buffer=output)
                with mock.patch.object(
                    contract, "validate_gate2_contract", return_value=returned
                ), mock.patch.object(contract.sys, "stdout", stdout):
                    status = contract._run_gate2(self.root, self.task_path)
                self.assertEqual(status, returned.exit_status)
                output.write.assert_called_once_with(returned.publication_bytes)

    def test_mid_invocation_and_after_pre_success_ref_drift_fail_closed(self) -> None:
        for drift_operation in ("tree", "head-probe-final"):
            with self.subTest(drift_operation=drift_operation):
                original = contract._Gate2Git._execute
                operations: list[str] = []
                moved = False

                def execute_spy(root, argv, operation):
                    nonlocal moved
                    operations.append(operation)
                    if operation == drift_operation and not moved:
                        moved = True
                        subprocess.run(
                            ("git", "commit", "--allow-empty", "-qm", "ref drift"),
                            cwd=self.root, check=True,
                        )
                    return original(root, argv, operation)

                with mock.patch.object(contract._Gate2Git, "_execute", side_effect=execute_spy):
                    result = contract.validate_gate2_contract(
                        self.root, self.task_path, enforce_frozen_count=False
                    )
                self.assertEqual(result.findings[0].code, "GATE2_HEAD_DRIFT")
                if drift_operation == "head-probe-final":
                    self.assertEqual(operations[-1], "head-probe-final")

    def test_final_probe_is_the_last_git_object_observation(self) -> None:
        original_execute = contract._Gate2Git._execute
        original_getattribute = contract._Gate2Git.__getattribute__
        final_probe_complete = False

        def execute_spy(root, argv, operation):
            nonlocal final_probe_complete
            output = original_execute(root, argv, operation)
            if operation == "head-probe-final":
                final_probe_complete = True
            return output

        def guarded_getattribute(instance, name):
            if final_probe_complete:
                raise AssertionError(f"post-final-probe Git observation: {name}")
            return original_getattribute(instance, name)

        with mock.patch.object(contract._Gate2Git, "_execute", side_effect=execute_spy), \
             mock.patch.object(contract._Gate2Git, "__getattribute__", guarded_getattribute):
            result = contract.validate_gate2_contract(
                self.root, self.task_path, enforce_frozen_count=False
            )
        self.assertEqual(result.findings, ())

    def test_final_probe_seals_all_external_and_cache_observations(self) -> None:
        original_probe = contract._Gate2Git.probe_head
        original_git_getattribute = contract._Gate2Git.__getattribute__
        original_invocation_getattribute = contract._Gate2Invocation.__getattribute__
        original_path_open = pathlib.Path.open
        original_path_stat = pathlib.Path.stat
        original_popen = contract.subprocess.Popen
        original_run = contract.subprocess.run
        original_open = builtins.open
        sealed = False

        def reject(surface):
            if sealed:
                raise AssertionError(f"post-final-probe external observation: {surface}")

        def probe_spy(instance, operation):
            nonlocal sealed
            value = original_probe(instance, operation)
            if operation == "head-probe-final":
                sealed = True
            return value

        def git_getattribute(instance, name):
            reject(f"git.{name}")
            return original_git_getattribute(instance, name)

        def invocation_getattribute(instance, name):
            reject(f"invocation.{name}")
            return original_invocation_getattribute(instance, name)

        def path_open(instance, *args, **kwargs):
            reject("path.open")
            return original_path_open(instance, *args, **kwargs)

        def path_stat(instance, *args, **kwargs):
            reject("path.stat")
            return original_path_stat(instance, *args, **kwargs)

        def popen_spy(*args, **kwargs):
            reject("subprocess.Popen")
            return original_popen(*args, **kwargs)

        def run_spy(*args, **kwargs):
            reject("subprocess.run")
            return original_run(*args, **kwargs)

        def open_spy(*args, **kwargs):
            reject("open")
            return original_open(*args, **kwargs)

        with mock.patch.object(contract._Gate2Git, "probe_head", probe_spy), \
             mock.patch.object(contract._Gate2Git, "__getattribute__", git_getattribute), \
             mock.patch.object(
                 contract._Gate2Invocation, "__getattribute__", invocation_getattribute
             ), \
             mock.patch.object(pathlib.Path, "open", path_open), \
             mock.patch.object(pathlib.Path, "stat", path_stat), \
             mock.patch.object(contract.subprocess, "Popen", side_effect=popen_spy), \
             mock.patch.object(contract.subprocess, "run", side_effect=run_spy), \
             mock.patch.object(builtins, "open", side_effect=open_spy):
            result = contract.validate_gate2_contract(
                self.root, self.task_path, enforce_frozen_count=False
            )
            sealed = False
        self.assertEqual(result.findings, ())

    def test_manifest_receipt_and_destination_tampering_fail_closed(self) -> None:
        mutations = (
            ("manifest", "records", [], "manifest/ledger bijection mismatch"),
            ("envelope", "reports", [], "report/batch census mismatch"),
            (
                "receipts", "receipts", [],
                "receipts missing, extra, duplicated, or reordered",
            ),
        )
        for section, key, value, expected in mutations:
            with self.subTest(section=section, key=key):
                mutant = copy.deepcopy(self.bundle)
                mutant[section][key] = value
                self._assert_contract_detail(self._validate(mutant), expected)
        # The anchor is preserved so this case isolates one variable: the
        # destination's bytes changed since review. Dropping the anchor too
        # would add a destination-resolution finding and stop the assertion
        # below from being about byte drift at all.
        (self.root / "destination.md").write_text(
            "changed\n\n## anchor-a\n", encoding="utf-8"
        )
        self._assert_contract_detail(
            self._validate(self.bundle), "destination bytes changed since review"
        )

    def test_provenance_basis_digest_and_set_authority_mutants_fail_closed(self) -> None:
        cases = (
            (("envelope", "assignment", "batches", 0, "reviewer_identity", "agent_id"), "row-review implementer must be code-reviewer"),
            (("envelope", "reports", 0, "reviewer_final", "candidates", 0, "reviewer_identity", "seat"), "reviewer final identity substitution"),
            (("envelope", "reports", 0, "reviewer_final", "candidates", 0, "basis", "source_fidelity"), "candidate verdict/basis mismatch"),
            (("envelope", "reports", 0, "reviewer_final", "candidates", 0, "finding_ids"), "candidate verdict/basis mismatch"),
            (("receipts", "p4_set_authority", "set_assignment", "review_round"), "set assignment review_round must be the non-boolean integer 1"),
            (("receipts", "p4_set_authority", "set_assignment", "reviewers", 0, "agent_id"), "set reviewer role/path/seat substitution"),
            (("receipts", "p4_set_authority", "attestations", 0, "attestation", "important"), "set attestation is not APPROVED C0/I0/M0"),
            (("receipts", "receipts", 0, "receipt_digest_v1"), "receipt receipt_digest_v1 is not a canonical SHA-256 digest"),
        )
        for path, expected in cases:
            with self.subTest(path=path):
                mutant = copy.deepcopy(self.bundle)
                cursor = mutant
                for component in path[:-1]:
                    cursor = cursor[component]
                leaf = path[-1]
                current = cursor[leaf]
                cursor[leaf] = ["finding"] if leaf == "finding_ids" else (
                    "FAIL" if current == "PASS" else current + 1 if isinstance(current, int) else "tampered"
                )
                self._assert_contract_detail(self._validate(mutant), expected)

    def test_independent_reordering_and_replay_fail_closed(self) -> None:
        for section, key, expected in (
            ("manifest", "records", "duplicate manifest record_id"),
            (
                "receipts", "receipts",
                "receipts missing, extra, duplicated, or reordered",
            ),
        ):
            mutant = copy.deepcopy(self.bundle)
            mutant[section][key] = mutant[section][key] * 2
            self._assert_contract_detail(self._validate(mutant), expected)

    def test_set_member_and_attestation_kill_matrix_fails_closed(self) -> None:
        authority_path = ("receipts", "p4_set_authority")
        mutations: list[tuple[str, object, str]] = []

        def mutate(label, callback, expected):
            mutations.append((label, callback, expected))

        member_census = "set members are missing, extra, duplicated, or reordered"
        review_census = "attestation review kinds missing, duplicated, or reordered"
        mutate("remove member", lambda a: a["set_assignment"].__setitem__("members", []), member_census)
        mutate("duplicate member", lambda a: a["set_assignment"]["members"].append(copy.deepcopy(a["set_assignment"]["members"][0])), member_census)
        mutate(
            "add member",
            lambda a: a["set_assignment"]["members"].append(
                {"batch_id": "gate2-batch-v1:999:" + _digest_placeholder()}
            ),
            "set member keys differ: missing=['candidate_digests_v1', 'record_ids', "
            "'report_bytes_digest_v1', 'report_path', 'reviewer_final_digest_v1'] extra=[]",
        )
        mutate("remove review kind", lambda a: a["attestations"].pop(), review_census)
        mutate("duplicate review kind", lambda a: a["attestations"].append(copy.deepcopy(a["attestations"][0])), review_census)
        mutate("reorder review kinds", lambda a: a["attestations"].reverse(), review_census)
        for field in ("role", "report_path", "agent_id", "seat", "task_id"):
            mutate(
                "swap reviewer " + field,
                lambda a, field=field: a["set_assignment"]["reviewers"][0].__setitem__(field, "substituted"),
                (
                    "set assignment digest mismatch"
                    if field == "task_id"
                    else "set reviewer role/path/seat substitution"
                ),
            )
        mutate("reuse reviewer task", lambda a: a["set_assignment"]["reviewers"][1].__setitem__("task_id", a["set_assignment"]["reviewers"][0]["task_id"]), "set reviewer task identity reused")
        mutate("change reviewed commit", lambda a: a["set_assignment"].__setitem__("reviewed_commit", "f" * 40), "set assignment reviewed commit mismatch")
        mutate("change round", lambda a: a["set_assignment"].__setitem__("review_round", 2), "set assignment review_round must be the non-boolean integer 1")
        mutate("change row assignment", lambda a: a["set_assignment"].__setitem__("row_assignment_digest_v1", _digest_placeholder()), "set assignment freshness mismatch")
        mutate("change envelope", lambda a: a["set_assignment"].__setitem__("evidence_envelope_digest_v1", _digest_placeholder()), "set assignment freshness mismatch")
        mutate("change member record", lambda a: a["set_assignment"]["members"][0]["record_ids"].__setitem__(0, "g2r-999999"), "set member population gap")
        mutate("change candidate pairing", lambda a: a["set_assignment"]["members"][0]["candidate_digests_v1"].__setitem__(0, _digest_placeholder()), "set member/report projection mismatch")
        mutate("flip set basis", lambda a: a["attestations"][0]["attestation"]["basis"].__setitem__("candidate_integrity", "FAIL"), "set attestation is not APPROVED C0/I0/M0")
        for severity in ("critical", "important", "minor"):
            mutate("nonzero " + severity, lambda a, severity=severity: a["attestations"][0]["attestation"].__setitem__(severity, 1), "set attestation is not APPROVED C0/I0/M0")
        mutate("finding asserted", lambda a: a["attestations"][0]["attestation"].__setitem__("finding_ids", ["finding"]), "set attestation is not APPROVED C0/I0/M0")
        mutate("verdict rejected", lambda a: a["attestations"][0]["attestation"].__setitem__("verdict", "REJECTED"), "set attestation is not APPROVED C0/I0/M0")
        mutate("cross-round attestation", lambda a: a["attestations"][0]["attestation"].__setitem__("review_round", 2), "set attestation review_round must be the non-boolean integer 1")
        mutate("cross-envelope attestation", lambda a: a["attestations"][0]["attestation"].__setitem__("evidence_envelope_digest_v1", _digest_placeholder()), "set attestation evidence_envelope_digest_v1 mismatch")
        mutate("attestation digest", lambda a: a["attestations"][0]["attestation"].__setitem__("attestation_digest_v1", _digest_placeholder()), "set attestation digest mismatch")
        mutate("authority digest", lambda a: a.__setitem__("set_authority_digest_v1", _digest_placeholder()), "set authority digest mismatch")
        for label, callback, expected in mutations:
            with self.subTest(label=label):
                mutant = copy.deepcopy(self.bundle)
                authority = mutant
                for component in authority_path:
                    authority = authority[component]
                callback(authority)
                self._assert_contract_detail(self._validate(mutant), expected)

    def test_candidate_receipt_digest_kill_matrix_fails_closed(self) -> None:
        candidate_fields = (
            ("manifest_digest_v1", "candidate manifest_digest_v1 mismatch"),
            ("ledger_digest_v1", "candidate ledger_digest_v1 mismatch"),
            ("population_digest_v1", "candidate population_digest_v1 mismatch"),
            ("subject_digest_v1", "candidate subject_digest_v1 mismatch"),
            ("destination_digest_v1", "candidate destination digest mismatch"),
            ("assignment_digest_v1", "candidate assignment_digest_v1 mismatch"),
            ("candidate_digest_v1", "candidate digest mismatch"),
        )
        receipt_fields = (
            ("report_bytes_digest_v1", "receipt report_bytes_digest_v1 mismatch"),
            ("reviewer_body_digest_v1", "receipt reviewer_body_digest_v1 mismatch"),
            ("reviewer_final_digest_v1", "receipt reviewer_final_digest_v1 mismatch"),
            ("evidence_envelope_digest_v1", "receipt evidence_envelope_digest_v1 mismatch"),
            ("p4_set_authority_digest_v1", "receipt p4_set_authority_digest_v1 mismatch"),
            ("receipt_digest_v1", "receipt digest mismatch or replay"),
        )
        for field, expected in candidate_fields:
            with self.subTest(surface="candidate", field=field):
                mutant = copy.deepcopy(self.bundle)
                candidate = mutant["envelope"]["reports"][0]["reviewer_final"]["candidates"][0]
                candidate[field] = _digest_placeholder()
                self._assert_contract_detail(self._validate(mutant), expected)
        for field, expected in receipt_fields:
            with self.subTest(surface="receipt", field=field):
                mutant = copy.deepcopy(self.bundle)
                mutant["receipts"]["receipts"][0][field] = _digest_placeholder()
                self._assert_contract_detail(self._validate(mutant), expected)


class MultiRecordAssignmentFixtureTests(unittest.TestCase):
    def test_committed_mixed_population_forms_two_batches_and_one_shared_carry_block(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(("git", "init", "-q"), cwd=root, check=True)
            subprocess.run(("git", "config", "user.email", "gate2@example.invalid"), cwd=root, check=True)
            subprocess.run(("git", "config", "user.name", "Gate2 Fixture"), cwd=root, check=True)
            row_values: list[tuple[str, ...]] = []
            dispositions = ["Retain"] * 22 + ["Correct"] + ["Carry"] * 3
            for index, disposition in enumerate(dispositions, start=1):
                values = list(_row(
                    claim=f"claim-{index:03d}", disposition=disposition,
                    destination="task.md" if disposition == "Carry" else "destination.md",
                ))
                values[8] = f"anchor-{index:03d}"
                row_values.append(tuple(values))
            ledger = _ledger(*row_values)
            rows = contract.parse_ledger_text(ledger)
            records = []
            for index, row in enumerate(sorted(rows, key=lambda item: item.claim_key_v1), start=1):
                records.append({
                    "record_id": f"g2r-{index:06d}", "status": "ACTIVE",
                    "identity_revision": 1, "claim_key_v1": row.claim_key_v1,
                    "subject_digest_v1": row.subject_digest_v1,
                })
            manifest = {
                "schema": "gate2-review-manifest/v1",
                "bootstrap_commit": contract.BOOTSTRAP_COMMIT,
                "records": records, "identity_transitions": [],
            }
            carry = (
                "### Gate 3 carried claims\n\n**Shared.** "
                + " ".join(
                    f"{{ledger-anchor: claim-{index:03d}}}" for index in range(24, 27)
                )
                + " complete shared block.\n\n"
            )
            (root / "destination.md").write_text(
                "# Destination\n\n## anchor-a\n", encoding="utf-8"
            )
            (root / "task.md").write_text(
                ledger + carry + _block(contract.MANIFEST_HEADING, manifest), encoding="utf-8"
            )
            subprocess.run(("git", "add", "destination.md", "task.md"), cwd=root, check=True)
            subprocess.run(("git", "commit", "-qm", "committed P3 fixture"), cwd=root, check=True)
            git = contract._Gate2Git.start(root)
            invocation = contract._Gate2Invocation(root, "task.md", git)
            _raw, _text, committed_rows, committed_manifest, carries = invocation.task_state(
                "working", None
            )
            self.assertEqual(set(carries), {"claim-024", "claim-025", "claim-026"})
            self.assertEqual(len({contract.raw_digest(value) for value in carries.values()}), 1)
            by_id, manifest_digest, ledger_digest, population_digest = contract.validate_manifest(
                committed_manifest, committed_rows, enforce_frozen_count=False
            )
            rows_by_key = {row.claim_key_v1: row for row in committed_rows}
            keys = sorted(rows_by_key)
            batches = []
            for ordinal, start in enumerate(range(0, len(keys), 25), start=1):
                claim_keys = keys[start : start + 25]
                batches.append({
                    "ordinal": f"{ordinal:03d}",
                    "batch_id": f"gate2-batch-v1:{ordinal:03d}:{contract.canonical_digest(claim_keys)}",
                    "reviewer_identity": {
                        "agent_id": "code-reviewer", "seat": f"row-{ordinal:03d}",
                        "task_id": f"row-task-{ordinal:03d}",
                    },
                    "record_ids": [
                        next(record_id for record_id, record in by_id.items()
                             if record["claim_key_v1"] == key)
                        for key in claim_keys
                    ],
                    "claim_keys": claim_keys,
                })
            assignment = {
                "schema": "gate2-review-assignment/v1", "review_round": 1,
                "reviewed_commit": git.pinned_head,
                "manifest_digest_v1": manifest_digest, "ledger_digest_v1": ledger_digest,
                "population_digest_v1": population_digest, "batches": batches,
            }
            git.bind_reviewed_commit(git.pinned_head)
            document_bytes = (root / "destination.md").read_bytes()
            document_oid = git.run("oid", git.pinned_head, "destination.md").decode().strip()
            for row in committed_rows:
                subject = row.as_subject()
                if row.disposition == "Carry":
                    destination = {
                        "kind": "CARRY_PARAGRAPH", "path": "task.md",
                        "anchor_locator": "{ledger-anchor: " + subject["claim_anchor"] + "}",
                        "blob_oid": None,
                        "content_digest_v1": contract.raw_digest(carries[subject["claim_anchor"]]),
                    }
                else:
                    destination = {
                        "kind": "DOCUMENT_FILE", "path": "destination.md",
                        "anchor_locator": subject["new_anchor"], "blob_oid": document_oid,
                        "content_digest_v1": contract.raw_digest(document_bytes),
                    }
                contract._validate_destination(invocation, row, destination, git.pinned_head)
            digest, by_batch = contract._validate_assignment(
                assignment, by_id, rows_by_key, manifest_digest, ledger_digest,
                population_digest, invocation,
            )
            self.assertTrue(contract.DIGEST_RE.fullmatch(digest))
            self.assertEqual(len(by_batch), 2)
            for field in ("seat", "task_id"):
                mutant = copy.deepcopy(assignment)
                mutant["batches"][1]["reviewer_identity"][field] = (
                    mutant["batches"][0]["reviewer_identity"][field]
                )
                with self.subTest(reused=field), self.assertRaises(contract.Gate2ContractError):
                    contract._validate_assignment(
                        mutant, by_id, rows_by_key, manifest_digest, ledger_digest,
                        population_digest, invocation,
                    )
            collision_destination = {
                "kind": "DOCUMENT_FILE", "path": "destination.md",
                "anchor_locator": "same", "blob_oid": document_oid,
                "content_digest_v1": contract.raw_digest(document_bytes),
            }
            with self.assertRaisesRegex(contract.Gate2ContractError, "collision"):
                contract._assert_unique_destination_locators({
                    "g2r-000001": {"destination": collision_destination},
                    "g2r-000002": {"destination": copy.deepcopy(collision_destination)},
                })
            unsafe = copy.deepcopy(collision_destination)
            unsafe["path"] = "../outside.md"
            with self.assertRaises(contract.Gate2ContractError):
                contract._validate_destination(
                    invocation, committed_rows[0], unsafe, git.pinned_head
                )
            missing = copy.deepcopy(collision_destination)
            missing["path"] = "missing.md"
            missing_values = list(committed_rows[0].values)
            missing_values[7] = "missing.md"
            missing_row = contract.LedgerRow(
                committed_rows[0].line_number, tuple(missing_values)
            )
            missing["anchor_locator"] = missing_row.as_subject()["new_anchor"]
            with self.assertRaisesRegex(contract.Gate2ContractError, "Git operation failed: show"):
                contract._validate_destination(
                    invocation, missing_row, missing, git.pinned_head
                )


class CommittedTwoBatchGate2FixtureTests(unittest.TestCase):
    """Exercise the complete public contract with two committed review batches."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temporary.name)
        self.task_path = "task.md"
        subprocess.run(("git", "init", "-q"), cwd=self.root, check=True)
        subprocess.run(
            ("git", "config", "user.email", "gate2@example.invalid"),
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ("git", "config", "user.name", "Gate2 Fixture"),
            cwd=self.root,
            check=True,
        )
        self.row_specs: list[tuple[str, str]] = [
            *( (f"claim-{index:03d}", "Retain") for index in range(1, 23) ),
            ("claim-023", "Correct"),
            *( (f"claim-{index:03d}", "Carry") for index in range(24, 27) ),
        ]
        # Every anchor the fixture's own rows name has to exist in the
        # destination, or the destination-resolution check reports the fixture
        # rather than the behaviour under test.
        (self.root / "destination.md").write_text(
            "# Destination\n\n## anchor-a\n\n"
            + "".join(f"## anchor-{claim}\n\n" for claim, _ in self.row_specs)
            + "Retain and corrected claims.\n",
            encoding="utf-8",
        )
        self.rows_not_run = self._rows()
        parsed = contract.parse_ledger_text(_ledger(*self.rows_not_run))
        records = []
        for index, row in enumerate(
            sorted(parsed, key=lambda item: item.claim_key_v1), start=1
        ):
            records.append(
                {
                    "record_id": f"g2r-{index:06d}",
                    "status": "ACTIVE",
                    "identity_revision": 1,
                    "claim_key_v1": row.claim_key_v1,
                    "subject_digest_v1": row.subject_digest_v1,
                }
            )
        self.manifest = {
            "schema": "gate2-review-manifest/v1",
            "bootstrap_commit": contract.BOOTSTRAP_COMMIT,
            "records": records,
            "identity_transitions": [],
        }
        self.carry_section = (
            "### Gate 3 carried claims\n\n**Shared.** Prefix owner. "
            + " ".join(
                f"{{ledger-anchor: claim-{index:03d}}}" for index in range(24, 27)
            )
            + " complete shared suffix.\n\n"
        )
        self._write_p3()
        subprocess.run(
            ("git", "add", "destination.md", self.task_path), cwd=self.root, check=True
        )
        subprocess.run(
            ("git", "commit", "-qm", "committed P3 two-batch fixture"),
            cwd=self.root,
            check=True,
        )
        self.reviewed_commit = subprocess.run(
            ("git", "rev-parse", "HEAD"),
            cwd=self.root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        self.bundle = self._build_bundle()
        self._write_final(self.bundle)
        subprocess.run(("git", "add", self.task_path), cwd=self.root, check=True)
        subprocess.run(
            ("git", "commit", "-qm", "committed P5 two-batch evidence"),
            cwd=self.root,
            check=True,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _rows(self, verdicts: dict[str, str] | None = None) -> list[tuple[str, ...]]:
        rows = []
        for claim, disposition in self.row_specs:
            values = list(
                _row(
                    claim=claim,
                    disposition=disposition,
                    destination=self.task_path if disposition == "Carry" else "destination.md",
                    review_verdict=(verdicts or {}).get(claim, "Not Run"),
                )
            )
            values[8] = f"anchor-{claim}"
            rows.append(tuple(values))
        return rows

    def _write_p3(self) -> None:
        text = _ledger(*self.rows_not_run)
        text += self.carry_section
        text += _block(contract.MANIFEST_HEADING, self.manifest)
        (self.root / self.task_path).write_text(text, encoding="utf-8")

    def _write_final(self, bundle: dict[str, object]) -> None:
        authority = bundle["receipts"]["p4_set_authority"]
        authority_digest = authority["set_authority_digest_v1"]
        by_record = {
            receipt["record_id"]: receipt
            for receipt in bundle["receipts"]["receipts"]
            if isinstance(receipt, dict) and isinstance(receipt.get("record_id"), str)
        }
        claim_by_record = {
            record["record_id"]: next(
                row.values[3]
                for row in contract.parse_ledger_text(_ledger(*self.rows_not_run))
                if row.claim_key_v1 == record["claim_key_v1"]
            )
            for record in self.manifest["records"]
        }
        verdicts = {
            claim_by_record[record_id]: (
                "SETTLED {gate2-receipt="
                + receipt["receipt_digest_v1"]
                + ";gate2-set-authority="
                + authority_digest
                + "}"
            )
            for record_id, receipt in by_record.items()
        }
        text = _ledger(*self._rows(verdicts))
        text += self.carry_section
        text += _block(contract.MANIFEST_HEADING, bundle["manifest"])
        text += _block(contract.ENVELOPE_HEADING, bundle["envelope"])
        text += _block(contract.RECEIPTS_HEADING, bundle["receipts"])
        (self.root / self.task_path).write_text(text, encoding="utf-8")

    def _build_bundle(self) -> dict[str, object]:
        rows = contract.parse_ledger_text(_ledger(*self.rows_not_run))
        by_id, manifest_digest, ledger_digest, population_digest = contract.validate_manifest(
            self.manifest, rows, enforce_frozen_count=False
        )
        rows_by_key = {row.claim_key_v1: row for row in rows}
        ids_by_key = {record["claim_key_v1"]: record_id for record_id, record in by_id.items()}
        keys = sorted(rows_by_key)
        batches = []
        for ordinal, start in enumerate(range(0, len(keys), 25), start=1):
            claim_keys = keys[start : start + 25]
            batches.append(
                {
                    "ordinal": f"{ordinal:03d}",
                    "batch_id": (
                        f"gate2-batch-v1:{ordinal:03d}:"
                        + contract.canonical_digest(claim_keys)
                    ),
                    "reviewer_identity": {
                        "agent_id": "code-reviewer",
                        "seat": f"row-{ordinal:03d}",
                        "task_id": f"row-task-{ordinal:03d}",
                    },
                    "record_ids": [ids_by_key[key] for key in claim_keys],
                    "claim_keys": claim_keys,
                }
            )
        assignment = {
            "schema": "gate2-review-assignment/v1",
            "review_round": 1,
            "reviewed_commit": self.reviewed_commit,
            "manifest_digest_v1": manifest_digest,
            "ledger_digest_v1": ledger_digest,
            "population_digest_v1": population_digest,
            "batches": batches,
        }
        assignment_digest = contract.canonical_digest(assignment)
        destination_bytes = (self.root / "destination.md").read_bytes()
        document_oid = subprocess.run(
            ("git", "rev-parse", f"{self.reviewed_commit}:destination.md"),
            cwd=self.root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        carry_blocks = contract._carried_blocks(
            (self.root / self.task_path).read_bytes()
        )
        reports = []
        for batch in batches:
            report_path = (
                ".superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/"
                f"task-10i-gate2-p4-row-review-{batch['ordinal']}.md"
            )
            reviewer = {**batch["reviewer_identity"], "report_path": report_path}
            body = f"reviewed batch {batch['ordinal']}"
            candidates = []
            for record_id, claim_key in zip(
                batch["record_ids"], batch["claim_keys"], strict=True
            ):
                row = rows_by_key[claim_key]
                record = by_id[record_id]
                if row.disposition == "Carry":
                    anchor = row.as_subject()["claim_anchor"]
                    destination = {
                        "kind": "CARRY_PARAGRAPH",
                        "path": self.task_path,
                        "anchor_locator": f"{{ledger-anchor: {anchor}}}",
                        "blob_oid": None,
                        "content_digest_v1": contract.raw_digest(carry_blocks[anchor]),
                    }
                else:
                    destination = {
                        "kind": "DOCUMENT_FILE",
                        "path": "destination.md",
                        "anchor_locator": row.as_subject()["new_anchor"],
                        "blob_oid": document_oid,
                        "content_digest_v1": contract.raw_digest(destination_bytes),
                    }
                candidate = {
                    "schema": "gate2-review-candidate/v1",
                    "review_round": 1,
                    "manifest_digest_v1": manifest_digest,
                    "ledger_digest_v1": ledger_digest,
                    "population_digest_v1": population_digest,
                    "record_id": record_id,
                    "identity_revision": 1,
                    "claim_key_v1": claim_key,
                    "subject_digest_v1": record["subject_digest_v1"],
                    "destination": destination,
                    "destination_digest_v1": contract.canonical_digest(destination),
                    "reviewer_identity": reviewer,
                    "reviewed_commit": self.reviewed_commit,
                    "batch_id": batch["batch_id"],
                    "reviewer_body": body,
                    "verdict": "SETTLED",
                    "basis": contract._expected_basis(row.disposition),
                    "finding_ids": [],
                    "assignment_digest_v1": assignment_digest,
                    "candidate_digest_v1": _digest_placeholder(),
                }
                candidate["candidate_digest_v1"] = contract.canonical_digest(
                    candidate, omit="candidate_digest_v1"
                )
                candidates.append(candidate)
            final = {
                "schema": "gate2-review-final/v1",
                "review_round": 1,
                "assignment_digest_v1": assignment_digest,
                "batch_id": batch["batch_id"],
                "reviewer_identity": reviewer,
                "reviewed_commit": self.reviewed_commit,
                "candidates": candidates,
                "batch_verdict": "SETTLED",
                "finding_ids": [],
            }
            reports.append(
                {
                    "report_path": report_path,
                    "report_bytes_digest_v1": contract.raw_digest(
                        f"row report {batch['ordinal']}".encode()
                    ),
                    "reviewer_body_digest_v1": contract.raw_digest(body.encode()),
                    "reviewer_final_digest_v1": contract.canonical_digest(final),
                    "reviewer_final": final,
                }
            )
        envelope = {
            "schema": "gate2-review-evidence-envelope/v1",
            "review_round": 1,
            "assignment": assignment,
            "assignment_digest_v1": assignment_digest,
            "reports": reports,
            "evidence_envelope_digest_v1": _digest_placeholder(),
        }
        envelope["evidence_envelope_digest_v1"] = contract.canonical_digest(
            envelope, omit="evidence_envelope_digest_v1"
        )
        members = [
            {
                "batch_id": report["reviewer_final"]["batch_id"],
                "report_path": report["report_path"],
                "report_bytes_digest_v1": report["report_bytes_digest_v1"],
                "reviewer_final_digest_v1": report["reviewer_final_digest_v1"],
                "record_ids": [
                    item["record_id"] for item in report["reviewer_final"]["candidates"]
                ],
                "candidate_digests_v1": [
                    item["candidate_digest_v1"]
                    for item in report["reviewer_final"]["candidates"]
                ],
            }
            for report in reports
        ]
        policy = {
            "review_kind": "POLICY",
            "agent_id": "rules-engineer",
            "role": "SPECIFICATION_POLICY",
            "seat": "p4-set-policy",
            "task_id": "set-policy-task",
            "report_path": ".superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/task-10i-gate2-p4-set-policy-review.md",
        }
        quality = {
            "review_kind": "QUALITY_SECURITY",
            "agent_id": "code-reviewer",
            "role": "QUALITY_SECURITY",
            "seat": "p4-set-quality-security",
            "task_id": "set-quality-task",
            "report_path": ".superpowers/sdd/2026-08-08-agentic-research-pack-rebuild/task-10i-gate2-p4-set-quality-security-review.md",
        }
        set_assignment = {
            "schema": "gate2-review-set-assignment/v1",
            "review_round": 1,
            "reviewed_commit": self.reviewed_commit,
            "row_assignment_digest_v1": assignment_digest,
            "evidence_envelope_digest_v1": envelope["evidence_envelope_digest_v1"],
            "members": members,
            "reviewers": [policy, quality],
            "set_assignment_digest_v1": _digest_placeholder(),
        }
        set_assignment["set_assignment_digest_v1"] = contract.canonical_digest(
            set_assignment, omit="set_assignment_digest_v1"
        )
        attestations = []
        for reviewer in (policy, quality):
            body = f"set reviewed {reviewer['review_kind']}"
            attestation = {
                "schema": "gate2-review-set-attestation/v1",
                "review_round": 1,
                "review_kind": reviewer["review_kind"],
                "reviewer_identity": reviewer,
                "reviewed_commit": self.reviewed_commit,
                "row_assignment_digest_v1": assignment_digest,
                "evidence_envelope_digest_v1": envelope["evidence_envelope_digest_v1"],
                "set_assignment_digest_v1": set_assignment["set_assignment_digest_v1"],
                "members": members,
                "reviewer_body": body,
                "reviewer_body_digest_v1": contract.raw_digest(body.encode()),
                "basis": {key: "PASS" for key in contract.SET_BASIS_KEYS},
                "verdict": "APPROVED",
                "critical": 0,
                "important": 0,
                "minor": 0,
                "finding_ids": [],
                "attestation_digest_v1": _digest_placeholder(),
            }
            attestation["attestation_digest_v1"] = contract.canonical_digest(
                attestation, omit="attestation_digest_v1"
            )
            attestations.append(
                {
                    "review_kind": reviewer["review_kind"],
                    "report_path": reviewer["report_path"],
                    "report_bytes_digest_v1": contract.raw_digest(
                        reviewer["review_kind"].encode()
                    ),
                    "attestation": attestation,
                }
            )
        authority = {
            "schema": "gate2-review-set-authority/v1",
            "review_round": 1,
            "set_assignment": set_assignment,
            "set_assignment_digest_v1": set_assignment["set_assignment_digest_v1"],
            "attestations": attestations,
            "set_authority_digest_v1": _digest_placeholder(),
        }
        authority["set_authority_digest_v1"] = contract.canonical_digest(
            authority, omit="set_authority_digest_v1"
        )
        reports_by_batch = {
            report["reviewer_final"]["batch_id"]: report for report in reports
        }
        receipts = []
        for report in reports:
            for candidate in report["reviewer_final"]["candidates"]:
                receipt = {
                    **{
                        key: copy.deepcopy(candidate[key])
                        for key in (
                            "manifest_digest_v1", "ledger_digest_v1", "population_digest_v1",
                            "record_id", "identity_revision", "claim_key_v1", "subject_digest_v1",
                            "destination", "destination_digest_v1", "reviewer_identity",
                            "reviewed_commit", "batch_id", "reviewer_body", "verdict", "basis",
                            "finding_ids", "assignment_digest_v1", "candidate_digest_v1",
                        )
                    },
                    "schema": "gate2-review-receipt/v1",
                    "review_round": 1,
                    "report_bytes_digest_v1": reports_by_batch[candidate["batch_id"]]["report_bytes_digest_v1"],
                    "reviewer_body_digest_v1": reports_by_batch[candidate["batch_id"]]["reviewer_body_digest_v1"],
                    "reviewer_final_digest_v1": reports_by_batch[candidate["batch_id"]]["reviewer_final_digest_v1"],
                    "evidence_envelope_digest_v1": envelope["evidence_envelope_digest_v1"],
                    "p4_set_authority_digest_v1": authority["set_authority_digest_v1"],
                    "receipt_digest_v1": _digest_placeholder(),
                }
                receipt["receipt_digest_v1"] = contract.canonical_digest(
                    receipt, omit="receipt_digest_v1"
                )
                receipts.append(receipt)
        receipts.sort(key=lambda item: item["record_id"])
        return {
            "manifest": copy.deepcopy(self.manifest),
            "envelope": envelope,
            "receipts": {
                "schema": "gate2-review-receipts/v1",
                "review_round": 1,
                "p4_set_authority": authority,
                "receipts": receipts,
            },
        }

    def _rehash(
        self,
        bundle: dict[str, object],
        *,
        preserve_set_members: bool = False,
    ) -> None:
        envelope = bundle["envelope"]
        assignment = envelope["assignment"]
        assignment_digest = contract.canonical_digest(assignment)
        envelope["assignment_digest_v1"] = assignment_digest
        candidates_by_id = {}
        reports_by_batch = {}
        for report in envelope["reports"]:
            final = report["reviewer_final"]
            final["assignment_digest_v1"] = assignment_digest
            for candidate in final["candidates"]:
                candidate["assignment_digest_v1"] = assignment_digest
                candidate["destination_digest_v1"] = contract.canonical_digest(
                    candidate["destination"]
                )
                candidate["candidate_digest_v1"] = contract.canonical_digest(
                    candidate, omit="candidate_digest_v1"
                )
                candidates_by_id[candidate["record_id"]] = candidate
            report["reviewer_final_digest_v1"] = contract.canonical_digest(final)
            reports_by_batch[final["batch_id"]] = report
        envelope["evidence_envelope_digest_v1"] = contract.canonical_digest(
            envelope, omit="evidence_envelope_digest_v1"
        )
        authority = bundle["receipts"]["p4_set_authority"]
        set_assignment = authority["set_assignment"]
        set_assignment["row_assignment_digest_v1"] = assignment_digest
        set_assignment["evidence_envelope_digest_v1"] = envelope[
            "evidence_envelope_digest_v1"
        ]
        for member in set_assignment["members"]:
            report = reports_by_batch.get(member["batch_id"])
            if report is not None and not preserve_set_members:
                final = report["reviewer_final"]
                member.update(
                    {
                        "report_path": report["report_path"],
                        "report_bytes_digest_v1": report["report_bytes_digest_v1"],
                        "reviewer_final_digest_v1": report["reviewer_final_digest_v1"],
                        "record_ids": [item["record_id"] for item in final["candidates"]],
                        "candidate_digests_v1": [
                            item["candidate_digest_v1"] for item in final["candidates"]
                        ],
                    }
                )
        set_assignment["set_assignment_digest_v1"] = contract.canonical_digest(
            set_assignment, omit="set_assignment_digest_v1"
        )
        authority["set_assignment_digest_v1"] = set_assignment[
            "set_assignment_digest_v1"
        ]
        for wrapper, reviewer in zip(
            authority["attestations"], set_assignment["reviewers"], strict=True
        ):
            attestation = wrapper["attestation"]
            attestation.update(
                {
                    "reviewer_identity": copy.deepcopy(reviewer),
                    "row_assignment_digest_v1": assignment_digest,
                    "evidence_envelope_digest_v1": envelope[
                        "evidence_envelope_digest_v1"
                    ],
                    "set_assignment_digest_v1": set_assignment[
                        "set_assignment_digest_v1"
                    ],
                    "members": copy.deepcopy(set_assignment["members"]),
                }
            )
            attestation["attestation_digest_v1"] = contract.canonical_digest(
                attestation, omit="attestation_digest_v1"
            )
        authority["set_authority_digest_v1"] = contract.canonical_digest(
            authority, omit="set_authority_digest_v1"
        )
        for receipt in bundle["receipts"]["receipts"]:
            candidate = candidates_by_id.get(receipt["record_id"])
            if candidate is None:
                continue
            report = reports_by_batch[candidate["batch_id"]]
            for key in (
                "manifest_digest_v1", "ledger_digest_v1", "population_digest_v1", "record_id",
                "identity_revision", "claim_key_v1", "subject_digest_v1", "destination",
                "destination_digest_v1", "reviewer_identity", "reviewed_commit", "batch_id",
                "reviewer_body", "verdict", "basis", "finding_ids", "assignment_digest_v1",
                "candidate_digest_v1",
            ):
                receipt[key] = copy.deepcopy(candidate[key])
            receipt.update(
                {
                    "report_bytes_digest_v1": report["report_bytes_digest_v1"],
                    "reviewer_body_digest_v1": report["reviewer_body_digest_v1"],
                    "reviewer_final_digest_v1": report["reviewer_final_digest_v1"],
                    "evidence_envelope_digest_v1": envelope[
                        "evidence_envelope_digest_v1"
                    ],
                    "p4_set_authority_digest_v1": authority[
                        "set_authority_digest_v1"
                    ],
                }
            )
            receipt["receipt_digest_v1"] = contract.canonical_digest(
                receipt, omit="receipt_digest_v1"
            )

    def _validate(self, bundle: dict[str, object]) -> contract.Gate2Result:
        self._write_final(bundle)
        subprocess.run(("git", "add", self.task_path), cwd=self.root, check=True)
        subprocess.run(
            ("git", "commit", "--allow-empty", "-qm", "two-batch mutation"),
            cwd=self.root,
            check=True,
        )
        return contract.validate_gate2_contract(
            self.root, self.task_path, enforce_frozen_count=False
        )

    def test_full_committed_two_batch_bundle_is_green(self) -> None:
        result = contract.validate_gate2_contract(
            self.root, self.task_path, enforce_frozen_count=False
        )
        self.assertEqual(result.findings, ())
        self.assertEqual(
            (result.ledger_records, result.population_records, result.settled, result.held),
            (26, 26, 26, 0),
        )
        self.assertEqual(len(self.bundle["envelope"]["reports"]), 2)
        carries = contract._carried_blocks((self.root / self.task_path).read_bytes())
        self.assertEqual(set(carries), {"claim-024", "claim-025", "claim-026"})
        self.assertEqual(len({contract.raw_digest(value) for value in carries.values()}), 1)

    def test_marker_population_is_censused_in_all_three_task_states(self) -> None:
        task = self.root / self.task_path
        text = task.read_text(encoding="utf-8")
        cases = (
            (
                "missing section",
                "",
                "expected one '### Gate 3 carried claims' heading, found 0",
            ),
            (
                "duplicate section",
                self.carry_section + "### Gate 3 carried claims\n\n",
                "expected one '### Gate 3 carried claims' heading, found 2",
            ),
            (
                "unknown marker",
                self.carry_section.replace(
                    " complete shared suffix.",
                    " {ledger-anchor: UNKNOWN} complete shared suffix.",
                ),
                "Carry marker population has unknown or unserved rows",
            ),
            (
                "fenced marker",
                self.carry_section.replace(
                    "**Shared.",
                    "```text\n{ledger-anchor: UNKNOWN}\n```\n\n**Shared.",
                ),
                "Carry marker occurs outside a carried block",
            ),
            (
                "outside marker",
                self.carry_section.replace(
                    "**Shared.", "plain {ledger-anchor: UNKNOWN}\n\n**Shared."
                ),
                "Carry marker occurs outside a carried block",
            ),
            (
                "duplicate marker",
                self.carry_section.replace(
                    " complete shared suffix.",
                    " {ledger-anchor: claim-024} complete shared suffix.",
                ),
                "duplicate Carry marker in Gate 3 section",
            ),
            (
                "noncanonical spacing",
                self.carry_section.replace(
                    "{ledger-anchor: claim-024}", "{ledger-anchor:claim-024}"
                ),
                "Carry marker spacing is not canonical",
            ),
            (
                "cross-block duplicate",
                self.carry_section.replace(
                    " complete shared suffix.",
                    " complete shared suffix.\n\n**Second.** "
                    "{ledger-anchor: claim-024}",
                ),
                "marker occurs in multiple blocks: claim-024",
            ),
        )
        for label, carry_section, expected in cases:
            with self.subTest(label=label):
                task.write_text(
                    text.replace(self.carry_section, carry_section, 1),
                    encoding="utf-8",
                )
                subprocess.run(
                    ("git", "add", self.task_path), cwd=self.root, check=True
                )
                subprocess.run(
                    ("git", "commit", "--allow-empty", "-qm", label),
                    cwd=self.root,
                    check=True,
                )
                result = contract.validate_gate2_contract(
                    self.root, self.task_path, enforce_frozen_count=False
                )
                self.assertEqual(len(result.findings), 1)
                self.assertEqual(result.findings[0].code, "GATE2-CONTRACT")
                self.assertEqual(result.findings[0].detail, expected)
                completed = subprocess.run(
                    (
                        sys.executable,
                        str(pathlib.Path(contract.__file__).resolve()),
                        "--root", str(self.root), "--task", self.task_path,
                    ),
                    check=False,
                    capture_output=True,
                )
                self.assertEqual(completed.returncode, 1)
                self.assertEqual(completed.stderr, b"")
                self.assertIn(expected.encode(), completed.stdout)
                self.assertNotIn(b"Traceback", completed.stdout)

    def test_dependency_consistent_two_batch_kill_matrix(self) -> None:
        mutations = (
            (
                "cross-batch gap",
                lambda b: b["envelope"]["assignment"]["batches"][0]["claim_keys"].pop(),
                "assignment batch order/membership mismatch",
                False,
            ),
            (
                "cross-batch overlap",
                lambda b: b["envelope"]["assignment"]["batches"][1]["claim_keys"].append(
                    b["envelope"]["assignment"]["batches"][0]["claim_keys"][0]
                ),
                "assignment batch order/membership mismatch",
                False,
            ),
            (
                "cross-batch substitution",
                lambda b: b["envelope"]["assignment"]["batches"][1]["record_ids"].__setitem__(
                    0, b["envelope"]["assignment"]["batches"][0]["record_ids"][0]
                ),
                "assignment record/key positional mismatch",
                False,
            ),
            (
                "candidate replay",
                lambda b: b["envelope"]["reports"][1]["reviewer_final"]["candidates"].append(
                    copy.deepcopy(
                        b["envelope"]["reports"][0]["reviewer_final"]["candidates"][0]
                    )
                ),
                "candidate replay/cross-batch duplicate",
                False,
            ),
            (
                "report reorder",
                lambda b: b["envelope"]["reports"].reverse(),
                "reports are reordered or duplicated",
                False,
            ),
            (
                "receipt duplicate",
                lambda b: b["receipts"]["receipts"].append(
                    copy.deepcopy(b["receipts"]["receipts"][0])
                ),
                "receipts missing, extra, duplicated, or reordered",
                False,
            ),
            (
                "set member overlap",
                lambda b: b["receipts"]["p4_set_authority"]["set_assignment"]["members"][1]["record_ids"].__setitem__(
                    0,
                    b["receipts"]["p4_set_authority"]["set_assignment"]["members"][0]["record_ids"][0],
                ),
                "set member record overlap",
                True,
            ),
            (
                "set member gap",
                lambda b: b["receipts"]["p4_set_authority"]["set_assignment"]["members"][1].__setitem__(
                    "record_ids", []
                ),
                "set member population gap",
                True,
            ),
        )
        for label, mutate, expected, preserve_set_members in mutations:
            with self.subTest(label=label):
                mutant = copy.deepcopy(self.bundle)
                mutate(mutant)
                self._rehash(mutant, preserve_set_members=preserve_set_members)
                result = self._validate(mutant)
                self.assertEqual(result.findings[0].code, "GATE2-CONTRACT")
                self.assertEqual(result.findings[0].detail, expected)

    def test_dependency_consistent_provenance_and_disposition_kills(self) -> None:
        for disposition in ("Retain", "Correct", "Carry"):
            with self.subTest(disposition=disposition):
                mutant = copy.deepcopy(self.bundle)
                candidate = next(
                    item
                    for report in mutant["envelope"]["reports"]
                    for item in report["reviewer_final"]["candidates"]
                    if contract.parse_ledger_text(_ledger(*self.rows_not_run))[
                        next(
                            index
                            for index, row in enumerate(
                                contract.parse_ledger_text(_ledger(*self.rows_not_run))
                            )
                            if row.claim_key_v1 == item["claim_key_v1"]
                        )
                    ].disposition == disposition
                )
                candidate["basis"]["destination_resolution"] = "FAIL"
                self._rehash(mutant)
                result = self._validate(mutant)
                self.assertEqual(result.findings[0].code, "GATE2-CONTRACT")
                self.assertEqual(
                    result.findings[0].detail, "candidate verdict/basis mismatch"
                )

        report_provenance = copy.deepcopy(self.bundle)
        report = report_provenance["envelope"]["reports"][0]
        substituted_path = report["report_path"].replace("001.md", "999.md")
        report["report_path"] = substituted_path
        report["reviewer_final"]["reviewer_identity"]["report_path"] = substituted_path
        for candidate in report["reviewer_final"]["candidates"]:
            candidate["reviewer_identity"]["report_path"] = substituted_path
        self._rehash(report_provenance)
        result = self._validate(report_provenance)
        self.assertEqual(result.findings[0].code, "GATE2-CONTRACT")
        self.assertEqual(
            result.findings[0].detail,
            "row report path does not match its batch ordinal",
        )

        missing_destination = copy.deepcopy(self.bundle)
        retained_candidate = next(
            candidate
            for report in missing_destination["envelope"]["reports"]
            for candidate in report["reviewer_final"]["candidates"]
            if candidate["destination"]["kind"] == "DOCUMENT_FILE"
        )
        retained_candidate["destination"]["path"] = "missing.md"
        self._rehash(missing_destination)
        result = self._validate(missing_destination)
        self.assertEqual(result.findings[0].code, "GATE2-CONTRACT")
        self.assertEqual(result.findings[0].detail, "Git operation failed: show")
        completed = subprocess.run(
            (
                sys.executable,
                str(pathlib.Path(contract.__file__).resolve()),
                "--root", str(self.root), "--task", self.task_path,
            ),
            check=False,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stderr, b"")
        self.assertIn(b"Git operation failed: show", completed.stdout)
        self.assertNotIn(b"Traceback", completed.stdout)

        receipt_provenance = copy.deepcopy(self.bundle)
        receipt = receipt_provenance["receipts"]["receipts"][0]
        receipt["report_bytes_digest_v1"] = _digest_placeholder()
        receipt["receipt_digest_v1"] = contract.canonical_digest(
            receipt, omit="receipt_digest_v1"
        )
        result = self._validate(receipt_provenance)
        self.assertEqual(result.findings[0].code, "GATE2-CONTRACT")
        self.assertEqual(
            result.findings[0].detail,
            "receipt report_bytes_digest_v1 mismatch",
        )


class LiveGate2ExpectedRedTests(unittest.TestCase):
    def test_live_mode_is_expected_red_until_p3_and_p5_evidence(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        result = contract.validate_gate2_contract(
            root, contract.TASK_PATH
        )
        self.assertEqual((result.ledger_records, result.population_records), (253, 150))
        self.assertEqual((result.settled, result.held), (0, 150))
        self.assertEqual(result.findings[-1].code, "GATE2-CONTRACT")
        self.assertEqual(
            result.findings[-1].detail,
            "current committed Task lacks the canonical manifest",
        )

    def test_every_gate2_destination_resolves(self) -> None:
        """The 2026-08-28 pack overwrite, now repaired, held as a fact.

        This test previously asserted the defect: 148 unresolved anchors across
        111 of the 150 rows, after `bbe8d9f3` wrote an independently authored
        draft over the successor pack at the same path. It was written to fail
        when the regression was repaired, so that whoever repaired it had to
        come here and say so rather than let the number drift quietly.

        Repaired 2026-08-29 by restoring the pack from `49522aa1` and merging
        the draft's own sections on top, so both bodies survive. The assertion
        is now the one that matters: every gate-2 destination resolves, and any
        future overwrite turns this red again.
        """

        root = pathlib.Path(__file__).resolve().parents[2]
        result = contract.validate_gate2_contract(root, contract.TASK_PATH)
        destination = [
            finding
            for finding in result.findings
            if finding.code.startswith("GATE2-DEST-")
        ]
        self.assertEqual(destination, [], "a gate-2 destination stopped resolving")


class DestinationResolutionTests(unittest.TestCase):
    """`resolve_destinations` is the machine-checkable half of gate 2.

    Whether a destination is the *right* one for a claim is a reading and stays
    with a seat. Whether it exists at all is not, and nothing checked it: the
    destination column is prose in a table cell, so the link checker has no link
    to follow, and this contract stopped at the absent manifest before reaching
    a destination. Six days of a 111-row regression went unreported that way.
    """

    def _row(self, new_path: str, new_anchor: str) -> contract.LedgerRow:
        values = ["" for _ in contract.LEDGER_HEADERS]
        values[5] = "Retain"
        values[7] = new_path
        values[8] = new_anchor
        return contract.LedgerRow(line_number=1, values=tuple(values))

    def test_a_resolving_destination_produces_no_finding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "leaf.md").write_text("## Present heading\n", encoding="utf-8")
            row = self._row("`leaf.md`", "`Present heading`")
            self.assertEqual(contract.resolve_destinations(root, [row]), ())

    def test_an_absent_anchor_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "leaf.md").write_text("## Present heading\n", encoding="utf-8")
            row = self._row("`leaf.md`", "`Absent heading`")
            findings = contract.resolve_destinations(root, [row])
            self.assertEqual([f.code for f in findings], ["GATE2-DEST-MISSING-ANCHOR"])

    def test_an_absent_file_is_reported_once_not_per_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            row = self._row("`gone.md`", "`One` and `Two`")
            findings = contract.resolve_destinations(pathlib.Path(tmp), [row])
            self.assertEqual([f.code for f in findings], ["GATE2-DEST-MISSING-FILE"])

    def test_a_cell_naming_no_file_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            row = self._row("the owning Task", "`Anything`")
            findings = contract.resolve_destinations(pathlib.Path(tmp), [row])
            self.assertEqual([f.code for f in findings], ["GATE2-DEST-UNNAMED"])

    def test_every_anchor_of_a_multi_anchor_cell_is_checked(self) -> None:
        """One resolving anchor must not vouch for its neighbours."""

        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "leaf.md").write_text("## Present\n", encoding="utf-8")
            row = self._row("`leaf.md`", "`Present`; `Absent`")
            findings = contract.resolve_destinations(root, [row])
            self.assertEqual(len(findings), 1)
            self.assertIn("Absent", findings[0].detail)


class DestinationExtractionFidelityTests(unittest.TestCase):
    """The extraction is validated in the direction that can produce a false red.

    A path-and-anchor scraper that under-matches would report absent
    destinations that are really present, and the whole 111-row finding would be
    a parsing artefact. It is not: replayed against the pack at `49522aa1`,
    where the migration destinations were authored, the identical extraction
    resolves every one of the 150 gate-2 rows. So a token it cannot find at HEAD
    is an absent destination and not a token it cannot parse.
    """

    PACK = "docs/90.references/research/0002-agentic-engineering-research-pack"
    AUTHORED = "49522aa1"

    def test_all_150_destinations_resolve_against_the_authored_pack(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        listing = subprocess.run(
            ["git", "-C", str(root), "ls-tree", "-r", "--name-only",
             self.AUTHORED, "--", self.PACK],
            capture_output=True, text=True, check=False,
        )
        if listing.returncode != 0 or not listing.stdout.strip():
            self.skipTest(f"commit {self.AUTHORED} is unavailable in this clone")
        with tempfile.TemporaryDirectory() as tmp:
            replay = pathlib.Path(tmp)
            (replay / self.PACK).mkdir(parents=True)
            for relative in listing.stdout.split():
                blob = subprocess.run(
                    ["git", "-C", str(root), "show", f"{self.AUTHORED}:{relative}"],
                    capture_output=True, text=True, check=True,
                )
                (replay / relative).write_text(blob.stdout, encoding="utf-8")
            # The 39 Carry rows destine to the owning Task itself, so the replay
            # root needs today's Task beside the authored pack. Only the pack is
            # rolled back; the ledger under test stays the current one.
            task_text = (root / contract.TASK_PATH).read_text(encoding="utf-8")
            (replay / contract.TASK_PATH).parent.mkdir(parents=True, exist_ok=True)
            (replay / contract.TASK_PATH).write_text(task_text, encoding="utf-8")
            rows = [
                row
                for row in contract.parse_ledger_text(task_text)
                if row.disposition in contract.GATE2_DISPOSITIONS
            ]
            self.assertEqual(len(rows), 150)
            self.assertEqual(contract.resolve_destinations(replay, rows), ())


class CarriedBlockWrapperTests(unittest.TestCase):
    """The one behaviour this port changed, pinned in both directions.

    The branch required a carried block to begin with a bolded lead. Stage 00
    later required historical quotations retained in current Markdown to be a
    contiguous blockquote opening with an exact sentence
    (`docs/00.agent-governance/policies/documentation-protocol.md:44`), and five
    carried blocks in the owning Task now use it, so the branch's rule rejected
    the corpus it was ported onto. A Stage 00 policy outranks this module's
    assumption about how a block starts, so the wrapper is accepted -- but the
    widening has to stop exactly there, which is what the second test holds.
    """

    WRAPPER = contract.HISTORICAL_EVIDENCE_WRAPPER

    def test_the_registered_historical_wrapper_is_a_carried_block(self) -> None:
        block = self.WRAPPER + b"> **Lead.** body\n"
        self.assertTrue(contract._is_carried_block(block))

    def test_a_bare_bolded_block_is_still_a_carried_block(self) -> None:
        self.assertTrue(contract._is_carried_block(b"**Lead.** body\n"))

    def test_nothing_else_becomes_a_carried_block(self) -> None:
        """A quote that is not the registered wrapper, or whose lead is not
        bolded, must still be rejected. Accepting either would let a marker sit
        in prose and be silently counted as a carried claim."""
        rejected = (
            b"> Some other quotation:\n> **Lead.** body\n",
            self.WRAPPER + b"> plain body, no bolded lead\n",
            self.WRAPPER.rstrip(b"\n") + b" trailing\n> **Lead.** body\n",
            b"ordinary paragraph carrying a marker\n",
            b"> **Lead.** bolded but not the registered wrapper\n",
        )
        for block in rejected:
            with self.subTest(block=block[:40]):
                self.assertFalse(contract._is_carried_block(block))


if __name__ == "__main__":
    unittest.main()
