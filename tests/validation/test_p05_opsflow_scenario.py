"""Docker-free stateful P05 orchestration tests; these are not native evidence."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import re
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tests.validation import _p05_opsflow_native as native


class MemoryFixture:
    def __init__(self, fail=None):
        self.fail = fail
        self.events = []
        self.receipt = {}
        self.attempt = "opsflow-native-" + "a" * 24
        self.smtp_values = {1: "synthetic-first", 2: "synthetic-second"}
        self.smtp_epoch = 1
        self.generation = 1
        self.containers = {
            role: role for role in ("main", "runner", "worker", "mailpit")
        }
        self.running = {role: False for role in self.containers}
        self.running[native.HOLD] = False
        self.session = None
        self.expired = set()
        self.metadata_present = True
        self.dev_present = True
        self.metadata = {"smtp_id": "same-smtp-id", "material": None}
        self.rows = {}
        self.executions = {}
        self.captured = []
        self.active = True
        # Bull jobs that outlived their worker (active, lock expiring).
        self.jobs = set()
        # A restarted worker settles stalled jobs once their lock expires,
        # modelled as the next wait after the start.
        self.settle_pending = False

    def event(self, name):
        self.events.append(name)
        if self.fail == name:
            raise native.RehearsalFailure("synthetic interruption")

    def verify_prerequisites(self):
        self.event("preflight")

    def create_secrets(self):
        self.event("synthetic-inputs")
        return {
            name: ("synthetic", Path("/unused"))
            for name in ("metadata_pg", "valkey_server", "runner")
        }

    def prepare_smtp(self):
        self.event("tls-material")

    def create_networks(self):
        self.event("networks")

    def start_postgres(self, role, _path):
        self.event("start:" + role)

    def psql(self, role, database, sql, **kwargs):
        self.event("sql:" + role)
        if database == "n8n" and kwargs.get("container") == "metadata-pg":
            execution = re.search(r"WHERE id=([0-9]+)\)", sql)[1]
            return SimpleNamespace(
                stdout=self.executions[execution] + "|1\n", stderr="", returncode=0
            )
        if database != "opsflow_dev":
            raise AssertionError("unexpected database")
        return SimpleNamespace(stdout="", stderr="", returncode=0)

    def private(self, _name, content):
        self.event("private-write")
        self.workflow_payload = json.loads(content)

    def start_valkey(self, _path):
        self.event("queue")

    def start_mailpit(self):
        self.event("smtp:" + str(self.smtp_epoch))
        self.running["mailpit"] = True

    def start_n8n(self, _values):
        self.event("n8n")
        self.running.update(main=True, worker=True)

    def start_runner(self, _path):
        self.event("runner")
        self.running["runner"] = True

    def stop(self, role):
        self.event("stop:" + role)
        self.running[role] = self.fail == "live-process"

    def kill(self, role):
        self.event("kill:" + role)
        self.running[role] = False
        if role == "worker" and self.session == "held":
            # A killed worker records nothing; the variants model a transport
            # timeout (unknown) and a silent success that must both fail.
            self.session = "closed"
            run, execution = self.held
            if self.fail in {"graceful-unknown", "silent-success"}:
                self.rows[run] = (
                    "unknown" if self.fail == "graceful-unknown" else "accepted_by_smtp"
                )
                self.executions[execution] = "error"

    def hold_facts(self):
        held = self.session is not None and self.fail != "no-data"
        closed = self.session == "closed" or self.fail == "closed-before-kill"
        return {
            "data_started": held,
            "body_held_at_ms": self.body_at if held else None,
            "closed_after_body_ms": (5000 if self.fail == "late-close" else 300)
            if held and closed
            else None,
        }

    def start(self, role):
        self.event("start:" + role)
        self.running[role] = True
        if role == "worker" and self.jobs:
            self.settle_pending = True
        if role == "main" and self.fail != "no-startup-recovery":
            # The leader main's startup queue recovery: an in-progress
            # execution with no active or waiting job is marked crashed.
            for execution, status in self.executions.items():
                if status == "running" and execution not in self.jobs:
                    self.executions[execution] = "crashed"

    def settle(self):
        # n8n 2.43.6: the restarted worker's Bull stall check fails the job
        # (maxStalledCount 0) and deletes it (keepLastFailed 0). Only a main
        # that still awaits the job marks its execution crashed.
        self.settle_pending = False
        if self.fail == "no-stall-recovery":
            return
        for execution in self.jobs:
            if self.running["main"] and self.fail != "not-crashed":
                self.executions[execution] = "crashed"
        self.jobs.clear()

    def start_smtp_hold(self):
        if self.running["mailpit"]:
            raise native.RehearsalFailure("capture still running")
        self.event("smtp-hold")
        self.running[native.HOLD] = True

    def logs_contain(self, role, pattern):
        if role != "worker":
            raise AssertionError("unexpected log probe")
        return True

    def remove(self, role):
        self.event("remove:" + role)
        if role == native.HOLD:
            self.running[role] = False
        if self.running[role]:
            raise native.RehearsalFailure("cannot remove running fixture")

    def _verify_owned(self, role):
        running = self.running[role]
        return {
            "State": {
                "Status": "running" if running else "exited",
                "Running": running,
                "Pid": 9 if running else 0,
            }
        }

    def exec_result(self, role, *args, input_=None):
        self.event("old-job-probe")
        if role not in {"main", "worker"} or args[:2] != ("node", "-e"):
            raise AssertionError("unexpected probe")
        if not self.running[role]:
            return SimpleNamespace(returncode=1, stdout="")
        ids = json.loads(input_)["ids"]
        value = {
            "scanned": True,
            "matching": 1
            if self.fail == "old-job"
            else len(self.jobs.intersection(ids)),
            "ids": ids,
        }
        if self.fail == "wrong-job-ids":
            value["ids"] = ["999"]
        return SimpleNamespace(
            returncode=7 if self.fail == "probe-unavailable" else 0,
            stdout=json.dumps(value),
        )

    def wait_until(self, condition, _message, _seconds):
        if self.settle_pending:
            self.settle()
        if not condition():
            raise native.RehearsalFailure("synthetic wait incomplete")


class ScenarioModel:
    """The double models state loss: only explicit restore repopulates a DB."""

    def __init__(self, fail=None):
        self.fixture = MemoryFixture(fail)
        self.fail = fail
        self.workflow = "owned-workflow"
        self.scenario = native.P05Scenario(
            "test_actual_queue_runner_capture_unknown_reconcile_and_restore"
        )
        with (
            mock.patch.object(native, "P05Fixture", return_value=self.fixture),
            mock.patch.object(native, "local_artifact", return_value={}),
        ):
            self.scenario.setUp()
        self.scenario.start_dev_cluster = lambda: self.fixture.event("dev-start")
        self.scenario.bind_and_import = self.bind
        self.scenario.publish = self.publish
        self.scenario.run_manual = self.run_manual
        self.scenario.await_execution = self.await_execution
        self.scenario.wait_state = self.wait_state
        self.scenario.capture = self.capture
        self.scenario.restore_and_restart = self.restore
        self.scenario.db_value = self.db_value

    def db_value(self, sql, _role=None):
        f = self.fixture
        if "next_attempt_at<=clock_timestamp()" in sql:
            return "f" if self.fail == "retry-not-ready" else "t"
        if sql == native.recovery.SNAPSHOT_SQL:
            return "\n".join(
                f"outbox|{index}|{run}|{state}|1|5"
                for index, (run, state) in enumerate(f.rows.items(), 1)
            )
        if "SET lease_until=clock_timestamp()" in sql:
            run = re.search(r"run_id='([0-9a-f]{64})'", sql)[1]
            if f.rows[run] != "sending":
                return ""
            f.expired.add(run)
            return "7"
        if "last_error_code" in sql:
            run = re.search(r"run_id='([0-9a-f]{64})'", sql)[1]
            return f.rows[run] + "|1|lease_expired_delivery_unknown"
        if sql == native.recovery.CLAIMABLE_SQL:
            return str(list(f.rows.values()).count("pending"))
        if "publish_manifest" in sql:
            digest = re.search(
                r"publish_manifest\('[^']*','[^']*','([0-9a-f]{64})'", sql
            )[1]
            if digest in f.rows and self.fail != "replay-duplicate":
                return "replayed"
            f.rows[digest] = "pending"
            return "published"
        state = f.rows[re.search(r"run_id='([0-9a-f]{64})'", sql)[1]]
        return state + "|1" if "attempts" in sql else state

    def bind(self):
        self.fixture.event("bind")
        self.scenario.credential_ids = {"smtp": "same-smtp-id"}
        return self.workflow, "Synthetic"

    def api(self, action, **payload):
        f = self.fixture
        if not f.running["main"]:
            raise native.RehearsalFailure("n8n REST operation failed (main down)")
        if action == "trace":
            stored = f.executions.get(payload["executionId"])
            # A crashed execution keeps no start stack (n8n 2.43.6).
            stack = ["Claim"] if self.fail == "retry-has-stack" else []
            return {
                "stack": stack if stored in {"crashed", "error"} else ["Manual"],
                "runNodes": [],
                "last": "",
                "error": None,
            }
        if action == "retry":
            if f.executions[payload["executionId"]] != "crashed":
                raise native.RehearsalFailure("synthetic retry conflict")
            retried = str(len(f.executions) + 1)
            f.executions[retried] = "error"
            if self.fail == "retry-resend":
                f.captured.extend(f.held_runs)
            pending = [r for r, st in f.rows.items() if st == "pending"]
            if self.fail == "retry-claims" and pending:
                f.rows[pending[0]] = "accepted_by_smtp"
                f.captured.append(pending[0])
            return {
                "id": retried,
                "retryOf": "999"
                if self.fail == "retry-unbound"
                else payload["executionId"],
                "status": f.executions[retried],
            }
        if action == "setup":
            return {
                "id": "bad/id"
                if self.fail == "owner-id"
                else "00000000-0000-4000-8000-000000000001"
            }
        if action == "credential":
            identifier = (
                "same-pg-id"
                if payload["credential"]["type"] == "postgres"
                else "same-smtp-id"
            )
            return {"id": "bad/id" if self.fail == "credential-id" else identifier}
        if action == "workflow_create":
            f.event("workflow-create")
            f.active = False
            return {
                "id": self.workflow,
                "active": False,
                "personal": True,
                "project_id": "personal",
                "personal_project_id": "personal",
            }
        if action == "credential_update":
            if not f.metadata_present:
                raise native.RehearsalFailure("metadata missing")
            self.scenario.assertEqual("same-smtp-id", payload["credentialId"])
            f.metadata["material"] = payload["credential"]["data"]["password"]
            f.event("credential-update")
            return {"id": "wrong-id" if self.fail == "changed-id" else "same-smtp-id"}
        if action == "workflows":
            if self.fail == "readback-missing":
                return {"rows": []}
            return {
                "rows": [
                    {
                        "id": self.workflow,
                        "active": f.active or self.fail == "readback-active",
                        "versionId": "version",
                        "name": "Opsflow native " + f.attempt,
                    }
                ]
            }
        if action == "execution":
            status = f.executions[payload["executionId"]]
            return {"status": status, "terminal": status != "running"}
        if action == "deactivate":
            f.event("deactivate")
            f.active = self.fail == "still-active"
        elif action != "profile":
            raise AssertionError("unexpected API action")
        return {"id": self.workflow}

    def publish(self, _source, digest, captured):
        f = self.fixture
        if not f.dev_present:
            raise native.RehearsalFailure("DEV restore missing")
        # SQL001 publish_manifest: an older capture is 'historical' and adds
        # no outbox row, which the shared publish() helper refuses.
        if captured <= getattr(f, "latest_capture", ""):
            raise native.RehearsalFailure("synthetic publication failed")
        # SQL003 runs_source_business_date_uidx: one run per source per UTC date.
        days = f.__dict__.setdefault("capture_days", set())
        if captured[:10] in days:
            raise native.RehearsalFailure("synthetic publication failed")
        days.add(captured[:10])
        f.latest_capture = captured
        f.rows[digest] = "pending"
        f.event("publish")
        return digest

    def run_manual(self, workflow):
        f = self.fixture
        if not f.metadata_present or not f.dev_present:
            raise native.RehearsalFailure("restored DB missing")
        self.scenario.assertEqual(self.workflow, workflow)
        for run in f.expired:
            if f.rows[run] == "sending":
                f.rows[run] = "unknown"
        pending = [run for run, state in f.rows.items() if state == "pending"]
        if self.fail == "reclaim-interrupted" and f.session == "closed":
            f.captured.append(f.held[0])
        if self.fail == "resend-unknown" and f.generation == 2:
            resent = next(run for run, state in f.rows.items() if state == "unknown")
            f.rows[resent] = "accepted_by_smtp"
            f.captured.append(resent)
        self.scenario.assertEqual(1, len(pending))
        run = pending[0]
        if f.running[native.HOLD]:
            execution = str(len(f.executions) + 1)
            f.rows[run], f.executions[execution] = "sending", "running"
            if self.fail != "job-not-surviving":
                f.jobs.add(execution)
            f.session, f.held = "held", (run, execution)
            f.held_runs = [*getattr(f, "held_runs", []), run]
            f.body_at = int(native.time.time() * 1000)
            f.event("execute:held")
            return execution
        accepted = f.metadata["material"] == f.smtp_values[f.smtp_epoch]
        f.rows[run] = "accepted_by_smtp" if accepted else "unknown"
        if accepted:
            f.captured.append(run)
        execution = str(len(f.executions) + 1)
        f.executions[execution] = "success" if accepted else "error"
        f.event("execute:" + f.executions[execution])
        return execution

    def await_execution(self, execution, state, _node):
        self.scenario.assertEqual(state, self.fixture.executions[execution])

    def wait_state(self, run, state):
        self.scenario.assertEqual(state, self.fixture.rows[run])

    def capture(self, run):
        return {
            "matched": run in self.fixture.captured,
            "safe": True,
            "total": len(self.fixture.captured),
        }

    def restore(self):
        f = self.fixture
        self.scenario.assertIn("recovery_barrier", f.receipt)
        saved_metadata, saved_rows = copy.deepcopy(f.metadata), dict(f.rows)
        f.metadata.clear()
        f.rows.clear()
        f.metadata_present = f.dev_present = False
        f.event("destroy-old-databases")
        f.generation = 2
        if self.fail != "omit-metadata-restore":
            f.metadata.update(saved_metadata)
            f.metadata_present = True
            f.event("restore-metadata")
        if self.fail != "omit-dev-restore":
            f.rows.update(saved_rows)
            if self.fail == "restore-drift":
                f.rows[next(iter(f.rows))] = "retry"
            f.dev_present = True
            f.event("restore-dev")
        f.running.update(main=True, worker=True, runner=True, mailpit=True)
        # Captures belong to the independent generation; unknown DB rows remain.
        f.captured.clear()

    def run(self):
        # Patch only inherited I/O, leaving every new P05 scenario method real.
        with (
            mock.patch.object(
                native.historical.OpsflowN8nNativeRehearsal, "api", self.api
            ),
            mock.patch.object(
                native.legacy, "node_status_probe", return_value=(True, {})
            ),
            mock.patch.object(
                native.historical.OpsflowN8nNativeRehearsal,
                "provision",
                lambda _self: self.fixture.event("provision-v3"),
            ),
            redirect_stdout(io.StringIO()),
        ):
            self.scenario.run_scenario()
        return self.fixture.receipt


class P05ScenarioStateTests(unittest.TestCase):
    def test_editor_registration_normal_refusal_and_interruption(self):
        for failure in (
            None,
            "owner-id",
            "credential-id",
            "readback-missing",
            "readback-active",
            "workflow-create",
            "private-write",
        ):
            with self.subTest(failure=failure):
                model = ScenarioModel(failure)
                model.scenario.secrets = {"notifier": ("synthetic", None)}
                model.fixture.running["main"] = True
                del model.scenario.bind_and_import
                with mock.patch.object(
                    native.historical.OpsflowN8nNativeRehearsal, "api", model.api
                ):
                    if failure is not None:
                        with self.assertRaises(native.RehearsalFailure):
                            model.scenario.bind_and_import()
                        self.assertNotIn("workflow_registration", model.fixture.receipt)
                    else:
                        identifier, _ = model.scenario.bind_and_import()
                        self.assertEqual(model.workflow, identifier)
                        self.assertFalse(model.fixture.active)
                        self.assertEqual(
                            "same-smtp-id", model.scenario.credential_ids["smtp"]
                        )
                        self.assertTrue(
                            model.fixture.workflow_payload["settings"][
                                "saveManualExecutions"
                            ]
                        )
                        self.assertEqual(
                            "NOT_RUN",
                            model.fixture.receipt["workflow_registration"][
                                "cold_cli_import"
                            ],
                        )

    def test_already_inactive_workflow_skips_deactivate_but_rechecks_barrier(self):
        model = ScenarioModel()
        model.fixture.active = False
        receipt = model.run()
        self.assertNotIn("deactivate", model.fixture.events)
        self.assertTrue(receipt["recovery_barrier"]["workflow_inactive"])
        self.assertEqual("PASS", receipt["native"])

    def test_complete_sequence_preserves_unknown_and_restores_real_double_state(self):
        model = ScenarioModel()
        receipt = model.run()
        self.assertEqual("PASS", receipt["native"])
        self.assertEqual("complete", receipt["phase"])
        self.assertEqual("QUIESCED_ONLY", receipt["recovery_scope"])
        self.assertEqual("PASS", receipt["live_inflight_interruption"])
        self.assertEqual("unknown", receipt["interrupted_recovery"]["state"])
        self.assertEqual(
            "sending", receipt["active_send_interruption"]["state_after_kill"]
        )
        self.assertEqual(
            "not_terminal", receipt["active_send_interruption"]["execution_status"]
        )
        self.assertEqual(300, receipt["active_send_interruption"]["body_to_close_ms"])
        self.assertFalse(receipt["interrupted_recovery"]["resent"])
        self.assertEqual(1, receipt["interrupted_broker_job_matching"])
        self.assertEqual(
            {
                "jobs_before_restart": 1,
                "jobs_after_recovery": 0,
                "execution_status": "crashed",
            },
            receipt["interrupted_queue_recovery"],
        )
        self.assertTrue(receipt["recovery_barrier"]["old_executions_terminal"])
        self.assertIn(
            receipt["interrupted_execution_id"],
            receipt["recovery_barrier"]["old_execution_ids"],
        )
        self.assertEqual(
            {
                "jobs_before_restart": 1,
                "kill_to_probe_ms": receipt["main_restart_recovery"][
                    "kill_to_probe_ms"
                ],
                "jobs_after_worker_recovery": 0,
                "status_while_main_down": "running",
                "execution_status": "crashed",
            },
            receipt["main_restart_recovery"],
        )
        self.assertEqual(
            "main_down", receipt["main_restart_interruption"]["execution_status"]
        )
        self.assertEqual("unknown", receipt["main_restart_quarantine"]["state"])
        self.assertEqual(
            {
                "retried": 2,
                "statuses": ["error", "error"],
                "start_stacks_empty": True,
                "claimed_by_retry": 0,
                "interrupted_resent": 0,
                "rows_unchanged_by_retry": True,
                "fresh_execution_delivered": True,
            },
            receipt["execution_retry"],
        )
        self.assertIn(
            receipt["main_restart_execution_id"],
            receipt["recovery_barrier"]["old_execution_ids"],
        )
        self.assertEqual(10, receipt["same_input_replay"]["replayed"])
        self.assertEqual(
            {"accepted_by_smtp": 6, "unknown": 4},
            receipt["restored_outbox_equivalence"]["states"],
        )
        self.assertEqual(4, list(model.fixture.rows.values()).count("unknown"))
        self.assertEqual(7, list(model.fixture.rows.values()).count("accepted_by_smtp"))
        self.assertEqual("same-smtp-id", model.fixture.metadata["smtp_id"])
        self.assertEqual(2, model.fixture.generation)
        events = model.fixture.events
        self.assertIn("deactivate", events)
        for before, after in (
            ("preflight", "tls-material"),
            ("tls-material", "networks"),
            ("provision-v3", "queue"),
            ("smtp-hold", "execute:held"),
            # The interrupted job is recovered before the barrier and restore.
            ("execute:held", "stop:worker"),
            ("remove:" + native.HOLD, "start:worker"),
            ("start:worker", "deactivate"),
            # Main is killed only in the second interruption and restarted
            # after the worker has settled the job, before any retry.
            ("kill:main", "start:main"),
            ("start:main", "deactivate"),
            ("destroy-old-databases", "restore-metadata"),
            ("restore-metadata", "restore-dev"),
        ):
            self.assertLess(events.index(before), events.index(after))
        # The barrier probe is the last one before teardown, after the stop.
        barrier = max(
            index
            for index, name in enumerate(
                events[: events.index("destroy-old-databases")]
            )
            if name == "old-job-probe"
        )
        self.assertLess(events.index("stop:worker"), barrier)
        held = events.index("execute:held")
        self.assertIn(
            "kill:worker", events[held : events.index("remove:" + native.HOLD)]
        )

    def test_unrecovered_interruption_blocks_the_barrier_and_restore(self):
        for failure in (
            "graceful-unknown",
            "silent-success",
            "closed-before-kill",
            "late-close",
            "no-data",
            "reclaim-interrupted",
            "job-not-surviving",
            "no-stall-recovery",
            "not-crashed",
        ):
            with self.subTest(failure=failure):
                model = ScenarioModel(failure)
                with self.assertRaises(native.RehearsalFailure):
                    model.run()
                self.assertIn("execute:held", model.fixture.events)
                # Refused before the fence even runs, not only by the barrier.
                self.assertNotIn("recovery_barrier_facts", model.fixture.receipt)
                self.assertNotIn("destroy-old-databases", model.fixture.events)
                self.assertNotEqual("PASS", model.fixture.receipt.get("native"))
                self.assertNotEqual(
                    "PASS", model.fixture.receipt.get("live_inflight_interruption")
                )

    def test_main_restart_and_retry_violations_block_the_barrier(self):
        for failure in (
            "no-startup-recovery",
            "retry-resend",
            "retry-unbound",
            "retry-claims",
            "retry-has-stack",
        ):
            with self.subTest(failure=failure):
                model = ScenarioModel(failure)
                with self.assertRaises(native.RehearsalFailure):
                    model.run()
                self.assertIn("kill:main", model.fixture.events)
                self.assertNotIn("recovery_barrier_facts", model.fixture.receipt)
                self.assertNotIn("destroy-old-databases", model.fixture.events)
                self.assertNotEqual("PASS", model.fixture.receipt.get("native"))

    def test_replay_and_next_claim_violations_cannot_pass(self):
        for failure in (
            "restore-drift",
            "replay-duplicate",
            "resend-unknown",
        ):
            with self.subTest(failure=failure):
                model = ScenarioModel(failure)
                with self.assertRaises(native.RehearsalFailure):
                    model.run()
                self.assertIn("restore-dev", model.fixture.events)
                self.assertNotEqual("PASS", model.fixture.receipt.get("native"))
                self.assertNotEqual(
                    "PASS", model.fixture.receipt.get("live_inflight_interruption")
                )

    def test_each_barrier_failure_prevents_database_teardown_and_success(self):
        for failure in (
            "live-process",
            "still-active",
            "old-job",
            "wrong-job-ids",
            "probe-unavailable",
        ):
            with self.subTest(failure=failure):
                model = ScenarioModel(failure)
                with self.assertRaises(native.RehearsalFailure):
                    model.run()
                self.assertNotIn("destroy-old-databases", model.fixture.events)
                self.assertNotIn("same_encryption_key_restore", model.fixture.receipt)
                self.assertNotEqual("PASS", model.fixture.receipt.get("native"))

    def test_omitted_database_restore_cannot_pass_after_state_is_destroyed(self):
        for failure in ("omit-metadata-restore", "omit-dev-restore"):
            with self.subTest(failure=failure):
                model = ScenarioModel(failure)
                with self.assertRaises(native.RehearsalFailure):
                    model.run()
                self.assertIn("destroy-old-databases", model.fixture.events)
                self.assertNotIn("same_encryption_key_restore", model.fixture.receipt)
                self.assertNotEqual("PASS", model.fixture.receipt.get("native"))

    def test_interruptions_do_not_report_later_phase_acceptance(self):
        for failure in (
            "preflight",
            "tls-material",
            "networks",
            "start:metadata-pg",
            "queue",
            "n8n",
            "credential-update",
        ):
            with self.subTest(failure=failure):
                model = ScenarioModel(failure)
                with self.assertRaises(native.RehearsalFailure):
                    model.run()
                self.assertNotIn("worker_queue_starttls_auth", model.fixture.receipt)
                self.assertNotEqual("PASS", model.fixture.receipt.get("native"))

    def test_changed_credential_identity_and_retry_not_ready_fail_closed(self):
        model = ScenarioModel("changed-id")
        with self.assertRaises(native.RehearsalFailure):
            model.run()
        self.assertNotIn("execute:success", model.fixture.events)
        model = ScenarioModel("retry-not-ready")
        with self.assertRaises(native.RehearsalFailure):
            model.scenario.ready_retry("synthetic-run")
        good = ScenarioModel()
        good.scenario.ready_retry("synthetic-run")


def artifact():
    dist = {"OpsflowSmtp.node.js": "a" * 64, "transport.js": "b" * 64}
    binding = "c" * 64
    return {
        "reference": "hy-home/p05-n8n-fixture:" + binding[:12],
        "image_id": "sha256:" + "d" * 64,
        "base_id": native.inputs.N8N_ID,
        "binding": binding,
        "dist_sha256": dist,
    }


def fixture_at(directory):
    def initialize(instance):
        instance.receipt = {"native": "NOT_RUN"}

    selected = artifact()
    with (
        mock.patch.object(
            native,
            "current_binding",
            return_value=(selected["binding"], selected["dist_sha256"]),
        ),
        mock.patch.object(native.legacy.NativeFixture, "__init__", initialize),
    ):
        fixture = native.P05Fixture(selected)
    fixture.directory = Path(directory)
    fixture.host_uid, fixture.host_gid = os.geteuid(), os.getegid()
    fixture.files = {}
    fixture.mailpit_dirs = {}
    fixture.generation = 1
    return fixture


class P05FixtureAdapterTests(unittest.TestCase):
    def test_source_dist_and_dependency_changes_invalidate_current_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "package"
            analysis = Path(directory) / "analysis"
            package.mkdir()
            analysis.mkdir()
            (package / "dist").mkdir()
            dependency = package / "node_modules/nodemailer/lib"
            dependency.mkdir(parents=True)
            for name in (
                "transport.ts",
                "OpsflowSmtp.node.ts",
                "package.json",
                "package-lock.json",
                "tsconfig.json",
                "dist/transport.js",
                "dist/OpsflowSmtp.node.js",
                "node_modules/nodemailer/lib/smtp.js",
            ):
                (package / name).write_text("public synthetic " + name)
            (package / "package-lock.json").write_text(
                json.dumps(
                    {
                        "name": "synthetic-capture",
                        "version": "0.0.0",
                        "packages": {
                            "": {"devDependencies": {"unused-test-tool": "0.0.0"}},
                            "node_modules/nodemailer": {"version": "0.0.0"},
                        },
                    }
                )
            )
            with (
                mock.patch.object(native, "PACKAGE", package),
                mock.patch.object(native, "ANALYSIS", analysis),
            ):
                binding, dist = native.current_binding()
                selected = {
                    **artifact(),
                    "reference": "hy-home/p05-n8n-fixture:" + binding[:12],
                    "binding": binding,
                    "dist_sha256": dist,
                }
                (analysis / "candidate-artifact.json").write_text(json.dumps(selected))
                self.assertEqual(selected, native.local_artifact())
                minimal = json.loads(native.runtime_lock())
                self.assertEqual(3, minimal["lockfileVersion"])
                self.assertEqual(
                    {"node_modules/nodemailer": {"version": "0.0.0"}},
                    minimal["packages"],
                )
                deployed = native.deployment_files()
                self.assertEqual(
                    hashlib.sha256(native.runtime_lock()).hexdigest(),
                    deployed["node_modules/.package-lock.json"],
                )
                expected_manifest = "".join(
                    digest + "  " + name + "\n"
                    for name, digest in sorted(deployed.items())
                    if name != "SHA256SUMS"
                ).encode()
                self.assertEqual(
                    hashlib.sha256(expected_manifest).hexdigest(),
                    deployed["SHA256SUMS"],
                )
                for name in (
                    "transport.ts",
                    "dist/transport.js",
                    "node_modules/nodemailer/lib/smtp.js",
                ):
                    original = (package / name).read_text()
                    (package / name).write_text(original + " changed")
                    changed, _ = native.current_binding()
                    self.assertNotEqual(binding, changed)
                    with self.assertRaises(native.RehearsalFailure):
                        native.local_artifact()
                    (package / name).write_text(original)

    def test_deployment_closed_metadata_and_root_modes_reject_structural_confusion(
        self,
    ):
        expected = {"package.json": hashlib.sha256(b"public synthetic").hexdigest()}
        directory = {
            "name": "opsflow",
            "kind": "directory",
            "uid": 0,
            "gid": 0,
            "mode": 0o755,
        }
        file = {
            "name": "opsflow/package.json",
            "kind": "file",
            "uid": 0,
            "gid": 0,
            "mode": 0o644,
            "sha256": expected["package.json"],
        }
        self.assertEqual(
            {"files": 1, "directories": 1},
            native.validate_deployment([directory, file], expected),
        )
        for rows in (
            None,
            [],
            [directory] * 1025,
            [file],
            [directory, "not metadata"],
            [directory, {**file, "uid": False}],
            [directory, {**file, "name": "external/package.json"}],
            [directory, {**file, "name": "opsflow//package.json"}],
            [{**directory, "sha256": "unexpected"}, file],
            [directory, {**file, "mode": 0o600}],
            [directory, {**file, "unexpected": "private-placeholder"}],
        ):
            with (
                self.subTest(rows=type(rows).__name__),
                self.assertRaises(native.RehearsalFailure),
            ):
                native.validate_deployment(rows, expected)

    def test_public_artifact_rejects_directory_and_multiple_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(native.RehearsalFailure):
                native.public_digest(root)
            path = root / "public.js"
            path.write_text("synthetic public")
            (root / "second.js").hardlink_to(path)
            with self.assertRaises(native.RehearsalFailure):
                native.public_digest(path)

    def test_tls_preparation_tracks_only_owned_files_and_hides_command_output(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = fixture_at(directory)

            def openssl(command, **kwargs):
                self.assertEqual(Path(directory), kwargs["cwd"])
                self.assertEqual(subprocess.DEVNULL, kwargs["stdout"])
                self.assertEqual(subprocess.DEVNULL, kwargs["stderr"])
                for flag in ("-keyout", "-out"):
                    if flag in command:
                        (Path(directory) / command[command.index(flag) + 1]).write_text(
                            "synthetic file"
                        )
                if "-CAcreateserial" in command:
                    (Path(directory) / "p05-ca.srl").write_text("synthetic serial")

            with (
                mock.patch.object(
                    native.shutil, "which", return_value="/owned/openssl"
                ),
                mock.patch.object(
                    native.subprocess, "run", side_effect=openssl
                ) as commands,
            ):
                fixture.prepare_smtp()
            self.assertEqual(3, commands.call_count)
            self.assertEqual({1, 2}, set(fixture.smtp_files))
            self.assertNotEqual(fixture.smtp_values[1], fixture.smtp_values[2])
            for path, metadata in fixture.files.items():
                self.assertEqual(Path(directory), path.parent)
                self.assertEqual(0o600, metadata.mode)
                self.assertEqual(1, path.stat().st_nlink)

    def test_tls_generator_failure_does_not_mint_ready_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = fixture_at(directory)
            with (
                mock.patch.object(native.shutil, "which", return_value=None),
                self.assertRaises(native.RehearsalFailure),
            ):
                fixture.prepare_smtp()
            with (
                mock.patch.object(
                    native.shutil, "which", return_value="/owned/openssl"
                ),
                mock.patch.object(
                    native.subprocess,
                    "run",
                    side_effect=subprocess.TimeoutExpired("owned", 30),
                ),
                self.assertRaises(subprocess.TimeoutExpired),
            ):
                fixture.prepare_smtp()
            self.assertEqual(
                {
                    "native": "NOT_RUN",
                    "task": "SPEC-0212-TSK-0044",
                    "candidate": {
                        key: fixture.artifact[key]
                        for key in ("reference", "image_id", "base_id", "binding")
                    },
                },
                fixture.receipt,
            )

    def test_role_image_translation_mount_and_global_bindings_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = fixture_at(directory)
            original = native.legacy.N8N_REF
            with fixture.bindings():
                self.assertEqual(fixture.artifact["reference"], native.legacy.N8N_REF)
                self.assertEqual(fixture.artifact["image_id"], native.legacy.N8N_ID)
            self.assertEqual(original, native.legacy.N8N_REF)
            with self.assertRaises(RuntimeError), fixture.bindings():
                raise RuntimeError("synthetic interruption")
            self.assertEqual(original, native.legacy.N8N_REF)
            with mock.patch.object(
                native.legacy.NativeFixture, "create", return_value="created"
            ) as create:
                for role, image in (
                    ("main", native.inputs.N8N_REF),
                    ("worker", native.inputs.N8N_REF),
                    ("dev-pg", native.inputs.PG_REF),
                    ("valkey", native.inputs.VALKEY_REF),
                    ("mailpit", native.inputs.MAILPIT_REF),
                    ("runner", native.inputs.RUNNER_REF),
                ):
                    self.assertEqual(
                        "created",
                        fixture.create(
                            role, image, "1000:1000", ("owned",), mounts=("original",)
                        ),
                    )
                    if role in {"main", "worker"}:
                        self.assertIn(
                            "/run/secrets/p05-ca.pem",
                            create.call_args.kwargs["mounts"][-1],
                        )
                        self.assertIn("readonly", create.call_args.kwargs["mounts"][-1])
                count = create.call_count
                for role, image in (
                    ("unknown", native.inputs.PG_REF),
                    ("worker", native.inputs.PG_REF),
                    ("main", "latest"),
                ):
                    with self.assertRaises(native.RehearsalFailure):
                        fixture.create(role, image, "1000:1000", ())
                self.assertEqual(count, create.call_count)
            with mock.patch.object(
                native.legacy.NativeFixture, "verify_prerequisites"
            ) as verify:
                fixture.verify_prerequisites()
                verify.assert_called_once_with()

    def test_scoped_starttls_mounts_and_store_identity_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = fixture_at(directory)
            fixture.smtp_files = {1: Path(directory) / "synthetic-auth"}
            with (
                mock.patch.object(fixture, "create") as create,
                mock.patch.object(fixture, "start") as start,
            ):
                fixture.start_mailpit()
                options = create.call_args.kwargs
                self.assertIn("MP_SMTP_REQUIRE_STARTTLS=true", options["env"])
                self.assertIn("MP_SMTP_AUTH_ALLOW_INSECURE=false", options["env"])
                self.assertIn(
                    "MP_SMTP_AUTH_FILE=/run/secrets/smtp-auth", options["env"]
                )
                self.assertFalse(any("KEY=" in value for value in options["env"]))
                self.assertEqual(
                    ("--smtp-tls-key=/run/secrets/server.key",), options["command"]
                )
                self.assertEqual(4, len(options["mounts"]))
                start.assert_called_once_with("mailpit")
                data = Path(directory) / "mailpit-data-1"
                data.chmod(0o755)
                with self.assertRaises(native.RehearsalFailure):
                    fixture.start_mailpit()
                self.assertEqual(1, create.call_count)

    def test_smtp_hold_replaces_only_a_stopped_capture_under_its_alias(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = fixture_at(directory)
            fixture.containers = {"mailpit": "mailpit"}
            state = {"Running": True}
            fixture._verify_owned = lambda _record: {"State": state}
            fixture.logs_contain = mock.Mock(return_value=True)
            with (
                mock.patch.object(fixture, "create") as create,
                mock.patch.object(fixture, "start") as start,
            ):
                with self.assertRaises(native.RehearsalFailure):
                    fixture.start_smtp_hold()
                create.assert_not_called()
                state["Running"] = False
                with mock.patch.object(fixture, "wait_until") as wait:
                    fixture.start_smtp_hold()
                    self.assertTrue(wait.call_args.args[0]())
                options = create.call_args
                self.assertEqual(
                    (native.HOLD, fixture.artifact["reference"]), options.args[:2]
                )
                self.assertEqual(("capture",), options.args[3])
                self.assertEqual(
                    ("-e", native.recovery.HOLD_JS), options.kwargs["command"]
                )
                self.assertTrue(
                    all("readonly" in mount for mount in options.kwargs["mounts"])
                )
                start.assert_called_once_with(native.HOLD)
            seen = {}

            def verify(_self, record):
                seen.update(
                    alias=native.legacy.ALIASES[record],
                    caps=native.legacy.RESOURCE_CAPS[record],
                )

            with mock.patch.object(
                native.legacy.NativeFixture, "_verify_container", verify
            ):
                fixture._verify_container(native.HOLD)
            self.assertEqual("mailpit", seen["alias"])
            self.assertEqual(native.inputs.RESOURCE_CAPS["capture-probe"], seen["caps"])
            self.assertNotIn(native.HOLD, native.legacy.ALIASES)

    def test_hold_facts_and_kill_use_only_verified_owned_containers(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = fixture_at(directory)
            fixture.containers = {
                native.HOLD: SimpleNamespace(cid="hold"),
                "worker": SimpleNamespace(cid="worker"),
            }
            fixture._verify_container = mock.Mock()
            fixture._verify_owned = lambda _record: {"State": {"Running": False}}
            fixture.wait_until = lambda condition, *_args: self.assertTrue(condition())
            log = "P05_HOLD DATA_STARTED\nP05_HOLD BODY_HELD at=5\n"
            fixture.client = mock.Mock()
            fixture.client.run_result.return_value = SimpleNamespace(
                returncode=0, stdout=log
            )
            self.assertEqual(5, fixture.hold_facts()["body_held_at_ms"])
            fixture.kill("worker")
            self.assertEqual(
                [mock.call("logs", "hold"), mock.call("kill", "worker")],
                fixture.client.run_result.call_args_list,
            )
            fixture.client.run_result.return_value = SimpleNamespace(
                returncode=1, stdout=""
            )
            for action in (fixture.hold_facts, lambda: fixture.kill("worker")):
                with self.assertRaises(native.RehearsalFailure):
                    action()

    def test_ca_environment_closed_diagnostics_and_receipt_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = fixture_at(directory)
            with mock.patch.object(
                native.legacy.NativeFixture, "_n8n_env", return_value=("BASE=1",)
            ):
                self.assertEqual(
                    ("BASE=1", "NODE_EXTRA_CA_CERTS=/run/secrets/p05-ca.pem"),
                    fixture._n8n_env(),
                )

            def diagnostic(_self, _values):
                native.evidence.retain_failure_output(None, None, fixture.receipt, None)

            with mock.patch.object(
                native.legacy.NativeFixture, "start_n8n", diagnostic
            ):
                fixture.start_n8n({})
            self.assertEqual(
                "CLOSED_FACTS_ONLY", fixture.receipt["p05_readiness_evidence"]
            )
            with mock.patch.object(
                native.legacy.NativeFixture,
                "receipt_json",
                return_value='{"native":"NOT_RUN"}',
            ):
                result = json.loads(fixture.receipt_json())
                self.assertEqual(fixture.artifact["image_id"], result["image_id"])
                self.assertEqual(fixture.artifact["binding"], result["source_binding"])

    def test_entrypoint_opt_in_and_finalization_on_failure_or_cancellation(self):
        with (
            mock.patch.dict(os.environ, {"P05_OPSFLOW_NATIVE": "0"}),
            self.assertRaises(native.RehearsalFailure),
        ):
            native.run_current_rehearsal()
        for failure in (None, RuntimeError("synthetic"), KeyboardInterrupt()):
            events = []
            selected = SimpleNamespace(
                setUp=lambda events=events: events.append("setup"),
                finish=lambda events=events: events.append("finish"),
            )

            def run(events=events, failure=failure):
                events.append("run")
                if failure is not None:
                    raise failure

            selected.run_scenario = run
            with (
                mock.patch.dict(os.environ, {"P05_OPSFLOW_NATIVE": "1"}),
                mock.patch.object(native, "P05Scenario", return_value=selected),
            ):
                if failure is None:
                    native.run_current_rehearsal()
                else:
                    with self.assertRaises(type(failure)):
                        native.run_current_rehearsal()
            self.assertEqual(["setup", "run", "finish"], events)


if __name__ == "__main__":
    unittest.main()
