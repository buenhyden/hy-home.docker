from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import re
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from scripts.lib.supply_chain.latest_version_gate import evaluate
from scripts.lib.supply_chain.security_update_gate import assess

NOW = datetime(2026, 10, 10, 10, tzinfo=UTC)
DIGEST = "sha256:" + "a" * 64


def replay_service_refreshes(initial, refreshes):
    current = set(initial)
    for refresh in refreshes:
        current.difference_update(refresh.get("removed_services", []))
        current.update(refresh.get("added_services", []))
    return current


def assert_public_observation_consistency(testcase, report, names):
    rows = report["observations"]
    observed = [row for row in rows if row["result"] == "OBSERVED"]
    failed = [row for row in rows if row["result"] == "ACCESS_FAILED"]
    testcase.assertEqual(len(rows), len(observed) + len(failed))
    testcase.assertEqual(len(observed), report["observed_source_count"])
    testcase.assertEqual(len(failed), report["failed_source_count"])
    related = {name for row in rows for name in row["related_root_services"]}
    testcase.assertLessEqual(related, names)
    testcase.assertEqual(len(related), report["services_with_related_source"])
    testcase.assertEqual(
        sorted(names - related), report["services_without_related_source"]
    )
    start = datetime.fromisoformat(report["observation_window_start_utc"])
    end = datetime.fromisoformat(report["observation_window_end_utc"])
    testcase.assertIsNotNone(start.tzinfo)
    testcase.assertLessEqual(start, end)
    for row in rows:
        checked = datetime.fromisoformat(row["checked_at_utc"])
        testcase.assertIsNotNone(checked.tzinfo)
        testcase.assertLessEqual(start, checked)
        testcase.assertLessEqual(checked, end)
        freshness = row["source_cache_freshness"]
        testcase.assertTrue(
            freshness in {"today", "yesterday", "UNKNOWN"}
            or re.fullmatch(r"[1-9][0-9]* (?:day|week|month|year)s? ago", freshness)
        )
        testcase.assertIs(row["freshness_verified"], False)
        testcase.assertIs(row["stable_channel_verified"], False)
        testcase.assertIs(row["oci_availability_verified"], False)
        if row["result"] == "ACCESS_FAILED":
            testcase.assertEqual("UNKNOWN", row["source_cache_freshness"])
            testcase.assertIsNone(row["resolved_url"])
            testcase.assertIsNone(row["observed_release_tag"])
        elif "/releases/latest" in row["query_url"]:
            testcase.assertTrue(row["resolved_url"].startswith("https://github.com/"))
            testcase.assertIn("/releases/tag/", row["resolved_url"])
            testcase.assertEqual(
                row["resolved_url"].split("/releases/tag/", 1)[1],
                row["observed_release_tag"],
            )
        else:
            testcase.assertIsNone(row["observed_release_tag"])


class StableScannerContractTests(unittest.TestCase):
    def test_current_readiness_binds_exact_registry_and_tool_identities(self):
        root = Path(__file__).resolve().parents[3]
        raw = (root / "infra/supply-chain.tool-images.json").read_bytes()
        registry = json.loads(raw)
        readiness = json.loads(
            (
                root / "infra/09-platform-ops/security-updates/tool-readiness.json"
            ).read_text()
        )
        self.assertEqual(hashlib.sha256(raw).hexdigest(), readiness["registry_sha256"])
        current = {entry["name"]: entry for entry in readiness["tools"]}
        self.assertEqual({entry["name"] for entry in registry["tools"]}, set(current))
        for entry in registry["tools"]:
            with self.subTest(tool=entry["name"]):
                observed = current[entry["name"]]
                for field in (
                    "image",
                    "digest",
                    "expected_version",
                    "config_id",
                    "repo_digest",
                    "target_descriptor_digest",
                ):
                    self.assertEqual(entry[field], observed[field])
                self.assertEqual(
                    "docker buildx imagetools inspect " + entry["repo_digest"],
                    observed["next_metadata_command"],
                )

    def test_tool_registry_uses_current_stable_scanners(self):
        """2026-10-10 official releases replace stale and vulnerable scanners."""
        root = Path(__file__).resolve().parents[3]
        registry = json.loads(
            (root / "infra/supply-chain.tool-images.json").read_text()
        )
        tools = {entry["name"]: entry for entry in registry["tools"]}
        expected = {
            "syft": (
                "v1.54.1",
                "3eb5379ba7b409c3f4069b686110527af0c47df993fa5c10d13e7cf34f49b1aa",
            ),
            "grype": (
                "v0.120.1",
                "e4a44ef45d285b829ce6efe2642980329661bd2d18eab5fc539138d4adaebbbe",
            ),
            "cosign": (
                "v3.1.3",
                "9e5c2f2edc34351160407ca3416c61855bdf9403c3c5936e0f0be7fc261611b8",
            ),
        }
        for name, (version, digest) in expected.items():
            with self.subTest(tool=name):
                self.assertEqual(version, tools[name]["expected_version"])
                self.assertEqual("sha256:" + digest, tools[name]["digest"])
                self.assertTrue(tools[name]["image"].endswith(":" + version))


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

    def test_candidate_match_never_proves_current_source_declaration(self):
        row = dict(latest_row(), current_declared="openbao/openbao:2.6.2")
        result = evaluate([row], ["openbao"], NOW)
        self.assertTrue(result["ready"])
        self.assertTrue(result["entries"][0]["matches_target_latest"])
        self.assertIsNone(result["entries"][0]["matches_declared_latest"])
        self.assertIn("submitted target", result["meaning"].lower())

    def test_unknown_source_and_mismatching_target_never_prove_declaration(self):
        for declared in (None, "UNKNOWN", "openbao/openbao:2.7.1"):
            row = dict(latest_row(), current_declared=declared, target_version="2.6.2")
            result = evaluate([row], ["openbao"], NOW)
            with self.subTest(declared=declared):
                self.assertFalse(result["ready"])
                self.assertFalse(result["entries"][0]["matches_target_latest"])
                self.assertIsNone(result["entries"][0]["matches_declared_latest"])

    def test_matching_target_does_not_hide_stale_or_invalid_evidence(self):
        for field, value in (
            ("checked_at", "2026-10-08T10:00:00+00:00"),
            ("release_url", "not-https"),
            ("channel", "unknown"),
        ):
            result = evaluate([dict(latest_row(), **{field: value})], ["openbao"], NOW)
            with self.subTest(field=field):
                self.assertTrue(result["entries"][0]["matches_target_latest"])
                self.assertFalse(result["entries"][0]["evidence_complete"])
                self.assertFalse(result["ready"])

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
    def test_current_native_aggregate_cannot_claim_a_single_invocation(self):
        root = Path(__file__).resolve().parents[3]
        package = root / "infra/09-platform-ops/security-updates"
        ledger = json.loads((package / "update-ledger.json").read_text())
        verification = json.loads((package / "verification.json").read_text())
        assessment = verification["current_receipt_assessment"]
        self.assertFalse(assessment["valid_for_current_source"])
        for row in ledger["entries"]:
            if "candidate_openbao_receipt" not in row:
                continue
            reference = row["current_candidate_receipt"]
            self.assertEqual("verification.json#/current_receipt_assessment", reference)
        summary = assessment["reported_aggregate"]
        self.assertEqual("aggregate", summary["kind"])
        self.assertFalse(
            {"command", "argv", "exit_code", "duration_seconds"} & summary.keys()
        )
        runs = summary["members"]
        self.assertGreater(len(runs), 1)
        self.assertEqual(len(runs), len({run["member_id"] for run in runs}))
        self.assertEqual(
            summary["reported_passed_tests"],
            sum(run["reported_passed_tests"] for run in runs),
        )
        self.assertAlmostEqual(
            summary["cumulative_reported_duration_seconds"],
            sum(run["reported_duration_seconds"] for run in runs),
        )
        for run in runs:
            self.assertEqual("REPOSITORY_REPORTED", run["evidence_status"])
            self.assertEqual("RAW_EVIDENCE_UNAVAILABLE", run["raw_evidence_status"])
            for field in ("run_id", "argv", "exit_code", "started_at", "ended_at"):
                self.assertIsNone(run[field])
            self.assertEqual("NOT_VERIFIED", run["raw_fields_verification"])
        self.assertFalse(summary["deduplicated_coverage_verified"])
        self.assertFalse(summary["split_acceptance_verified"])

    def test_current_rows_match_root_compose_source(self):
        from scripts.lib.document_governance.operations_catalog import (
            _compose_mapping,
        )

        root = Path(__file__).resolve().parents[3]
        ledger = json.loads(
            (
                root / "infra/09-platform-ops/security-updates/update-ledger.json"
            ).read_text()
        )
        for row in ledger["entries"]:
            service = _compose_mapping(root, Path(row["compose_file"]))["services"][
                row["service"]
            ]
            with self.subTest(service=row["service"]):
                self.assertEqual(
                    service.get("image", "UNKNOWN"), row["current_declared"]
                )
                self.assertEqual(service.get("build"), row["build_source"])
                self.assertEqual(
                    hashlib.sha256(
                        (root / row["compose_file"]).read_bytes()
                    ).hexdigest(),
                    row["source_input_sha256"],
                )

    def test_current_root_supplier_references_resolve_without_acceptance_promotion(
        self,
    ):
        root = Path(__file__).resolve().parents[3]
        package = root / "infra/09-platform-ops/security-updates"
        ledger = json.loads((package / "update-ledger.json").read_text())
        releases = json.loads((package / "release-lookups.json").read_text())
        refresh = releases["root_official_refresh"]
        suppliers = {row["supplier"] for row in refresh["observations"]}
        for row in ledger["entries"]:
            references = row["official_supplier_lookup_refs"]
            self.assertTrue(references or row["supplier_lookup_blocker"])
            self.assertLessEqual(set(references), suppliers)
        self.assertFalse(refresh["verified_security_or_runtime"])

    def test_current_root_census_excludes_relocated_lab_history(self):
        from scripts.lib.supply_chain.latest_version_gate import expected_from_root

        root = Path(__file__).resolve().parents[3]
        ledger = json.loads(
            (
                root / "infra/09-platform-ops/security-updates/update-ledger.json"
            ).read_text()
        )
        expected, inventory = expected_from_root(root)
        self.assertEqual(set(expected), {row["service"] for row in ledger["entries"]})
        self.assertEqual(set(expected), set(ledger["expected_services"]))
        self.assertEqual(inventory["input_files"], ledger["include_inputs"])
        historical = ledger["historical_lab_entries"]
        self.assertTrue(historical)
        old_census = ledger["historical_root_census"]
        old_inputs = {row["path"] for row in old_census["include_inputs"]}
        current_inputs = {row["path"] for row in inventory["input_files"]}
        self.assertIn("infra/04-data/supabase/docker-compose.yml", old_inputs)
        self.assertNotIn("infra/04-data/supabase/docker-compose.yml", current_inputs)
        historical_services = {row["service"] for row in historical}
        initial = set(old_census["expected_services"]) - historical_services
        self.assertEqual(
            set(expected), replay_service_refreshes(initial, ledger["source_refreshes"])
        )
        self.assertLessEqual(historical_services, set(old_census["expected_services"]))
        self.assertEqual(len(historical_services), len(historical))
        for row in historical:
            self.assertEqual("lab", row["current_scope"])
            self.assertEqual("labs/supabase.yml", row["current_compose_file"])
            self.assertEqual("root", row["original_root_row"]["scope"])
            self.assertEqual(row["service"], row["original_root_row"]["service"])

    def test_service_refresh_history_supports_removal_and_readdition(self):
        refreshes = [
            {"removed_services": ["b"], "added_services": ["c"]},
            {"removed_services": ["c"], "added_services": ["b"]},
        ]
        self.assertEqual({"a", "b"}, replay_service_refreshes({"a", "b"}, refreshes))

    def test_public_lookup_observations_never_promote_unverified_acceptance(self):
        root = Path(__file__).resolve().parents[3]
        ledger = json.loads(
            (
                root / "infra/09-platform-ops/security-updates/update-ledger.json"
            ).read_text()
        )
        report = ledger["p08_public_release_observations"]
        rows = report["observations"]
        names = {row["service"] for row in ledger["entries"]}
        assert_public_observation_consistency(self, report, names)
        for key, value in (
            ("observed_source_count", -1),
            ("failed_source_count", -1),
            ("services_with_related_source", -1),
            ("services_without_related_source", ["nonexistent"]),
        ):
            corrupted = copy.deepcopy(report)
            corrupted[key] = value
            with self.subTest(corrupted=key), self.assertRaises(AssertionError):
                assert_public_observation_consistency(self, corrupted, names)
        failed_index = next(
            i for i, row in enumerate(rows) if row["result"] == "ACCESS_FAILED"
        )
        general_index = next(
            i
            for i, row in enumerate(rows)
            if row["result"] == "OBSERVED"
            and "/releases/latest" not in row["query_url"]
        )
        for index, field, value in (
            (0, "checked_at_utc", "2000-01-01T00:00:00Z"),
            (0, "observed_release_tag", "not-the-resolved-tag"),
            (0, "related_root_services", ["nonexistent"]),
            (failed_index, "observed_release_tag", "unavailable"),
            (general_index, "observed_release_tag", "invented"),
            (0, "source_cache_freshness", "VERIFIED_WITHIN_24H"),
            (0, "freshness_verified", True),
            (0, "stable_channel_verified", True),
            (0, "oci_availability_verified", True),
        ):
            corrupted = copy.deepcopy(report)
            corrupted["observations"][index][field] = value
            with (
                self.subTest(index=index, field=field),
                self.assertRaises(AssertionError),
            ):
                assert_public_observation_consistency(self, corrupted, names)
        self.assertTrue(rows)
        self.assertEqual(len(rows), len({row["query_url"] for row in rows}))
        self.assertEqual(len(ledger["entries"]), report["root_service_denominator"])
        self.assertEqual(len(rows), report["source_query_denominator"])
        self.assertFalse(report["verified_external_facts"])
        self.assertFalse(report["deployed"])
        for row in rows:
            with self.subTest(url=row["query_url"]):
                self.assertTrue(row["query_url"].startswith("https://"))
                self.assertTrue(row["checked_at_utc"].endswith("Z"))
                self.assertEqual(
                    "PUBLIC_SOURCE_OBSERVATION_ONLY", row["evidence_scope"]
                )
                self.assertEqual("NOT_SAVED", row["raw_receipt"])
                self.assertIn(row["result"], {"OBSERVED", "ACCESS_FAILED"})

    def test_new_local_source_does_not_inherit_security_or_runtime_acceptance(self):
        root = Path(__file__).resolve().parents[3]
        ledger = json.loads(
            (
                root / "infra/09-platform-ops/security-updates/update-ledger.json"
            ).read_text()
        )
        rows = [row for row in ledger["entries"] if row["service"] == "blog-ingestion"]
        self.assertEqual(1, len(rows))
        row = rows[0]
        self.assertEqual("NOT_RUN", row["deployment"])
        self.assertEqual("NOT_RUN", row["signature"])
        self.assertEqual("NOT_RUN", row["sbom_scan"])
        self.assertEqual("NOT_OBSERVED", row["runtime_presence"])
        self.assertEqual("UNKNOWN", row["latest_version"])
        self.assertEqual("BLOCKED", row["disposition"])
        for field in (
            "target_index_digest",
            "target_manifest_digest",
            "target_config_digest",
        ):
            with self.subTest(field=field):
                self.assertEqual("UNKNOWN", row[field])
        for field in ("compatibility", "backup", "rollback", "native_test"):
            with self.subTest(field=field):
                self.assertEqual("NOT_RUN", row[field])
        self.assertTrue(row["supplier_lookup_blocker"])

    def test_selected_security_candidates_are_current_without_promoting_acceptance(
        self,
    ):
        root = Path(__file__).resolve().parents[3]
        ledger = json.loads(
            (
                root / "infra/09-platform-ops/security-updates/update-ledger.json"
            ).read_text()
        )
        by_name = {row["service"]: row for row in ledger["entries"]}
        groups = (
            (
                [
                    "airflow-valkey",
                    "dev-valkey",
                    "mng-valkey",
                    "n8n-valkey",
                    "oauth2-proxy-valkey",
                ],
                "9.1.3",
                "GHSA-f4q9-j22m-xqq9",
            ),
            (
                ["n8n", "n8n-worker", "n8n-task-runner", "n8n-task-runner-worker"],
                "2.45.7",
                "GHSA-prmc-fg87-r4gh",
            ),
        )
        for names, version, advisory in groups:
            for name in names:
                with self.subTest(service=name):
                    row = by_name[name]
                    self.assertEqual(version, row["latest_version"])
                    self.assertEqual(version, row["target_version"])
                    self.assertTrue(
                        any(advisory in url for url in row["advisory_urls"])
                    )
                    self.assertEqual("NOT_RUN", row["deployment"])
                    self.assertEqual("NOT_RUN", row["compatibility"])
                    self.assertEqual("NOT_RUN", row["native_test"])
                    self.assertEqual("NOT_RUN", row["signature"])
                    self.assertEqual("NOT_RUN", row["sbom_scan"])
                    self.assertIn("p08_previous_release_assessment", row)
                    self.assertIn("p08_candidate_assessment", row)

    def test_valkey_candidate_pull_receipt_is_not_promoted_from_self_report(self):
        root = Path(__file__).resolve().parents[3]
        ledger = json.loads(
            (
                root / "infra/09-platform-ops/security-updates/update-ledger.json"
            ).read_text()
        )
        names = {
            "airflow-valkey",
            "dev-valkey",
            "mng-valkey",
            "n8n-valkey",
            "oauth2-proxy-valkey",
        }
        rows = [row for row in ledger["entries"] if row["service"] in names]
        self.assertEqual(names, {row["service"] for row in rows})
        for row in rows:
            with self.subTest(service=row["service"]):
                receipt = row["p08_candidate_assessment"]["local_artifact_inspection"]
                self.assertEqual(
                    "REPORTED_PASS_RAW_RECEIPT_UNAVAILABLE", receipt["status"]
                )
                self.assertEqual("NOT_SAVED", receipt["raw_receipt"])
                self.assertIsNone(receipt["exact_timestamp"])
                self.assertEqual(2, len(receipt["steps"]))
                for step in receipt["steps"]:
                    self.assertIsNone(step["exit_code"])
                    self.assertTrue(step["command"])
                self.assertEqual("NOT_RUN", row["compatibility"])
                self.assertEqual("NOT_RUN", row["signature"])

    def test_upstream_attestations_do_not_promote_custom_image_or_deployment(self):
        root = Path(__file__).resolve().parents[3]
        ledger = json.loads(
            (
                root / "infra/09-platform-ops/security-updates/update-ledger.json"
            ).read_text()
        )
        evidence = ledger["p08_upstream_supply_chain_observations"]
        self.assertEqual(
            "https://token.actions.githubusercontent.com",
            evidence["expected_oidc_issuer"],
        )
        kinds = {row["observation_id"] for row in evidence["reported_checks"]}
        self.assertEqual(
            {"n8n-signature", "n8n-slsa", "runner-cyclonedx", "runner-openvex"},
            kinds,
        )
        self.assertIs(evidence["custom_image_verified"], False)
        self.assertIs(evidence["deployment_verified"], False)
        self.assertEqual("NOT_SAVED", evidence["raw_receipt"])
        commit = evidence["observed_workflow_commit"]
        for key in ("official_expected_identity_source", "official_workflow_source"):
            self.assertIn(f"/blob/{commit}/", evidence[key])
        n8n = "ghcr.io/n8n-io/n8n@sha256:9a8d8dcea75667496695d7810d7e1fe018a65efb36cc499d347f3931b3957b5d"
        runner = "ghcr.io/n8n-io/runners@sha256:2f07088829b6a1df2b6a84746bb8b32c1eaef270315fb5466aa01b1045e9b300"
        expected = {
            "n8n-signature": (n8n, "signature"),
            "n8n-slsa": (n8n, "slsaprovenance1"),
            "runner-cyclonedx": (runner, "cyclonedx"),
            "runner-openvex": (runner, "openvex"),
        }
        for row in evidence["reported_checks"]:
            self.assertEqual("REPORTED_PASS_RAW_RECEIPT_UNAVAILABLE", row["status"])
            self.assertEqual("NOT_SAVED", row["raw_receipt"])
            subject, verification_type = expected[row["observation_id"]]
            self.assertEqual(subject, row["subject"])
            self.assertEqual(verification_type, row["verification_type"])
            self.assertEqual(0, row["reported_exit_code"])
            argv = row["command_argv"]
            self.assertEqual(row["subject"], argv[-1])
            verify_index = argv.index("--output-file") + 2
            if verification_type == "signature":
                self.assertEqual("verify", argv[verify_index])
                self.assertNotIn("--type", argv)
            else:
                self.assertEqual("verify-attestation", argv[verify_index])
                self.assertEqual(verification_type, argv[argv.index("--type") + 1])
            self.assertEqual(
                evidence["expected_oidc_issuer"],
                argv[argv.index("--certificate-oidc-issuer") + 1],
            )
            self.assertEqual(
                evidence["expected_certificate_identity_regexp"],
                argv[argv.index("--certificate-identity-regexp") + 1],
            )
            self.assertFalse(any("insecure-ignore" in arg for arg in argv))
        self.assertEqual("NOT_REVIEWED", evidence["slsa_builder_and_parameters"])
        self.assertEqual(
            "NOT_REVIEWED", evidence["sbom_contents_and_vulnerability_state"]
        )
        negatives = evidence["reported_negative_checks"]
        self.assertEqual(4, len(negatives))
        self.assertEqual(
            [10, 1, 1, 1], [row["reported_exit_code"] for row in negatives]
        )
        for row in negatives:
            self.assertEqual("NOT_SAVED", row["raw_receipt"])
            self.assertEqual(row["subject"], row["command_argv"][-1])
        followup = evidence["exact_identity_followup"]
        self.assertEqual("NOT_SAVED", followup["raw_receipt"])
        self.assertEqual(evidence["expected_oidc_issuer"], followup["oidc_issuer"])
        self.assertEqual(
            "https://github.com/n8n-io/n8n/.github/workflows/docker-build-push.yml@refs/heads/release/2.45.7",
            followup["certificate_identity"],
        )
        self.assertEqual("NOT_REVIEWED", followup["slsa_builder_and_parameters"])
        self.assertEqual(
            "NOT_REVIEWED", followup["sbom_contents_and_vulnerability_state"]
        )
        self.assertIs(followup["custom_image_verified"], False)
        self.assertIs(followup["deployment_verified"], False)
        checks = {row["observation_id"]: row for row in followup["reported_checks"]}
        self.assertEqual(set(expected), set(checks))
        tool_registry = json.loads(
            (root / "infra/supply-chain.tool-images.json").read_text()
        )
        cosign = next(row for row in tool_registry["tools"] if row["name"] == "cosign")
        for name, (subject, verification_type) in expected.items():
            check = checks[name]
            self.assertEqual(subject, check["subject"])
            self.assertEqual(verification_type, check["verification_type"])
            self.assertEqual("REPORTED_PASS_RAW_RECEIPT_UNAVAILABLE", check["status"])
            self.assertEqual(0, check["reported_exit_code"])
            self.assertEqual("NOT_SAVED", check["raw_receipt"])
            argv = check["command_argv"]
            self.assertEqual(subject, argv[-1])
            self.assertIn(cosign["repo_digest"], argv)
            self.assertEqual("/dev/null", argv[argv.index("--output-file") + 1])
            verify_index = argv.index("--output-file") + 2
            if verification_type == "signature":
                self.assertEqual("verify", argv[verify_index])
                self.assertNotIn("--type", argv)
            else:
                self.assertEqual("verify-attestation", argv[verify_index])
                self.assertEqual(verification_type, argv[argv.index("--type") + 1])
            self.assertEqual(
                followup["certificate_identity"],
                argv[argv.index("--certificate-identity") + 1],
            )
            self.assertEqual(
                followup["oidc_issuer"],
                argv[argv.index("--certificate-oidc-issuer") + 1],
            )
            self.assertNotIn("--certificate-identity-regexp", argv)
            self.assertFalse(any("insecure-ignore" in arg for arg in argv))
            self.assertEqual(2, len(check["run_window_utc"]))
            start, end = (
                datetime.fromisoformat(value) for value in check["run_window_utc"]
            )
            self.assertLess(start, end)

    def test_local_valkey_sbom_is_not_publisher_attestation_or_scan(self):
        root = Path(__file__).resolve().parents[3]
        ledger = json.loads(
            (
                root / "infra/09-platform-ops/security-updates/update-ledger.json"
            ).read_text()
        )
        evidence = ledger["p08_valkey_local_sbom_observation"]
        self.assertEqual(
            "valkey/valkey@sha256:de6fbe9626fea9f6f297b6867d2c8cf8f0394ee5ed171613166fc093cb49d0a6",
            evidence["subject"],
        )
        self.assertEqual("LOCALLY_GENERATED", evidence["sbom_origin"])
        self.assertEqual("REPORTED_PASS_RAW_RECEIPT_UNAVAILABLE", evidence["status"])
        self.assertEqual("NOT_SAVED", evidence["raw_receipt"])
        self.assertIs(evidence["publisher_attested"], False)
        self.assertIs(evidence["publisher_signature_verified"], False)
        self.assertIs(evidence["publisher_provenance_verified"], False)
        self.assertEqual("NOT_RUN", evidence["vulnerability_scan"])
        exported = evidence["export"]["command_argv"]
        self.assertEqual(evidence["subject"], exported[-1])
        archive = exported[exported.index("--output") + 1]
        syft = evidence["syft"]
        mount = syft["container_command_argv"][
            syft["container_command_argv"].index("--mount") + 1
        ]
        self.assertEqual(
            f"type=bind,source={archive},target=/input/valkey.tar,readonly", mount
        )
        self.assertIn(
            "docker-archive:/input/valkey.tar", syft["container_command_argv"]
        )
        self.assertEqual("bash -o pipefail -c", syft["pipeline_shell"])
        self.assertEqual("CycloneDX", syft["format"])
        self.assertEqual("NOT_SAVED", syft["raw_receipt"])
        self.assertEqual(0, syft["reported_exit_code"])
        rejected = evidence["rejected_attempts"][0]
        self.assertEqual(0, rejected["reported_pipeline_exit_code"])
        self.assertTrue(rejected["status"].startswith("REJECTED:"))
        self.assertEqual(1, evidence["grype_db_preflight"]["reported_exit_code"])
        self.assertEqual("DATABASE_MISSING", evidence["grype_db_preflight"]["status"])
        self.assertEqual("NOT_SAVED", evidence["grype_db_preflight"]["raw_receipt"])

    def test_runtime_candidates_report_their_own_upstream_tag(self):
        root = Path(__file__).resolve().parents[3]
        ledger = json.loads(
            (
                root / "infra/09-platform-ops/security-updates/update-ledger.json"
            ).read_text()
        )

        def canonical_tag(value: str) -> str:
            return value.rsplit("@", 1)[-1].removeprefix("v")

        for row in ledger["entries"]:
            if row.get("disposition") != "VERIFY_RUNTIME":
                continue
            target = row.get("target_version")
            reported = row.get("upstream_reported_tag")
            if target in (None, "UNKNOWN") or reported in (None, "UNKNOWN"):
                continue
            with self.subTest(service=row["service"]):
                self.assertEqual(canonical_tag(target), canonical_tag(reported))

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
            if row["service"] in {"openbao", "openbao-agent"}:
                self.assertEqual(
                    "sha256:a58fb1109971e506e9de1a360aec48ae07af7b6ccf409f8bac329e30e8fde8c8",
                    row["target_declared_digest"],
                )
                self.assertEqual(
                    "PASS: selected owned artifact scan receipt SHA256 "
                    "8e32274b3b95bb3eddd911be57e1fd1200e29e676e41783a73ede34c0cf6f87b",
                    row["sbom_scan"],
                )
                self.assertEqual("NOT_UPSTREAM_SIGNED", row["signature"])
            elif row["service"] in {"traefik", "prometheus"}:
                # 2026-10-30: the adopted fixed pin is unscanned; the prior
                # pin's offline scan receipt is kept as history.
                self.assertTrue(row["sbom_scan"].startswith("NOT_RUN"))
                self.assertTrue(
                    row["previous_adopted_pin_assessment"]["sbom_scan"].startswith(
                        "PASS: offline Syft v1.54.1/Grype v0.120.1"
                    )
                )
                self.assertTrue(row["signature"].startswith("NOT_RUN"))
            else:
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
    def test_cli_reports_target_match_without_claiming_source_declaration(self):
        from scripts.lib.supply_chain import latest_version_gate

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            leaf = root / "infra/service/docker-compose.yml"
            leaf.parent.mkdir(parents=True)
            leaf.write_text("services:\n  openbao:\n    image: openbao/openbao:2.6.2\n")
            (root / "docker-compose.yml").write_text(
                "include:\n  - infra/service/docker-compose.yml\n"
            )
            path = root / "submitted.json"
            row = dict(latest_row(), checked_at=datetime.now(UTC).isoformat())
            path.write_text(json.dumps({"entries": [row]}))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(
                    0,
                    latest_version_gate.main(
                        ["--input", str(path), "--repo-root", str(root)]
                    ),
                )
            result = json.loads(output.getvalue())
            self.assertTrue(result["ready"])
            self.assertTrue(result["entries"][0]["matches_target_latest"])
            self.assertIsNone(result["entries"][0]["matches_declared_latest"])
            self.assertFalse(result["deployed"])
            self.assertFalse(result["verified_external_facts"])

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
