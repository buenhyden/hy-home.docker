"""Synthetic, source-only checks for mng-valkey ACL generation."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import uuid
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "infra/04-data/mng-db/valkey/scripts/render-acl.sh"
)

BULL_CLIENT_PATH = Path(__file__).with_name("_mng_valkey_bull_client.cjs")
BULL_CLIENT_SCRIPT = BULL_CLIENT_PATH.read_text(encoding="utf-8")


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

    def test_cleanup_absence_refuses_daemon_errors(self):
        fixture = MngValkeyAclNativeTests()
        for message in ("No such container: owned", "network owned not found"):
            fixture.assert_absent(subprocess.CompletedProcess([], 1, "", message))
        for code, message in (
            (0, ""),
            (1, "permission denied"),
            (1, "Cannot connect to the Docker daemon"),
        ):
            with (
                self.subTest(code=code, message=message),
                self.assertRaises(AssertionError),
            ):
                fixture.assert_absent(
                    subprocess.CompletedProcess([], code, "", message)
                )

    def test_default_bull_method_skips_before_any_fixture_or_docker_call(self):
        probe = """
import unittest
from unittest import mock
from tests.validation.test_mng_valkey_acl import MngValkeyAclNativeTests
with mock.patch.object(MngValkeyAclNativeTests, 'setUp', side_effect=AssertionError('fixture entered')):
    result = unittest.TestResult()
    MngValkeyAclNativeTests('test_pinned_bull_jobs_retry_delay_and_locks').run(result)
assert len(result.skipped) == 1 and not result.errors and not result.failures
"""
        result = subprocess.run(
            [sys.executable, "-c", probe],
            cwd=Path(__file__).resolve().parents[2],
            env={"PATH": os.environ["PATH"]},
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_bull_identity_guard_rejects_version_path_patch_and_uid_mismatches(self):
        client = self.root / "bull-client.cjs"
        client.write_text(BULL_CLIENT_SCRIPT)
        probe = """
const assert = require('node:assert/strict');
const {identityValid} = require(process.argv[1]);
const good = {uid:1000, gid:1000, n8n:{version:'2.43.6'}, bull:{version:'4.16.4',entry:'/bull',expectedEntry:'/bull',jobGit:'3301e3fbc7296f545b65331dad1f12c820267e0d'}, ioredis:{version:'5.3.2',entry:'/ioredis',expectedEntry:'/ioredis'}};
assert.equal(identityValid(good), true);
for (const bad of [{...good,uid:0},{...good,bull:{...good.bull,version:'4.16.3'}},{...good,bull:{...good.bull,entry:'/other'}},{...good,bull:{...good.bull,jobGit:'unpatched'}},{...good,ioredis:{...good.ioredis,version:'5.4.0'}},{...good,n8n:{version:'other'}},{}]) assert.equal(identityValid(bad),false);
"""
        result = subprocess.run(
            [shutil.which("node") or "node", "-e", probe, str(client)],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        self.assertEqual(0, result.returncode, result.stderr)

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
    CLIENT_IMAGE = (
        "sha256:222a7fd94f471b0b464f873e001a2ec00fc589158066209f0ee8028e43e11131"
    )
    CONTAINER_FLAGS = tuple(
        "--pull never --read-only --cap-drop ALL --security-opt no-new-privileges".split()
    )

    def docker(self, *arguments, password=None, limit=20):
        environment = self.environment | (
            {"REDISCLI_AUTH": password} if password is not None else {}
        )
        remaining = self.deadline - time.monotonic()
        cleanup = arguments[0] in ("inspect", "rm") or arguments[:2] in (
            ("network", "inspect"),
            ("network", "rm"),
            ("volume", "inspect"),
        )
        if not cleanup and remaining <= 0:
            self.fail("isolated ACL rehearsal exceeded its 180 second budget")
        command = [
            "docker",
            "--config",
            self.environment["DOCKER_CONFIG"],
            "--context",
            "default",
            *arguments,
        ]
        try:
            result = subprocess.run(
                command,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
                timeout=20 if cleanup else min(limit, remaining),
            )
        except subprocess.TimeoutExpired as error:
            self.record_docker(
                command, None, error.stdout, error.stderr, timed_out=True
            )
            raise
        self.record_docker(command, result.returncode, result.stdout, result.stderr)
        return result

    def record_docker(self, command, exit_code, stdout, stderr, timed_out=False):
        if self.evidence is None:
            return
        self.retain(
            f"docker-{self.sequence:03d}.json",
            {
                "argv": command,
                "exit_code": exit_code,
                "timed_out": timed_out,
                "stdout": stdout.decode(errors="replace")
                if isinstance(stdout, bytes)
                else stdout,
                "stderr": stderr.decode(errors="replace")
                if isinstance(stderr, bytes)
                else stderr,
            },
        )
        self.sequence += 1

    def retain(self, name, value):
        descriptor = os.open(
            self.evidence / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
        with os.fdopen(descriptor, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")

    def setUp(self):
        fixture = MngValkeyAclTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root = fixture.root
        self.evidence = None
        self.sequence = 0
        self.cids = {}
        (self.root / "docker").mkdir(mode=0o700)
        self.environment = {
            "PATH": os.environ["PATH"],
            "DOCKER_CONFIG": str(self.root / "docker"),
        }
        self.deadline = time.monotonic() + 180
        secret = self.root / "n8n"
        secret.write_text("synthetic-n8n\n")
        secret.chmod(0o600)
        self.assertEqual(0, fixture.render(MNG_VALKEY_N8N_ENABLED="1").returncode)
        self.name = "hyhome-n8n-acl-" + uuid.uuid4().hex

    def cached_image(self, image):
        inspected = self.docker(
            "image",
            "inspect",
            image,
            "--format",
            '{"Id":{{json .Id}},"Volumes":{{json .Config.Volumes}}}',
        )
        self.assertEqual(
            0, inspected.returncode, "required exact cached fixture image unavailable"
        )
        self.assertEqual({"Id": image, "Volumes": None}, json.loads(inspected.stdout))

    def start_broker(self, network="none", port="0"):
        self.cached_image(self.IMAGE)
        self.addCleanup(self.remove_owned_container)
        created = self.docker(
            "create",
            "--name",
            self.name,
            "--label",
            "hyhome.n8n-acl=" + self.name,
            *self.CONTAINER_FLAGS,
            "--network",
            network,
            *(("--network-alias", "broker") if network != "none" else ()),
            *"--memory 64m --memory-swap 64m --cpus 0.25 --pids-limit 32".split(),
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
            port,
            *"--unixsocket /tmp/valkey.sock --unixsocketperm 700 --aclfile /fixture/users.acl".split(),
            "--save",
            "",
            *"--appendonly no --dir /tmp --loglevel warning".split(),
        )
        self.assertEqual(0, created.returncode, "isolated container creation failed")
        self.cids = self.cids | {self.name: created.stdout.strip()}
        self.verify_container(
            self.name,
            self.IMAGE,
            64,
            0.25,
            32,
            network,
            {"/fixture/users.acl": str(self.root / "users.acl")},
        )
        self.assertEqual(0, self.docker("start", self.cids[self.name]).returncode)
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
            self.cids[self.name],
            "valkey-cli",
            "--user",
            user,
            "--raw",
            "-s",
            "/tmp/valkey.sock",
            *command,
            password=password,
        )

    def verify_container(self, name, image, memory, cpus, pids, network, bindings):
        inspected = self.docker(
            "inspect",
            "--format",
            '{"Id":{{json .Id}},"Image":{{json .Image}},"User":{{json .Config.User}},"owner":{{json (index .Config.Labels "hyhome.n8n-acl")}},"Host":{{json .HostConfig}},"Mounts":{{json .Mounts}}}',
            self.cids[name],
        )
        self.assertEqual(0, inspected.returncode)
        state = json.loads(inspected.stdout)
        self.assertEqual(
            (self.cids[name], image, self.name),
            (state["Id"], state["Image"], state["owner"]),
        )
        self.assertEqual(f"{os.getuid()}:{os.getgid()}", state["User"])
        host = state["Host"]
        for key, expected in {
            "ReadonlyRootfs": True,
            "Privileged": False,
            "Memory": memory * 1024 * 1024,
            "MemorySwap": memory * 1024 * 1024,
            "NanoCpus": int(cpus * 1e9),
            "PidsLimit": pids,
            "NetworkMode": network,
        }.items():
            self.assertEqual(expected, host[key], key)
        self.assertEqual(["ALL"], host["CapDrop"])
        self.assertTrue(
            any(
                value in ("no-new-privileges", "no-new-privileges:true")
                for value in host["SecurityOpt"]
            )
        )
        self.assertFalse(host["PortBindings"])
        self.verify_fixture_mounts(image, host, state["Mounts"], bindings)

    def verify_fixture_mounts(self, image, host, mounts, bindings):
        expected_tmpfs = (
            {"/tmp": 16, "/data": 16}
            if image == self.IMAGE
            else {"/tmp": 32, "/run": 16}
        )
        self.assertEqual(set(expected_tmpfs), set(host["Tmpfs"]))
        for destination, size in expected_tmpfs.items():
            self.assertEqual(
                {
                    "rw",
                    "noexec",
                    "nosuid",
                    "nodev",
                    f"size={size}m",
                    "mode=0700",
                    f"uid={os.getuid()}",
                    f"gid={os.getgid()}",
                },
                set(host["Tmpfs"][destination].split(",")),
            )
        self.assertFalse(any(mount["Type"] == "volume" for mount in mounts))
        actual = {
            mount["Destination"]: mount["Source"]
            for mount in mounts
            if mount["Type"] == "bind" and not mount["RW"]
        }
        self.assertEqual(bindings, actual)
        self.assertEqual(
            len(bindings), sum(mount["Type"] == "bind" for mount in mounts)
        )

    def network_state(self, absent_ok=False):
        result = self.docker(
            "network",
            "inspect",
            "--format",
            '{"Id":{{json .Id}},"Internal":{{json .Internal}},"owner":{{json (index .Labels "hyhome.n8n-acl")}},"Containers":{{json .Containers}}}',
            self.network_id or self.network_name,
        )
        if result.returncode and absent_ok:
            self.assertTrue(
                any(
                    value in result.stderr.lower() for value in ("no such", "not found")
                )
            )
            return None
        self.assertEqual(0, result.returncode, result.stderr)
        state = json.loads(result.stdout)
        self.assertEqual(self.name, state["owner"])
        self.assertTrue(state["Internal"])
        if self.network_id:
            self.assertEqual(self.network_id, state["Id"])
        return state

    def remove_owned_network(self):
        state = self.network_state(absent_ok=True)
        if state is None:
            return
        self.assertFalse(state["Containers"], "owned network still has peers")
        self.assertEqual(0, self.docker("network", "rm", state["Id"]).returncode)
        self.assert_absent(self.docker("network", "inspect", state["Id"]))

    def acl_log(self, reset=False):
        result = self.docker(
            "exec",
            "--env",
            "REDISCLI_AUTH",
            self.cids[self.name],
            "valkey-cli",
            "--user",
            "default",
            "--json",
            "-s",
            "/tmp/valkey.sock",
            "ACL",
            "LOG",
            *(("RESET",) if reset else ()),
            password="synthetic-default",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        if reset:
            return []
        rows = json.loads(result.stdout)
        return [
            {"reason": row["reason"], "count": row["count"]}
            for row in (
                record
                if isinstance(record, dict)
                else dict(zip(record[::2], record[1::2], strict=True))
                for record in rows
            )
        ]

    def prepare_bull_inputs(self):
        self.evidence = Path(tempfile.mkdtemp(prefix="hyhome-n8n-bull-evidence-"))
        print(f"U1_BULL_EVIDENCE={self.evidence}", flush=True)
        client = self.root / "bull-client.cjs"
        client.write_text(BULL_CLIENT_SCRIPT)
        inputs = self.root / "input.json"
        inputs.write_text(
            json.dumps(
                {
                    "host": "broker",
                    "port": 6379,
                    "db": 0,
                    "username": "n8n",
                    "password": "synthetic-n8n",
                }
            )
        )
        inputs.chmod(0o600)
        self.retain(
            "inputs.json",
            {
                "client_sha256": hashlib.sha256(client.read_bytes()).hexdigest(),
                "client_source_sha256": hashlib.sha256(
                    BULL_CLIENT_PATH.read_bytes()
                ).hexdigest(),
                "input_sha256": hashlib.sha256(inputs.read_bytes()).hexdigest(),
                "acl_sha256": hashlib.sha256(
                    (self.root / "users.acl").read_bytes()
                ).hexdigest(),
                "renderer_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
                "test_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "images": [self.IMAGE, self.CLIENT_IMAGE],
            },
        )
        return client, inputs

    def test_pinned_bull_jobs_retry_delay_and_locks(self):
        self.assertEqual(
            (1000, 1000),
            (os.getuid(), os.getgid()),
            "synthetic fixture requires UID/GID 1000",
        )
        client, inputs = self.prepare_bull_inputs()
        self.cached_image(self.CLIENT_IMAGE)
        self.cached_image(self.IMAGE)
        self.network_name = self.name + "-net"
        self.network_id = None
        self.addCleanup(self.remove_owned_network)
        created = self.docker(
            "network",
            "create",
            "--internal",
            "--driver",
            "bridge",
            "--label",
            "hyhome.n8n-acl=" + self.name,
            self.network_name,
        )
        self.assertEqual(0, created.returncode, created.stderr)
        self.network_id = created.stdout.strip()
        self.network_state()
        self.start_broker(self.network_name, "6379")
        cid = self.start_client(client, inputs)
        self.await_client_identity(cid)
        self.execute_bull_phases(cid)

    def start_client(self, client, inputs):
        client_name = self.name + "-client"
        self.addCleanup(self.remove_owned_container, client_name, self.CLIENT_IMAGE)
        created = self.docker(
            "create",
            "--name",
            client_name,
            "--label",
            "hyhome.n8n-acl=" + self.name,
            *self.CONTAINER_FLAGS,
            "--network",
            self.network_name,
            *"--memory 256m --memory-swap 256m --cpus 0.5 --pids-limit 64".split(),
            "--user",
            f"{os.getuid()}:{os.getgid()}",
            "--tmpfs",
            f"/tmp:rw,noexec,nosuid,nodev,size=32m,mode=0700,uid={os.getuid()},gid={os.getgid()}",
            "--tmpfs",
            f"/run:rw,noexec,nosuid,nodev,size=16m,mode=0700,uid={os.getuid()},gid={os.getgid()}",
            "--mount",
            f"type=bind,src={client},dst=/fixture/bull-client.cjs,readonly",
            "--mount",
            f"type=bind,src={inputs},dst=/fixture/input.json,readonly",
            "--entrypoint",
            "/usr/local/bin/node",
            self.CLIENT_IMAGE,
            "--max-old-space-size=128",
            "/fixture/bull-client.cjs",
            "hold",
        )
        self.assertEqual(0, created.returncode, created.stderr)
        self.cids = self.cids | {client_name: created.stdout.strip()}
        cid = self.cids[client_name]
        self.verify_container(
            client_name,
            self.CLIENT_IMAGE,
            256,
            0.5,
            64,
            self.network_name,
            {
                "/fixture/bull-client.cjs": str(client),
                "/fixture/input.json": str(inputs),
            },
        )
        self.assertEqual(0, self.docker("start", cid).returncode)
        return cid

    def await_client_identity(self, cid):
        until = time.monotonic() + 10
        while time.monotonic() < until:
            logs = self.docker("logs", cid)
            events = [json.loads(line) for line in logs.stdout.splitlines()]
            if any(event.get("kind") == "blocked" for event in events):
                self.fail(
                    "BLOCKED_CLIENT_VERSION_OR_LAYOUT; probe retained in evidence"
                )
            if any(event.get("kind") == "ready" for event in events):
                break
            time.sleep(0.2)
        else:
            self.fail("synthetic client identity preflight did not become ready")
        self.assertEqual(
            set(self.cids.values()), set(self.network_state()["Containers"])
        )

    def execute_bull_phases(self, cid):
        self.acl_log(reset=True)
        for mode, count in (("positive", 5), ("negative", 10)):
            result = self.docker(
                "exec",
                cid,
                "/usr/local/bin/node",
                "--max-old-space-size=128",
                "/fixture/bull-client.cjs",
                mode,
                limit=60,
            )
            self.assertEqual(
                0,
                result.returncode,
                f"real Bull {mode} phase failed; raw receipt retained",
            )
            events = [json.loads(line) for line in result.stdout.splitlines()]
            completed = [event for event in events if event.get("kind") == "complete"]
            self.assertEqual(1, len(completed))
            self.assertEqual(count, len(completed[0]["cases"]))
            denials = self.acl_log()
            self.retain(mode + "-acl-counts.json", denials)
            if mode == "positive":
                self.assertEqual([], denials, "unexpected positive-phase ACL denial")
            else:
                self.assertTrue(
                    {"key", "channel", "command", "auth"}.issubset(
                        {row["reason"] for row in denials}
                    )
                )

    def remove_owned_container(self, name=None, image=None):
        name = name or self.name
        image = image or self.IMAGE
        inspected = self.docker(
            "inspect",
            "--format",
            '{"Id":{{json .Id}},"Image":{{json .Image}},"owner":{{json (index .Config.Labels "hyhome.n8n-acl")}},"Mounts":{{json .Mounts}}}',
            name,
        )
        if inspected.returncode != 0:
            self.assertIn("no such", inspected.stderr.lower())
            return
        found = json.loads(inspected.stdout)
        self.assertEqual(
            (self.name, image),
            (found["owner"], found["Image"]),
            "container ownership mismatch",
        )
        if name in self.cids:
            self.assertEqual(self.cids[name], found["Id"])
        volumes = [
            mount["Name"] for mount in found["Mounts"] if mount["Type"] == "volume"
        ]
        self.assertEqual(
            0, self.docker("rm", "--force", "--volumes", found["Id"]).returncode
        )
        self.assert_absent(self.docker("inspect", found["Id"]))
        for volume in volumes:
            self.assert_absent(self.docker("volume", "inspect", volume))

    def assert_absent(self, result):
        self.assertNotEqual(0, result.returncode)
        self.assertTrue(
            any(value in result.stderr.lower() for value in ("no such", "not found")),
            "absence requires an explicit daemon not-found response",
        )

    def test_named_queue_acl_allows_its_namespace_and_refuses_other_authority(self):
        self.start_broker()
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
