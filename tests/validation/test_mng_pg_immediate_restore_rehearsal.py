"""SPEC-0182 W7: safety contract of the RUN-0021 step 5a rehearsal script.

No Docker runs here. A fake runner answers like `mng-pg` and its clone, so the
tests pin what the script asks Docker to do, not what a database returns.
"""

import argparse
import errno
import fcntl
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/operations/mng-pg-immediate-restore-rehearsal.py"
LABEL = "20261024-184214F_20261029-221825D"
IMAGE_ID = "sha256:" + "ab" * 32
RESTORE_ID, CLONE_ID = "1" * 64, "2" * 64
SYSID = "7123456789012345678"
DBS = "app_db,mlflow,platform_dev,postgres"
FIELDS = [
    "result",
    "reason",
    "verify_rc",
    "restore_rc",
    "elapsed_seconds",
    "system_id_match",
    "db_list_match",
    "app_db_present",
    "mlflow_present",
    "heartbeat_present",
    "dbt_present",
    "count_stable",
    "extension_count",
    "sequence_count",
    "probe_result",
    "clone_hba_probe_rule",
    "scratch_mode_0700",
    "cleanup_status",
]


def _load():
    spec = importlib.util.spec_from_file_location("mng_pg_5a", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeDocker:
    """Records every call and answers like mng-pg and its restored clone."""

    def __init__(self, state, *, verify_rc=0, restore_rc="0", clone_sysid=SYSID, **kw):
        self.state, self.verify_rc, self.restore_rc = state, verify_rc, restore_rc
        self.clone_sysid = clone_sysid
        self.kw = kw
        self.calls, self.inputs, self.created, self.removed = [], [], {}, []
        self.auth_ok = kw.get("auth_enforced", True)
        self.timeouts = {}
        self.hba_write = None  # (container, path, line) the clone was asked to write
        self.lock_held = {}  # event -> whether the host backup lock was held

    def held(self, event):
        probe = open(self.state / ".hyhome-backup.lock", "a")
        try:
            fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.lock_held[event] = False
        except BlockingIOError:
            self.lock_held[event] = True
        finally:
            probe.close()

    def source_info(self):
        return [
            {
                "Image": IMAGE_ID,
                "State": {"Running": True},
                "Config": {
                    "Image": "hy-home/mng-pg:18.6-pgbackrest",
                    "Env": ["POSTGRES_USER=admin_role", "PGDATA=/x"],
                },
                "Mounts": [
                    {
                        "Destination": "/var/lib/pgbackrest",
                        "Source": str(self.state / "pgbackrest"),
                    },
                    {
                        "Destination": "/run/secrets/pgbackrest_cipher_pass",
                        "Source": str(self.state / "cipher.txt"),
                    },
                ],
            }
        ]

    def __call__(self, argv, *, timeout, input=None):
        self.calls.append(argv)
        self.inputs.append(input)
        self.timeouts[" ".join(argv[:2])] = timeout
        if argv[:3] == ["docker", "context", "show"]:
            return 0, self.kw.get("context", "default") + "\n"
        if argv[:3] == ["docker", "ps", "-a"]:
            cid = next(a.split("=", 2)[2] for a in argv if a.startswith("--filter=id="))
            gone = cid in self.removed and not self.kw.get("ps_still_lists")
            return self.kw.get("ps_rc", 0), "" if gone else cid + "\n"
        if argv[:3] == ["docker", "inspect", "mng-pg"]:
            return 0, json.dumps(self.source_info())
        if argv[:2] == ["docker", "create"]:
            name = argv[2].split("=", 1)[1]
            cid = RESTORE_ID if "restore" in name else CLONE_ID
            self.created[name] = cid
            return 0, cid + "\n"
        if argv[:2] == ["docker", "start"]:
            return 0, ""
        if argv[:2] == ["docker", "wait"]:
            self.held("restore_wait")
            if self.kw.get("wait_timeout"):
                return 1, ""  # what _run returns on TimeoutExpired
            return 0, self.restore_rc + "\n"
        if argv[:2] == ["docker", "stop"]:
            return 0, ""
        if argv[:2] == ["docker", "rm"]:
            if not self.kw.get("rm_noop"):
                self.removed.append(argv[-1])
            return 0, ""
        if argv[:2] == ["docker", "inspect"]:
            if "{{.State.Running}}" in argv:
                return 0, "false\n" if self.kw.get("clone_down") else "true\n"
            if self.kw.get("inspect_fail"):
                return 1, ""
            if argv[-1] in self.created:  # by name
                return 0, self.kw.get("inspect_id", self.created[argv[-1]])
            return 0, "true"
        if "verify" in argv:
            self.held("verify")
            return self.verify_rc, ""
        if argv[-2].endswith("pg_hba.conf"):
            self.hba_write = (argv[argv.index("--user") + 2], argv[-2], argv[-1])
            return self.kw.get("hba_write_rc", 0), ""
        if "psql" in argv:
            return self.psql(argv, input or "")
        if "sh" in argv:
            return self.tcp(input or "")
        raise AssertionError(argv)

    def psql(self, argv, sql):
        container = argv[argv.index("--user") + 2]
        if "pg_is_in_recovery" in sql:
            self.held("ready")
            if self.kw.get("clone_down"):
                return 1, ""
            return 0, "t\n" if self.kw.get("in_recovery") else "f\n"
        if "current_setting('hba_file')" in sql:
            return 0, "hba=" + self.kw.get(
                "hba_file", "/var/lib/postgresql/data/pgdata/pg_hba.conf"
            ) + "\n"
        if "pg_reload_conf" in sql:
            role = self.hba_write[2].split()[2] if self.hba_write else ""
            rule1 = f"host|app_db|{role}|127.0.0.1|255.255.255.255|scram-sha-256|"
            rule1 = self.kw.get("rule1", rule1)
            return (
                0,
                f"reload=true\nrule1={rule1}\nerrors={self.kw.get('hba_errors', 0)}\n",
            )
        if "pg_control_system" in sql:
            self.held(f"identity_{container}")
            sysid = SYSID if container == "mng-pg" else self.clone_sysid
            dbs = DBS if container == "mng-pg" else self.kw.get("clone_dbs", DBS)
            return 0, f"sysid={sysid}\ndbs={dbs}\n"
        if "to_regnamespace" in sql or "to_regclass" in sql:
            return 0, "t\n" if self.kw.get("objects", True) else "f\n"
        if "REPEATABLE READ" in sql:
            second = self.kw.get("second_count", "5")
            return 0, f"t0a=5\nt0b={second}\n"
        if "pg_extension" in sql:
            return 0, "e=plpgsql 1.0\ns=public.seq_a\n"
        if "aclexplode" in sql:
            grants = {
                "acl": "CONNECT,TEMPORARY",
                "other_deps": "0",
                "members": "0",
                "table_writes": self.kw.get("table_writes", "0"),
                "schema_create": "0",
                "db_create": "false",
            }
            return 0, "".join(f"{k}={v}\n" for k, v in grants.items())
        if "CREATE ROLE" in sql:
            return 0, ""
        if "DROP ROLE" in sql:
            return 0, ""
        if "pg_roles" in sql:
            return 0, f"role={self.kw.get('role_left', '0')}\ntemp=0\n"
        raise AssertionError(sql)

    def tcp(self, text):
        _, _, sql = text.partition("\n")
        if sql.strip() == "SELECT 1;":  # wrong-password attempt
            return (1, "") if self.auth_ok else (0, "1\n")
        if self.kw.get("session_fail"):
            return 1, ""
        return 0, "rows=1\ntcp=true\ntemp_after=0\n"


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        self.now += 0.5
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class RehearsalTests(unittest.TestCase):
    def setUp(self):
        self.m = _load()
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.state = self.tmp / "state"
        (self.state / "pgbackrest").mkdir(parents=True)
        self.scratch = self.tmp / "scratch"
        self.scratch.mkdir(mode=0o700)
        # the scratch root lives under /tmp in the test; the real list refuses it
        self.m.FORBIDDEN_ROOTS = ()

    def args(self, **over):
        values = {
            "label": LABEL,
            "scratch_root": self.scratch,
            "heartbeat": "platform_dev.debezium_heartbeat",
            "dbt": "platform_dev.analytics",
            "count_table": ["mlflow.public.experiments"],
            "min_free_gib": 0,
        }
        values.update(over)
        return argparse.Namespace(**values)

    def run_rehearsal(self, **kw):
        for old in self.scratch.iterdir():  # one fresh target per run
            shutil.rmtree(old) if old.is_dir() else old.unlink()
        fake = FakeDocker(self.state, **kw)
        clock = Clock()
        result = self.m.rehearse(
            self.args(), run=fake, sleep=clock.sleep, clock=clock, env={}
        )
        return result, fake

    def test_refuses_bad_inputs(self):
        real = _load()
        cases = {
            "label": {"label": "latest"},
            "label_short": {"label": "20261024-184214F_"},
            "scratch_not_empty": {},
            "scratch_path": {"scratch_root": Path("relative/dir")},
            "count_table_missing": {"count_table": None},
            "heartbeat_identifier": {"heartbeat": "db.sch;drop"},
        }
        (self.scratch / "old").write_text("x")
        for reason, over in cases.items():
            with self.assertRaises(self.m.Refused, msg=reason):
                self.m.check_inputs(self.args(**over))
        (self.scratch / "old").unlink()
        # the real forbidden list refuses /tmp even for an otherwise valid root
        with self.assertRaises(real.Refused) as caught:
            real.check_inputs(self.args())
        self.assertEqual(str(caught.exception), "scratch_forbidden_root")
        self.scratch.chmod(0o755)
        with self.assertRaises(self.m.Refused):
            self.m.check_inputs(self.args())

    def test_refusal_runs_nothing(self):
        fake = FakeDocker(self.state)
        with self.assertRaises(self.m.Refused):
            self.m.rehearse(self.args(label="latest"), run=fake)
        self.assertEqual(fake.calls, [])

    def test_verify_failure_stops_before_lock_and_restore(self):
        result, fake = self.run_rehearsal(verify_rc=1)
        self.assertEqual((result["result"], result["reason"]), ("FAIL", "verify"))
        self.assertEqual(result["verify_rc"], 1)
        self.assertEqual(fake.created, {})
        self.assertEqual(result["cleanup_status"], "none_created")

    def test_busy_host_lock_stops_with_75(self):
        holder = open(self.state / ".hyhome-backup.lock", "w")
        self.addCleanup(holder.close)
        fcntl.flock(holder, fcntl.LOCK_EX)
        result, fake = self.run_rehearsal()
        self.assertEqual(result["reason"], "lock_busy")
        self.assertEqual(fake.created, {})

    def test_success_contract(self):
        result, fake = self.run_rehearsal()
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(result["cleanup_status"], "removed")
        self.assertIs(result["scratch_mode_0700"], True)
        for key in ("system_id_match", "db_list_match", "count_stable"):
            self.assertIs(result[key], True)
        creates = [c for c in fake.calls if c[:2] == ["docker", "create"]]
        self.assertEqual(len(creates), 2)
        for argv in creates:
            self.assertIn("--network=none", argv)
            self.assertIn(IMAGE_ID, argv)
            self.assertFalse([a for a in argv if "--entrypoint" in a])
            self.assertFalse([a for a in argv if a.startswith(("-p", "--publish"))])
            self.assertFalse([a for a in argv if "latest" in a])
        restore, clone = creates
        text = " ".join(restore)
        self.assertEqual(restore[-3:-1], ["sh", "-ec"])
        for option in (
            f"--set={LABEL}",
            "--type=immediate",
            "--target-action=promote",
            "--archive-mode=off",
            "gosu postgres pgbackrest",
        ):
            self.assertIn(option, text)
        self.assertNotIn("--type=time", text)
        self.assertTrue(any("dst=/var/lib/pgbackrest,readonly" in a for a in restore))
        self.assertTrue(any("pgbackrest_cipher_pass,readonly" in a for a in restore))
        self.assertIn("archive_mode=off", clone)
        # pgbackrest.conf has no archive-copy: recovery needs archive-get
        self.assertTrue(any("dst=/var/lib/pgbackrest,readonly" in a for a in clone))
        self.assertFalse(
            any(
                "dst=/var/lib/pgbackrest" in a and "readonly" not in a
                for a in creates[0] + clone
            )
        )
        for argv in creates:
            self.assertIn(f"--memory={self.m.MEMORY}", argv)
            self.assertIn(f"--memory-swap={self.m.MEMORY}", argv)
            self.assertIn(f"--cpus={self.m.CPUS}", argv)

    def test_refuses_remote_or_non_default_docker_target(self):
        fake = FakeDocker(self.state)
        with self.assertRaises(self.m.Refused) as caught:
            self.m.rehearse(self.args(), run=fake, env={"DOCKER_HOST": "ssh://x"})
        self.assertEqual(str(caught.exception), "docker_host_set")
        self.assertEqual(fake.calls, [])
        fake = FakeDocker(self.state, context="remote")
        with self.assertRaises(self.m.Refused) as caught:
            self.m.rehearse(self.args(), run=fake, env={})
        self.assertEqual(str(caught.exception), "docker_context")
        self.assertEqual(fake.calls, [["docker", "context", "show"]])

    def test_limits_are_bounded(self):
        self.assertRegex(self.m.MEMORY, r"^[1-8]g$")
        self.assertTrue(1 <= float(self.m.CPUS) <= 8)

    def test_source_and_clone_queries_use_uid_70_socket(self):
        _, fake = self.run_rehearsal()
        execs = [c for c in fake.calls if c[:2] == ["docker", "exec"] and "psql" in c]
        self.assertTrue(execs)
        for argv in execs:
            self.assertEqual(argv[argv.index("--user") + 1], "70")
            self.assertNotIn("-h", argv)
            self.assertIn("admin_role", argv)

    def test_probe_password_never_in_argv(self):
        _, fake = self.run_rehearsal()
        secret_inputs = [i for i in fake.inputs if i and "PASSWORD '" in i]
        self.assertEqual(len(secret_inputs), 1)
        password = secret_inputs[0].split("PASSWORD '")[1].split("'")[0]
        self.assertTrue(password)
        self.assertFalse([a for call in fake.calls for a in call if password in a])
        tcp = [c for c in fake.calls if "sh" in c and "-p 5432" in " ".join(c)]
        self.assertEqual(len(tcp), 2)  # wrong password first, then the real one

    def test_probe_blocked_when_public_could_write(self):
        result, _ = self.run_rehearsal(table_writes="3")
        self.assertEqual(result["reason"], "probe_privileges")
        self.assertEqual(result["probe_result"], "FAIL")
        self.assertEqual(result["result"], "FAIL")

    def test_probe_session_never_logs_the_password_statement(self):
        _, fake = self.run_rehearsal()
        sql = next(i for i in fake.inputs if i and "CREATE ROLE" in i)
        self.assertLess(sql.index("SET log_statement = none"), sql.index("CREATE ROLE"))

    def test_role_dropped_in_finally_after_mid_probe_failure(self):
        for over, reason in (
            ({"table_writes": "3"}, "probe_privileges"),
            ({"session_fail": True}, "probe_session"),
        ):
            result, fake = self.run_rehearsal(**over)
            self.assertEqual(result["reason"], reason)
            idx = [i for i, t in enumerate(fake.inputs) if t and "DROP ROLE" in t]
            self.assertEqual(len(idx), 1, reason)  # only the finally drop ran
            stop = next(
                i for i, c in enumerate(fake.calls) if c[:2] == ["docker", "stop"]
            )
            self.assertLess(idx[0], stop)

    def test_failing_probe_cleanup_is_a_failure(self):
        result, _ = self.run_rehearsal(role_left="1")
        self.assertEqual(result["reason"], "probe_cleanup")
        self.assertEqual(result["probe_result"], "FAIL")
        self.assertEqual(result["result"], "FAIL")

    def test_wait_timeout_is_a_restore_failure(self):
        result, fake = self.run_rehearsal(wait_timeout=True)
        self.assertEqual((result["reason"], result["restore_rc"]), ("restore", 1))
        self.assertEqual(fake.timeouts["docker wait"], self.m.RESTORE_TIMEOUT)
        self.assertEqual(list(fake.created), [next(iter(fake.created))])  # no clone
        timed_out = subprocess.TimeoutExpired("docker", 1)
        with mock.patch.object(self.m.subprocess, "run", side_effect=timed_out):
            self.assertEqual(self.m._run(["docker", "wait", "x"], timeout=1), (1, ""))

    def test_clone_exit_and_ready_timeout(self):
        result, _ = self.run_rehearsal(clone_down=True)
        self.assertEqual(result["reason"], "clone_exited")
        result, _ = self.run_rehearsal(in_recovery=True)
        self.assertEqual(result["reason"], "clone_ready_timeout")

    def test_lock_is_held_from_verify_until_ready(self):
        result, fake = self.run_rehearsal()
        self.assertEqual(result["result"], "PASS")
        for event in ("verify", "restore_wait", "ready", "identity_mng-pg"):
            self.assertIs(fake.lock_held[event], True, event)
        clone = next(k for k in fake.lock_held if k.startswith("identity_hyhome"))
        self.assertIs(fake.lock_held[clone], False)  # released once ready

    def test_busy_lock_runs_no_verify(self):
        holder = open(self.state / ".hyhome-backup.lock", "w")
        self.addCleanup(holder.close)
        fcntl.flock(holder, fcntl.LOCK_EX)
        _, fake = self.run_rehearsal()
        self.assertFalse([c for c in fake.calls if "verify" in c])

    def test_oserror_becomes_fixed_output_and_unknown_removal_is_not_removed(self):
        eio = OSError(errno.EIO, "io")
        with mock.patch.object(self.m.fcntl, "flock", side_effect=eio):
            result, _ = self.run_rehearsal()
        self.assertEqual((result["result"], result["reason"]), ("FAIL", "io_error"))
        with mock.patch.object(self.m, "inventory", side_effect=eio):
            result, _ = self.run_rehearsal()
        self.assertEqual(result["reason"], "io_error")
        self.assertEqual(result["cleanup_status"], "removed")
        self.assertEqual(len(self.m.render(result).splitlines()), len(FIELDS))

    def test_removed_needs_a_by_id_absence_check(self):
        for over in ({"ps_still_lists": True}, {"ps_rc": 1}, {"rm_noop": True}):
            result, fake = self.run_rehearsal(**over)
            self.assertTrue(result["cleanup_status"].startswith("failed:"), over)
            self.assertEqual(result["result"], "FAIL")
            ps = [c for c in fake.calls if c[:3] == ["docker", "ps", "-a"]]
            self.assertIn("--no-trunc", ps[0])
            self.assertIn(f"--filter=id={RESTORE_ID}", ps[0])
        # a failed inspect is unknown: still stopped and removed by ID, then confirmed
        result, fake = self.run_rehearsal(inspect_fail=True)
        self.assertEqual(result["cleanup_status"], "removed")
        self.assertEqual(sorted(fake.removed), sorted({RESTORE_ID, CLONE_ID}))
        result, _ = self.run_rehearsal(inspect_fail=True, ps_rc=1)
        self.assertTrue(result["cleanup_status"].startswith("failed:"))

    def test_trust_auth_is_a_failure(self):
        result, fake = self.run_rehearsal(auth_enforced=False)
        self.assertEqual(result["reason"], "probe_auth_not_enforced")
        wrong = [i for i in fake.inputs if i and i.endswith("\nSELECT 1;\n")]
        self.assertEqual(len(wrong), 5)  # retried while the reload settles, then closed

    def probe_role(self, fake):
        return fake.hba_write[2].split()[2]

    def test_hba_rule_goes_only_into_the_clone_scratch_pgdata(self):
        result, fake = self.run_rehearsal()
        self.assertEqual(result["clone_hba_probe_rule"], "added")
        container, path, line = fake.hba_write
        self.assertTrue(container.startswith("hyhome-5a-clone-"))
        self.assertEqual(path, self.m.HBA_FILE)
        self.assertTrue(path.startswith(self.m.DATA_TARGET + "/pgdata/"))
        self.assertEqual(
            line, f"host app_db {self.probe_role(fake)} 127.0.0.1/32 scram-sha-256"
        )
        exec_call = next(c for c in fake.calls if path in c)
        self.assertEqual(exec_call[exec_call.index("--user") + 1], "70")
        # order: role created, path checked, rule written, reloaded, then TCP auth
        texts = [
            (i or "") + " ".join(c)
            for c, i in zip(fake.calls, fake.inputs, strict=True)
        ]
        first = lambda needle: next(n for n, t in enumerate(texts) if needle in t)  # noqa: E731
        self.assertLess(first("CREATE ROLE"), first("current_setting('hba_file')"))
        self.assertLess(first("current_setting('hba_file')"), first(path))
        self.assertLess(first(path), first("pg_reload_conf"))
        self.assertLess(first("pg_reload_conf"), first("127.0.0.1 -p 5432"))

    def test_hba_prepend_script_puts_rule_before_trust_and_keeps_mode(self):
        hba = self.tmp / "pg_hba.conf"
        hba.write_text("local all all trust\nhost all all 127.0.0.1/32 trust\n")
        hba.chmod(0o640)
        before = hba.stat()
        rule = "host app_db hy_5a_probe_ab12cd34 127.0.0.1/32 scram-sha-256"
        argv = ["sh", "-ec", self.m.HBA_PREPEND, "sh", str(hba), rule]
        subprocess.run(argv, check=True)
        lines = hba.read_text().splitlines()
        self.assertEqual(lines[0], rule)
        self.assertEqual(
            lines[1:], ["local all all trust", "host all all 127.0.0.1/32 trust"]
        )
        after = hba.stat()
        self.assertEqual(
            (after.st_ino, after.st_mode, after.st_uid),
            (before.st_ino, before.st_mode, before.st_uid),
        )
        self.assertFalse((self.tmp / "pg_hba.conf.probe").exists())

    def test_hba_role_name_is_validated(self):
        for bad in ('x"; DROP', "a b", "1abc", "", "a\nhost all all 0.0.0.0/0 trust"):
            with self.assertRaises(self.m.Stop, msg=bad) as caught:
                self.m.hba_rule(bad)
            self.assertEqual(str(caught.exception), "probe_identifier")
            calls = []
            with self.assertRaises(self.m.Stop):
                self.m.probe(
                    lambda *a, calls=calls, **k: calls.append(a) or (0, ""),
                    "c",
                    "adm",
                    bad,
                    {},
                )
            self.assertEqual(calls, [])

    def test_hba_failures_stop_closed(self):
        result, fake = self.run_rehearsal(hba_file="/etc/postgresql/pg_hba.conf")
        self.assertEqual(result["reason"], "probe_hba_path")
        self.assertIsNone(fake.hba_write)
        self.assertEqual(result["clone_hba_probe_rule"], "NOT_RUN")
        result, _ = self.run_rehearsal(hba_write_rc=1)
        self.assertEqual(result["reason"], "probe_hba_write")
        self.assertEqual(result["clone_hba_probe_rule"], "unknown")
        for over in (
            {"hba_errors": 1},
            {"rule1": "host|all|all|127.0.0.1|255.255.255.255|trust|"},
        ):
            result, fake = self.run_rehearsal(**over)
            self.assertEqual(result["reason"], "probe_hba_check", over)
            self.assertEqual(result["clone_hba_probe_rule"], "added")
            self.assertFalse(
                [i for i in fake.inputs if i and i.endswith("\nSELECT 1;\n")]
            )

    def test_source_container_is_never_modified(self):
        _, fake = self.run_rehearsal()
        for argv, text in zip(fake.calls, fake.inputs, strict=True):
            if "mng-pg" not in argv:
                continue
            ok = (
                argv[:3] == ["docker", "inspect", "mng-pg"]
                or "verify" in argv
                or "pg_control_system" in (text or "")
            )
            self.assertTrue(ok, argv)
        self.assertEqual(fake.hba_write[0][:16], "hyhome-5a-clone-")
        for argv, text in zip(fake.calls, fake.inputs, strict=True):
            if text and any(
                k in text for k in ("CREATE ROLE", "DROP ROLE", "pg_reload_conf")
            ):
                self.assertNotIn("mng-pg", argv)

    def test_identity_mismatch_and_missing_objects_fail(self):
        result, _ = self.run_rehearsal(clone_sysid="1")
        self.assertEqual(result["reason"], "identity_mismatch")
        self.assertIs(result["system_id_match"], False)
        result, _ = self.run_rehearsal(clone_dbs="app_db,platform_dev,postgres")
        self.assertIs(result["db_list_match"], False)
        result, _ = self.run_rehearsal(objects=False)
        self.assertEqual(result["reason"], "required_object_missing")
        self.assertIs(result["heartbeat_present"], False)

    def test_unequal_counts_fail(self):
        result, _ = self.run_rehearsal(second_count="6")
        self.assertEqual(result["reason"], "count_unstable")
        self.assertIs(result["count_stable"], False)

    def test_restore_failure_cleans_up_only_owned_and_keeps_scratch(self):
        result, fake = self.run_rehearsal(restore_rc="1")
        self.assertEqual((result["reason"], result["restore_rc"]), ("restore", 1))
        self.assertEqual(fake.removed, [RESTORE_ID])
        self.assertTrue((self.scratch / "data").is_dir())
        self.assertIs(result["scratch_mode_0700"], True)

    def test_id_mismatch_is_never_removed(self):
        result, fake = self.run_rehearsal(inspect_id="f" * 64)
        self.assertEqual(fake.removed, [])
        self.assertTrue(result["cleanup_status"].startswith("failed:"))
        self.assertEqual(result["result"], "FAIL")

    def test_removal_targets_are_created_ids_only(self):
        _, fake = self.run_rehearsal()
        self.assertEqual(sorted(fake.removed), sorted({RESTORE_ID, CLONE_ID}))
        for argv in fake.calls:
            if argv[:2] in (["docker", "rm"], ["docker", "stop"]):
                self.assertIn(argv[-1], (RESTORE_ID, CLONE_ID))
                self.assertNotIn("mng-pg", argv)

    def test_lock_is_released_before_checks_and_always(self):
        result, _ = self.run_rehearsal()
        holder = open(self.state / ".hyhome-backup.lock", "a")
        self.addCleanup(holder.close)
        fcntl.flock(holder, fcntl.LOCK_EX | fcntl.LOCK_NB)  # raises if still held
        self.assertEqual(result["result"], "PASS")
        result, _ = self.run_rehearsal(restore_rc="1")
        fcntl.flock(holder, fcntl.LOCK_UN)
        fcntl.flock(holder, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def test_output_has_only_fixed_fields(self):
        result, _ = self.run_rehearsal()
        lines = self.m.render(result).splitlines()
        self.assertEqual([line.split("=")[0] for line in lines], FIELDS)
        self.assertEqual(list(self.m.FIELDS), FIELDS)
        text = "\n".join(lines)
        self.assertNotIn("hy_5a_probe_", text)
        self.assertNotIn(SYSID, text)

    def test_source_text_has_no_forbidden_forms(self):
        text = SCRIPT.read_text()
        self.assertNotIn("--entrypoint", text)
        self.assertNotIn("latest", text)
        self.assertNotIn("--type=time", text)
        self.assertNotIn("--publish", text)
        self.assertIn("--network=none", text)
        self.assertIn("--archive-mode=off", text)
        self.assertIn("archive_mode=off", text)
        self.assertTrue(os.access(SCRIPT, os.X_OK))


if __name__ == "__main__":
    unittest.main()
