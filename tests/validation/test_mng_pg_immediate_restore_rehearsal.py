"""SPEC-0182 W7: safety contract of the RUN-0021 step 5a rehearsal script.

No Docker runs here. A fake runner answers like `mng-pg` and its clone, so the
tests pin what the script asks Docker to do, not what a database returns.
"""

import argparse
import fcntl
import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

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
        self.lock_held_at_ready = None

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
            return 0, self.restore_rc + "\n"
        if argv[:2] == ["docker", "stop"]:
            return 0, ""
        if argv[:2] == ["docker", "rm"]:
            self.removed.append(argv[-1])
            return 0, ""
        if argv[:2] == ["docker", "inspect"]:
            if argv[-1] in self.created:  # by name
                return 0, self.kw.get("inspect_id", self.created[argv[-1]])
            if argv[-1] in self.removed:
                return 1, ""
            return 0, "true"
        if "verify" in argv:
            return self.verify_rc, ""
        if "psql" in argv:
            return self.psql(argv, input or "")
        if "sh" in argv:
            return self.tcp(input or "")
        raise AssertionError(argv)

    def psql(self, argv, sql):
        container = argv[argv.index("--user") + 2]
        if "pg_is_in_recovery" in sql:
            return 0, "f\n"
        if "pg_control_system" in sql:
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
            return 0, "role=0\ntemp=0\n"
        raise AssertionError(sql)

    def tcp(self, text):
        _, _, sql = text.partition("\n")
        if sql.strip() == "SELECT 1;":  # wrong-password attempt
            return (1, "") if self.auth_ok else (0, "1\n")
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
        result = self.m.rehearse(self.args(), run=fake, sleep=clock.sleep, clock=clock)
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
        self.assertFalse(any("/var/lib/pgbackrest" in a for a in clone))

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
        tcp = [c for c in fake.calls if "sh" in c and "127.0.0.1" in " ".join(c)]
        self.assertEqual(len(tcp), 2)  # wrong password first, then the real one

    def test_probe_blocked_when_public_could_write(self):
        result, _ = self.run_rehearsal(table_writes="3")
        self.assertEqual(result["reason"], "probe_privileges")
        self.assertEqual(result["probe_result"], "FAIL")
        self.assertEqual(result["result"], "FAIL")

    def test_trust_auth_is_a_failure(self):
        result, _ = self.run_rehearsal(auth_enforced=False)
        self.assertEqual(result["reason"], "probe_auth_not_enforced")

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
