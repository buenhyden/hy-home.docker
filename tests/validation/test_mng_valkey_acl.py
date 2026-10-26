"""Synthetic, source-only checks for mng-valkey ACL generation."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import time
import unittest
import uuid
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "infra/04-data/mng-db/valkey/scripts/render-acl.sh"
)


class MngValkeyAclTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        (self.root / "default").write_text("synthetic-default\n", encoding="utf-8")
        (self.root / "monitor").write_text("synthetic-monitor\n", encoding="utf-8")
        (self.root / "inspector").write_text("synthetic-inspector\n", encoding="utf-8")

    def render(self, **overrides: str) -> subprocess.CompletedProcess[str]:
        env = {
            **os.environ,
            "MNG_VALKEY_DEFAULT_SECRET_FILE": str(self.root / "default"),
            "MNG_VALKEY_MONITOR_SECRET_FILE": str(self.root / "monitor"),
            "MNG_VALKEY_INSPECTOR_SECRET_FILE": str(self.root / "inspector"),
            "MNG_VALKEY_ACL_FILE": str(self.root / "users.acl"),
            "MNG_VALKEY_N8N_SECRET_FILE": str(self.root / "n8n"),
            **overrides,
        }
        return subprocess.run(
            ["sh", str(SCRIPT)], env=env, capture_output=True, text=True, check=False
        )

    def test_named_queue_user_is_opt_in_and_scoped_to_existing_db_and_prefix(self):
        self.assertEqual(0, self.render().returncode)
        self.assertNotIn("user n8n ", (self.root / "users.acl").read_text())
        secret = self.root / "n8n"
        secret.write_text("synthetic-n8n\n")
        secret.chmod(0o640)
        result = self.render(MNG_VALKEY_N8N_ENABLED="1")
        self.assertEqual(0, result.returncode, result.stderr)
        line = next(
            line
            for line in (self.root / "users.acl").read_text().splitlines()
            if line.startswith("user n8n ")
        )
        self.assertIn(hashlib.sha256(b"synthetic-n8n").hexdigest(), line)
        for rule in (
            "db=0",
            "~n8n:*",
            "&n8n:*",
            "-@all",
            "+evalsha",
            "+hmset",
            "+linsert",
            "+psetex",
            "+rename",
            "+quit",
        ):
            self.assertIn(rule, line.split())
        for rule in (
            "~*",
            "&*",
            "+@all",
            "+@write",
            "+@admin",
            "+flushdb",
            "+keys",
            "+scan",
            "+config",
            "+acl",
        ):
            self.assertNotIn(rule, line.split())
        self.assertNotIn("synthetic-", result.stdout + result.stderr + line)

    def test_invalid_named_inputs_preserve_the_previous_acl(self):
        self.assertEqual(0, self.render().returncode)
        previous = (self.root / "users.acl").read_bytes()
        secret = self.root / "n8n"
        for flag, content, mode in (
            ("true", "synthetic-n8n\n", 0o640),
            ("1", None, 0o640),
            ("1", "\n", 0o640),
            ("1", "a\nb\n", 0o640),
            ("1", "synthetic-default\n", 0o640),
            ("1", "synthetic-monitor\n", 0o640),
            ("1", "synthetic-inspector\n", 0o640),
            ("1", "synthetic-n8n\n", 0o644),
            ("1", "synthetic-n8n\n", 0o660),
        ):
            with self.subTest(flag=flag, content=content, mode=mode):
                secret.unlink(missing_ok=True)
                if content is not None:
                    secret.write_text(content)
                    secret.chmod(mode)
                result = self.render(MNG_VALKEY_N8N_ENABLED=flag)
                self.assertNotEqual(0, result.returncode)
                self.assertEqual(previous, (self.root / "users.acl").read_bytes())
                self.assertNotIn("synthetic-", result.stdout + result.stderr)
        secret.unlink()
        target = self.root / "n8n-original"
        target.write_text("synthetic-n8n-unique\n")
        target.chmod(0o640)
        secret.symlink_to(target)
        self.assertNotEqual(0, self.render(MNG_VALKEY_N8N_ENABLED="1").returncode)
        secret.unlink()
        os.link(target, secret)
        self.assertNotEqual(0, self.render(MNG_VALKEY_N8N_ENABLED="1").returncode)
        self.assertEqual(previous, (self.root / "users.acl").read_bytes())

    def test_default_keeps_shared_secret_and_service_roles_are_read_only(self) -> None:
        result = self.render()
        self.assertEqual(result.returncode, 0, result.stderr)
        acl = (self.root / "users.acl").read_text(encoding="utf-8")
        default = hashlib.sha256(b"synthetic-default").hexdigest()
        monitor = hashlib.sha256(b"synthetic-monitor").hexdigest()
        inspector = hashlib.sha256(b"synthetic-inspector").hexdigest()
        self.assertEqual(
            acl,
            f"user default on #{default} ~* &* +@all\n"
            f"user mngmonitor on #{monitor} -@all +ping +info +command|info "
            "+slowlog|len +commandlog|len\n"
            f"user mnginspector on #{inspector} ~* resetchannels -@all +@read "
            "+@connection -@dangerous +info\n",
        )
        self.assertNotIn("synthetic-", acl)
        self.assertEqual((self.root / "users.acl").stat().st_mode & 0o777, 0o600)

    def test_no_two_roles_share_a_secret(self) -> None:
        for role, other in (
            ("inspector", "default"),
            ("monitor", "default"),
            ("monitor", "inspector"),
        ):
            with self.subTest(role=role, other=other):
                (self.root / role).write_text(f"synthetic-{other}\n", encoding="utf-8")
                result = self.render()
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.root / "users.acl").exists())
                (self.root / role).write_text(f"synthetic-{role}\n", encoding="utf-8")

    def test_missing_or_multiline_secret_fails_closed(self) -> None:
        for name, content in [
            (n, c) for n in ("monitor", "inspector") for c in (None, "a\nb\n", "\n")
        ]:
            with self.subTest(name=name, content=content):
                path = self.root / name
                if content is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_text(content, encoding="utf-8")
                result = self.render()
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.root / "users.acl").exists())
                path.write_text(f"synthetic-{name}\n", encoding="utf-8")
        self.assertEqual(self.render().returncode, 0)

    def test_compose_replaces_requirepass_with_the_rendered_acl(self) -> None:
        compose = (SCRIPT.parents[2] / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertNotIn("--requirepass", compose)
        self.assertIn("/usr/local/libexec/mng-valkey/start.sh", compose)
        self.assertIn("/run/valkey:uid=999,gid=999,mode=0700", compose)


@unittest.skipUnless(
    os.environ.get("HYHOME_N8N_ACL_REHEARSAL") == "1",
    "opt-in isolated synthetic Valkey ACL rehearsal",
)
class MngValkeyAclNativeTests(unittest.TestCase):
    IMAGE = "sha256:a0dbf4c1d5708782907c10e2c72deff317518518b5288a58416981d9db95d30b"

    def docker(self, *arguments, password=None):
        environment = self.environment | (
            {"REDISCLI_AUTH": password} if password is not None else {}
        )
        remaining = self.deadline - time.monotonic()
        cleanup = arguments[0] in ("inspect", "rm")
        if not cleanup and remaining <= 0:
            self.fail("isolated ACL rehearsal exceeded its 180 second budget")
        return subprocess.run(
            ["docker", "--context", "default", *arguments],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=20 if cleanup else min(20, remaining),
        )

    def setUp(self):
        fixture = MngValkeyAclTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root = fixture.root
        self.environment = {
            "PATH": os.environ["PATH"],
            "DOCKER_CONFIG": str(self.root / "docker"),
        }
        self.deadline = time.monotonic() + 180
        secret = self.root / "n8n"
        secret.write_text("synthetic-n8n\n")
        secret.chmod(0o600)
        self.assertEqual(0, fixture.render(MNG_VALKEY_N8N_ENABLED="1").returncode)
        inspected = self.docker("image", "inspect", self.IMAGE, "--format", "{{.Id}}")
        self.assertEqual(
            0, inspected.returncode, "required cached Valkey image unavailable"
        )
        self.assertEqual(self.IMAGE, inspected.stdout.strip())
        self.name = "hyhome-n8n-acl-" + uuid.uuid4().hex
        self.addCleanup(self.remove_owned_container)
        created = self.docker(
            "create",
            "--name",
            self.name,
            "--label",
            "hyhome.n8n-acl=" + self.name,
            "--pull",
            "never",
            "--network",
            "none",
            "--read-only",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--memory",
            "64m",
            "--cpus",
            "0.25",
            "--pids-limit",
            "32",
            "--user",
            f"{os.getuid()}:{os.getgid()}",
            "--tmpfs",
            f"/tmp:rw,noexec,nosuid,nodev,size=16m,mode=0700,uid={os.getuid()},gid={os.getgid()}",
            "--tmpfs",
            f"/data:rw,noexec,nosuid,nodev,size=16m,mode=0700,uid={os.getuid()},gid={os.getgid()}",
            "--mount",
            f"type=bind,src={self.root / 'users.acl'},dst=/fixture/users.acl,readonly",
            self.IMAGE,
            "valkey-server",
            "--port",
            "0",
            "--unixsocket",
            "/tmp/valkey.sock",
            "--unixsocketperm",
            "700",
            "--aclfile",
            "/fixture/users.acl",
            "--save",
            "",
            "--appendonly",
            "no",
            "--dir",
            "/tmp",
            "--loglevel",
            "warning",
        )
        self.assertEqual(0, created.returncode, "isolated container creation failed")
        inspected = self.docker("inspect", "--format", "{{json .Mounts}}", self.name)
        self.assertEqual(0, inspected.returncode)
        mounts = json.loads(inspected.stdout)
        self.assertFalse(any(mount["Type"] == "volume" for mount in mounts))
        bindings = [mount for mount in mounts if mount["Type"] == "bind"]
        self.assertEqual(1, len(bindings))
        self.assertEqual(str(self.root / "users.acl"), bindings[0]["Source"])
        self.assertFalse(bindings[0]["RW"])
        self.assertEqual(0, self.docker("start", self.name).returncode)
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            if self.query("PING").stdout.strip() == "PONG":
                return
            time.sleep(0.2)
        self.fail("isolated Valkey ACL did not become ready")

    def query(self, *command, user="n8n", password="synthetic-n8n"):
        return self.docker(
            "exec",
            "--env",
            "REDISCLI_AUTH",
            self.name,
            "valkey-cli",
            "--user",
            user,
            "--raw",
            "-s",
            "/tmp/valkey.sock",
            *command,
            password=password,
        )

    def remove_owned_container(self):
        inspected = self.docker(
            "inspect",
            "--format",
            '{{index .Config.Labels "hyhome.n8n-acl"}}',
            self.name,
        )
        if inspected.returncode != 0:
            self.assertIn("no such", inspected.stderr.lower())
            return
        self.assertEqual(
            self.name, inspected.stdout.strip(), "container ownership mismatch"
        )
        self.assertEqual(0, self.docker("rm", "--force", self.name).returncode)
        absent = self.docker("inspect", self.name)
        self.assertNotEqual(0, absent.returncode)
        self.assertIn("no such", absent.stderr.lower())

    def test_named_queue_acl_allows_its_namespace_and_refuses_other_authority(self):
        for command, expected in (
            (("PING",), "PONG"),
            (("SELECT", "0"), "OK"),
            (("SET", "n8n:jobs:test", "synthetic-job"), "OK"),
            (("GET", "n8n:jobs:test"), "synthetic-job"),
            (("HMSET", "n8n:jobs:hash", "field", "synthetic"), "OK"),
            (
                ("EVAL", "return redis.call('GET', KEYS[1])", "1", "n8n:jobs:test"),
                "synthetic-job",
            ),
            (("PUBLISH", "n8n:n8n.commands", "synthetic"), "0"),
        ):
            with self.subTest(command=command[0]):
                result = self.query(*command)
                self.assertEqual(0, result.returncode)
                self.assertEqual(expected, result.stdout.strip())
        for command in (
            ("GET", "other:secret"),
            ("SET", "other:key", "synthetic"),
            ("SELECT", "1"),
            ("PUBLISH", "other:channel", "synthetic"),
            ("FLUSHDB",),
            ("FLUSHALL",),
            ("ACL", "LIST"),
            ("CONFIG", "GET", "*"),
            ("KEYS", "*"),
            ("SCAN", "0"),
            ("EVAL", "return redis.call('GET', 'other:secret')", "0"),
            ("EVAL", "return redis.call('FLUSHDB')", "0"),
        ):
            with self.subTest(denied=command[0]):
                result = self.query(*command)
                self.assertTrue(
                    any(message in result.stdout for message in ("NOPERM", "ACL")),
                    "expected command/key/database/channel denial",
                )
        wrong = self.query("PING", password="synthetic-wrong")
        self.assertIn("WRONGPASS", wrong.stdout + wrong.stderr)


if __name__ == "__main__":
    unittest.main()
