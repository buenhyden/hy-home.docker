from __future__ import annotations

import fcntl
import hashlib
import importlib.metadata
import json
import os
import pathlib
import stat
import sys
import tempfile
import unittest
from unittest import mock

from scripts.lib.gate.ci_gate_evidence import (
    EvidenceError,
    EvidenceStore,
    _active_locked_packages,
    capture_controller_toolchain,
    local_toolchain_mismatch,
)

ROOT = pathlib.Path(__file__).resolve().parents[3]


class LocalToolchainTests(unittest.TestCase):
    """A local run must use the hosted Python pin and the controller lock."""

    def fixture(self, pin: str, lock: str) -> pathlib.Path:
        root = pathlib.Path(self.enterContext(tempfile.TemporaryDirectory()))
        (root / ".github/workflows").mkdir(parents=True)
        (root / ".github/workflows/ci-quality.yml").write_text(
            f"        with:\n          python-version: '{pin}'\n", encoding="utf-8"
        )
        (root / "scripts").mkdir()
        (root / "scripts/requirements-controller.lock").write_text(
            lock, encoding="utf-8"
        )
        return root

    def setUp(self) -> None:
        self.current = ".".join(str(part) for part in sys.version_info[:3])
        version = importlib.metadata.version("pyyaml")
        self.lock = f"pyyaml=={version} \\\n    --hash=sha256:{'0' * 64}\n"

    def test_matching_interpreter_and_lock_pass(self) -> None:
        with mock.patch.object(fcntl, "F_ADD_SEALS", 1033, create=True):
            self.assertIsNone(
                local_toolchain_mismatch(self.fixture(self.current, self.lock))
            )

    def test_other_python_version_is_rejected(self) -> None:
        reason = local_toolchain_mismatch(self.fixture("3.0.0", self.lock))
        self.assertIn("differs from the hosted 3.0.0", reason)

    def test_build_without_memfd_sealing_is_rejected(self) -> None:
        with mock.patch.object(fcntl, "F_ADD_SEALS", create=True):
            del fcntl.F_ADD_SEALS
            reason = local_toolchain_mismatch(self.fixture(self.current, self.lock))
        self.assertIn("memfd sealing", reason)

    def test_package_drift_from_lock_is_rejected(self) -> None:
        drift = self.lock.replace("pyyaml==", "pyyaml==0.0.0+")
        with mock.patch.object(fcntl, "F_ADD_SEALS", 1033, create=True):
            reason = local_toolchain_mismatch(self.fixture(self.current, drift))
        self.assertEqual("installed dependency differs from lock: pyyaml", reason)


class EvidenceStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = pathlib.Path(self.temp.name) / "ci-gate-evidence"
        self.identity = {
            "event_name": "pull_request",
            "profile": "changed",
            "execution_context": "pull_request",
            "input_sha": "1" * 40,
            "base_sha": "2" * 40,
            "head_sha": "3" * 40,
            "run_id": "12345",
            "run_attempt": "2",
            "job": "candidate-quality",
        }
        self.rows = [
            {
                "gate_id": "leaf.example",
                "argv": ["scripts/validation/example.py", "--check"],
                "selection_reason": "changed_path",
                "environment_keys": ["CI", "GITHUB_ACTIONS"],
                "source": {
                    "path": "scripts/validation/example.py",
                    "sha256": "4" * 64,
                    "git_object": "5" * 40,
                    "size_bytes": 123,
                },
                "tool_image_digest": "NOT_AVAILABLE",
            },
            {
                "gate_id": "leaf.second",
                "argv": ["scripts/validation/second.sh"],
                "selection_reason": "dependency",
                "environment_keys": [],
                "source": {
                    "path": "scripts/validation/second.sh",
                    "sha256": "6" * 64,
                    "git_object": "7" * 40,
                    "size_bytes": 45,
                },
                "tool_image_digest": "sha256:" + "8" * 64,
            },
        ]

    def create(self) -> EvidenceStore:
        return EvidenceStore.create(
            self.output,
            identity=self.identity,
            rows=self.rows,
            retention_days=14,
        )

    def test_complete_lifecycle_is_private_canonical_and_hash_linked(self) -> None:
        self.create()
        self.assertEqual(stat.S_IMODE(self.output.stat().st_mode), 0o700)
        plan_path = self.output / "plan.json"
        self.assertEqual(stat.S_IMODE(plan_path.stat().st_mode), 0o600)

        reopened = EvidenceStore.open(
            self.output,
            identity=self.identity,
            rows=self.rows,
            retention_days=14,
        )
        reopened.initialize_result()
        reopened.mark_started(
            "leaf.example",
            started_at_utc="2026-10-16T00:00:00Z",
        )
        reopened.mark_terminal(
            "leaf.example",
            status="PASS",
            exit_code=0,
            ended_at_utc="2026-10-16T00:00:01Z",
            duration_ms=1000,
            artifact={
                "status": "CAPTURED",
                "path": "results.sarif",
                "sha256": "9" * 64,
                "size_bytes": 321,
            },
        )
        metadata = reopened.finalize(blocked_reason="blocked_by_prior")

        plan = json.loads(plan_path.read_text())
        result_path = self.output / "result.json"
        result_raw = result_path.read_bytes()
        result = json.loads(result_raw)
        manifest_path = self.output / "evidence-manifest.json"
        manifest_raw = manifest_path.read_bytes()
        manifest = json.loads(manifest_raw)

        self.assertEqual(plan["owner"], "SPEC-0211-TSK-0003")
        self.assertEqual(plan["retention_days"], 14)
        self.assertEqual([row["status"] for row in result["rows"]], ["PASS", "NOT_RUN"])
        self.assertTrue(result["complete"])
        self.assertEqual("CAPTURED", result["rows"][0]["artifact"]["status"])
        self.assertEqual(
            manifest["plan_sha256"], hashlib.sha256(plan_path.read_bytes()).hexdigest()
        )
        self.assertEqual(
            manifest["result_sha256"], hashlib.sha256(result_raw).hexdigest()
        )
        self.assertEqual(
            metadata["manifest_sha256"], hashlib.sha256(manifest_raw).hexdigest()
        )
        self.assertEqual(stat.S_IMODE(result_path.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(manifest_path.stat().st_mode), 0o600)
        for path in (plan_path, result_path, manifest_path):
            canonical = (
                json.dumps(
                    json.loads(path.read_bytes()),
                    allow_nan=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ).encode()
                + b"\n"
            )
            self.assertEqual(path.read_bytes(), canonical)

    def test_plan_creation_collision_fails_closed(self) -> None:
        self.create()
        with self.assertRaisesRegex(EvidenceError, "already exists"):
            self.create()

    def test_directory_rename_and_replacement_fails_before_result_write(self) -> None:
        store = self.create()
        moved = self.output.with_name("moved-evidence")
        self.output.rename(moved)
        self.output.mkdir(mode=0o700)
        with self.assertRaisesRegex(EvidenceError, "directory identity changed"):
            store.initialize_result()
        self.assertFalse((self.output / "result.json").exists())
        self.assertFalse((moved / "result.json").exists())

    def test_push_identity_admits_explicit_unavailable_base(self) -> None:
        identity = {
            **self.identity,
            "event_name": "push",
            "execution_context": "push",
            "base_sha": "NOT_AVAILABLE",
            "head_sha": self.identity["input_sha"],
            "job": "main-security",
        }
        with EvidenceStore.create(
            self.output,
            identity=identity,
            rows=self.rows,
            retention_days=14,
        ):
            pass

    def test_toolchain_and_post_setup_node_observation_are_bounded(self) -> None:
        toolchain = {
            "status": "CAPTURED",
            "executables": [
                {"name": "python", "version": "3.14.8", "sha256": "a" * 64},
                {"name": "uv", "version": "0.12.18", "sha256": "b" * 64},
            ],
            "dependency_inputs": [
                {"path": "scripts/requirements-controller.lock", "sha256": "c" * 64}
            ],
            "installed_packages": [
                {"name": "pyyaml", "version": "6.0.3"},
                {"name": "zizmor", "version": "1.28.0"},
            ],
            "runner_image": {
                "image_os": "ubuntu24",
                "image_version": "20261015.1",
                "architecture": "X64",
                "image_digest": "NOT_AVAILABLE",
            },
            "node": {
                "status": "SELECTED_NOT_YET_OBSERVED",
                "version": "24.22.0",
                "sha256": None,
            },
        }
        store = EvidenceStore.create(
            self.output,
            identity=self.identity,
            rows=self.rows,
            retention_days=14,
            toolchain=toolchain,
        )
        store.close()
        reopened = EvidenceStore.open(
            self.output,
            identity=self.identity,
            rows=self.rows,
            retention_days=14,
            toolchain=toolchain,
        )
        reopened.initialize_result(
            runtime_observation={
                "node": {
                    "status": "CAPTURED",
                    "version": "v24.22.0",
                    "sha256": "d" * 64,
                }
            }
        )
        reopened.close()
        plan = json.loads((self.output / "plan.json").read_bytes())
        result = json.loads((self.output / "result.json").read_bytes())
        self.assertEqual("CAPTURED", plan["toolchain"]["status"])
        self.assertEqual("v24.22.0", result["runtime_observation"]["node"]["version"])

    def test_controller_toolchain_captures_allowlisted_identity_and_rejects_drift(
        self,
    ) -> None:
        lock = (ROOT / "scripts/requirements-controller.lock").read_text()
        versions = dict(_active_locked_packages(lock))
        self.assertTrue(versions)
        environment = {
            "TRUSTED_IMAGE_OS": "ubuntu24",
            "TRUSTED_IMAGE_VERSION": "20261015.1",
            "TRUSTED_RUNNER_ARCH": "X64",
        }
        for name in ("git", "python", "uv"):
            executable = pathlib.Path(self.temp.name) / name
            executable.write_bytes(f"{name}-executable".encode())
            executable.chmod(0o755)
            environment[f"TRUSTED_{name.upper()}_PATH"] = str(executable)
            environment[f"TRUSTED_{name.upper()}_VERSION"] = f"{name}-version"
            environment[f"TRUSTED_{name.upper()}_SHA256"] = hashlib.sha256(
                executable.read_bytes()
            ).hexdigest()

        with mock.patch(
            "scripts.lib.gate.ci_gate_evidence.importlib.metadata.version",
            side_effect=versions.__getitem__,
        ):
            toolchain = capture_controller_toolchain(
                ROOT, environment, node_selected=True
            )
        self.assertEqual("CAPTURED", toolchain["status"])
        self.assertEqual(
            ["git", "python", "uv"],
            [item["name"] for item in toolchain["executables"]],
        )
        self.assertEqual("SELECTED_NOT_YET_OBSERVED", toolchain["node"]["status"])
        self.assertEqual(len(versions), len(toolchain["installed_packages"]))
        self.assertNotIn(str(self.temp.name), repr(toolchain))

        environment["TRUSTED_UV_SHA256"] = "0" * 64
        with (
            mock.patch(
                "scripts.lib.gate.ci_gate_evidence.importlib.metadata.version",
                side_effect=versions.__getitem__,
            ),
            self.assertRaisesRegex(EvidenceError, "changed after capture: uv"),
        ):
            capture_controller_toolchain(ROOT, environment, node_selected=False)

        environment["TRUSTED_UV_SHA256"] = hashlib.sha256(
            (pathlib.Path(self.temp.name) / "uv").read_bytes()
        ).hexdigest()
        for mode in (0o777, 0o775, 0o757):
            (pathlib.Path(self.temp.name) / "python").chmod(mode)
            with (
                self.subTest(mode=oct(mode)),
                mock.patch(
                    "scripts.lib.gate.ci_gate_evidence.importlib.metadata.version",
                    side_effect=versions.__getitem__,
                ),
                self.assertRaisesRegex(EvidenceError, r"python \(EPERM: .*mode="),
            ):
                capture_controller_toolchain(ROOT, environment, node_selected=False)

    def test_open_rejects_mismatched_or_noncanonical_plan(self) -> None:
        self.create()
        changed = {**self.identity, "run_attempt": "3"}
        with self.assertRaisesRegex(EvidenceError, "plan does not match"):
            EvidenceStore.open(
                self.output,
                identity=changed,
                rows=self.rows,
                retention_days=14,
            )

        plan_path = self.output / "plan.json"
        document = json.loads(plan_path.read_bytes())
        plan_path.write_text(json.dumps(document, indent=2))
        os.chmod(plan_path, 0o600)
        with self.assertRaisesRegex(EvidenceError, "canonical JSON"):
            EvidenceStore.open(
                self.output,
                identity=self.identity,
                rows=self.rows,
                retention_days=14,
            )

    def test_schema_rejects_untyped_or_sensitive_payloads(self) -> None:
        bad_identity = {**self.identity, "token": "secret"}
        with self.assertRaisesRegex(EvidenceError, "identity fields"):
            EvidenceStore.create(
                self.output,
                identity=bad_identity,
                rows=self.rows,
                retention_days=14,
            )

        bad_rows = [{**self.rows[0], "environment": {"TOKEN": "secret"}}]
        with self.assertRaisesRegex(EvidenceError, r"row\[0\] fields"):
            EvidenceStore.create(
                self.output,
                identity=self.identity,
                rows=bad_rows,
                retention_days=14,
            )

    def test_hard_kill_state_remains_started_and_incomplete(self) -> None:
        self.create()
        store = EvidenceStore.open(
            self.output,
            identity=self.identity,
            rows=self.rows,
            retention_days=14,
        )
        store.initialize_result()
        store.mark_started("leaf.example", started_at_utc="2026-10-16T00:00:00Z")

        result = json.loads((self.output / "result.json").read_bytes())
        self.assertFalse(result["complete"])
        self.assertEqual(result["rows"][0]["status"], "STARTED")
        self.assertEqual(result["rows"][1]["status"], "NOT_RUN")
        self.assertFalse((self.output / "evidence-manifest.json").exists())

    def test_terminal_validation_and_started_finalize_fail_closed(self) -> None:
        store = self.create()
        store.initialize_result()
        with self.assertRaisesRegex(EvidenceError, "terminal status"):
            store.mark_terminal(
                "leaf.example",
                status="STARTED",
                exit_code=0,
                ended_at_utc="2026-10-16T00:00:01Z",
                duration_ms=1,
            )
        store.mark_started("leaf.example", started_at_utc="2026-10-16T00:00:00Z")
        with self.assertRaisesRegex(EvidenceError, "STARTED"):
            store.finalize(blocked_reason="blocked_by_prior")

    def test_update_detects_stale_result_bytes(self) -> None:
        store = self.create()
        store.initialize_result()
        result_path = self.output / "result.json"
        document = json.loads(result_path.read_bytes())
        document["complete"] = True
        result_path.write_bytes(
            json.dumps(
                document,
                allow_nan=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode()
            + b"\n"
        )
        os.chmod(result_path, 0o600)

        with self.assertRaisesRegex(EvidenceError, "changed since"):
            store.mark_started("leaf.example", started_at_utc="2026-10-16T00:00:00Z")

    def test_atomic_update_collision_preserves_prior_result(self) -> None:
        store = self.create()
        store.initialize_result()
        temporary = self.output / "result.json.tmp"
        temporary.write_text("collision")
        os.chmod(temporary, 0o600)

        with self.assertRaisesRegex(EvidenceError, "temporary file already exists"):
            store.mark_started("leaf.example", started_at_utc="2026-10-16T00:00:00Z")

        result = json.loads((self.output / "result.json").read_bytes())
        self.assertEqual(result["rows"][0]["status"], "NOT_RUN")

    def test_update_rejects_symlink_and_hardlink_result(self) -> None:
        store = self.create()
        store.initialize_result()
        result_path = self.output / "result.json"
        saved = result_path.read_bytes()

        result_path.unlink()
        result_path.symlink_to(self.output / "missing")
        with self.assertRaisesRegex(EvidenceError, "regular file"):
            store.mark_started("leaf.example", started_at_utc="2026-10-16T00:00:00Z")

        result_path.unlink()
        result_path.write_bytes(saved)
        os.chmod(result_path, 0o600)
        hardlink = self.output / "result-copy.json"
        os.link(result_path, hardlink)
        with self.assertRaisesRegex(EvidenceError, "single link"):
            store.mark_started("leaf.example", started_at_utc="2026-10-16T00:00:00Z")

    def test_result_transition_rules_are_closed(self) -> None:
        store = self.create()
        store.initialize_result()
        with self.assertRaisesRegex(EvidenceError, "must be STARTED"):
            store.mark_terminal(
                "leaf.example",
                status="ERROR",
                exit_code=124,
                ended_at_utc="2026-10-16T00:00:01Z",
                duration_ms=1000,
                reason="TIMEOUT",
            )
        store.mark_started("leaf.example", started_at_utc="2026-10-16T00:00:00Z")
        store.mark_terminal(
            "leaf.example",
            status="ERROR",
            exit_code=124,
            ended_at_utc="2026-10-16T00:00:01Z",
            duration_ms=1000,
            reason="TIMEOUT",
        )
        with self.assertRaisesRegex(EvidenceError, "must be NOT_RUN"):
            store.mark_started("leaf.example", started_at_utc="2026-10-16T00:00:02Z")

    def test_invalid_path_digest_timestamp_and_oversize_are_rejected(self) -> None:
        cases = [
            {**self.rows[0], "source": {**self.rows[0]["source"], "path": "../secret"}},
            {**self.rows[0], "source": {**self.rows[0]["source"], "sha256": "bad"}},
            {**self.rows[0], "argv": ["x" * 5000]},
            {**self.rows[0], "argv": ["scripts/validation/example.py"] * 257},
            {**self.rows[0], "argv": []},
        ]
        for index, row in enumerate(cases):
            with self.subTest(index=index), self.assertRaises(EvidenceError):
                EvidenceStore.create(
                    self.output,
                    identity=self.identity,
                    rows=[row],
                    retention_days=14,
                )

        store = self.create()
        store.initialize_result()
        with self.assertRaisesRegex(EvidenceError, "UTC timestamp"):
            store.mark_started("leaf.example", started_at_utc="not-a-time")

    def test_registered_module_list_argv_is_accepted(self) -> None:
        row = {
            **self.rows[0],
            "argv": ["scripts/validation/example.py", *(["tests.m"] * 80)],
        }
        EvidenceStore.create(
            self.output, identity=self.identity, rows=[row], retention_days=14
        )
        boundary = {**row, "argv": ["scripts/validation/example.py"] * 256}
        EvidenceStore.create(
            pathlib.Path(self.temp.name) / "boundary",
            identity=self.identity,
            rows=[boundary],
            retention_days=14,
        )

    def test_output_directory_must_be_new_visible_and_private(self) -> None:
        hidden = pathlib.Path(self.temp.name) / ".hidden"
        with self.assertRaisesRegex(EvidenceError, "visible"):
            EvidenceStore.create(
                hidden,
                identity=self.identity,
                rows=self.rows,
                retention_days=14,
            )

        existing = pathlib.Path(self.temp.name) / "existing"
        existing.mkdir(mode=0o755)
        with self.assertRaisesRegex(EvidenceError, "already exists"):
            EvidenceStore.create(
                existing,
                identity=self.identity,
                rows=self.rows,
                retention_days=14,
            )


if __name__ == "__main__":
    unittest.main()
