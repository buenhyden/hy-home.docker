"""P05 source/guard tests and an explicit current-artifact native rehearsal."""

import hashlib
import inspect
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tests.validation import _p05_opsflow_native as native
from tests.validation import _p05_opsflow_recovery as recovery


class P05NativeGuards(unittest.TestCase):
    def test_registration_uses_authenticated_personal_project_rest_and_rejects_mismatch(
        self,
    ):
        from tests.validation import _p05_opsflow_registration as registration

        for change in (
            {},
            {"active": True},
            {"project_id": "foreign"},
            {"personal": False},
            {"id": "bad/id"},
            {"unexpected": "private-canary"},
        ):
            calls = []
            fixture = SimpleNamespace(
                attempt="opsflow-native-" + "a" * 24, receipt={}, private=mock.Mock()
            )
            scenario = SimpleNamespace(
                fixture=fixture,
                secrets={"notifier": ("synthetic", None)},
                credential_ids={},
                postgres_credential=lambda _value: {"type": "postgres"},
            )

            def api(action, _calls=calls, _change=change, _fixture=fixture, **payload):
                _calls.append((action, payload))
                if action == "setup":
                    return {"id": "00000000-0000-4000-8000-000000000001"}
                if action == "credential":
                    return {
                        "id": "pg-id"
                        if payload["credential"]["type"] == "postgres"
                        else "smtp-id"
                    }
                if action == "workflow_create":
                    return {
                        "id": "workflow-id",
                        "active": False,
                        "project_id": "personal-id",
                        "personal_project_id": "personal-id",
                        "personal": True,
                        **_change,
                    }
                if action == "workflows":
                    return {
                        "rows": [
                            {
                                "id": "workflow-id",
                                "active": False,
                                "name": "Opsflow native " + _fixture.attempt,
                            }
                        ]
                    }
                raise AssertionError("unexpected API action")

            scenario.api = api
            if change:
                with (
                    self.subTest(fields=tuple(change)),
                    self.assertRaises(native.RehearsalFailure),
                ):
                    registration.register(scenario)
            else:
                identifier, name = registration.register(scenario)
                self.assertEqual("workflow-id", identifier)
                self.assertEqual("Opsflow native " + fixture.attempt, name)
                body = next(
                    payload["workflow"]
                    for action, payload in calls
                    if action == "workflow_create"
                )
                self.assertEqual(
                    {"name", "nodes", "connections", "settings"}, set(body)
                )
                self.assertEqual(
                    "EDITOR_REST_PINNED_2_43_6",
                    fixture.receipt["workflow_registration"]["transport"],
                )

    def test_deployed_public_tree_requires_root_ownership_modes_and_exact_hashes(self):
        expected = {"package.json": "a" * 64}
        rows = [
            {"name": "opsflow", "kind": "directory", "uid": 0, "gid": 0, "mode": 0o755},
            {
                "name": "opsflow/package.json",
                "kind": "file",
                "uid": 0,
                "gid": 0,
                "mode": 0o644,
                "sha256": "a" * 64,
            },
        ]
        self.assertEqual(
            {"files": 1, "directories": 1}, native.validate_deployment(rows, expected)
        )
        for change in (
            {"uid": 1000},
            {"gid": 1000},
            {"mode": 0o664},
            {"sha256": "b" * 64},
            {"kind": "symlink"},
            {"name": "opsflow/../secret"},
        ):
            with (
                self.subTest(fields=tuple(change)),
                self.assertRaises(native.RehearsalFailure),
            ):
                native.validate_deployment([rows[0], {**rows[1], **change}], expected)
        for changed in (
            rows + rows[1:],
            rows[:1],
            [*rows, {**rows[1], "name": "opsflow/extra"}],
        ):
            with self.assertRaises(native.RehearsalFailure):
                native.validate_deployment(changed, expected)

    def test_already_inactive_workflow_fence_uses_verified_state(self):
        scenario = native.P05Scenario(
            "test_actual_queue_runner_capture_unknown_reconcile_and_restore"
        )
        scenario.execution_ids = ["42"]
        scenario.fixture = SimpleNamespace(
            stop=mock.Mock(),
            containers={role: role for role in ("runner", "worker", "mailpit")},
            _verify_owned=lambda _record: {
                "State": {"Status": "exited", "Running": False, "Pid": 0}
            },
            exec_result=lambda *args, **kwargs: SimpleNamespace(
                returncode=0, stdout='{"scanned":true,"matching":0,"ids":["42"]}'
            ),
            receipt={},
            attempt="opsflow-native-" + "a" * 24,
        )

        terminal = {"value": True}

        def api(action, **payload):
            if action == "execution":
                self.assertEqual("42", payload["executionId"])
                return {"status": "crashed", "terminal": terminal["value"]}
            self.assertEqual("workflows", action)
            return {"rows": [{"id": "owned", "active": False, "versionId": "v"}]}

        scenario.api = api
        scenario.fence("owned")
        self.assertTrue(
            scenario.fixture.receipt["recovery_barrier"]["workflow_inactive"]
        )
        self.assertTrue(
            scenario.fixture.receipt["recovery_barrier"]["old_executions_terminal"]
        )
        # A non-terminal old execution in n8n metadata keeps the barrier shut.
        terminal["value"] = False
        with self.assertRaises(recovery.RehearsalFailure):
            scenario.fence("owned")

    def test_mailpit_key_uses_filename_flag_and_keeps_secret_environment_guard(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = object.__new__(native.P05Fixture)
            fixture.directory = Path(directory)
            fixture.generation = 1
            fixture.host_uid = os.geteuid()
            fixture.mailpit_dirs = {}
            fixture.smtp_epoch = 1
            fixture.smtp_files = {1: Path(directory) / "synthetic-auth"}
            fixture.create = mock.Mock()
            fixture.start = mock.Mock()
            fixture.start_mailpit()
            call = fixture.create.call_args
            self.assertIn(
                "--smtp-tls-key=/run/secrets/server.key", call.kwargs.get("command", ())
            )
            self.assertFalse(
                any(
                    "KEY=" in value or "PASSWORD=" in value or "TOKEN=" in value
                    for value in call.kwargs["env"]
                )
            )
            self.assertIn(
                native.inputs.bind_mount(
                    Path(directory) / "p05-server.key", "/run/secrets/server.key"
                ),
                call.kwargs["mounts"],
            )
            fixture.start.assert_called_once_with("mailpit")

    def test_public_artifact_reader_rejects_symlinks_and_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "public.js"
            source.write_bytes(b"public code")
            self.assertEqual(
                hashlib.sha256(b"public code").hexdigest(), native.public_digest(source)
            )
            linked = root / "linked.js"
            linked.symlink_to(source)
            with self.assertRaises(native.RehearsalFailure):
                native.public_digest(linked)
            (root / "linked-dir").symlink_to(root, target_is_directory=True)
            with self.assertRaises(native.RehearsalFailure):
                native.public_digest(root / "linked-dir/public.js")
            original = os.read

            def changed(descriptor, count):
                result = original(descriptor, count)
                if result:
                    source.write_bytes(b"changed")
                return result

            with mock.patch.object(native.os, "read", side_effect=changed):
                with self.assertRaises(native.RehearsalFailure):
                    native.public_digest(source)

    def test_candidate_is_bound_to_independent_current_dist_and_exact_base(self):
        expected = {"OpsflowSmtp.node.js": "a" * 64, "transport.js": "b" * 64}
        value = {
            "reference": "hy-home/p05-n8n-fixture:" + "c" * 12,
            "image_id": "sha256:" + "d" * 64,
            "base_id": native.inputs.N8N_ID,
            "binding": "c" * 64,
            "dist_sha256": expected,
        }
        self.assertEqual(value, native.validate_artifact(value, "c" * 64, expected))
        for change in (
            {"image_id": "latest"},
            {"base_id": "sha256:" + "e" * 64},
            {"binding": "f" * 64},
            {"dist_sha256": {**expected, "transport.js": "f" * 64}},
            {"unexpected": "private-payload"},
        ):
            with (
                self.subTest(change=tuple(change)),
                self.assertRaises(native.RehearsalFailure),
            ):
                native.validate_artifact({**value, **change}, "c" * 64, expected)

    def test_recovery_requires_real_process_socket_and_exact_job_barriers(self):
        good = {
            "smtp_egress_held": True,
            "workflow_inactive": True,
            "old_execution_ids": ["42"],
            "old_processes_absent": True,
            "old_sockets_absent": True,
            "old_broker_jobs_absent": True,
            "old_executions_terminal": True,
            "owned_attempt": "opsflow-native-" + "a" * 24,
        }
        self.assertEqual(good, recovery.validate_barrier(good))
        for field in (
            "smtp_egress_held",
            "workflow_inactive",
            "old_processes_absent",
            "old_sockets_absent",
            "old_broker_jobs_absent",
            "old_executions_terminal",
        ):
            for value in (False, 1, None):
                with (
                    self.subTest(field=field, value=value),
                    self.assertRaises(recovery.RehearsalFailure),
                ):
                    recovery.validate_barrier({**good, field: value})
        for change in (
            {"old_execution_ids": []},
            {"old_execution_ids": ["42", "42"]},
            {"cancel_response": True},
            {"old_execution_ids": ["private-payload"]},
        ):
            with self.assertRaises(recovery.RehearsalFailure):
                recovery.validate_barrier({**good, **change})


class P05RestoreReplayAndInterruptionGuards(unittest.TestCase):
    RUN = "a" * 64
    FRESH = "f" * 64
    LINES = (
        "outbox|1|" + "a" * 64 + "|accepted_by_smtp|1|5||t|t||x|y",
        "outbox|2|" + "b" * 64 + "|unknown|1|5|smtp_outcome_unknown||t||x|y",
        "run|" + "a" * 64 + "|hy-home.k8s|published|z",
    )

    def test_snapshot_shape_is_closed_and_nonempty(self):
        self.assertEqual(self.LINES, recovery.snapshot_lines("\n".join(self.LINES)))
        for text in ("", "run|only", "private|x\noutbox|1|r|unknown|1"):
            with self.subTest(text=text), self.assertRaises(recovery.RehearsalFailure):
                recovery.snapshot_lines(text)

    def test_restored_state_must_equal_pre_restore_rows_exactly(self):
        summary = recovery.validate_restored_state(self.LINES, self.LINES)
        self.assertEqual({"accepted_by_smtp": 1, "unknown": 1}, summary["states"])
        drifted = (self.LINES[0].replace("|1|5|", "|2|5|"), *self.LINES[1:])
        for after in (drifted, self.LINES[:2], (*self.LINES, "audit|x")):
            with self.assertRaises(recovery.RehearsalFailure):
                recovery.validate_restored_state(self.LINES, after)

    def test_same_input_replay_is_dedup_only_and_claims_nothing(self):
        self.assertEqual(
            {"replayed": 2, "claimable": 0},
            recovery.validate_replay(
                ["replayed", "replayed"], self.LINES, self.LINES, "0"
            ),
        )
        for results, after, claimable in (
            ([], self.LINES, "0"),
            (["replayed", "published"], self.LINES, "0"),
            (["replayed"], (*self.LINES, "outbox|3|" + "c" * 64 + "|pending"), "0"),
            (["replayed"], self.LINES, "1"),
        ):
            with self.assertRaises(recovery.RehearsalFailure):
                recovery.validate_replay(results, self.LINES, after, claimable)

    def test_next_claim_sends_only_the_fresh_row(self):
        fresh = "outbox|3|" + self.FRESH + "|accepted_by_smtp|1|5||t|t||x|y"
        after = (*self.LINES, fresh, "run|" + self.FRESH + "|hy-home.k8s|published|z")
        self.assertTrue(
            recovery.validate_next_claim(self.LINES, after, self.FRESH)[
                "old_rows_unchanged"
            ]
        )
        resent = (self.LINES[0], self.LINES[1].replace("unknown", "accepted_by_smtp"))
        for changed in (
            (*resent, self.LINES[2], fresh),
            (*self.LINES, fresh.replace("accepted_by_smtp", "unknown")),
            (*self.LINES, fresh.replace("|1|5|", "|2|5|")),
            self.LINES,
        ):
            with self.assertRaises(recovery.RehearsalFailure):
                recovery.validate_next_claim(self.LINES, changed, self.FRESH)

    def test_next_claim_filters_the_parsed_run_id_not_a_substring(self):
        fresh = "outbox|3|" + self.FRESH + "|accepted_by_smtp|1|5||t|t||x|y"
        audit = "audit|req|2|1|requeue_dead|" + self.FRESH + "|t1"
        before = (*self.LINES, audit)
        after = (*before, fresh, "run|" + self.FRESH + "|hy-home.k8s|published|z")
        self.assertTrue(
            recovery.validate_next_claim(before, after, self.FRESH)[
                "old_rows_unchanged"
            ]
        )
        drifted = (*self.LINES, audit.replace("|t1", "|t2"), fresh)
        with self.assertRaises(recovery.RehearsalFailure):
            recovery.validate_next_claim(before, drifted, self.FRESH)

    def test_hold_log_parser_reads_only_closed_tokens(self):
        text = (
            "P05_HOLD LISTENING\nP05_HOLD DATA_STARTED\n"
            "P05_HOLD BODY_HELD at=1762300000123\n"
            "P05_HOLD CLIENT_CLOSED after_body_ms=412\nunrelated private text\n"
        )
        self.assertEqual(
            {
                "data_started": True,
                "body_held_at_ms": 1762300000123,
                "closed_after_body_ms": 412,
            },
            recovery.parse_hold(text),
        )
        self.assertEqual(
            {
                "data_started": False,
                "body_held_at_ms": None,
                "closed_after_body_ms": None,
            },
            recovery.parse_hold("P05_HOLD LISTENING\n"),
        )
        for text in (
            "P05_HOLD BODY_HELD at=1\nP05_HOLD BODY_HELD at=2\n",
            "P05_HOLD CLIENT_CLOSED after_body_ms=-1\n",
            "P05_HOLD BODY_HELD at=abc\n",
        ):
            with self.subTest(text=text), self.assertRaises(recovery.RehearsalFailure):
                recovery.parse_hold(text)

    def test_active_send_interruption_requires_a_kill_inside_the_socket_timeout(self):
        good = {
            "data_started": True,
            "session_open_at_kill": True,
            "body_to_kill_ms": 420,
            "body_to_close_ms": 431,
            "state_after_kill": "sending",
            "execution_status": "not_terminal",
        }
        self.assertEqual(good, recovery.validate_interruption(good))
        limit = int(recovery.SOCKET_TIMEOUT_SECONDS * 1000)
        for change in (
            {"data_started": False},
            {"session_open_at_kill": False},
            {"body_to_kill_ms": limit},
            {"body_to_kill_ms": True},
            {"body_to_kill_ms": -1},
            {"body_to_close_ms": limit},
            {"body_to_close_ms": None},
            # The transport's own timeout records unknown: not an interruption.
            {"state_after_kill": "unknown"},
            {"state_after_kill": "accepted_by_smtp"},
            {"state_after_kill": "retry"},
            {"execution_status": "success"},
            {"unexpected": "private-payload"},
        ):
            with (
                self.subTest(change=tuple(change)),
                self.assertRaises(recovery.RehearsalFailure),
            ):
                recovery.validate_interruption({**good, **change})

    def test_broker_job_count_requires_a_complete_probe_of_the_exact_ids(self):
        ids = ["7"]
        self.assertEqual(
            1,
            recovery.broker_job_count(
                {"scanned": True, "matching": 1, "ids": ["7"]}, ids
            ),
        )
        for observed in (
            {"scanned": False, "matching": 0, "ids": ["7"]},
            {"scanned": True, "matching": 0, "ids": ["6"]},
            {"scanned": True, "matching": True, "ids": ["7"]},
            {"scanned": True, "matching": 0, "ids": ["7"], "extra": 1},
            None,
        ):
            with self.subTest(observed=observed):
                with self.assertRaises(recovery.RehearsalFailure):
                    recovery.broker_job_count(observed, ids)

    def test_queue_recovery_requires_n8n_to_fail_the_job_and_crash_the_execution(
        self,
    ):
        # n8n 2.43.6 forces Bull maxStalledCount 0 and keeps no failed jobs:
        # the restarted worker fails the stalled job and Bull deletes it; main
        # then marks the execution crashed. Nothing else is accepted.
        good = {
            "jobs_before_restart": 1,
            "jobs_after_recovery": 0,
            "execution_status": "crashed",
        }
        self.assertEqual(good, recovery.validate_queue_recovery(good))
        for change in (
            # The job must really have outlived the kill, or nothing recovered.
            {"jobs_before_restart": 0},
            {"jobs_before_restart": True},
            {"jobs_after_recovery": 1},
            {"jobs_after_recovery": False},
            {"execution_status": "not_terminal"},
            {"execution_status": "running"},
            {"execution_status": "success"},
            {"execution_status": "error"},
            {"unexpected": "private-payload"},
        ):
            with (
                self.subTest(change=tuple(change)),
                self.assertRaises(recovery.RehearsalFailure),
            ):
                recovery.validate_queue_recovery({**good, **change})
        self.assertGreaterEqual(
            recovery.STALL_RECOVERY_SECONDS,
            recovery.N8N_LOCK_DURATION_SECONDS
            + 2 * recovery.N8N_STALLED_INTERVAL_SECONDS,
        )

    def test_main_restart_recovery_requires_worker_settle_then_startup_crash(self):
        # With main also killed, nobody awaits the job: the restarted worker
        # deletes it but the execution stays running until the restarted
        # leader main's startup queue recovery marks it crashed.
        lock_ms = recovery.N8N_LOCK_DURATION_SECONDS * 1000
        good = {
            "jobs_before_restart": 1,
            "kill_to_probe_ms": lock_ms - 1,
            "jobs_after_worker_recovery": 0,
            "status_while_main_down": "running",
            "execution_status": "crashed",
        }
        self.assertEqual(good, recovery.validate_main_restart_recovery(good))
        for change in (
            {"jobs_before_restart": 0},
            # Probed after the lock expired: the job may already be gone.
            {"kill_to_probe_ms": lock_ms},
            {"kill_to_probe_ms": -1},
            {"kill_to_probe_ms": 1.5},
            {"jobs_after_worker_recovery": 1},
            # Already terminal means something other than main's recovery ran.
            {"status_while_main_down": "crashed"},
            {"execution_status": "running"},
            {"execution_status": "not_terminal"},
            {"unexpected": "private-payload"},
        ):
            with (
                self.subTest(change=tuple(change)),
                self.assertRaises(recovery.RehearsalFailure),
            ):
                recovery.validate_main_restart_recovery({**good, **change})

    def test_execution_retry_is_a_no_op_and_a_new_execution_replays(self):
        # n8n 2.43.6 stores a worker-killed execution with an empty start
        # stack, so its retry runs no node and ends error (native attempt 8).
        good = {
            "retried": 2,
            "statuses": ["error", "error"],
            "start_stacks_empty": True,
            "claimed_by_retry": 0,
            "interrupted_resent": 0,
            "rows_unchanged_by_retry": True,
            "fresh_execution_delivered": True,
        }
        self.assertEqual(good, recovery.validate_execution_retry(good))
        # The copied empty run can also end before n8n attaches its result
        # promise: ExecutionService.retry then throws "The retry did not
        # start" (HTTP 500, native attempt 11). Still no node ran.
        mixed = {**good, "statuses": ["not_started", "error"]}
        self.assertEqual(mixed, recovery.validate_execution_retry(mixed))
        for change in (
            {"retried": 0, "statuses": []},
            {"statuses": ["error"]},
            {"statuses": ["refused", "error"]},
            # A retry that ran is no longer the measured n8n behavior.
            {"statuses": ["success", "error"]},
            {"start_stacks_empty": False},
            {"claimed_by_retry": 1},
            {"interrupted_resent": 1},
            {"rows_unchanged_by_retry": False},
            {"fresh_execution_delivered": False},
            {"retried": True},
            {"unexpected": "private-payload"},
        ):
            with (
                self.subTest(change=tuple(change)),
                self.assertRaises(recovery.RehearsalFailure),
            ):
                recovery.validate_execution_retry({**good, **change})

    def test_postgres_readiness_waits_for_the_tcp_listener(self):
        # The entrypoint's init server listens on the socket only and then
        # restarts; only the final server answers on TCP.
        source = inspect.getsource(native.legacy.NativeFixture.start_postgres)
        self.assertIn('"pg_isready", "-h", "127.0.0.1"', source)

    def test_queue_probe_skips_jobs_removed_during_the_scan(self):
        # Bull 4 getJobs returns null for a job deleted between listing and
        # reading; dereferencing it failed the probe mid-recovery (run3).
        self.assertIn("j!==null&&data.ids.includes", recovery.QUEUE_PROBE)

    def test_hold_endpoint_stops_after_data_and_prints_only_closed_facts(self):
        script = recovery.HOLD_JS
        self.assertIn("354", script)
        self.assertNotIn("'250 ", script.split("DATA")[-1])
        self.assertNotRegex(script, r"fact\([^)]*(line|chunk|pending)")
        self.assertIn("/run/secrets/server.key", script)


@unittest.skipUnless(
    os.environ.get("P05_OPSFLOW_NATIVE") == "1",
    "exact current candidate and owned isolated runtime required",
)
class P05NativeRehearsal(unittest.TestCase):
    def test_current_notifier_queue_credentials_and_recovery(self):
        native.run_current_rehearsal()


if __name__ == "__main__":
    unittest.main()
