"""Unit contracts for the bounded P07 public assessment helper."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from scripts.lib.ops import root_resource_assessment as assessment

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "scripts/operations/root-resource-assessment.py"

METRIC_UNITS = {
    "cpu_throttled_seconds": "seconds",
    "cpu_throttled_periods": "count",
    "rss_bytes": "bytes",
    "heap_bytes": "bytes",
    "work_mem_bytes": "bytes",
    "connections": "count",
    "tmpfs_bytes": "bytes",
    "shm_bytes": "bytes",
    "cache_bytes": "bytes",
    "off_heap_bytes": "bytes",
    "resource_overhead_bytes": "bytes",
    "worker_count": "count",
    "pid_peak": "count",
    "oom_events": "count",
    "exit_events": "count",
    "latency_p95_ms": "milliseconds",
    "throughput_per_second": "per_second",
    "recovery_seconds": "seconds",
    "gpu_memory_bytes": "bytes",
    "gpu_utilization_ratio": "ratio",
}

BUDGET_UNITS = {
    "cpu_limit_cores": "cores",
    "memory_limit_bytes": "bytes",
    "connection_limit": "count",
    "tmpfs_limit_bytes": "bytes",
    "shm_limit_bytes": "bytes",
    "worker_limit": "count",
    "pid_limit": "count",
    "latency_p95_budget_ms": "milliseconds",
    "throughput_floor_per_second": "per_second",
    "recovery_budget_seconds": "seconds",
    "gpu_memory_limit_bytes": "bytes",
}


def _facts(units: dict[str, str], *, value: float = 1.0) -> dict[str, object]:
    return {
        name: {"status": "known", "value": value, "unit": unit}
        for name, unit in units.items()
    }


def valid_document(*, evidence_kind: str = "measurement") -> dict[str, object]:
    source_digest = "sha256:" + "b" * 64
    service = {
        "security_opt": ["no-new-privileges:true"],
        "cap_drop": ["ALL"],
        "init": True,
        "restart": "unless-stopped",
        "healthcheck": {"test": ["CMD", "true"]},
        "cpus": "1.0",
        "mem_limit": "512m",
        "pids_limit": 128,
    }
    controls = {
        "no_new_privileges": "required",
        "cap_drop_all": "required",
        "cap_add": "empty",
        "privileged": "false",
        "restart": "daemon policy",
        "healthcheck": "required",
        "cpus": "required",
        "mem_limit": "required",
        "secrets_group": "exact consumer",
        "init": "required",
        "gpu": "exception",
        "pids_limit": "required",
    }
    document = {
        "schema_version": 1,
        "evidence_kind": evidence_kind,
        "provenance": {
            "status": "known",
            "collector_id": "synthetic-fixture"
            if evidence_kind == "synthetic"
            else "public-collector",
            "method": "synthetic"
            if evidence_kind == "synthetic"
            else "read-only-export",
            "receipt_sha256": "9" * 64,
            "aggregation": "window-peaks-and-counters",
        },
        "source": {
            "repository_sha": "a" * 40,
            "compose_file": "infra/07-workflow/example/docker-compose.yml",
            "compose_file_sha256": "c" * 64,
            "effective_config_sha256": "e" * 64,
            "image_reference": "example/service:1.0",
            "image_digest": source_digest,
            "image_config_sha256": "d" * 64,
        },
        "deployed": {
            "status": "observed",
            "repository_sha": "a" * 40,
            "compose_file_sha256": "c" * 64,
            "effective_config_sha256": "e" * 64,
            "image_digest": source_digest,
            "image_config_sha256": "d" * 64,
            "platform": "linux/amd64",
        },
        "target": {
            "service": "example-service",
            "environment_id": "public-home-a",
            "workload_id": "public-workload-a",
        },
        "window": {
            "started_at": "2026-10-11T00:00:00Z",
            "ended_at": "2026-10-11T00:05:00Z",
            "duration_seconds": 300,
            "cadence_seconds": 5,
            "sample_count": 60,
            "phase": "steady",
        },
        "workload": {
            "representative": True,
            "consumer_id": "public-consumer-a",
            "data_owner_id": "public-owner-a",
            "failure_cost": "degraded-home-capability",
        },
        "metrics": _facts(METRIC_UNITS),
        "budgets": _facts(BUDGET_UNITS, value=10.0),
        "controls": {
            "as_of": "2026-10-11",
            "compose_file": "infra/07-workflow/example/docker-compose.yml",
            "secret_roots": ["/synthetic-public/secrets/"],
            "effective_service": service,
            "registry": {
                "schema_version": 2,
                "policy_id": "OPS-TPL-EXCEPTIONS-001",
                "template_source": "infra/common-optimizations.yml",
                "controls": controls,
                "exceptions": [],
            },
        },
        "proposal": {
            "kind": "assessment_only",
            "lower_memory_limit": False,
            "lower_cpu_limit": False,
        },
    }
    document["metrics"]["throughput_per_second"]["value"] = 20.0
    return document


class AssessmentTests(unittest.TestCase):
    def test_complete_measurement_is_reviewable_but_never_authorizes_mutation(
        self,
    ) -> None:
        result = assessment.evaluate(valid_document(), today=date(2026, 10, 11))

        self.assertEqual("REVIEWABLE", result["status"])
        self.assertEqual([], result["blockers"])
        self.assertFalse(result["mutation_authorized"])
        self.assertEqual("SOURCE/UNIT/STATIC", result["evidence_scope"])
        self.assertFalse(result["runtime_acceptance"])

    def test_synthetic_unknown_and_idle_lowering_remain_blocked(self) -> None:
        candidate = valid_document(evidence_kind="synthetic")
        candidate["metrics"]["rss_bytes"] = {
            "status": "unknown",
            "unit": "bytes",
        }
        candidate["window"]["phase"] = "idle"
        candidate["proposal"]["lower_memory_limit"] = True

        result = assessment.evaluate(candidate, today=date(2026, 10, 11))

        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual(
            ["SYNTHETIC_EVIDENCE", "UNKNOWN_FACTS", "IDLE_ONLY_LOWERING"],
            result["blockers"],
        )

    def test_identity_mismatch_and_contradictory_budget_block(self) -> None:
        candidate = valid_document()
        candidate["deployed"]["image_digest"] = "sha256:" + "e" * 64
        candidate["metrics"]["rss_bytes"]["value"] = 20
        candidate["budgets"]["memory_limit_bytes"]["value"] = 10

        result = assessment.evaluate(candidate, today=date(2026, 10, 11))

        self.assertEqual(
            ["SOURCE_DEPLOYED_MISMATCH", "CONTRADICTORY_FACTS"],
            result["blockers"],
        )

    def test_control_assessment_reuses_existing_pure_apis(self) -> None:
        candidate = valid_document()
        with (
            mock.patch.object(
                assessment.compose_controls,
                "deviations",
                wraps=assessment.compose_controls.deviations,
            ) as deviations,
            mock.patch.object(
                assessment.compose_controls,
                "check",
                wraps=assessment.compose_controls.check,
            ) as check,
        ):
            result = assessment.evaluate(candidate, today=date(2026, 10, 11))

        self.assertGreaterEqual(deviations.call_count, 2)
        check.assert_called_once()
        self.assertEqual({}, result["control_deviations"])
        self.assertEqual([], result["control_findings"])

    def test_exact_root_exception_mismatch_blocks(self) -> None:
        candidate = valid_document()
        candidate["controls"]["effective_service"]["cap_add"] = ["CHOWN"]
        candidate["controls"]["registry"]["exceptions"] = []

        result = assessment.evaluate(candidate, today=date(2026, 10, 11))

        self.assertEqual("BLOCKED", result["status"])
        self.assertIn("CONTROL_FINDINGS", result["blockers"])
        self.assertEqual({"cap_add": ["CHOWN"]}, result["control_deviations"])

    def test_required_memory_fact_cannot_be_erased_as_not_applicable(self) -> None:
        candidate = valid_document()
        candidate["metrics"]["rss_bytes"] = {
            "status": "not_applicable",
            "unit": "bytes",
            "reason_code": "not-applicable-to-service",
        }

        result = assessment.evaluate(candidate, today=date(2026, 10, 11))

        self.assertIn("REQUIRED_FACTS_NOT_APPLICABLE", result["blockers"])

    def test_source_and_selected_control_file_mismatch_blocks(self) -> None:
        candidate = valid_document()
        candidate["controls"]["compose_file"] = "infra/other/docker-compose.yml"

        result = assessment.evaluate(candidate, today=date(2026, 10, 11))

        self.assertIn("SOURCE_DEPLOYED_MISMATCH", result["blockers"])

    def test_unknown_platform_blocks(self) -> None:
        candidate = valid_document()
        candidate["deployed"]["platform"] = None
        result = assessment.evaluate(candidate, today=date(2026, 10, 11))
        self.assertIn("SOURCE_DEPLOYED_MISMATCH", result["blockers"])

    def test_future_window_blocks(self) -> None:
        candidate = valid_document()
        candidate["window"]["started_at"] = "2099-10-11T00:00:00Z"
        candidate["window"]["ended_at"] = "2099-10-11T00:05:00Z"
        result = assessment.evaluate(candidate, today=date(2026, 10, 11))
        self.assertIn("CONTRADICTORY_FACTS", result["blockers"])

    def test_unknown_provenance_and_relabelled_synthetic_input_block(self) -> None:
        candidate = valid_document()
        candidate["provenance"] = {
            "status": "unknown",
            "collector_id": None,
            "method": "unknown",
            "receipt_sha256": None,
            "aggregation": "unknown",
        }
        result = assessment.evaluate(candidate, today=date(2026, 10, 11))
        self.assertIn("UNKNOWN_FACTS", result["blockers"])
        candidate = valid_document(evidence_kind="synthetic")
        candidate["evidence_kind"] = "measurement"
        result = assessment.evaluate(candidate, today=date(2026, 10, 11))
        self.assertIn("SYNTHETIC_EVIDENCE", result["blockers"])

    def test_zero_effective_limits_are_refused(self) -> None:
        for name in ("cpus", "mem_limit"):
            for value in (0, "0", "0.0" if name == "cpus" else "0m"):
                with self.subTest(name=name, value=value):
                    candidate = valid_document()
                    candidate["controls"]["effective_service"][name] = value
                    with self.assertRaises(assessment.PublicInputError) as caught:
                        assessment.evaluate(candidate)
                    self.assertEqual("INVALID_DOCUMENT", caught.exception.code)
        for name in ("cpus", "memory"):
            with self.subTest(deploy_limit=name):
                candidate = valid_document()
                candidate["controls"]["effective_service"]["deploy"] = {
                    "resources": {"limits": {name: "0"}}
                }
                with self.assertRaises(assessment.PublicInputError) as caught:
                    assessment.evaluate(candidate)
                self.assertEqual("INVALID_DOCUMENT", caught.exception.code)

    def test_missing_measurement_provenance_is_refused(self) -> None:
        candidate = valid_document()
        candidate.pop("provenance", None)
        with self.assertRaises(assessment.PublicInputError) as caught:
            assessment.evaluate(candidate)
        self.assertEqual("INVALID_DOCUMENT", caught.exception.code)

    def test_non_normalized_public_paths_are_refused(self) -> None:
        for path in ("infra/..", "infra/.", "infra//service.yml"):
            with self.subTest(path=path):
                candidate = valid_document()
                candidate["source"]["compose_file"] = path
                candidate["controls"]["compose_file"] = path
                with self.assertRaises(assessment.PublicInputError) as caught:
                    assessment.evaluate(candidate)
                self.assertEqual("INVALID_DOCUMENT", caught.exception.code)
        candidate = valid_document()
        candidate["controls"]["secret_roots"] = ["/synthetic-public/../"]
        with self.assertRaises(assessment.PublicInputError):
            assessment.evaluate(candidate)

    def test_direct_nonfinite_and_too_deep_inputs_have_fixed_errors(self) -> None:
        candidate = valid_document()
        candidate["metrics"]["rss_bytes"]["value"] = float("inf")
        with self.assertRaises(assessment.PublicInputError) as caught:
            assessment.evaluate(candidate)
        self.assertEqual("NONFINITE_NUMBER", caught.exception.code)

        nested: object = None
        for _ in range(40):
            nested = {"value": nested}
        with self.assertRaises(assessment.PublicInputError) as caught:
            assessment.evaluate(nested)
        self.assertEqual("INPUT_TOO_COMPLEX", caught.exception.code)

    def test_schema_invalid_document_has_fixed_error_without_candidate_data(
        self,
    ) -> None:
        candidate = valid_document()
        marker = "DO-NOT-ECHO-CANDIDATE"
        candidate["target"]["service"] = marker
        candidate[marker] = marker

        with self.assertRaises(assessment.PublicInputError) as caught:
            assessment.evaluate(candidate)

        self.assertEqual("INVALID_DOCUMENT", caught.exception.code)
        self.assertNotIn(marker, str(caught.exception))

    def test_security_option_substring_cannot_impersonate_exact_control(self) -> None:
        candidate = valid_document()
        candidate["controls"]["effective_service"]["security_opt"] = [
            "prefix-no-new-privileges:true-suffix"
        ]
        with self.assertRaises(assessment.PublicInputError) as caught:
            assessment.evaluate(candidate)
        self.assertEqual("INVALID_DOCUMENT", caught.exception.code)

    def test_conflicting_security_options_are_refused(self) -> None:
        candidate = valid_document()
        candidate["controls"]["effective_service"]["security_opt"] = [
            "no-new-privileges:true",
            "no-new-privileges:false",
        ]
        with self.assertRaises(assessment.PublicInputError) as caught:
            assessment.evaluate(candidate)
        self.assertEqual("INVALID_DOCUMENT", caught.exception.code)


class LoaderTests(unittest.TestCase):
    def _write(self, directory: Path, body: str, name: str = "facts.json") -> Path:
        path = directory / name
        path.write_text(body, encoding="utf-8")
        return path

    def test_duplicate_and_nonfinite_json_are_rejected_with_fixed_codes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            duplicate = self._write(root, '{"value": 1, "value": 2}')
            with self.assertRaises(assessment.PublicInputError) as caught:
                assessment.load_document(duplicate)
            self.assertEqual("DUPLICATE_FIELD", caught.exception.code)

            nonfinite = self._write(root, '{"value": NaN}')
            with self.assertRaises(assessment.PublicInputError) as caught:
                assessment.load_document(nonfinite)
            self.assertEqual("NONFINITE_NUMBER", caught.exception.code)

    def test_missing_traversal_private_directory_and_hardlink_are_refused(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            regular = self._write(root, "{}")
            hardlink = root / "second.json"
            os.link(regular, hardlink)
            private = root / "credentials" / "facts.json"
            for path, code in (
                (root / "missing.json", "INPUT_UNAVAILABLE"),
                (root / ".." / "facts.json", "UNSAFE_INPUT_PATH"),
                (root / "facts.txt", "UNSAFE_INPUT_PATH"),
                (private, "PRIVATE_INPUT_PATH"),
                (hardlink, "UNSAFE_INPUT_PATH"),
            ):
                with self.subTest(code=code, name=path.name):
                    with self.assertRaises(assessment.PublicInputError) as caught:
                        assessment.load_document(path)
                    self.assertEqual(code, caught.exception.code)

    def test_malformed_nonobject_and_deep_json_are_refused(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for body, code in (
                ("{", "INVALID_JSON"),
                ("[]", "INVALID_DOCUMENT"),
                ("[" * 40 + "0" + "]" * 40, "INPUT_TOO_COMPLEX"),
                ('{"value": "' + "x" * 1025 + '"}', "INPUT_TOO_COMPLEX"),
            ):
                with self.subTest(code=code):
                    path = self._write(root, body)
                    with self.assertRaises(assessment.PublicInputError) as caught:
                        assessment.load_document(path)
                    self.assertEqual(code, caught.exception.code)

    def test_symlink_nonregular_private_named_and_oversized_inputs_are_rejected(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            regular = self._write(root, "{}")
            link = root / "linked.json"
            link.symlink_to(regular)
            private = self._write(root, "{}", ".env.json")
            large = self._write(
                root, " " * (assessment.MAX_INPUT_BYTES + 1), "large.json"
            )
            fifo = root / "facts-fifo.json"
            os.mkfifo(fifo)

            for path, code in (
                (link, "UNSAFE_INPUT_PATH"),
                (private, "PRIVATE_INPUT_PATH"),
                (large, "INPUT_TOO_LARGE"),
                (fifo, "UNSAFE_INPUT_PATH"),
            ):
                with self.subTest(path=path.name):
                    with self.assertRaises(assessment.PublicInputError) as caught:
                        assessment.load_document(path)
                    self.assertEqual(code, caught.exception.code)

    def test_valid_file_round_trip_and_cli_output_are_sanitized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "measurement.json"
            path.write_text(json.dumps(valid_document()), encoding="utf-8")

            loaded = assessment.load_document(path)
            self.assertEqual(1, loaded["schema_version"])
            result = subprocess.run(
                [sys.executable, os.fspath(CLI), os.fspath(path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual("REVIEWABLE", output["status"])
        self.assertNotIn(os.fspath(path), result.stdout + result.stderr)

    def test_parent_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real = root / "real"
            real.mkdir()
            (real / "facts.json").write_text("{}", encoding="utf-8")
            linked = root / "linked"
            linked.symlink_to(real, target_is_directory=True)

            with self.assertRaises(assessment.PublicInputError) as caught:
                assessment.load_document(linked / "facts.json")

        self.assertEqual("UNSAFE_INPUT_PATH", caught.exception.code)

    def test_cli_rejects_extra_arguments_without_echoing_them(self) -> None:
        marker = "DO-NOT-ECHO-ARGUMENT"
        result = subprocess.run(
            [sys.executable, os.fspath(CLI), marker, marker],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(2, result.returncode)
        self.assertEqual("ERROR INVALID_ARGUMENTS\n", result.stderr)
        self.assertNotIn(marker, result.stderr)


if __name__ == "__main__":
    unittest.main()
