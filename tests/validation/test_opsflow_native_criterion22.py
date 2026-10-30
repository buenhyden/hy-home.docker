"""Docker-free guards for the SPEC-0204 criterion 22 native scenarios."""

from __future__ import annotations

import hashlib
import inspect
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.validation import _opsflow_native_criterion22 as c22
from tests.validation import test_opsflow_native_rehearsal as native_driver
from tests.validation._opsflow_native_evidence import PrivateFile
from tests.validation._opsflow_native_fixture import RehearsalFailure
from tests.validation.test_opsflow_database_rehearsal import WORKLOAD

ROOT = Path(__file__).resolve().parents[2]
NOTIFIER = ROOT / "infra/07-workflow/n8n/workloads/manifest-outbox-notifier"
SQL = {
    name: (WORKLOAD / "sql" / name).read_text()
    for name in ("001_opsflow.sql", "004_notification_quarantine.sql")
}
SHELL = shutil.which("sh")
NODE = shutil.which("node")


def driver() -> native_driver.OpsflowN8nNativeRehearsal:
    case = native_driver.OpsflowN8nNativeRehearsal(
        "test_actual_queue_runner_capture_unknown_reconcile_and_restore"
    )
    case.fixture = mock.Mock()
    case.fixture.receipt = {}
    case.credential_ids = {"postgres": "pg1", "smtp": "smtp1"}
    case.secrets = {"notifier": ("a" * 43, Path("/owned/notifier.secret"))}
    case.published = 0
    case.stale_notifier = "s" * 43
    return case


class Criterion22ContractTests(unittest.TestCase):
    def test_receipt_fields_and_scenario_order_are_pinned(self):
        self.assertEqual(
            (
                "scheduled_execution",
                "concurrent_claims",
                "retry_dead_letter",
                "empty_queue",
                "credential_rotation",
                "paired_restore_decrypt",
                "wrong_key_fail_closed",
            ),
            c22.RECEIPT_FIELDS,
        )
        self.assertEqual(
            {field: "NOT_RUN" for field in c22.RECEIPT_FIELDS}, c22.initial_receipt()
        )
        case = driver()
        self.assertEqual(
            c22.GENERATION_1_STEPS,
            tuple(name for name, _ in case.generation_1_scenarios("w")),
        )
        self.assertEqual(
            c22.RESTORE_STEPS, tuple(name for name, _ in case.restore_scenarios())
        )
        # Generation 1 steps run before the restore, the restore steps after it,
        # and `native` is only set `PASS` after the final gate.
        source = inspect.getsource(native_driver.OpsflowN8nNativeRehearsal.run_scenario)
        order = [
            source.index(marker)
            for marker in (
                "generation_1_scenarios",
                "self.restore_and_restart()",
                "restore_scenarios",
                "require_criterion_22_pass",
                '"native": "PASS"',
            )
        ]
        self.assertEqual(sorted(order), order)

    def test_step_marks_pass_and_fail_and_keeps_the_error(self):
        case = driver()
        case.step("empty_queue", lambda: None)
        self.assertEqual("PASS", case.fixture.receipt["empty_queue"])
        for failure in (RehearsalFailure("x"), KeyboardInterrupt()):
            with self.subTest(failure=type(failure).__name__):

                def boom(failure=failure):
                    raise failure

                with self.assertRaises(type(failure)):
                    case.step("concurrent_claims", boom)
                self.assertEqual("FAIL", case.fixture.receipt["concurrent_claims"])

    def test_native_pass_requires_every_criterion_22_field(self):
        case = driver()
        case.fixture.receipt.update(c22.initial_receipt())
        with self.assertRaises(RehearsalFailure):
            case.require_criterion_22_pass()
        case.fixture.receipt.update({field: "PASS" for field in c22.RECEIPT_FIELDS})
        case.require_criterion_22_pass()
        case.fixture.receipt["wrong_key_fail_closed"] = "FAIL"
        with self.assertRaises(RehearsalFailure):
            case.require_criterion_22_pass()

    def test_db_interface_the_scenarios_use_still_exists(self):
        both = "\n".join(SQL.values())
        for signature in (
            "ops_flow.claim_notification()",
            "ops_flow.ack_notification(p_id bigint,p_token uuid)",
            "ops_flow.retry_not_sent_notification(p_id bigint,p_token uuid)",
            "ops_flow.unknown_notification(p_id bigint,p_token uuid)",
        ):
            self.assertIn(signature, both)
        self.assertIn(
            "attempts integer NOT NULL DEFAULT 0 CHECK(attempts BETWEEN 0 AND 5)",
            SQL["001_opsflow.sql"],
        )
        self.assertEqual(5, c22.MAX_ATTEMPTS)
        self.assertIn(
            "least(900,30*pg_catalog.power(2,o.attempts)::integer)",
            SQL["004_notification_quarantine.sql"],
        )
        self.assertEqual(
            [60, 120, 240, 480], [c22.backoff_seconds(n) for n in range(1, 5)]
        )
        self.assertEqual(900, c22.backoff_seconds(9))
        self.assertIn(
            "last_error_code='smtp_not_started'", SQL["004_notification_quarantine.sql"]
        )
        self.assertIn("'retry_exhausted'", SQL["004_notification_quarantine.sql"])
        self.assertIn(
            "GRANT EXECUTE ON FUNCTION ops_flow.unknown_notification(bigint,uuid),ops_flow.retry_not_sent_notification(bigint,uuid) TO opsflow_notifier",
            SQL["004_notification_quarantine.sql"],
        )

    def test_workflow_has_the_one_minute_trigger_the_scenarios_activate(self):
        workflow = json.loads(
            (NOTIFIER / "workflows/manifest-outbox-mailpit.json").read_text()
        )
        self.assertIs(False, workflow["active"])
        nodes = {node["name"]: node for node in workflow["nodes"]}
        self.assertEqual(
            {"rule": {"interval": [{"field": "minutes", "minutesInterval": 1}]}},
            nodes["Every Minute"]["parameters"],
        )
        self.assertEqual(
            "n8n-nodes-base.scheduleTrigger", nodes["Every Minute"]["type"]
        )
        self.assertIn(
            "ops_flow.claim_notification()", nodes["Claim"]["parameters"]["query"]
        )

    def test_retry_and_maintenance_sql_builders_refuse_bad_input(self):
        self.assertEqual("retry|1|smtp_not_started|true", c22.retry_expected(1))
        self.assertEqual("dead|5|smtp_not_started|n/a", c22.retry_expected(5))
        for bad in (0, 6):
            with self.assertRaises(ValueError):
                c22.retry_expected(bad)
            with self.assertRaises(ValueError):
                c22.retry_row_sql("1", bad)
        self.assertIn("interval '30 seconds'", c22.retry_row_sql("7", 1))
        self.assertIn("interval '61 seconds'", c22.retry_row_sql("7", 1))
        self.assertIn("interval '481 seconds'", c22.retry_row_sql("7", 4))
        for build in (
            c22.fast_forward_sql,
            c22.exhaust_sql,
            lambda value: c22.outbox_row_sql(value, "state"),
        ):
            with self.assertRaises(ValueError):
                build("1; DROP TABLE x")
        self.assertIn("RETURNING id", c22.fast_forward_sql("3"))
        for role, password in (
            ("postgres", "a" * 43),
            ("opsflow_notifier", "short"),
            ("opsflow_notifier", "a" * 42 + "'"),
        ):
            with self.assertRaises(ValueError):
                c22.rotate_role_sql(role, password)
        with self.assertRaises(ValueError):
            c22.terminate_role_sql("x'; --")
        with self.assertRaises(ValueError):
            c22.role_sessions_sql("x'; --")

    def test_race_parser_accepts_one_winner_per_row_only(self):
        winner = "job{}:,claim|5,stale|false,ack|true,again|false,"
        loser = "job{}:,claim|0,stale|false,ack|false,again|false,"
        output = "\n".join(
            [winner.format(1), loser.format(2), loser.format(3), loser.format(4)]
        )
        rows = c22.parse_race(output, 4)
        c22.race_winners(rows, {5})
        two = c22.parse_race(
            "\n".join([winner.format(1), winner.format(2), loser.format(3)]), 3
        )
        with self.assertRaises(ValueError):
            c22.race_winners(two, {5})
        with self.assertRaises(ValueError):
            c22.race_winners(c22.parse_race(loser.format(1), 1), {5})
        with self.assertRaises(ValueError):
            c22.race_winners(rows, {5, 6})
        stale_accepted = c22.parse_race(
            "job1:,claim|5,stale|true,ack|true,again|false,", 1
        )
        with self.assertRaises(ValueError):
            c22.race_winners(stale_accepted, {5})
        replay_accepted = c22.parse_race(
            "job1:,claim|5,stale|false,ack|true,again|true,", 1
        )
        with self.assertRaises(ValueError):
            c22.race_winners(replay_accepted, {5})
        for bad, jobs in (
            ("garbage", 1),
            (winner.format(1), 2),
            (winner.format(1) + "\n" + winner.format(1), 2),
            ("job1:,claim|5,ack|true,stale|false,again|false,", 1),
            ("job1:,claim|x,stale|false,ack|true,again|false,", 1),
            ("job1:,claim|5,stale|false,ack|true,", 1),
            ("job1:,claim|5,stale|maybe,ack|true,again|false,", 1),
            ("job1:,claim|5,stale|f,ack|t,again|f,", 1),
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                c22.parse_race(bad, jobs)

    def test_probe_summary_is_closed_booleans(self):
        good = '{"exported":true,"present":true,"match":false}'
        self.assertEqual(
            {"exported": True, "present": True, "match": False}, c22.parse_probe(good)
        )
        for bad in (
            '{"exported":true,"present":true}',
            '{"exported":true,"present":true,"match":"yes"}',
            '{"exported":true,"present":true,"match":true,"password":"x"}',
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                c22.parse_probe(bad)

    def test_scripts_take_secrets_from_stdin_and_stay_inside_the_container(self):
        scripts = (
            c22.RACE_SCRIPT,
            c22.PASSWORD_PROBE_SCRIPT,
            c22.CREDENTIAL_PROBE_SCRIPT,
        )
        for script in scripts:
            self.assertNotIn("docker", script)
            self.assertNotRegex(script, r"(?i)password\s*=\s*['\"][^'\"$]")
        self.assertIn("IFS= read -r PGPASSWORD", c22.PASSWORD_PROBE_SCRIPT)
        self.assertIn("-h dev-pg", c22.PASSWORD_PROBE_SCRIPT)
        self.assertIn("IFS= read -r key", c22.CREDENTIAL_PROBE_SCRIPT)
        self.assertIn("unset N8N_ENCRYPTION_KEY_FILE", c22.CREDENTIAL_PROBE_SCRIPT)
        # The node program sits in single quotes in the shell script.
        program = c22.CREDENTIAL_PROBE_SCRIPT.split("node -e '", 1)[1].split(
            '\' "$out"'
        )[0]
        self.assertNotIn("'", program)
        self.assertNotIn("console.log", program)
        self.assertNotIn("lease_token", c22.RACE_SQL.split("SELECT 'claim|'")[1])

    @unittest.skipUnless(SHELL, "POSIX sh required")
    def test_scripts_parse_as_posix_sh(self):
        for script in (
            c22.RACE_SCRIPT,
            c22.PASSWORD_PROBE_SCRIPT,
            c22.CREDENTIAL_PROBE_SCRIPT,
        ):
            result = subprocess.run(
                [SHELL, "-n", "-c", script], capture_output=True, text=True, check=False
            )
            self.assertEqual(0, result.returncode, result.stderr)

    @unittest.skipUnless(SHELL, "POSIX sh required")
    def test_race_script_fans_out_and_prints_parseable_jobs(self):
        # A stub psql: the first job to create the lock directory wins.
        stub = r"""#!/bin/sh
case "$*" in *"-c"*) echo '2026-10-16 00:00:00+00'; exit 0;; esac
cat >/dev/null
echo
if mkdir "$LOCK" 2>/dev/null; then
 printf 'claim|5\nstale|false\nack|true\nagain|false\n'
else
 printf 'claim|0\nstale|false\nack|false\nagain|false\n'
fi
"""
        with tempfile.TemporaryDirectory() as root:
            bindir = Path(root) / "bin"
            bindir.mkdir()
            psql = bindir / "psql"
            psql.write_text(stub)
            psql.chmod(0o755)
            env = {
                "PATH": f"{bindir}:/usr/bin:/bin",
                "LOCK": str(Path(root) / "lock"),
            }
            result = subprocess.run(
                [SHELL, "-ec", c22.RACE_SCRIPT, "race", "4"],
                input=c22.RACE_SQL,
                capture_output=True,
                check=False,
                text=True,
                env=env,
                timeout=30,
            )
        self.assertEqual(0, result.returncode, result.stderr)
        rows = c22.parse_race(result.stdout, 4)
        c22.race_winners(rows, {5})

    @unittest.skipUnless(SHELL and NODE, "sh and node required")
    def test_credential_probe_reports_match_and_fails_closed_on_a_wrong_key(self):
        stub = r"""#!/bin/sh
for arg in "$@"; do case "$arg" in --output=*) out=${arg#--output=};; esac; done
if [ -n "${N8N_ENCRYPTION_KEY:-}" ] && [ "$N8N_ENCRYPTION_KEY" != right-key ]; then exit 1; fi
if [ -z "${N8N_ENCRYPTION_KEY:-}" ] && [ -z "${N8N_ENCRYPTION_KEY_FILE:-}" ]; then exit 1; fi
printf '[{"id":"c1","data":{"password":"right-secret"}}]' >"$out"
"""
        with tempfile.TemporaryDirectory() as root:
            bindir = Path(root) / "bin"
            bindir.mkdir()
            n8n = bindir / "n8n"
            n8n.write_text(stub)
            n8n.chmod(0o755)
            env = {
                "PATH": f"{bindir}:{Path(NODE).parent}:/usr/bin:/bin",
                "N8N_ENCRYPTION_KEY_FILE": "/run/secrets/key",
                "TMPDIR": root,
            }

            def probe(value: str, key: str = ""):
                digest = hashlib.sha256(value.encode()).hexdigest()
                result = subprocess.run(
                    [
                        SHELL,
                        "-ec",
                        c22.CREDENTIAL_PROBE_SCRIPT,
                        "p",
                        "c1",
                        "password",
                        digest,
                    ],
                    input=key + "\n",
                    capture_output=True,
                    check=False,
                    text=True,
                    env=env,
                    timeout=30,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertNotIn("right-secret", result.stdout + result.stderr)
                return c22.parse_probe(result.stdout)

            self.assertEqual(
                {"exported": True, "present": True, "match": True},
                probe("right-secret"),
            )
            self.assertEqual(
                {"exported": True, "present": True, "match": False},
                probe("other-secret"),
            )
            self.assertEqual(
                {"exported": True, "present": True, "match": True},
                probe("right-secret", key="right-key"),
            )
            self.assertEqual(
                {"exported": False, "present": False, "match": False},
                probe("right-secret", key="wrong-key"),
            )
            self.assertFalse((Path(root) / "credential-probe.json").exists())


class ExecutionTimeoutFactsTests(unittest.TestCase):
    def test_facts_are_closed_booleans_and_never_mask_the_timeout(self):
        lines = {"worker": 'Registered runner "js"\nWorker started execution 7'}
        facts = c22.execution_timeout_facts(
            "running", lambda role, text: text in lines.get(role, "")
        )
        self.assertEqual("running", facts["last_status"])
        self.assertEqual({"enqueued": False}, facts["main_log"])
        self.assertEqual(
            {
                "started": True,
                "finished": False,
                "unknown_node": False,
                "runner_timeout": False,
                "runner_registered": True,
            },
            facts["worker_log"],
        )
        self.assertEqual(
            "other",
            c22.execution_timeout_facts("secret text", lambda *a: False)["last_status"],
        )

        def broken(role, text):
            raise RehearsalFailure("container gone")

        facts = c22.execution_timeout_facts("none", broken)
        self.assertEqual("unavailable", facts["worker_log"])

    def test_await_execution_records_the_facts_on_timeout(self):
        case = driver()
        case.api = lambda *a, **k: {"id": "e1", "status": "new"}
        case.fixture.logs_contain = lambda role, text: False

        def wait_until(probe, message, seconds, failure=None):
            self.assertFalse(probe())
            failure()
            raise RehearsalFailure(message)

        case.fixture.wait_until = wait_until
        with self.assertRaises(RehearsalFailure):
            case.await_execution("e1", "success")
        self.assertEqual(
            "new", case.fixture.receipt["execution_timeout_facts"]["last_status"]
        )


class Criterion22DriverTests(unittest.TestCase):
    def test_concurrent_claims_scenario_races_with_the_budgeted_jobs(self):
        case = driver()
        published = iter([("r1", "5"), ("r2", "6"), ("r3", "7")])
        case.publish_next = lambda source: next(published)
        case.assert_claimable = lambda count: None
        case.db_value = lambda sql, role="p04_audit": "3"
        jobs = []

        def race(count):
            jobs.append(count)
            ids = [5] if len(jobs) == 1 else [6, 7]
            won = [
                {"claim": i, "stale": False, "ack": True, "again": False} for i in ids
            ]
            lost = {"claim": 0, "stale": False, "ack": False, "again": False}
            return won + [dict(lost) for _ in range(count - len(ids))]

        case.race = race
        case.scenario_concurrent_claims()
        self.assertEqual([c22.RACE_JOBS, c22.RACE_JOBS], jobs)

    def test_race_fits_the_notifier_connection_budget(self):
        from tests.validation.test_opsflow_database_rehearsal import provision_sql

        limit = f"ALTER ROLE opsflow_notifier CONNECTION LIMIT {c22.NOTIFIER_CONNECTION_LIMIT};"
        self.assertEqual(1, provision_sql().count(limit))
        pool = native_driver.OpsflowN8nNativeRehearsal.postgres_credential("x")
        self.assertEqual(c22.WORKFLOW_POOL_CONNECTIONS, pool["data"]["maxConnections"])
        self.assertEqual(3, c22.RACE_JOBS)

    def test_publish_next_uses_rising_unique_capture_times_and_safe_ids(self):
        case = driver()
        seen = []
        case.publish = lambda source, digest, captured: (
            seen.append((source, digest, captured)) or digest
        )
        case.db_value = lambda sql, role="p04_audit": "42"
        ids = [case.publish_next("hy-home.docker")[1] for _ in range(3)]
        self.assertEqual(["42"] * 3, ids)
        self.assertEqual(
            ["2026-10-17T00:00:00Z", "2026-10-18T00:00:00Z", "2026-10-19T00:00:00Z"],
            [captured for _, _, captured in seen],
        )
        self.assertEqual(3, len({digest for _, digest, _ in seen}))
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{64}", d) for _, d, _ in seen))
        case.db_value = lambda sql, role="p04_audit": "1; DROP"
        with self.assertRaises(RehearsalFailure):
            case.publish_next("blog-data")

    def test_password_probe_refusals(self):
        case = driver()

        def run(returncode, stdout="", stderr=""):
            case.password_probe = lambda role, password: subprocess.CompletedProcess(
                [], returncode, stdout, stderr
            )

        run(0, "1\n")
        case.assert_password("opsflow_notifier", "p", True)
        run(2, "", "FATAL:  password authentication failed")
        case.assert_password("opsflow_notifier", "p", False)
        with self.assertRaises(RehearsalFailure):
            case.assert_password("opsflow_notifier", "p", True)
        run(0, "1\n")
        with self.assertRaises(RehearsalFailure):
            case.assert_password("opsflow_notifier", "p", False)
        run(2, "", "connection refused")
        with self.assertRaises(RehearsalFailure):
            case.assert_password("opsflow_notifier", "p", False)

    def test_rewrite_secret_file_keeps_identity_and_refuses_a_swap(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "notifier.secret"
            path.write_text("old\n")
            path.chmod(0o600)
            meta = path.stat()
            case = driver()
            case.secrets = {"notifier": ("old", path)}
            case.fixture.files = {
                path: PrivateFile(
                    path, meta.st_dev, meta.st_ino, meta.st_uid, meta.st_gid, 0o600
                )
            }
            case.rewrite_secret_file("notifier", "new-value")
            self.assertEqual("new-value\n", path.read_text())
            self.assertEqual(meta.st_ino, path.stat().st_ino)
            self.assertEqual(0o600, stat.S_IMODE(path.stat().st_mode))
            self.assertEqual(("new-value", path), case.secrets["notifier"])
            case.fixture.files[path] = PrivateFile(
                path, meta.st_dev, meta.st_ino + 1, meta.st_uid, meta.st_gid, 0o600
            )
            with self.assertRaises(RehearsalFailure):
                case.rewrite_secret_file("notifier", "other")
            self.assertEqual("new-value\n", path.read_text())
            os.symlink(path, Path(root) / "link")
            case.secrets = {"notifier": ("x", Path(root) / "link")}
            case.fixture.files[Path(root) / "link"] = case.fixture.files[path]
            with self.assertRaises(OSError):
                case.rewrite_secret_file("notifier", "other")

    def test_credential_rotation_denies_stale_before_rotating_the_n8n_credential(self):
        case = driver()
        events: list[str] = []
        case.assert_password = lambda role, password, accepted: events.append(
            f"password:{'old' if password == 'a' * 43 else 'new'}:{accepted}"
            if password in {"a" * 43} or len(password) == 43
            else "password:control:False"
        )
        case.publish_next = lambda source: ("r" * 64, "9")
        case.mail_total = lambda: 3
        case.db_value = lambda sql, role="p04_audit": (
            "0"
            if "pg_stat_activity" in sql and "count(*)" in sql
            else events.append("db") or ""
        )
        case.fixture.psql = lambda *a, **k: events.append("alter")
        case.run_manual = lambda workflow: "e1"
        case.await_execution = lambda execution, status, node=None: events.append(
            f"await:{status}"
        )
        case.row = lambda outbox_id, columns: "pending|0"
        case.api = lambda action, **payload: events.append(action)
        case.drain_manual = lambda workflow, run: events.append("drain")
        case.capture = lambda run: {"total": 4, "matched": True, "safe": True}
        written = []
        case.rewrite_secret_file = lambda key, value: written.append((key, value))
        case.scenario_credential_rotation("w1")
        self.assertLess(events.index("alter"), events.index("await:error"))
        self.assertLess(events.index("await:error"), events.index("credential_update"))
        self.assertLess(events.index("credential_update"), events.index("drain"))
        self.assertEqual("notifier", written[0][0])
        self.assertNotEqual("a" * 43, written[0][1])
        self.assertEqual("a" * 43, case.stale_notifier)
        self.assertEqual(
            "NOT_RUN",
            case.fixture.receipt["credential_rotation_facts"]["smtp_rotation"],
        )
        # A stale workflow run that does not fail stops before the update.
        events.clear()
        case.await_execution = mock.Mock(side_effect=RehearsalFailure("success"))
        with self.assertRaises(RehearsalFailure):
            case.scenario_credential_rotation("w1")
        self.assertNotIn("credential_update", events)

    def test_restore_probes_demand_generation_two_and_the_rotated_value(self):
        case = driver()
        case.fixture.generation = 1
        with self.assertRaises(RehearsalFailure):
            case.scenario_paired_restore_decrypt()
        case.fixture.generation = 2
        yes = {"exported": True, "present": True, "match": True}
        no = {"exported": True, "present": True, "match": False}
        calls = []

        def probe(credential, field, value, key=""):
            calls.append((credential, field, value == case.stale_notifier))
            return no if value == case.stale_notifier else yes

        case.credential_probe = probe
        case.scenario_paired_restore_decrypt()
        self.assertEqual(
            [
                ("pg1", "password", False),
                ("pg1", "password", True),
                ("smtp1", "host", False),
            ],
            calls,
        )
        case.credential_probe = lambda *a, **k: yes
        with self.assertRaises(RehearsalFailure):
            case.scenario_paired_restore_decrypt()

    def test_wrong_key_must_not_decrypt(self):
        yes = {"exported": True, "present": True, "match": True}
        no = {"exported": False, "present": False, "match": False}

        def probes(*results):
            replies = iter(results)
            return lambda *a, **k: next(replies)

        case = driver()
        case.secrets["encryption"] = ("e" * 64, Path("/owned/encryption.secret"))
        case.credential_probe = probes(yes, no)
        case.scenario_wrong_key_fail_closed()
        self.assertEqual({"exported": False}, case.fixture.receipt["wrong_key_facts"])
        # A wrong key that decrypts fails.
        case.credential_probe = probes(yes, yes)
        with self.assertRaises(RehearsalFailure):
            case.scenario_wrong_key_fail_closed()
        # A broken explicit-key path fails instead of passing as a refusal.
        case.credential_probe = probes(no, no)
        with self.assertRaises(RehearsalFailure):
            case.scenario_wrong_key_fail_closed()

    def test_scheduled_scenario_requires_worker_only_dev_access_and_trigger_mode(self):
        def configured(modes, state="pending|0"):
            case = driver()
            case.fixture.containers = {
                "main": mock.Mock(networks=("ctl",)),
                "worker": mock.Mock(networks=("ctl", "runner", "dev", "capture")),
            }
            case.fixture.wait_until.side_effect = lambda probe, *a: probe() or 1 / 0
            case.assert_claimable = lambda expected: None
            case.publish_next = lambda source: ("r" * 64, "1")
            case.mail_total = lambda: 2
            case.db_value = lambda sql, role="p04_audit": (
                "accepted_by_smtp" if "delivery_status" in sql else state
            )
            active = []
            case.set_active = lambda workflow, value: active.append(value)
            listed = iter(
                [[], [], [{"id": "9", "mode": modes, "status": "success"}]] * 2
            )
            case.executions = lambda workflow: next(listed)
            case.api = lambda action, **payload: {
                "status": "success",
                "mode": modes,
                "acknowledged": "success",
            }
            case.capture = lambda run: {"total": 3, "matched": True, "safe": True}
            case.drain_manual = mock.Mock()
            return case, active

        clock = iter(range(0, 10_000, 10))
        with (
            mock.patch.object(native_driver.time, "sleep"),
            mock.patch.object(native_driver.time, "monotonic", lambda: next(clock)),
        ):
            case, active = configured("trigger")
            case.scenario_scheduled_execution("w1")
            self.assertEqual([True, False], active)
            case.drain_manual.assert_called_once()
            self.assertEqual(
                {"wait_seconds", "trigger_executions", "worker_only_dev_network"},
                set(case.fixture.receipt["scheduled_execution_facts"]),
            )
            case, _ = configured("manual")
            with self.assertRaises(RehearsalFailure):
                case.scenario_scheduled_execution("w1")
            case, _ = configured("trigger", state="sending|1")
            case.db_value = lambda sql, role="p04_audit": (
                "accepted_by_smtp" if "delivery_status" in sql else "sending|1"
            )
            with self.assertRaises(RehearsalFailure):
                case.scenario_scheduled_execution("w1")
            case, _ = configured("trigger")
            case.fixture.containers["main"] = mock.Mock(networks=("ctl", "dev"))
            with self.assertRaises(RehearsalFailure):
                case.scenario_scheduled_execution("w1")

    def test_default_run_is_still_gated_by_the_same_opt_in(self):
        self.assertIsNone(native_driver.native_selection({}))
        gated = native_driver.OpsflowN8nNativeRehearsal
        self.assertEqual(
            [
                "test_actual_queue_runner_capture_unknown_reconcile_and_restore",
            ],
            [name for name in dir(gated) if name.startswith("test_")],
        )


if __name__ == "__main__":
    unittest.main()
