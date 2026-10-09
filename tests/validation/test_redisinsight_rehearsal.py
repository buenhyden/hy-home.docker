"""Opt-in isolated rehearsal of RedisInsight against DEV and MNG Valkey.

Runs the pinned images with the repository's ACL renderers and RedisInsight
entrypoint on internal Docker networks, synthetic secrets and synthetic keys.
Everything it creates is named ``ri-rehearsal-*`` and removed by that name.
Enable with HYHOME_REDISINSIGHT_REHEARSAL=1.
"""

from __future__ import annotations

import json
import os
import secrets
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALKEY = "valkey/valkey:9.1.2-alpine"
INSIGHT = "redis/redisinsight:3.8.0"
PREFIX = "ri-rehearsal"
INGRESS_SUBNET = "172.31.251.0/24"
INGRESS_IP = "172.31.251.3"
API = f"http://{INGRESS_IP}:5540/api"

PROBE = r"""
const [method, path, body] = process.argv.slice(1);
(async () => {
  try {
    const r = await fetch(process.env.API + path, { method,
      headers: { "Content-Type": "application/json" }, body: body || undefined });
    console.log(JSON.stringify([r.status, (await r.text()).slice(0, 2000)]));
  } catch (e) { console.log(JSON.stringify([0, String(e.cause && e.cause.code || e)])); }
})();
"""


def docker(*args: str, check: bool = True, input_: str | None = None) -> str:
    result = subprocess.run(
        ["docker", *args],
        capture_output=True,
        text=True,
        check=False,
        input=input_,
        timeout=180,
    )
    if check and result.returncode != 0:
        raise AssertionError(f"docker {args[0]} failed: {result.stderr[-400:]}")
    return result.stdout


@unittest.skipUnless(
    os.environ.get("HYHOME_REDISINSIGHT_REHEARSAL") == "1",
    "set HYHOME_REDISINSIGHT_REHEARSAL=1 to run the isolated RedisInsight rehearsal",
)
class RedisInsightRehearsalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scratch = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.scratch.name)
        cls.dir.chmod(0o755)
        cls.secret = {}
        for name in (
            "dev_admin",
            "dev_monitor",
            "dev_inspector",
            "mng_default",
            "mng_inspector",
            "ri_key",
        ):
            cls.write_secret(name, secrets.token_urlsafe(24))
        (cls.dir / "projects.tsv").write_text("# none\n", encoding="utf-8")
        (cls.dir / "project-secrets").mkdir()
        cls.cleanup()
        try:
            cls.start()
        except BaseException:
            cls.cleanup()
            cls.scratch.cleanup()
            raise

    @classmethod
    def tearDownClass(cls) -> None:
        cls.cleanup()
        cls.scratch.cleanup()

    @classmethod
    def write_secret(cls, name: str, value: str) -> None:
        cls.secret[name] = value
        path = cls.dir / name
        path.write_text(value + "\n", encoding="utf-8")
        path.chmod(0o644)

    @classmethod
    def cleanup(cls) -> None:
        for name in ("insight", "dev", "mng", "peer", "mngpeer"):
            docker("rm", "-f", f"{PREFIX}-{name}", check=False)
        for net in ("ingress", "dev", "mng"):
            docker("network", "rm", f"{PREFIX}-{net}", check=False)

    @classmethod
    def start(cls) -> None:
        docker(
            "network",
            "create",
            "--internal",
            "--subnet",
            INGRESS_SUBNET,
            "--ip-range",
            "172.31.251.128/25",
            "-o",
            "com.docker.network.bridge.gateway_mode_ipv4=isolated",
            f"{PREFIX}-ingress",
        )
        docker("network", "create", "--internal", f"{PREFIX}-dev")
        docker("network", "create", "--internal", f"{PREFIX}-mng")
        cls.start_dev()
        cls.start_mng()
        cls.start_insight()
        for peer, net in (("peer", "dev"), ("mngpeer", "mng")):
            docker(
                "run", "-d", "--name", f"{PREFIX}-{peer}", "--network", f"{PREFIX}-{net}",
                "--entrypoint", "sleep", VALKEY, "600",
            )  # fmt: skip
        cls.seed()

    @classmethod
    def start_dev(cls) -> None:
        dev = ROOT / "infra/04-data/dev-db/valkey"
        docker(
            "run", "-d", "--name", f"{PREFIX}-dev", "--network", f"{PREFIX}-dev",
            "--network-alias", "dev-valkey", "--user", "999:999",
            "--tmpfs", "/run/valkey:uid=999,gid=999,mode=0700",
            "-v", f"{dev}/config/valkey.conf:/etc/dev-valkey/valkey.conf:ro",
            "-v", f"{dev}/scripts:/usr/local/libexec/dev-valkey:ro",
            "-v", f"{cls.dir}/projects.tsv:/etc/dev-valkey/projects.tsv:ro",
            "-v", f"{cls.dir}/project-secrets:/run/valkey-project-secrets:ro",
            "-v", f"{cls.dir}/dev_admin:/run/secrets/dev_valkey_admin_password:ro",
            "-v", f"{cls.dir}/dev_monitor:/run/secrets/dev_valkey_monitor_password:ro",
            "-v", f"{cls.dir}/dev_inspector:/run/secrets/dev_valkey_inspector_password:ro",
            "--entrypoint", "/bin/sh", VALKEY, "/usr/local/libexec/dev-valkey/start.sh",
        )  # fmt: skip

    @classmethod
    def start_mng(cls) -> None:
        mng = ROOT / "infra/04-data/mng-db/valkey/scripts"
        docker(
            "run", "-d", "--name", f"{PREFIX}-mng", "--network", f"{PREFIX}-mng",
            "--network-alias", "mng-valkey", "--user", "999:999",
            "--tmpfs", "/run/valkey:uid=999,gid=999,mode=0700",
            "-v", f"{mng}:/usr/local/libexec/mng-valkey:ro",
            "-v", f"{cls.dir}/mng_default:/run/secrets/mng_valkey_password:ro",
            "-v", f"{cls.dir}/mng_inspector:/run/secrets/mng_valkey_inspector_password:ro",
            "--entrypoint", "/bin/sh", VALKEY, "/usr/local/libexec/mng-valkey/start.sh",
        )  # fmt: skip

    @classmethod
    def start_insight(cls) -> None:
        scripts = ROOT / "infra/04-data/redisinsight/scripts"
        docker(
            "create", "--name", f"{PREFIX}-insight", "--network", f"{PREFIX}-ingress",
            "--ip", INGRESS_IP, "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges:true",
            "-e", f"RI_APP_HOST={INGRESS_IP}", "-e", "RI_APP_PORT=5540",
            "-e", "RI_ACCEPT_TERMS_AND_CONDITIONS=true",
            "-e", "RI_REDIS_HOST1=dev-valkey", "-e", "RI_REDIS_PORT1=6379",
            "-e", "RI_REDIS_DB1=0", "-e", "RI_REDIS_ALIAS1=DEV / dev-valkey",
            "-e", "RI_REDIS_USERNAME1=devinspector",
            "-e", "RI_REDIS_HOST2=mng-valkey", "-e", "RI_REDIS_PORT2=6379",
            "-e", "RI_REDIS_DB2=0", "-e", "RI_REDIS_ALIAS2=MNG / mng-valkey",
            "-e", "RI_REDIS_USERNAME2=mnginspector",
            "-v", f"{scripts}:/usr/local/libexec/redisinsight:ro",
            "-v", f"{cls.dir}/dev_inspector:/run/secrets/dev_valkey_inspector_password:ro",
            "-v", f"{cls.dir}/mng_inspector:/run/secrets/mng_valkey_inspector_password:ro",
            "-v", f"{cls.dir}/ri_key:/run/secrets/redisinsight_encryption_key:ro",
            "--entrypoint", "/bin/sh", INSIGHT, "/usr/local/libexec/redisinsight/start.sh",
        )  # fmt: skip
        docker("network", "connect", f"{PREFIX}-dev", f"{PREFIX}-insight")
        docker("network", "connect", f"{PREFIX}-mng", f"{PREFIX}-insight")
        docker("start", f"{PREFIX}-insight")
        cls.wait_insight()

    @classmethod
    def wait_insight(cls) -> None:
        for _ in range(60):
            out = docker(
                "exec",
                f"{PREFIX}-insight",
                "wget",
                "-qO-",
                f"{API}/health/",
                check=False,
            )
            if '"status":"up"' in out:
                break
            time.sleep(2)
        else:
            raise AssertionError("RedisInsight did not report healthy")
        # UI health is not database readiness. On these internet-less networks
        # each first database request after start can exceed the 25 s request
        # timeout while start-up lookups fail, so wait for both connections.
        for database in ("1", "2"):
            for _ in range(8):
                if cls.api("GET", f"/databases/{database}/info")[0] == 200:
                    break
                time.sleep(3)
            else:
                raise AssertionError(f"database {database} never connected")

    @classmethod
    def api(cls, method: str, path: str, body: object = None) -> tuple[int, str]:
        out = docker(
            "exec", "-e", f"API={API}", f"{PREFIX}-insight", "node", "-e", PROBE,
            method, path, json.dumps(body) if body is not None else "",
        )  # fmt: skip
        status, text = json.loads(out.strip().splitlines()[-1])
        return int(status), text

    @classmethod
    def cli(cls, container: str, user: str, password: str, *command: str) -> str:
        return docker(
            "exec", "-i", f"{PREFIX}-{container}", "sh", "-c",
            'REDISCLI_AUTH="$(cat)" valkey-cli --user "$0" --no-auth-warning "$@" 2>&1',
            user, *command, input_=password,
        ).strip()  # fmt: skip

    @classmethod
    def seed(cls) -> None:
        cls.cli(
            "dev", "devadmin", cls.secret["dev_admin"], "set", "dev:probe", "dev-value"
        )
        cls.cli(
            "mng", "default", cls.secret["mng_default"], "set", "mng:probe", "mng-value"
        )

    def keys(self, db: str) -> list[str]:
        status, text = self.api(
            "POST", f"/databases/{db}/keys?encoding=utf8",
            {"cursor": "0", "count": 500, "match": "*"},
        )  # fmt: skip
        self.assertEqual(200, status, text)
        return [key["name"] for key in json.loads(text)[0]["keys"]]

    def test_01_ui_health_and_listener_scope(self) -> None:
        status, text = self.api("GET", "/health/")
        self.assertEqual((200, '{"status":"up"}'), (status, text))
        loopback = docker(
            "exec", f"{PREFIX}-insight", "wget", "-qO-", "http://127.0.0.1:5540/api/health/",
            check=False,
        )  # fmt: skip
        self.assertNotIn("up", loopback)
        # Isolated gateway mode: no host address on the bridge, so host
        # processes cannot reach the UI either.
        host = subprocess.run(
            ["curl", "-s", "--max-time", "4", "-o", "/dev/null", "-w", "%{http_code}",
             f"http://{INGRESS_IP}:5540/api/health/"],
            capture_output=True, text=True, check=False, timeout=30,
        )  # fmt: skip
        self.assertEqual("000", host.stdout)

    def test_02_data_network_peer_cannot_bypass_the_gateway(self) -> None:
        for peer, net, store in (
            ("peer", "dev", "dev-valkey"),
            ("mngpeer", "mng", "mng-valkey"),
        ):
            ip = docker(
                "inspect", "-f",
                f'{{{{(index .NetworkSettings.Networks "{PREFIX}-{net}").IPAddress}}}}',
                f"{PREFIX}-insight",
            ).strip()  # fmt: skip
            self.assertRegex(ip, r"^\d+\.\d+\.\d+\.\d+$")

            def probe(host: str, port: int, peer: str = peer) -> str:
                return docker(
                    "exec", f"{PREFIX}-{peer}", "sh", "-c",
                    f"nc -z -w 3 {host} {port} && echo open || echo refused",
                ).strip()  # fmt: skip

            with self.subTest(net=net):
                # Positive control: the same probe reaches the store.
                self.assertEqual("open", probe(store, 6379))
                self.assertEqual("refused", probe(ip, 5540))

    def test_03_presetup_connections_are_distinct_and_named(self) -> None:
        status, text = self.api("GET", "/databases")
        self.assertEqual(200, status, text)
        databases = {row["id"]: row for row in json.loads(text)}
        self.assertEqual(
            {("1", "DEV / dev-valkey", "dev-valkey", 6379, 0),
             ("2", "MNG / mng-valkey", "mng-valkey", 6379, 0)},
            {(r["id"], r["name"], r["host"], r["port"], r["db"]) for r in databases.values()},
        )  # fmt: skip
        self.assertEqual(["dev:probe"], self.keys("1"))
        self.assertEqual(["mng:probe"], self.keys("2"))

    def test_04_inspector_reads_but_cannot_write(self) -> None:
        status, text = self.api(
            "POST",
            "/databases/1/string/get-value?encoding=utf8",
            {"keyName": "dev:probe"},
        )
        self.assertEqual(200, status, text)
        self.assertIn("dev-value", text)
        for db in ("1", "2"):
            status, text = self.api(
                "POST", f"/databases/{db}/string?encoding=utf8",
                {"keyName": "probe:new", "value": "x"},
            )  # fmt: skip
            self.assertEqual(403, status, text)
            self.assertIn("NOPERM", text)

    def test_05_forbidden_commands_are_denied(self) -> None:
        for container, user, secret in (
            ("dev", "devinspector", "dev_inspector"),
            ("mng", "mnginspector", "mng_inspector"),
        ):
            password = self.secret[secret]
            self.assertEqual("PONG", self.cli(container, user, password, "ping"))
            for command in (
                ("flushall",),
                ("flushdb",),
                ("config", "set", "maxmemory", "1"),
                ("config", "get", "maxmemory"),
                ("acl", "setuser", "x", "on"),
                ("keys", "*"),
                ("set", "x", "1"),
                ("del", "x"),
                ("eval", "return 1", "0"),
                ("publish", "c", "m"),
            ):
                with self.subTest(user=user, command=command):
                    self.assertIn(
                        "NOPERM", self.cli(container, user, password, *command)
                    )

    def test_05b_password_only_auth_still_reaches_the_default_user(self) -> None:
        # OAuth2 Proxy, n8n, Airflow, backups and the exporter send a password
        # with no username; MNG must keep answering them as before.
        out = docker(
            "exec", "-i", f"{PREFIX}-mng", "sh", "-c",
            'REDISCLI_AUTH="$(cat)" valkey-cli --no-auth-warning get mng:probe',
            input_=self.secret["mng_default"],
        ).strip()  # fmt: skip
        self.assertEqual("mng-value", out)
        out = docker(
            "exec", "-i", f"{PREFIX}-mng", "sh", "-c",
            'REDISCLI_AUTH="$(cat)" valkey-cli --no-auth-warning ping 2>&1',
            input_=self.secret["mng_inspector"],
        ).strip()  # fmt: skip
        self.assertIn("WRONGPASS", out)

    def test_06_stored_passwords_are_encrypted(self) -> None:
        status, text = self.api("GET", "/settings")
        self.assertEqual(200, status, text)
        self.assertTrue(json.loads(text)["agreements"]["encryption"])
        for name in ("dev_inspector", "mng_inspector", "ri_key"):
            found = docker(
                "exec", f"{PREFIX}-insight", "sh", "-c",
                "grep -rlF -e \"$0\" /data 2>/dev/null | wc -l", self.secret[name],
            ).strip()  # fmt: skip
            self.assertEqual("0", found, name)

    def test_07_dev_outage_is_an_error_and_recovery_reconnects(self) -> None:
        docker("stop", f"{PREFIX}-dev")
        try:
            status, _ = self.api(
                "POST", "/databases/1/keys?encoding=utf8",
                {"cursor": "0", "count": 10, "match": "*"},
            )  # fmt: skip
            self.assertGreaterEqual(status, 400)
            self.assertEqual(["mng:probe"], self.keys("2"))
        finally:
            docker("start", f"{PREFIX}-dev")
        for _ in range(30):
            if (
                self.cli("dev", "devinspector", self.secret["dev_inspector"], "ping")
                == "PONG"
            ):
                break
            time.sleep(1)
        # The volume-less rehearsal store restarts empty; reseed the probe key.
        self.cli(
            "dev", "devadmin", self.secret["dev_admin"], "set", "dev:probe", "dev-value"
        )
        for _ in range(15):
            status, _ = self.api("GET", "/databases/1/info")
            if status == 200:
                break
            time.sleep(2)
        self.assertEqual(["dev:probe"], self.keys("1"))

    def test_08_inspector_credential_rotation(self) -> None:
        old = self.secret["dev_inspector"]
        self.write_secret("dev_inspector", secrets.token_urlsafe(24))
        docker("restart", f"{PREFIX}-dev")
        for _ in range(30):
            if "PONG" in self.cli("dev", "devadmin", self.secret["dev_admin"], "ping"):
                break
            time.sleep(1)
        self.cli(
            "dev", "devadmin", self.secret["dev_admin"], "set", "dev:probe", "dev-value"
        )
        self.assertIn("WRONGPASS", self.cli("dev", "devinspector", old, "ping"))
        docker("restart", f"{PREFIX}-insight")
        self.wait_insight()
        self.assertEqual(["dev:probe"], self.keys("1"))


if __name__ == "__main__":
    unittest.main()
