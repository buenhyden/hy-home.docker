"""Metadata-only memory backup coordination with a synthetic Docker transport."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.lib.ops import memory_backup


class Transport:
    def __init__(self, root):
        self.root = root
        self.calls = []
        self.local = []
        self.remote = []
        self.fail = None
        self.offsite = True
        self.containers = []
        self.container_state = {"Status": "running", "Running": True}
        self.container_labels = {}
        self.state_repository = "a" * 64
        self.offsite_repository = "b" * 64

    def __call__(self, argv, **kwargs):
        self.calls.append((tuple(argv), kwargs))
        if self.fail and self.fail in argv:
            return subprocess.CompletedProcess(argv, 1, "", "private diagnostic")
        if "container" in argv and "rm" in argv:
            self.containers.remove(argv[-1])
            return subprocess.CompletedProcess(argv, 0, "removed\n", "")
        if "container" in argv and "ls" in argv:
            return subprocess.CompletedProcess(
                argv, 0, "\n".join(json.dumps(name) for name in self.containers), ""
            )
        if "budget-backup" in argv or "budget-copy" in argv:
            labels = [
                argv[index + 1]
                for index, value in enumerate(argv)
                if value == "--label"
            ]
            self.container_labels = dict(value.split("=", 1) for value in labels)
            self.containers = [argv[argv.index("--name") + 1]]
            self.container_state = {
                "Status": "exited",
                "Running": False,
                "ExitCode": 0,
                "OOMKilled": False,
                "Dead": False,
                "Error": "",
            }
        if "inspect" in argv:
            output = (
                self.container_labels
                if ".Config.Labels" in argv[-2]
                else self.container_state
            )
        elif "config" in argv and "--format" in argv:
            output = {
                "services": {
                    "restic": {
                        "volumes": [
                            {
                                "target": "/src/state/exports",
                                "source": str(self.root / "exports"),
                            }
                        ]
                    },
                    "restic-offsite": {
                        "environment": {
                            "BACKUP_OFFSITE_R2_ACCOUNT_ID": "0" * 32
                            if self.offsite
                            else "",
                            "BACKUP_OFFSITE_R2_BUCKET": "fixture-bucket"
                            if self.offsite
                            else "",
                        }
                    },
                }
            }
        elif argv[-2:] == ["cat", "config"]:
            output = {
                "id": self.offsite_repository
                if "restic-offsite" in argv
                else self.state_repository
            }
        elif "snapshots" in argv:
            output = self.remote if "restic-offsite" in argv else self.local
        elif "ls" in argv:
            snapshot_id = argv[-2]
            rows = self.remote if "restic-offsite" in argv else self.local
            snapshot = next(row for row in rows if row["id"] == snapshot_id)
            output = [{"struct_type": "snapshot", "id": snapshot_id}]
            if snapshot.get("memory", True):
                output.append(
                    {
                        "struct_type": "node",
                        "type": "file",
                        "path": memory_backup.MEMORY_EXPORT,
                        "size": 1024,
                    }
                )
            return subprocess.CompletedProcess(
                argv, 0, "\n".join(json.dumps(row) for row in output), ""
            )
        elif "budget-backup" in argv:
            operation_tag = "memory-op-" + kwargs["input"].split()[2]
            self.local.append(
                {
                    "id": "c" * 64,
                    "tree": "d" * 64,
                    "tags": ["hyhome-state", operation_tag],
                }
            )
            return subprocess.CompletedProcess(argv, 0, "backup completed\n", "")
        elif "budget-copy" in argv:
            copied = {row.get("original") or row["id"] for row in self.remote}
            self.remote.extend(
                {
                    **row,
                    "original": row["id"],
                    "id": hashlib.sha256(row["id"].encode()).hexdigest(),
                }
                for row in self.local
                if row["id"] not in copied
            )
            return subprocess.CompletedProcess(
                argv, 0, "R2 repository size: 1234 bytes\n", ""
            )
        else:
            raise AssertionError(argv)
        return subprocess.CompletedProcess(argv, 0, json.dumps(output), "")


class Ledger:
    def __init__(self):
        self.calls = []
        self.replay = False
        self.completed = False

    def status(self):
        return {"inventory_state": "complete", "generation": 0, "allocations": []}

    def reconcile(self, inventory, *, expected_generation=None):
        self.calls.append(("reconcile", inventory))
        return {}

    def reserve(self, key, fingerprint, amount):
        self.calls.append(("reserve", key, fingerprint, amount))
        return {
            "state": "completed" if self.completed else "pending",
            "replay": self.replay,
            "result": {"target": "state", "reused": True},
        }

    def settle(self, key, allocations, *, result=None):
        self.calls.append(("settle", key, allocations, result))
        return result

    def operation(self, key, fingerprint):
        if self.replay:
            return {
                "state": "completed" if self.completed else "pending",
                "result": {"target": "state", "reused": True},
            }
        return None


class BackupTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.memory = self.root / ".workspace-memory" / "memory.sqlite3"
        self.memory.parent.mkdir(mode=0o700)
        self.transport = Transport(self.root)
        self.ledger = Ledger()

    def run_backup(self, target="state", **kwargs):
        with patch.object(memory_backup, "MemoryCapacity", return_value=self.ledger):
            return memory_backup.run_backup(
                self.memory,
                target,
                request_key="fixture-request",
                runner=self.transport,
                **kwargs,
            )

    def test_inventory_lists_only_memory_metadata_and_remote_location(self):
        self.transport.local = [
            {"id": "c" * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
        ]
        self.transport.remote = [
            {"id": "e" * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
        ]
        result = memory_backup.inventory(self.memory, runner=self.transport)
        self.assertTrue(result["complete"])
        self.assertEqual(
            [row["location"] for row in result["external_snapshots"]],
            ["state", "offsite"],
        )
        self.assertFalse(any("dump" in argv for argv, _ in self.transport.calls))

    def test_reservation_precedes_io_and_new_snapshot_is_settled(self):
        result = self.run_backup()
        self.assertEqual(
            [row[0] for row in self.ledger.calls], ["reconcile", "reserve", "settle"]
        )
        self.assertEqual(result["snapshot_count"], 1)
        allocated = self.ledger.calls[-1][2]
        self.assertEqual(allocated[0]["charged_bytes"], 64 * 1024 * 1024)
        self.assertIn("c" * 64, allocated[0]["resource_key"])
        argv, kwargs = next(
            row for row in self.transport.calls if "budget-backup" in row[0]
        )
        payload = kwargs["input"]
        self.assertIn(hashlib.sha256(payload.encode()).hexdigest(), " ".join(argv))

    def test_failure_keeps_reservation_and_hides_diagnostics(self):
        self.transport.fail = "budget-backup"
        with self.assertRaises(memory_backup.BackupError) as error:
            self.run_backup()
        self.assertNotIn("private diagnostic", str(error.exception))
        self.assertEqual(
            [row[0] for row in self.ledger.calls], ["reconcile", "reserve"]
        )

    def test_pending_replay_starts_no_second_job(self):
        self.ledger.replay = True
        with self.assertRaises(memory_backup.BackupError):
            self.run_backup()
        self.assertFalse(
            any("budget-backup" in argv for argv, _ in self.transport.calls)
        )

    def test_completed_request_returns_recorded_result(self):
        self.ledger.completed = self.ledger.replay = True
        self.assertTrue(self.run_backup()["reused"])
        self.assertFalse(
            any("budget-backup" in argv for argv, _ in self.transport.calls)
        )

    def test_remote_inventory_failure_prevents_new_operation(self):
        self.transport.fail = "restic-offsite"
        with self.assertRaises(memory_backup.BackupError):
            self.run_backup()
        self.assertEqual(self.ledger.calls, [])

    def test_offsite_charges_only_new_memory_trees_and_preserves_size_metric(self):
        self.transport.local = [
            {"id": "c" * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
        ]
        result = self.run_backup("offsite")
        self.assertEqual(result["offsite_repo_bytes"], 1234)
        self.assertEqual(self.ledger.calls[1][-1], 64 * 1024 * 1024)
        self.assertEqual(self.ledger.calls[-1][2][0]["location"], "offsite")

    def test_distinct_source_snapshots_with_same_tree_each_reserve_capacity(self):
        self.transport.local = [
            {"id": identity * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
            for identity in ("c", "f")
        ]
        self.run_backup("offsite")
        self.assertEqual(self.ledger.calls[1][-1], 2 * 64 * 1024 * 1024)
        self.assertEqual(len(self.ledger.calls[-1][2]), 2)

    def test_unconfigured_offsite_is_explicitly_unavailable(self):
        self.transport.offsite = False
        with self.assertRaises(memory_backup.BackupError):
            self.run_backup("offsite")
        self.assertEqual(self.ledger.calls, [])

    def test_unknown_target_is_refused_before_transport(self):
        with self.assertRaises(memory_backup.BackupError):
            self.run_backup("another")
        self.assertEqual(self.transport.calls, [])

    def test_invalid_request_identity_is_refused_before_inventory_or_lock(self):
        for key in ("two words", "line\nbreak", "x" * 129):
            with self.subTest(key_length=len(key)):
                with self.assertRaises(memory_backup.BackupError):
                    memory_backup.run_backup(
                        self.memory, "state", request_key=key, runner=self.transport
                    )
        self.assertEqual(self.transport.calls, [])
        self.assertEqual(list(self.memory.parent.iterdir()), [])

    def test_readonly_inventory_excludes_nonmemory_and_host_snapshots(self):
        self.transport.offsite = False
        self.transport.local = [
            {
                "id": "c" * 64,
                "tree": "d" * 64,
                "tags": ["hyhome-state"],
                "memory": False,
            },
            {"id": "f" * 64, "tree": "d" * 64, "tags": ["hyhome-host"]},
        ]
        result = memory_backup.inventory(self.memory, runner=self.transport)
        self.assertEqual(result["external_snapshots"], [])
        self.assertFalse(
            any(
                "restic-offsite" in argv and "run" in argv
                for argv, _ in self.transport.calls
            )
        )

    def test_malformed_metadata_fails_before_reservation(self):
        real_runner = self.transport
        cases = [
            (lambda argv: "config" in argv and "--format" in argv, "not-json"),
            (
                lambda argv: "config" in argv and "--format" in argv,
                json.dumps({"services": {}}),
            ),
            (
                lambda argv: argv[-2:] == ["cat", "config"],
                json.dumps({"id": "invalid"}),
            ),
            (lambda argv: "snapshots" in argv, "{}"),
            (lambda argv: "snapshots" in argv, "[null]"),
            (
                lambda argv: "snapshots" in argv,
                json.dumps([{"id": "invalid", "tree": "a" * 64}]),
            ),
            (
                lambda argv: "snapshots" in argv,
                json.dumps([{"id": "c" * 64, "tree": "d" * 64, "tags": {}}]),
            ),
        ]
        for selector, output in cases:
            with self.subTest(output=output):

                def runner(argv, *, output=output, selector=selector, **kwargs):
                    return (
                        subprocess.CompletedProcess(argv, 0, output, "")
                        if selector(argv)
                        else real_runner(argv, **kwargs)
                    )

                with self.assertRaises(memory_backup.BackupError):
                    memory_backup.run_backup(self.memory, "state", runner=runner)

    def test_invalid_memory_node_metadata_is_not_absence(self):
        self.transport.local = [
            {"id": "c" * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
        ]
        for output in (
            "",
            "null",
            json.dumps(
                {"path": memory_backup.MEMORY_EXPORT, "type": "symlink", "size": 1}
            ),
        ):
            with self.subTest(output=output):

                def runner(argv, *, output=output, **kwargs):
                    return (
                        subprocess.CompletedProcess(argv, 0, output, "")
                        if "ls" in argv and "container" not in argv
                        else self.transport(argv, **kwargs)
                    )

                with self.assertRaises(memory_backup.BackupError):
                    memory_backup.inventory(self.memory, runner=runner)

    def test_duplicate_snapshot_identity_is_refused(self):
        row = {"id": "c" * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
        self.transport.local = [row, row]
        with self.assertRaises(memory_backup.BackupError):
            memory_backup.inventory(self.memory, runner=self.transport)

    def test_transport_failure_and_output_limit_hide_raw_details(self):
        for value in (
            OSError("private diagnostic"),
            subprocess.TimeoutExpired(["synthetic"], 1),
        ):
            with self.subTest(value=type(value).__name__):

                def runner(argv, *, value=value, **kwargs):
                    raise value

                with self.assertRaises(memory_backup.BackupError) as error:
                    memory_backup.inventory(self.memory, runner=runner)
                self.assertNotIn("private diagnostic", str(error.exception))
        with patch.object(memory_backup, "MAX_OUTPUT_BYTES", 10):
            with self.assertRaises(memory_backup.BackupError):
                memory_backup.inventory(self.memory, runner=self.transport)

    def test_safe_capture_runner_returns_only_stdout(self):
        result = memory_backup._default_runner(
            [
                sys.executable,
                "-c",
                "import sys; print('metadata'); print('private diagnostic',file=sys.stderr)",
            ]
        )
        self.assertEqual(result.stdout, "metadata\n")
        self.assertEqual(result.stderr, "")

    def test_owner_label_and_running_state_are_both_checked(self):
        transport = memory_backup.DockerMetadata(self.memory, self.transport)
        owner = memory_backup._owner(transport)
        request = "a" * 64
        self.transport.containers = [f"hyhome-memory-{owner[:16]}-{request[:16]}"]
        self.transport.container_labels = {
            "hyhome.memory.owner": owner,
            "hyhome.memory.target": "state",
            "hyhome.memory.request": request,
        }
        with self.assertRaises(memory_backup.BackupError):
            self.run_backup()
        self.assertEqual(self.ledger.calls, [])
        self.transport.container_state = {"Status": "exited", "Running": False}
        self.assertEqual(self.run_backup()["result"], "PASS")

    def test_unknown_owned_container_name_stops_coordinator(self):
        self.transport.containers = ["another-producer"]
        with self.assertRaises(memory_backup.BackupError):
            self.run_backup()
        self.assertEqual(self.ledger.calls, [])

    def test_missing_offsite_size_keeps_the_operation_pending(self):
        real = self.transport

        def runner(argv, **kwargs):
            result = real(argv, **kwargs)
            return (
                subprocess.CompletedProcess(argv, 0, "", "")
                if "budget-copy" in argv
                else result
            )

        with patch.object(memory_backup, "MemoryCapacity", return_value=self.ledger):
            with self.assertRaises(memory_backup.BackupError):
                memory_backup.run_backup(self.memory, "offsite", runner=runner)
        self.assertEqual(
            [row[0] for row in self.ledger.calls], ["reconcile", "reserve"]
        )


class RealLedgerTests(unittest.TestCase):
    def setUp(self):
        BackupTests.setUp(self)
        (self.root / "exports").mkdir(mode=0o700)
        memory_backup.MemoryCapacity(self.memory).reconcile(
            {
                "schema_version": 1,
                "complete": True,
                "local_paths": [],
                "external_snapshots": [],
            }
        )

    def test_interrupted_job_preserves_reservation_until_observed_result(self):
        real = self.transport

        def interrupted(argv, **kwargs):
            result = real(argv, **kwargs)
            if "budget-backup" in argv:
                raise KeyboardInterrupt
            return result

        with patch("pathlib.Path.home", return_value=self.root):
            with self.assertRaises(KeyboardInterrupt):
                memory_backup.run_backup(
                    self.memory, "state", request_key="crash", runner=interrupted
                )
            ledger = memory_backup.MemoryCapacity(self.memory)
            self.assertEqual(ledger.status()["reserved_bytes"], 64 * 1024 * 1024)
            with self.assertRaises(memory_backup.BackupError):
                memory_backup.run_backup(
                    self.memory, "state", request_key="new", runner=real
                )
            reconciled = memory_backup.reconcile_backups(self.memory, runner=real)
            self.assertEqual(reconciled["reserved_bytes"], 0)
            self.assertEqual(reconciled["resolved_operations"], ["crash"])
            again = memory_backup.run_backup(
                self.memory, "state", request_key="crash", runner=real
            )
            self.assertEqual(again["result"], "CAPACITY_RECONCILED")

    def test_timeout_with_running_container_blocks_reconciliation_and_new_job(self):
        real = self.transport

        def interrupted(argv, **kwargs):
            if "budget-backup" in argv:
                labels = [
                    argv[index + 1]
                    for index, value in enumerate(argv)
                    if value == "--label"
                ]
                self.transport.container_labels = dict(
                    value.split("=", 1) for value in labels
                )
                self.transport.containers = [argv[argv.index("--name") + 1]]
                raise subprocess.TimeoutExpired(argv, 1)
            return real(argv, **kwargs)

        with patch("pathlib.Path.home", return_value=self.root):
            with self.assertRaises(memory_backup.BackupError):
                memory_backup.run_backup(
                    self.memory, "state", request_key="timeout", runner=interrupted
                )
            for action in (
                lambda: memory_backup.reconcile_backups(self.memory, runner=real),
                lambda: memory_backup.run_backup(
                    self.memory, "state", request_key="new", runner=real
                ),
            ):
                with self.assertRaises(memory_backup.BackupError):
                    action()
            self.assertEqual(
                memory_backup.MemoryCapacity(self.memory).status()["reserved_bytes"],
                64 * 1024 * 1024,
            )

    def test_same_tree_without_original_identity_does_not_resolve_offsite(self):
        self.transport.local = [
            {"id": "c" * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
        ]
        real = self.transport

        def interrupted(argv, **kwargs):
            result = real(argv, **kwargs)
            if "budget-copy" in argv:
                self.transport.remote[0].pop("original")
                raise KeyboardInterrupt
            return result

        with patch("pathlib.Path.home", return_value=self.root):
            with self.assertRaises(KeyboardInterrupt):
                memory_backup.run_backup(
                    self.memory, "offsite", request_key="copy-crash", runner=interrupted
                )
            result = memory_backup.reconcile_backups(self.memory, runner=real)
            self.assertEqual(result["resolved_operations"], [])
            self.assertEqual(result["reserved_bytes"], 64 * 1024 * 1024)

    def test_preexisting_remote_coverage_and_delayed_create_never_release(self):
        self.transport.local = [
            {"id": "c" * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
        ]
        self.transport.remote = [
            {
                "id": "e" * 64,
                "original": "c" * 64,
                "tree": "d" * 64,
                "tags": ["hyhome-state"],
            }
        ]
        real = self.transport

        def delayed(argv, **kwargs):
            if "budget-copy" in argv:
                raise subprocess.TimeoutExpired(argv, 1)
            return real(argv, **kwargs)

        with patch("pathlib.Path.home", return_value=self.root):
            with self.assertRaises(memory_backup.BackupError):
                memory_backup.run_backup(
                    self.memory, "offsite", request_key="delayed-start", runner=delayed
                )
            observed = memory_backup.reconcile_backups(self.memory, runner=real)
            self.assertEqual(observed["resolved_operations"], [])
            self.assertEqual(observed["reserved_bytes"], 0)
            self.assertEqual(
                [row["request_key"] for row in observed["pending_operations"]],
                ["delayed-start"],
            )
            with self.assertRaises(memory_backup.BackupError):
                memory_backup.run_backup(
                    self.memory, "state", request_key="next", runner=real
                )

    def test_registered_legacy_output_is_metadata_only_and_control_files_refused(self):
        legacy = self.root / "legacy"
        legacy.mkdir(mode=0o700)
        output = legacy / "preserved.sqlite3"
        output.write_bytes(b"unread synthetic historical snapshot")
        output.chmod(0o600)
        with patch("pathlib.Path.home", return_value=self.root):
            observed = memory_backup.reconcile_backups(
                self.memory, runner=self.transport, legacy_outputs=(output,)
            )
            self.assertEqual(observed["local_backup_bytes"], 64 * 1024 * 1024)
            with self.assertRaises(memory_backup.BackupError):
                memory_backup.reconcile_backups(
                    self.memory, runner=self.transport, legacy_outputs=(self.memory,)
                )

    def test_partial_offsite_sync_reserves_only_missing_exact_identity_near_cap(self):
        self.transport.local = [
            {"id": str(index) * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
            for index in range(1, 6)
        ]
        self.transport.remote = [
            {
                **row,
                "original": row["id"],
                "id": hashlib.sha256(row["id"].encode()).hexdigest(),
            }
            for row in self.transport.local[:4]
        ]
        with patch("pathlib.Path.home", return_value=self.root):
            result = memory_backup.run_backup(
                self.memory, "offsite", request_key="one-missing", runner=self.transport
            )
            self.assertEqual(result["snapshot_count"], 1)
            self.assertEqual(
                memory_backup.MemoryCapacity(self.memory).status()["reserved_bytes"], 0
            )

    def test_fully_synced_offsite_needs_no_new_memory_allocation_near_cap(self):
        self.transport.local = [
            {"id": str(index) * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
            for index in range(1, 7)
        ]
        self.transport.remote = [
            {
                **row,
                "original": row["id"],
                "id": hashlib.sha256(row["id"].encode()).hexdigest(),
            }
            for row in self.transport.local
        ]
        manual = self.root / "backups" / "agent-memory"
        manual.mkdir(parents=True, mode=0o700)
        copy = manual / "memory.sqlite3"
        copy.write_bytes(b"synthetic historical snapshot")
        copy.chmod(0o600)
        with patch("pathlib.Path.home", return_value=self.root):
            result = memory_backup.run_backup(
                self.memory,
                "offsite",
                request_key="already-synced",
                runner=self.transport,
            )
            self.assertEqual(result["snapshot_count"], 0)
            self.assertLess(
                memory_backup.MemoryCapacity(self.memory).status()["available_bytes"],
                64 * 1024 * 1024,
            )

    def test_failed_terminal_job_cannot_resolve_using_existing_remote_coverage(self):
        self.transport.local = [
            {"id": "c" * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
        ]
        real = self.transport

        def interrupted(argv, **kwargs):
            result = real(argv, **kwargs)
            if "budget-copy" in argv:
                self.transport.container_state["ExitCode"] = 7
                raise subprocess.TimeoutExpired(argv, 1)
            return result

        with patch("pathlib.Path.home", return_value=self.root):
            with self.assertRaises(memory_backup.BackupError):
                memory_backup.run_backup(
                    self.memory,
                    "offsite",
                    request_key="failed-copy",
                    runner=interrupted,
                )
            result = memory_backup.reconcile_backups(self.memory, runner=real)
            self.assertEqual(result["resolved_operations"], [])
            self.assertEqual(result["reserved_bytes"], 64 * 1024 * 1024)

    def test_missing_ledger_refuses_growth_without_creating_a_lock_or_transport(self):
        another = self.root / "uninitialized"
        another.mkdir(mode=0o700)
        memory = another / "memory.sqlite3"
        with self.assertRaises(memory_backup.BackupError):
            memory_backup.run_backup(memory, "state", runner=self.transport)
        self.assertEqual(self.transport.calls, [])
        self.assertEqual(list(another.iterdir()), [])

    def test_repository_switch_keeps_unknown_old_repository_charges(self):
        with patch("pathlib.Path.home", return_value=self.root):
            memory_backup.run_backup(
                self.memory, "state", request_key="original-repo", runner=self.transport
            )
            before = memory_backup.MemoryCapacity(self.memory).status()[
                "external_bytes"
            ]
            self.transport.state_repository = "f" * 64
            with self.assertRaises(memory_backup.CapacityError):
                memory_backup.reconcile_backups(self.memory, runner=self.transport)
            self.assertEqual(
                memory_backup.MemoryCapacity(self.memory).status()["external_bytes"],
                before,
            )

    def test_disabling_offsite_keeps_its_unknown_existing_snapshot_charges(self):
        self.transport.local = [
            {"id": "c" * 64, "tree": "d" * 64, "tags": ["hyhome-state"]}
        ]
        with patch("pathlib.Path.home", return_value=self.root):
            memory_backup.run_backup(
                self.memory,
                "offsite",
                request_key="original-offsite",
                runner=self.transport,
            )
            before = memory_backup.MemoryCapacity(self.memory).status()[
                "external_bytes"
            ]
            self.transport.offsite = False
            with self.assertRaises(memory_backup.CapacityError):
                memory_backup.reconcile_backups(self.memory, runner=self.transport)
            self.assertEqual(
                memory_backup.MemoryCapacity(self.memory).status()["external_bytes"],
                before,
            )

    def test_same_fully_observed_repository_releases_only_completed_absent_snapshots(
        self,
    ):
        with patch("pathlib.Path.home", return_value=self.root):
            memory_backup.run_backup(
                self.memory, "state", request_key="retained-repo", runner=self.transport
            )
            self.transport.local = []
            observed = memory_backup.reconcile_backups(
                self.memory, runner=self.transport
            )
            self.assertEqual(observed["external_bytes"], 0)

    def test_legacy_outputs_share_reserved_namespace_guards_before_transport(self):
        controls = (
            "capacity.sqlite3-wal",
            "capacity.sqlite3-shm",
            "copy.lock",
            ".memory.sqlite3.tmp",
            ".memory.sqlite3.tmp-extra",
            ".memory.sqlite3.restore-" + "f" * 32,
        )
        for name in controls:
            with self.subTest(name=name):
                with self.assertRaises(memory_backup.BackupError):
                    memory_backup.reconcile_backups(
                        self.memory,
                        runner=self.transport,
                        legacy_outputs=(self.memory.parent / name,),
                    )
        self.assertEqual(self.transport.calls, [])

    def test_same_prefix_wrong_full_request_label_never_settles_or_reconciles(self):
        real = self.transport
        key = "exact-request-label"

        def forged_label(argv, **kwargs):
            result = real(argv, **kwargs)
            if "budget-backup" in argv:
                expected = hashlib.sha256(key.encode()).hexdigest()
                suffix = "0" * 48 if expected[16:] != "0" * 48 else "1" * 48
                self.transport.container_labels["hyhome.memory.request"] = (
                    expected[:16] + suffix
                )
            return result

        with patch("pathlib.Path.home", return_value=self.root):
            with self.assertRaises(memory_backup.BackupError):
                memory_backup.run_backup(
                    self.memory, "state", request_key=key, runner=forged_label
                )
            observed = memory_backup.reconcile_backups(self.memory, runner=real)
            self.assertEqual(observed["resolved_operations"], [])
            self.assertEqual(observed["reserved_bytes"], 64 * 1024 * 1024)


if __name__ == "__main__":
    unittest.main()
