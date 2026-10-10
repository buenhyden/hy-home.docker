from __future__ import annotations

import contextlib
import copy
import io
import json
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from scripts.lib.supply_chain.latest_version_gate import evaluate
from scripts.lib.supply_chain.security_update_gate import assess

NOW = datetime(2026, 10, 10, 10, tzinfo=UTC)
DIGEST = "sha256:" + "a" * 64


def latest_row():
    return {
        "service": "openbao",
        "scope": "root",
        "target_version": "2.7.1",
        "latest_version": "2.7.1",
        "channel": "stable",
        "checked_at": NOW.isoformat(),
        "release_url": "https://github.com/openbao/openbao/releases/tag/v2.7.1",
    }


def security_row():
    return {
        "service": "openbao",
        "scope": "root",
        "compose_file": "infra/03-security/openbao/docker-compose.yml",
        "current_version": "2.6.2",
        "candidate_version": "2.7.1",
        "candidate_image": "openbao/openbao:2.7.1@" + DIGEST,
        "affected_confirmed": True,
        "advisory_urls": ["https://openbao.org/docs/"],
        "reviewed_at": NOW.isoformat(),
        "scan_at": NOW.isoformat(),
        "scan_digest": DIGEST,
        "compatibility": "pass",
        "recovery": "pass",
        "residual_disposition": "approved",
        "decision": "patch",
    }


class LatestVersionGateTests(unittest.TestCase):
    def test_empty_expected_never_ready(self):
        with self.assertRaises(ValueError):
            evaluate([], [], NOW)

    def test_complete_evidence_is_not_deployment(self):
        result = evaluate([latest_row()], ["openbao"], NOW)
        self.assertTrue(result["ready"])
        self.assertFalse(result["deployed"])
        self.assertFalse(result["verified_external_facts"])

    def test_missing_unexpected_and_version_mismatch(self):
        row = latest_row()
        row["target_version"] = "2.6.4"
        result = evaluate([row], ["n8n"], NOW)
        self.assertEqual(["n8n"], result["missing_services"])
        self.assertEqual(["openbao"], result["unexpected_services"])
        self.assertIn("latest_mismatch", result["entries"][0]["missing"])

    def test_malformed_expected_rejected(self):
        for names in [[None], [True], ["a", "a"], ["../lab"], "a"]:
            with self.subTest(names=names), self.assertRaises(ValueError):
                evaluate([], names, NOW)

    def test_invalid_rows_are_safe(self):
        for row in [
            None,
            {},
            dict(latest_row(), scope="lab"),
            dict(latest_row(), service="../a"),
        ]:
            with self.subTest(row=row), self.assertRaises(ValueError):
                evaluate([row], ["openbao"], NOW)

    def test_freshness_channel_reference_are_required(self):
        for field, value in [
            ("checked_at", "bad"),
            ("checked_at", "2026-10-12T10:00:00Z"),
            ("channel", "beta"),
            ("release_url", "https://user:pass@example.org/x"),
            ("release_url", "https://[bad"),
            ("latest_version", "latest"),
            ("latest_version", "15.19.0.005-test-2"),
            ("latest_version", "2.7.2-rc1"),
        ]:
            row = dict(latest_row(), **{field: value})
            self.assertFalse(evaluate([row], ["openbao"], NOW)["ready"])

    def test_claimed_stable_test_tag_is_rejected(self):
        for version in ["15.19.0.005-test-2", "2.7.2-rc1", "nightly", "stable"]:
            row = dict(latest_row(), latest_version=version, target_version=version)
            self.assertFalse(evaluate([row], ["openbao"], NOW)["ready"])

    def test_does_not_mutate_rows(self):
        rows = [latest_row()]
        original = copy.deepcopy(rows)
        evaluate(rows, ["openbao"], NOW)
        self.assertEqual(original, rows)


class SecurityUpdateGateTests(unittest.TestCase):
    def test_complete_patch_evidence(self):
        result = assess([security_row()], NOW)
        self.assertEqual(
            "ledger-complete-pending-independent-verification",
            result["entries"][0]["status"],
        )
        self.assertFalse(result["deployed"])
        self.assertFalse(result["verified_external_facts"])

    def test_every_required_evidence_field_blocks(self):
        for field in [
            "advisory_urls",
            "scan_at",
            "reviewed_at",
            "scan_digest",
            "compatibility",
            "recovery",
            "residual_disposition",
            "candidate_image",
            "affected_confirmed",
        ]:
            row = security_row()
            row.pop(field)
            self.assertEqual(
                "blocked-evidence", assess([row], NOW)["entries"][0]["status"]
            )

    def test_digest_version_freshness_boundaries(self):
        for field, value in [
            ("scan_digest", "sha256:" + "b" * 64),
            ("candidate_version", "2.5.0"),
            ("scan_at", "2026-10-12T00:00:00Z"),
            ("scan_at", "2026-08-01T00:00:00Z"),
            ("candidate_image", "@" + DIGEST),
            ("candidate_version", "latest"),
        ]:
            row = dict(security_row(), **{field: value})
            self.assertEqual(
                "blocked-evidence", assess([row], NOW)["entries"][0]["status"]
            )

    def test_invalid_scope_duplicate_and_input_rejected(self):
        for rows in [
            [],
            [None],
            [security_row(), security_row()],
            [dict(security_row(), compose_file="infra/../../labs/a.yml")],
            [dict(security_row(), compose_file=None)],
            [dict(security_row(), scope="lab")],
        ]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                assess(rows, NOW)
        with self.assertRaises(ValueError):
            assess([security_row()], NOW, freshness_days=True)

    def test_not_affected_requires_explicit_false_reason(self):
        row = dict(security_row(), decision="not-affected", affected_confirmed=False)
        self.assertEqual("blocked-evidence", assess([row], NOW)["entries"][0]["status"])
        row["reason"] = "Reviewed installed package and applicable feature boundary."
        self.assertEqual(
            "ledger-complete-pending-independent-verification",
            assess([row], NOW)["entries"][0]["status"],
        )
        row["affected_confirmed"] = None
        self.assertEqual("blocked-evidence", assess([row], NOW)["entries"][0]["status"])

    def test_no_fix_is_blocked_and_unknown_is_not_safe(self):
        self.assertEqual(
            "blocked-no-fix",
            assess([dict(security_row(), decision="no-fix")], NOW)["entries"][0][
                "status"
            ],
        )
        self.assertEqual(
            "blocked-evidence",
            assess([dict(security_row(), decision="unknown")], NOW)["entries"][0][
                "status"
            ],
        )

    def test_invalid_advisory_is_safe(self):
        row = dict(security_row(), advisory_urls=["https://[bad"])
        self.assertEqual("blocked-evidence", assess([row], NOW)["entries"][0]["status"])

    def test_does_not_mutate_rows(self):
        rows = [security_row()]
        original = copy.deepcopy(rows)
        assess(rows, NOW)
        self.assertEqual(original, rows)


class UpdateEvidencePackageTests(unittest.TestCase):
    def test_source_membership_and_operational_boundaries_remain_explicit(self):
        root = Path(__file__).resolve().parents[3]
        package = root / "infra/09-platform-ops/security-updates"
        ledger = json.loads((package / "update-ledger.json").read_text())
        self.assertEqual(
            set(ledger["expected_services"]), {r["service"] for r in ledger["entries"]}
        )
        self.assertFalse(ledger["deployed"])
        self.assertFalse(ledger["verified_external_facts"])
        for row in ledger["entries"]:
            self.assertEqual("root", row["scope"])
            self.assertTrue(row["compose_file"].startswith("infra/"))
            self.assertEqual("NOT_RUN", row["deployment"])
            self.assertEqual("NOT_RUN", row["sbom_scan"])
            self.assertEqual("SEC01", row["blocker"]["owner"])
            discovered = datetime.fromisoformat(row["blocker"]["discovered_at"])
            due = datetime.fromisoformat(row["blocker"]["next_validation_due"])
            self.assertGreater(due, discovered)
            self.assertLessEqual((due - discovered).days, 7)
        self.assertFalse(
            evaluate(ledger["entries"], ledger["expected_services"])["ready"]
        )


class IndependentInventoryTests(unittest.TestCase):
    def test_deleting_both_submitted_arrays_cannot_shrink_cli_scope(self):
        from scripts.lib.supply_chain import latest_version_gate, security_update_gate

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            leaf = root / "infra/service/docker-compose.yml"
            leaf.parent.mkdir(parents=True)
            leaf.write_text("services:\n  openbao: {}\n  n8n: {}\n")
            (root / "docker-compose.yml").write_text(
                "include:\n  - infra/service/docker-compose.yml\n"
            )
            path = root / "submitted.json"
            for module, row in [
                (latest_version_gate, latest_row()),
                (security_update_gate, security_row()),
            ]:
                row = dict(
                    row,
                    checked_at=datetime.now(UTC).isoformat(),
                    reviewed_at=datetime.now(UTC).isoformat(),
                    scan_at=datetime.now(UTC).isoformat(),
                )
                path.write_text(
                    json.dumps({"entries": [row], "expected_services": ["openbao"]})
                )
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(
                        2, module.main(["--input", str(path), "--repo-root", str(root)])
                    )
                self.assertEqual(
                    ["n8n"], json.loads(output.getvalue())["missing_services"]
                )

    def test_self_attested_patch_is_never_rollout_ready(self):
        result = assess([security_row()], NOW)
        self.assertEqual(
            "ledger-complete-pending-independent-verification",
            result["entries"][0]["status"],
        )


class GateCLITests(unittest.TestCase):
    def test_cli_valid_and_invalid_inputs_do_not_echo_payload(self):
        from scripts.lib.supply_chain import latest_version_gate, security_update_gate

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.json"
            for module, doc in [
                (
                    latest_version_gate,
                    {"entries": [latest_row()], "expected_services": ["openbao"]},
                ),
                (security_update_gate, {"entries": [security_row()]}),
            ]:
                with self.subTest(module=module.__name__):
                    doc["entries"][0]["checked_at"] = "2000-01-01T00:00:00Z"
                    doc["entries"][0]["reviewed_at"] = "2000-01-01T00:00:00Z"
                    path.write_text(json.dumps(doc))
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(2, module.main(["--input", str(path)]))
                    path.write_text("PRIVATE_INPUT_BAD_JSON")
                    errors = io.StringIO()
                    with contextlib.redirect_stderr(errors):
                        self.assertEqual(2, module.main(["--input", str(path)]))
                    self.assertNotIn("PRIVATE_INPUT_BAD_JSON", errors.getvalue())

    def test_now_and_freshness_type_validation(self):
        for bad_now in ["now", datetime(2026, 10, 10)]:
            with self.assertRaises(ValueError):
                evaluate([latest_row()], ["openbao"], bad_now)
            with self.assertRaises(ValueError):
                assess([security_row()], bad_now)
        for days in [0, "7", -1]:
            with self.assertRaises(ValueError):
                assess([security_row()], NOW, days)


if __name__ == "__main__":
    unittest.main()
