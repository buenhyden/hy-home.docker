"""Behavior tests for shared pending/live environment admission."""

import json
import multiprocessing
import os
import sqlite3
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from scripts.lib.ops import environment_admission as admission

LIMITS = {"cpus": 8, "memory_bytes": 8000, "disk_bytes": 8000, "runtime_seconds": 60}
SMALL = {"cpus": 1, "memory_bytes": 100, "disk_bytes": 100, "runtime_seconds": 10}


def _reserve_process(directory, workspace, services, gate, results):
    store = admission.Admission(
        Path(directory),
        namespace="host",
        workspace_id=workspace,
        inventory=["a", "b", "c", "d"],
        limits=LIMITS,
    )
    gate.wait(timeout=5)
    try:
        store.admit(services=services, budget=SMALL, kind="test")
        results.put("admitted")
    except admission.AdmissionError:
        results.put("refused")


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def store(self, workspace="clone-a", **kwargs):
        return admission.Admission(
            self.directory,
            namespace="host",
            workspace_id=workspace,
            inventory=["a", "b", "c", "d"],
            limits=LIMITS,
            **kwargs,
        )

    def reserve(self, store=None, **kwargs):
        return (store or self.store()).admit(
            budget=kwargs.pop("budget", SMALL),
            kind=kwargs.pop("kind", "test"),
            **kwargs,
        )

    def test_two_clones_cannot_split_start_the_complete_inventory(self):
        gate = threading.Barrier(2)

        def start(workspace, services):
            store = self.store(workspace)
            gate.wait(timeout=5)
            try:
                return self.reserve(store, services=services)["token"]
            except admission.AdmissionError:
                return None

        with ThreadPoolExecutor(2) as pool:
            first = pool.submit(start, "clone-a", ["a", "b"])
            second = pool.submit(start, "clone-b", ["c", "d"])
            results = [first.result(timeout=10), second.result(timeout=10)]
        self.assertEqual(1, sum(value is not None for value in results))
        self.assertEqual(1, len(self.store().records()))

    def test_independent_processes_contend_on_the_same_host_reservations(self):
        context = multiprocessing.get_context("fork")
        gate, results = context.Barrier(2), context.Queue()
        processes = [
            context.Process(
                target=_reserve_process,
                args=(str(self.directory), name, services, gate, results),
            )
            for name, services in (("clone-a", ["a", "b"]), ("clone-b", ["c", "d"]))
        ]
        try:
            for process in processes:
                process.start()
            outcomes = sorted(results.get(timeout=10) for _ in processes)
            self.assertEqual(["admitted", "refused"], outcomes)
            for process in processes:
                process.join(timeout=5)
                self.assertEqual(0, process.exitcode)
        finally:
            for process in processes:
                if process.is_alive():
                    process.kill()
                process.join()
            results.close()

    def test_overlapping_services_count_once_but_budgets_count_each_run(self):
        store = self.store()
        budget = dict(SMALL, cpus=4)
        self.reserve(store, services=["a"], budget=budget)
        self.reserve(store, services=["a"], budget=budget)
        with self.assertRaisesRegex(admission.AdmissionError, "budget"):
            self.reserve(store, services=["b"])

    def test_observation_runs_under_the_same_write_transaction(self):
        store = self.store()
        calls = []

        def observe():
            connection = sqlite3.connect(store.path, timeout=0, isolation_level=None)
            try:
                with self.assertRaises(sqlite3.OperationalError):
                    connection.execute("BEGIN IMMEDIATE")
                calls.append(True)
            finally:
                connection.close()
            return {"services": ["a", "b", "c"], "budget": {}}

        store.observe = observe
        with self.assertRaisesRegex(admission.AdmissionError, "complete_inventory"):
            self.reserve(store, services=["d"])
        self.assertEqual([True], calls)
        self.assertEqual([], store.records())

    def test_external_usage_is_summed_without_false_shared_deduplication(self):
        store = self.store(observe=lambda: {"budget": {"cpus": 7.5}})
        with self.assertRaisesRegex(admission.AdmissionError, "budget"):
            self.reserve(store)

    def test_fill_disk_uses_one_locked_observation_and_subtracts_active_claims(self):
        store = self.store()
        existing = self.reserve(
            store, services=["a"], budget=dict(SMALL, disk_bytes=1500)
        )
        observations = []

        def observe():
            observations.append(True)
            used = 2400 + 100 * len(observations)
            return {"budget": {"disk_bytes": used}}

        store.observe = observe
        # This earlier external read changes before the transaction's observation.
        self.assertEqual(2500, observe()["budget"]["disk_bytes"])
        request = dict(SMALL)
        record = self.reserve(store, services=["b"], budget=request, fill_disk=True)
        self.assertEqual(2, len(observations))
        self.assertEqual(3900, record["budget"]["disk_bytes"])
        self.assertEqual(100, request["disk_bytes"])
        self.assertEqual(existing["token"], store.records()[0]["token"])
        with self.assertRaisesRegex(admission.AdmissionError, "disk_bytes_budget"):
            self.reserve(store, services=["c"])

    def test_fill_disk_requires_minimum_headroom_and_an_actual_boolean(self):
        store = self.store(observe=lambda: {"budget": {"disk_bytes": 7950}})
        with self.assertRaisesRegex(admission.AdmissionError, "disk_bytes_budget"):
            self.reserve(store, fill_disk=True)
        self.assertEqual([], store.records())
        for flag in (None, "true", 1, 0, []):
            with self.subTest(flag=flag), self.assertRaises(admission.AdmissionError):
                self.reserve(fill_disk=flag)

    def test_default_disk_reservation_stays_explicit_and_other_limits_still_apply(self):
        store = self.store()
        record = self.reserve(store)
        self.assertEqual(SMALL["disk_bytes"], record["budget"]["disk_bytes"])
        for field in ("cpus", "memory_bytes", "runtime_seconds"):
            with self.subTest(field=field), self.assertRaises(admission.AdmissionError):
                self.reserve(
                    store,
                    budget=dict(SMALL, **{field: LIMITS[field] + 1}),
                    fill_disk=True,
                )

    def test_disk_memory_and_runtime_bounds_are_enforced(self):
        for key in ("memory_bytes", "disk_bytes", "runtime_seconds"):
            with self.subTest(key=key), self.assertRaises(admission.AdmissionError):
                self.reserve(budget=dict(SMALL, **{key: LIMITS[key] + 1}))

    def test_numeric_values_reject_nan_infinity_booleans_and_negative(self):
        for value in (float("nan"), float("inf"), -1, True, "1"):
            with self.subTest(value=value), self.assertRaises(admission.AdmissionError):
                self.reserve(budget=dict(SMALL, cpus=value))

    def test_unknown_services_and_whole_selection_are_refused(self):
        for services in (["missing"], ["a", "b", "c", "d"], ["*"]):
            with (
                self.subTest(services=services),
                self.assertRaises(admission.AdmissionError),
            ):
                self.reserve(services=services)

    def test_expiration_does_not_reclaim_pending_resources(self):
        store = self.store()
        record = self.reserve(store, services=["a", "b"], budget=dict(SMALL, cpus=8))
        with mock.patch.object(
            admission.time, "time", return_value=record["expires_at"] + 100
        ):
            self.assertEqual(record["token"], store.records()[0]["token"])
            with self.assertRaises(admission.AdmissionError):
                self.reserve(store, services=["c"])

    def test_token_fences_cross_workspace_updates_and_cleanup(self):
        first, second = self.store(), self.store("clone-b")
        record = self.reserve(first)
        for operation in (
            lambda: second.update(record["token"], changed=True),
            lambda: second.release(record["token"], lambda _: True),
            lambda: first.attach("wrong-token"),
        ):
            with self.assertRaises(admission.AdmissionError):
                operation()
        self.assertEqual(1, len(first.records()))

    def test_live_unknown_and_unverified_resources_remain_charged(self):
        store = self.store()
        record = self.reserve(store)
        store.attach(record["token"], identity=admission.process_identity())
        self.assertFalse(store.release(record["token"], lambda _: True))
        with mock.patch.object(admission, "process_status", return_value="unknown"):
            self.assertFalse(store.release(record["token"], lambda _: True))
        with mock.patch.object(admission, "process_status", return_value="absent"):
            self.assertFalse(store.release(record["token"], lambda _: None))
            self.assertFalse(store.release(record["token"], lambda _: False))
            self.assertTrue(store.release(record["token"], lambda _: True))
        self.assertEqual([], store.records())
        with self.assertRaises(admission.AdmissionError):
            store.attach(record["token"])

    def test_detached_container_ownership_can_finish_without_attached_process(self):
        store = self.store()
        record = self.reserve(store)
        attached = store.attach(record["token"], type="compose", project="owned")
        self.assertIsNone(attached["identity"])
        self.assertEqual("compose", attached["metadata"]["type"])
        self.assertTrue(
            store.release(
                record["token"], lambda row: row["metadata"]["project"] == "owned"
            )
        )

    def test_metadata_cannot_mutate_reserved_authority(self):
        record = self.reserve()
        with self.assertRaises(admission.AdmissionError):
            self.store().update(record["token"], token="replacement")
        current = self.store().update(
            record["token"], process_file="owned.process.json"
        )
        self.assertEqual("owned.process.json", current["metadata"]["process_file"])

    def test_resource_keys_and_kind_limits_are_shared(self):
        store = self.store(kind_limits={"lab": 1})
        self.reserve(store, kind="lab", resources=["port:5432"])
        with self.assertRaises(admission.AdmissionError):
            self.reserve(self.store("clone-b"), resources=["port:5432"])
        with self.assertRaises(admission.AdmissionError):
            self.reserve(self.store("clone-b"), kind="lab")

    def test_numeric_reservations_sum_across_daemon_inventory_scopes(self):
        first = self.store(inventory_key="daemon-a:home")
        second = self.store("clone-b", inventory_key="daemon-b:home")
        self.reserve(first, services=["a", "b"], budget=dict(SMALL, cpus=8))
        with self.assertRaisesRegex(admission.AdmissionError, "budget"):
            self.reserve(second, services=["c", "d"])

    def test_changed_inventory_cannot_shrink_the_active_service_universe(self):
        self.reserve(services=["a"])
        with self.assertRaises(admission.AdmissionError):
            admission.Admission(
                self.directory,
                namespace="host",
                workspace_id="other",
                inventory=["a", "b"],
                limits=LIMITS,
            ).admit(services=["b"], budget=SMALL, kind="test")

    def test_private_state_refuses_symlink_and_public_directory(self):
        link = self.directory / "alias"
        link.symlink_to(self.directory, target_is_directory=True)
        for path in (link, self.directory / "public"):
            if not path.is_symlink():
                path.mkdir(mode=0o755)
            with self.subTest(path=path), self.assertRaises(admission.AdmissionError):
                admission.Admission(
                    path,
                    namespace="host",
                    workspace_id="x",
                    inventory=["a", "b"],
                    limits=LIMITS,
                )

    def test_corrupt_database_refuses_without_resetting_state(self):
        store = self.store()
        store.path.write_bytes(b"not a sqlite database")
        with self.assertRaises(admission.AdmissionError):
            self.reserve(store)
        self.assertEqual(b"not a sqlite database", store.path.read_bytes())

    def test_corrupt_record_never_disappears_from_accounting(self):
        store = self.store()
        record = self.reserve(store)
        with sqlite3.connect(store.path) as connection:
            connection.execute(
                "UPDATE runs SET record=? WHERE token=?",
                (json.dumps(dict(record, state="unknown-corruption")), record["token"]),
            )
        with self.assertRaises(admission.AdmissionError):
            store.records()
        with self.assertRaises(admission.AdmissionError):
            self.reserve(store)

    def test_active_policy_cannot_raise_the_host_budget(self):
        self.reserve()
        bigger = admission.Admission(
            self.directory,
            namespace="host",
            workspace_id="clone-b",
            inventory=["a", "b", "c", "d"],
            limits=dict(LIMITS, cpus=16),
        )
        with self.assertRaisesRegex(admission.AdmissionError, "policy_mismatch"):
            self.reserve(bigger)

    def test_public_database_and_database_symlink_are_refused(self):
        store = self.store()
        store.path.chmod(0o644)
        with self.assertRaises(admission.AdmissionError):
            self.store()
        store.path.unlink()
        outside = self.directory / "outside"
        outside.write_text("untouched")
        store.path.symlink_to(outside)
        with self.assertRaises(admission.AdmissionError):
            self.store()
        self.assertEqual("untouched", outside.read_text())

    def test_strict_observation_refuses_missing_resource_measurements(self):
        store = self.store(
            observe=lambda: {"budget": {"cpus": 0}}, strict_observation=True
        )
        with self.assertRaisesRegex(admission.AdmissionError, "incomplete_budget"):
            self.reserve(store)

    def test_live_observed_lab_and_conflicting_policy_are_not_ignored(self):
        store = self.store(
            kind_limits={"lab": 1}, observe=lambda: {"kind_counts": {"lab": 1}}
        )
        with self.assertRaisesRegex(admission.AdmissionError, "kind_budget"):
            self.reserve(store, kind="lab")
        store.observe = None
        self.reserve(store, kind="lab")
        second = self.store("clone-b", kind_limits={"lab": 2})
        with self.assertRaisesRegex(admission.AdmissionError, "policy_mismatch"):
            self.reserve(second, kind="lab")

    def test_attach_cannot_replace_a_recorded_process_identity(self):
        store = self.store()
        record, identity = self.reserve(store), admission.process_identity()
        store.attach(record["token"], identity=identity)
        with self.assertRaises(admission.AdmissionError):
            store.attach(
                record["token"],
                identity=dict(identity, start_ticks=identity["start_ticks"] + 1),
            )

    def test_production_factory_shares_host_across_daemons_and_ignores_home_override(
        self,
    ):
        fake_git = self.directory / ".git"
        fake_git.mkdir()

        def observe():
            return {"budget": {"cpus": 0, "memory_bytes": 0, "disk_bytes": 0}}

        with (
            mock.patch.object(
                admission.pwd,
                "getpwuid",
                return_value=SimpleNamespace(pw_dir=str(self.directory)),
            ),
            mock.patch.object(
                admission.subprocess,
                "run",
                return_value=SimpleNamespace(stdout=str(fake_git)),
            ),
            mock.patch.dict(
                os.environ, {"HOME": "/untrusted", "HY_HOME_CAPTURE_DIR": "/untrusted"}
            ),
        ):
            first = admission.host_admission(
                self.directory,
                daemon_id="daemon-a",
                inventory=["a", "b"],
                limits=LIMITS,
                observe=observe,
            )
            second = admission.host_admission(
                self.directory,
                daemon_id="daemon-b",
                inventory=["a", "b"],
                limits=LIMITS,
                observe=observe,
            )
        self.assertEqual(first.path, second.path)
        self.assertNotEqual(first.inventory_key, second.inventory_key)
        self.assertEqual(str(fake_git), first.workspace_id)
        self.reserve(first, services=["a"], budget=dict(SMALL, cpus=8))
        with self.assertRaisesRegex(admission.AdmissionError, "budget"):
            self.reserve(second, services=["a"])

    def test_recovery_needs_only_existing_identity_and_proven_absence(self):
        fake_git = self.directory / ".git"
        fake_git.mkdir()
        with (
            mock.patch.object(
                admission.pwd,
                "getpwuid",
                return_value=SimpleNamespace(pw_dir=str(self.directory)),
            ),
            mock.patch.object(
                admission.subprocess,
                "run",
                return_value=SimpleNamespace(stdout=str(fake_git)),
            ),
        ):
            with self.assertRaises(admission.AdmissionError):
                admission.recovery_admission(self.directory, daemon_id="daemon-a")
            store = admission.host_admission(
                self.directory,
                daemon_id="daemon-a",
                inventory=["a", "b"],
                limits=LIMITS,
                observe=lambda: {
                    "budget": {"cpus": 0, "memory_bytes": 0, "disk_bytes": 0}
                },
            )
            record = self.reserve(store, services=["a"])
            recovery = admission.recovery_admission(
                self.directory, daemon_id="daemon-a"
            )
            other = admission.recovery_admission(self.directory, daemon_id="daemon-b")
        self.assertIsNone(recovery.limits)
        self.assertEqual(record["token"], recovery.records()[0]["token"])
        for operation in (
            lambda: self.reserve(recovery),
            lambda: recovery.attach(record["token"]),
            lambda: recovery.update(record["token"], extra=True),
            lambda: other.release(record["token"], lambda _: True),
        ):
            with self.assertRaises(admission.AdmissionError):
                operation()
        self.assertTrue(recovery.release(record["token"], lambda _: True))

    def test_fixed_private_host_base_does_not_change_group_writable_state(self):
        fake_git = self.directory / ".git"
        fake_git.mkdir()
        local_state = self.directory / ".local/state"
        local_state.mkdir(parents=True)
        local_state.chmod(0o775)
        (local_state / "hy-home").mkdir(mode=0o755)
        with (
            mock.patch.object(
                admission.pwd,
                "getpwuid",
                return_value=SimpleNamespace(pw_dir=str(self.directory)),
            ),
            mock.patch.object(
                admission.subprocess,
                "run",
                return_value=SimpleNamespace(stdout=str(fake_git)),
            ),
        ):
            store = admission.host_admission(
                self.directory,
                daemon_id="daemon-a",
                inventory=["a", "b"],
                limits=LIMITS,
                observe=lambda: {
                    "budget": {"cpus": 0, "memory_bytes": 0, "disk_bytes": 0}
                },
            )
            record = self.reserve(store, services=["a"])
            recovered = admission.recovery_admission(
                self.directory, daemon_id="daemon-a"
            )
        canonical = self.directory / ".hy-home-execution"
        self.assertTrue(store.path.is_relative_to(canonical))
        self.assertEqual(0o700, canonical.stat().st_mode & 0o777)
        self.assertEqual(0o775, local_state.stat().st_mode & 0o777)
        self.assertFalse((local_state / "hy-home/execution").exists())
        self.assertEqual(store.path, recovered.path)
        self.assertTrue(recovered.release(record["token"], lambda _: True))

    def test_host_state_directory_is_readonly_and_uses_the_actual_uid_home(self):
        with (
            mock.patch.object(
                admission.pwd,
                "getpwuid",
                return_value=SimpleNamespace(pw_dir=str(self.directory)),
            ) as lookup,
            mock.patch.dict(
                os.environ, {"HOME": "/untrusted", "XDG_STATE_HOME": "/untrusted"}
            ),
        ):
            path = admission.host_state_directory()
        self.assertEqual(self.directory / ".hy-home-execution", path)
        self.assertFalse(path.exists())
        lookup.assert_called_once_with(os.getuid())

    def test_recovery_never_initializes_missing_tables(self):
        store = self.store()
        self.reserve(store)
        with sqlite3.connect(store.path) as connection:
            connection.execute("DROP TABLE runs")
        with self.assertRaisesRegex(
            admission.AdmissionError, "incomplete_admission_state"
        ):
            store.records()
        with sqlite3.connect(store.path) as connection:
            self.assertEqual(
                [],
                connection.execute(
                    "SELECT name FROM sqlite_master WHERE name='runs'"
                ).fetchall(),
            )

    def test_verified_release_keeps_no_completed_run_ledger(self):
        store = self.store()
        record = self.reserve(store, resources=["port:5432"])
        self.assertTrue(store.release(record["token"], lambda _: True))
        with sqlite3.connect(store.path) as connection:
            self.assertEqual(
                0, connection.execute("SELECT count(*) FROM runs").fetchone()[0]
            )
        with self.assertRaisesRegex(admission.AdmissionError, "unknown_lease_token"):
            store.release(record["token"], lambda _: True)
        replacement = self.reserve(store, resources=["port:5432"])
        self.assertNotEqual(record["token"], replacement["token"])

    def test_malformed_persisted_deadline_owner_and_project_fail_closed(self):
        store = self.store()
        record = self.reserve(store)
        changes = (
            ("expires_at", float("nan")),
            ("created_at", "yesterday"),
            ("expires_at", record["created_at"] - 1),
            ("owner", {}),
            ("project", "../other-project"),
        )
        for key, value in changes:
            with self.subTest(key=key, value=value):
                with sqlite3.connect(store.path) as connection:
                    connection.execute(
                        "UPDATE runs SET record=? WHERE token=?",
                        (json.dumps(dict(record, **{key: value})), record["token"]),
                    )
                with self.assertRaises(admission.AdmissionError):
                    store.records()
        with sqlite3.connect(store.path) as connection:
            connection.execute(
                "UPDATE runs SET record=? WHERE token=?",
                (json.dumps(record), record["token"]),
            )

    def test_invalid_project_is_refused_before_creating_an_intent(self):
        store = self.store()
        with self.assertRaises(admission.AdmissionError):
            self.reserve(store, project="../other-project")
        self.assertEqual([], store.records())


class ProcessIdentityTests(unittest.TestCase):
    def test_current_identity_and_pid_reuse_are_distinguished(self):
        identity = admission.process_identity()
        self.assertEqual(os.getpid(), identity["pid"])
        self.assertEqual(os.getpgrp(), identity["pgid"])
        self.assertEqual("alive", admission.process_status(identity))
        self.assertEqual(
            "absent",
            admission.process_status(
                dict(identity, start_ticks=identity["start_ticks"] + 1)
            ),
        )

    def test_missing_and_unreadable_processes_have_distinct_status(self):
        identity = admission.process_identity()
        with mock.patch.object(admission, "process_identity", return_value=None):
            self.assertEqual("absent", admission.process_status(identity))
        with mock.patch.object(
            admission,
            "process_identity",
            side_effect=admission.AdmissionError("denied"),
        ):
            self.assertEqual("unknown", admission.process_status(identity))

    def test_changed_process_group_is_unknown_not_proof_of_exit(self):
        identity = admission.process_identity()
        with mock.patch.object(
            admission,
            "process_identity",
            return_value=dict(identity, pgid=identity["pgid"] + 1),
        ):
            self.assertEqual("unknown", admission.process_status(identity))

    def test_unavailable_boot_identity_is_unknown_not_an_absent_process(self):
        original = Path.read_text

        def read(path, *args, **kwargs):
            if str(path) == "/proc/sys/kernel/random/boot_id":
                raise FileNotFoundError
            return original(path, *args, **kwargs)

        with (
            mock.patch.object(Path, "read_text", read),
            self.assertRaises(admission.AdmissionError),
        ):
            admission.process_identity()


if __name__ == "__main__":
    unittest.main()
