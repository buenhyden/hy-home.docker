"""Opt-in isolated rehearsal of the DEV and MNG datastore exporters.

Runs the pinned database, exporter and Prometheus images on internal Docker
networks with the repository's monitor-role SQL, ACL renderers, rendered
Compose exporter definitions, Prometheus configuration, start script and
alert rules, using synthetic secrets and keys. Password checks use a separate
client container over the network (scram-sha-256), never a loopback trust
login. Everything it creates is named ``obs-rehearsal-*`` and removed by that
name. Enable with HYHOME_DATASTORE_OBSERVATION_REHEARSAL=1.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PG = "postgres:18.6-alpine"
VALKEY = "valkey/valkey:9.1.2-alpine"
PROMETHEUS = "prom/prometheus:v3.15.0@sha256:efd719c99d83b060d9daefdcf00360461adf279f45ef5391f8d111892118753e"
PREFIX = "obs-rehearsal"
EXPORTERS = (
    ("mng-pg-exporter", "mng", 9187),
    ("mng-valkey-exporter", "mng", 9121),
    ("dev-pg-exporter", "dev", 9187),
    ("dev-valkey-exporter", "dev", 9121),
)
SEEDED_KEY = "rehearsal:customer:4711"
SEEDED_VALUE = "rehearsal-private-value"

ALERT_TESTS = """
rule_files: [alert_rules.local.datastores.yml]
evaluation_interval: 30s
tests:
  - interval: 30s
    input_series:
      - series: 'up{job="dev-pg-exporter",instance="d",db_scope="dev",db_engine="postgresql",expected_state="off"}'
        values: '0x40'
      - series: 'pg_up{job="dev-pg-exporter",instance="d",db_scope="dev",db_engine="postgresql",expected_state="off"}'
        values: '0x40'
      - series: 'up{job="manage-postgres",instance="m",db_scope="mng",db_engine="postgresql",expected_state="on"}'
        values: '1x40'
      - series: 'up{job="mng-valkey-exporter",instance="v",db_scope="mng",db_engine="valkey",expected_state="on"}'
        values: '1x40'
      - series: 'up{job="dev-valkey-exporter",instance="w",db_scope="dev",db_engine="valkey",expected_state="off"}'
        values: '0x40'
    alert_rule_test:
      - {eval_time: 15m, alertname: DevDatastoreExporterDown, exp_alerts: []}
      - {eval_time: 15m, alertname: DevPostgresDown, exp_alerts: []}
      - {eval_time: 15m, alertname: DatastoreScrapeTargetMissing, exp_alerts: []}
  - interval: 30s
    input_series:
      - series: 'up{job="dev-pg-exporter",instance="d",db_scope="dev",db_engine="postgresql",expected_state="on"}'
        values: '0x40'
      - series: 'pg_up{job="dev-pg-exporter",instance="e",db_scope="dev",db_engine="postgresql",expected_state="on"}'
        values: '0x40'
      - series: 'up{job="mng-valkey-exporter",instance="v",db_scope="mng",db_engine="valkey",expected_state="on"}'
        values: '0x40'
      - series: 'redis_up{job="mng-valkey-exporter",instance="r",db_scope="mng",db_engine="valkey",expected_state="on"}'
        values: '0x40'
      - series: 'pg_scrape_collector_success{job="manage-postgres",instance="m",collector="wal",db_scope="mng",db_engine="postgresql",expected_state="on"}'
        values: '0x40'
      - series: 'scrape_duration_seconds{job="manage-postgres",instance="m",db_scope="mng",db_engine="postgresql",expected_state="on"}'
        values: '7x40'
      - series: 'pg_up{job="manage-postgres",instance="p",db_scope="mng",db_engine="postgresql",expected_state="on"}'
        values: '0x40'
      - series: 'pg_exporter_last_scrape_error{job="manage-postgres",instance="p",db_scope="mng",db_engine="postgresql",expected_state="on"}'
        values: '1x40'
      - series: 'redis_up{job="dev-valkey-exporter",instance="dv",db_scope="dev",db_engine="valkey",expected_state="on"}'
        values: '0x40'
      - series: 'redis_rejected_connections_total{job="dev-valkey-exporter",instance="dv",db_scope="dev",db_engine="valkey",expected_state="on"}'
        values: '0+1x40'
      - series: 'up{job="dev-valkey-exporter",instance="dw",db_scope="dev",db_engine="valkey",expected_state="off"}'
        values: '1x200'
    promql_expr_test:
      - expr: sort(count by (alertname, severity) (ALERTS{alertstate="firing"}))
        eval_time: 15m
        exp_samples:
          - {labels: '{alertname="DatastoreCollectorFailed",severity="warning"}', value: 1}
          - {labels: '{alertname="DatastoreScrapeSlow",severity="warning"}', value: 1}
          - {labels: '{alertname="DatastoreScrapeTargetMissing",severity="warning"}', value: 1}
          - {labels: '{alertname="DevDatastoreExporterDown",severity="warning"}', value: 1}
          - {labels: '{alertname="DevPostgresDown",severity="warning"}', value: 1}
          - {labels: '{alertname="DevValkeyDown",severity="warning"}', value: 1}
          - {labels: '{alertname="MngDatastoreExporterDown",severity="critical"}', value: 1}
          - {labels: '{alertname="PostgresDown",severity="critical"}', value: 1}
          - {labels: '{alertname="ValkeyDown",severity="critical"}', value: 1}
          - {labels: '{alertname="ValkeyRejectedConnections",severity="warning"}', value: 1}
      # A MNG outage pages once: the exporter error is folded into PostgresDown.
      - expr: count(ALERTS{alertname="PostgresqlExporterError"})
        eval_time: 15m
        exp_samples: []
      - expr: count(ALERTS{alertname="DevDatastoreUpWhileDeclaredOff",alertstate="firing"})
        eval_time: 90m
        exp_samples: [{labels: '{}', value: 1}]
"""


def docker(*args: str, check: bool = True, input_: str | None = None) -> str:
    result = subprocess.run(
        ["docker", *args],
        capture_output=True,
        text=True,
        check=False,
        input=input_,
        timeout=240,
    )
    if check and result.returncode != 0:
        raise AssertionError(f"docker {args[0]} failed: {result.stderr[-400:]}")
    return result.stdout


def rendered_services() -> dict[str, dict]:
    out = subprocess.run(
        [
            "docker", "compose", "--env-file", str(ROOT / ".env.example"),
            "--profile", "mng", "--profile", "dev-data", "--profile", "obs",
            "config", "--format", "json",
        ],
        cwd=ROOT, capture_output=True, text=True, check=True, timeout=120,
    ).stdout  # fmt: skip
    services = json.loads(out)["services"]
    return {
        name: services[name] for name in [n for n, _, _ in EXPORTERS] + ["prometheus"]
    }


def dev_monitor_sql() -> str:
    provision = ROOT / "infra/04-data/dev-db/pg/provision"
    sys.path.insert(0, str(provision))
    try:
        spec = importlib.util.spec_from_file_location(
            "dev_monitor", provision / "monitor.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(provision))
    return module.sql()


@unittest.skipUnless(
    os.environ.get("HYHOME_DATASTORE_OBSERVATION_REHEARSAL") == "1",
    "set HYHOME_DATASTORE_OBSERVATION_REHEARSAL=1 to run the isolated rehearsal",
)
class DatastoreObservationRehearsalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scratch = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.scratch.name)
        cls.dir.chmod(0o755)
        cls.secret: dict[str, str] = {}
        for name in (
            "mng_postgres_password", "mng_pg_monitor_password",
            "dev_postgres_password", "dev_pg_monitor_password",
            "mng_valkey_password", "mng_valkey_monitor_password",
            "mng_valkey_inspector_password",
            "dev_valkey_admin_password", "dev_valkey_monitor_password",
            "dev_valkey_inspector_password",
        ):  # fmt: skip
            cls.write_secret(name, secrets.token_urlsafe(24))
        for name in (
            "openbao_token",
            "qdrant_read_only_api_key",
            "opensearch_exporter_password",
        ):
            cls.write_secret(name, "synthetic-unused")
        (cls.dir / "projects.tsv").write_text("# none\n", encoding="utf-8")
        (cls.dir / "project-secrets").mkdir()
        cls.services = rendered_services()
        cls.prometheus_tmpfs = next(
            t
            for t in cls.services["prometheus"]["tmpfs"]
            if t.startswith("/etc/prometheus")
        )
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
        names = docker("ps", "-aq", "--filter", f"name=^{PREFIX}-", check=False).split()
        if names:
            docker("rm", "-f", *names, check=False)
        for net in ("mng", "dev", "obs"):
            docker("network", "rm", f"{PREFIX}-{net}", check=False)

    # -- startup -----------------------------------------------------------

    @classmethod
    def start(cls) -> None:
        for net in ("mng", "dev", "obs"):
            docker("network", "create", "--internal", f"{PREFIX}-{net}")
        for scope in ("mng", "dev"):
            docker(
                "run", "-d", "--name", f"{PREFIX}-{scope}-pg",
                "--network", f"{PREFIX}-{scope}", "--network-alias", f"{scope}-pg",
                "-e", "POSTGRES_PASSWORD_FILE=/run/secrets/admin",
                "-v", f"{cls.dir}/{scope}_postgres_password:/run/secrets/admin:ro",
                PG,
            )  # fmt: skip
        cls.start_valkey("mng")
        cls.start_valkey("dev")
        for scope in ("mng", "dev"):
            cls.wait(
                lambda s=scope: (
                    cls.psql_admin(s, "SELECT 1", check=False).strip() == "1"
                )
            )
            cls.psql_admin(scope, "CREATE DATABASE app")
            cls.psql_admin(scope, "CREATE TABLE private (v text)", db="app")
        cls.provision("mng")
        cls.provision("dev")
        for scope in ("mng", "dev"):
            cls.valkey_admin(scope, "SET", SEEDED_KEY, SEEDED_VALUE)
        for name, _, _ in EXPORTERS:
            cls.start_exporter(name)
        cls.start_prometheus()
        for name, _, _ in EXPORTERS:
            cls.wait(lambda n=name: "_up 1" in cls.metrics(n))

    @classmethod
    def start_valkey(cls, scope: str) -> None:
        base = ROOT / f"infra/04-data/{scope}-db/valkey"
        mounts = ["-v", f"{base}/scripts:/usr/local/libexec/{scope}-valkey:ro"]
        if scope == "dev":
            mounts += [
                "-v", f"{base}/config/valkey.conf:/etc/dev-valkey/valkey.conf:ro",
                "-v", f"{cls.dir}/projects.tsv:/etc/dev-valkey/projects.tsv:ro",
                "-v", f"{cls.dir}/project-secrets:/run/valkey-project-secrets:ro",
            ]  # fmt: skip
            names = ("dev_valkey_admin_password", "dev_valkey_monitor_password",
                     "dev_valkey_inspector_password")  # fmt: skip
        else:
            names = ("mng_valkey_password", "mng_valkey_monitor_password",
                     "mng_valkey_inspector_password")  # fmt: skip
        for name in names:
            mounts += ["-v", f"{cls.dir}/{name}:/run/secrets/{name}:ro"]
        docker(
            "run", "-d", "--name", f"{PREFIX}-{scope}-valkey",
            "--network", f"{PREFIX}-{scope}", "--network-alias", f"{scope}-valkey",
            "--user", "999:999", "--tmpfs", "/run/valkey:uid=999,gid=999,mode=0700",
            *mounts, "--entrypoint", "/bin/sh", VALKEY,
            f"/usr/local/libexec/{scope}-valkey/start.sh",
        )  # fmt: skip
        cls.wait(lambda: cls.valkey_admin(scope, "PING", check=False).strip() == "PONG")

    @classmethod
    def start_exporter(
        cls, name: str, secret_file: Path | None = None, suffix: str = ""
    ) -> str:
        """Run the exporter exactly as Compose renders it, with a synthetic secret."""
        service = cls.services[name]
        scope = name.split("-")[0]
        secret = service["secrets"][0]["source"]
        source = secret_file or cls.dir / secret
        container = f"{PREFIX}-{name}{suffix}"
        args = [
            "run", "-d", "--name", container, "--network", f"{PREFIX}-{scope}",
            "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges:true",
            "-v", f"{source}:/run/secrets/{secret}:ro",
        ]  # fmt: skip
        for key, value in (service.get("environment") or {}).items():
            args += ["-e", f"{key}={value}"]
        entrypoint = service.get("entrypoint") or []
        if entrypoint:
            args += ["--entrypoint", entrypoint[0]]
        args.append(service["image"])
        args += entrypoint[1:]
        args += [part.replace("$$", "$") for part in service.get("command") or []]
        docker(*args)
        if not suffix:
            docker("network", "connect", "--alias", name, f"{PREFIX}-obs", container)
        return container

    @classmethod
    def start_prometheus(cls) -> None:
        config = ROOT / "infra/06-observability/prometheus"
        mounts = [
            "-v", f"{config}/config/prometheus.dev.yml:/etc/prometheus/prometheus.yml:ro",
            "-v", f"{config}/config/alert_rules:/etc/prometheus/alert_rules:ro",
            "-v", f"{config}/scripts:/usr/local/libexec/prometheus:ro",
        ]  # fmt: skip
        for name in (
            "openbao_token",
            "qdrant_read_only_api_key",
            "opensearch_exporter_password",
        ):
            mounts += ["-v", f"{cls.dir}/{name}:/run/secrets/{name}:ro"]
        docker(
            "run", "-d", "--name", f"{PREFIX}-prometheus",
            "--network", f"{PREFIX}-obs", "--tmpfs", cls.prometheus_tmpfs,
            "-e", "PROMETHEUS_DEV_DATA_EXPECTED=on", *mounts,
            "--entrypoint", "/bin/sh", PROMETHEUS,
            "/usr/local/libexec/prometheus/start.sh",
            "--config.file=/etc/prometheus/prometheus.yml",
            "--storage.tsdb.path=/prometheus",
        )  # fmt: skip

    @classmethod
    def provision(cls, scope: str) -> str:
        if scope == "mng":
            provision = ROOT / "infra/04-data/mng-db/pg/provision"
            return docker(
                "run", "--rm", "--network", f"{PREFIX}-mng",
                "-e", "PGHOST=mng-pg", "-e", "PGPORT=5432", "-e", "PGUSER=postgres",
                "-e", "PGDATABASE=postgres",
                "-e", "PROVISION_ADMIN_PASSWORD_FILE=/run/secrets/mng_postgres_password",
                "-e", "PROVISION_SQL=/provision/monitor.sql",
                "-e", "PROVISION_SECRETS=MNG_PG_MONITOR_PASSWORD="
                "/run/secrets/mng_pg_monitor_password",
                "-v", f"{provision}:/provision:ro",
                "-v", f"{cls.dir}/mng_postgres_password:"
                "/run/secrets/mng_postgres_password:ro",
                "-v", f"{cls.dir}/mng_pg_monitor_password:"
                "/run/secrets/mng_pg_monitor_password:ro",
                "--entrypoint", "/bin/sh", PG, "/provision/run-feature-provision.sh",
            )  # fmt: skip
        return docker(
            "run", "--rm", "-i", "--network", f"{PREFIX}-dev",
            "-e", f"PGPASSWORD={cls.secret['dev_postgres_password']}",
            "-e", f"DEV_MONITOR_PASSWORD={cls.secret['dev_pg_monitor_password']}",
            PG, "psql", "-X", "-q", "-h", "dev-pg", "-U", "postgres", "-d", "postgres",
            input_=dev_monitor_sql(),
        )  # fmt: skip

    # -- helpers -----------------------------------------------------------

    @staticmethod
    def wait(predicate, attempts: int = 60, delay: float = 2.0) -> None:
        for _ in range(attempts):
            if predicate():
                return
            time.sleep(delay)
        raise AssertionError("condition not reached")

    @classmethod
    def psql_admin(
        cls, scope: str, sql: str, db: str = "postgres", check: bool = True
    ) -> str:
        password = cls.secret[f"{scope}_postgres_password"]
        return docker(
            "run", "--rm", "--network", f"{PREFIX}-{scope}",
            "-e", f"PGPASSWORD={password}", PG, "psql", "-X", "-At",
            "-h", f"{scope}-pg", "-U", "postgres", "-d", db, "-c", sql, check=check,
        )  # fmt: skip

    @classmethod
    def psql_result(cls, scope, user, password, sql, db="postgres"):
        """A login from a separate client container over the network."""
        return subprocess.run(
            [
                "docker", "run", "--rm", "--network", f"{PREFIX}-{scope}",
                "-e", f"PGPASSWORD={password}", PG, "psql", "-X", "-At",
                "-h", f"{scope}-pg", "-U", user, "-d", db, "-c", sql,
            ],
            capture_output=True, text=True, check=False, timeout=120,
        )  # fmt: skip

    @classmethod
    def valkey(cls, scope, user, password, *command, check=True) -> str:
        return docker(
            "run", "--rm", "--network", f"{PREFIX}-{scope}",
            "-e", f"REDISCLI_AUTH={password}", VALKEY, "valkey-cli",
            "--no-auth-warning", "-h", f"{scope}-valkey", "--user", user,
            *command, check=check,
        )  # fmt: skip

    @classmethod
    def valkey_admin(cls, scope, *command, check=True) -> str:
        if scope == "mng":
            user, secret = "default", "mng_valkey_password"
        else:
            user, secret = "devadmin", "dev_valkey_admin_password"
        return cls.valkey(scope, user, cls.secret[secret], *command, check=check)

    @classmethod
    def metrics(cls, name: str, container: str | None = None) -> str:
        port = {n: p for n, _, p in EXPORTERS}[name]
        return docker(
            "exec", container or f"{PREFIX}-{name}", "wget", "-qO-",
            f"http://127.0.0.1:{port}/metrics", check=False,
        )  # fmt: skip

    @staticmethod
    def value(text: str, metric: str) -> str | None:
        match = re.search(rf"(?m)^{re.escape(metric)} (\S+)$", text)
        return match.group(1) if match else None

    def scrape_states(self) -> dict[str, tuple[str, str, str, str]]:
        out = docker(
            "exec", f"{PREFIX}-prometheus", "wget", "-qO-",
            "http://127.0.0.1:9090/api/v1/query?query=up%7Bdomain%3D%22datastores%22%7D",
            check=False,
        )  # fmt: skip
        result = json.loads(out or '{"data":{"result":[]}}')["data"]["result"]
        return {
            r["metric"]["job"]: (
                r["metric"].get("db_scope"),
                r["metric"].get("db_engine"),
                r["metric"].get("expected_state"),
                r["value"][1],
            )
            for r in result
            if "db_scope" in r["metric"]
        }

    # -- tests -------------------------------------------------------------

    def test_exporters_read_every_collector_through_the_monitor_roles(self) -> None:
        for name, _, _ in EXPORTERS:
            body = self.metrics(name)
            with self.subTest(exporter=name):
                if "pg" in name:
                    self.assertEqual(self.value(body, "pg_up"), "1")
                    failed = re.findall(
                        r'(?m)^pg_scrape_collector_success\{collector="(\w+)"\} 0$',
                        body,
                    )
                    self.assertEqual(failed, [])
                    self.assertEqual(
                        self.value(body, "pg_exporter_last_scrape_error"), "0"
                    )
                else:
                    self.assertEqual(self.value(body, "redis_up"), "1")
                    self.assertEqual(
                        self.value(body, 'redis_exporter_last_scrape_error{err=""}'),
                        "0",
                    )

    def test_metrics_and_logs_carry_no_secret_key_name_or_value(self) -> None:
        for name, _, _ in EXPORTERS:
            body = self.metrics(name)
            logs = docker("logs", f"{PREFIX}-{name}", check=False)
            with self.subTest(exporter=name):
                for value in self.secret.values():
                    self.assertNotIn(value, body)
                    self.assertNotIn(value, logs)
                self.assertNotIn(SEEDED_KEY, body)
                self.assertNotIn(SEEDED_VALUE, body)

    def test_pg_monitor_roles_authenticate_over_the_network_and_cannot_write(
        self,
    ) -> None:
        for scope in ("mng", "dev"):
            role = f"{scope}_pg_monitor"
            password = self.secret[f"{scope}_pg_monitor_password"]
            with self.subTest(scope=scope):
                ok = self.psql_result(
                    scope,
                    role,
                    password,
                    "SELECT current_setting('default_transaction_read_only')",
                )
                self.assertEqual(ok.stdout.strip(), "on", ok.stderr)
                wrong = self.psql_result(scope, role, password + "x", "SELECT 1")
                self.assertIn("password authentication failed", wrong.stderr)
                ddl = self.psql_result(scope, role, password, "CREATE TABLE t (v int)")
                self.assertIn("read-only transaction", ddl.stderr)
                read = self.psql_result(
                    scope, role, password, "SELECT * FROM private", db="app"
                )
                self.assertIn("permission denied", read.stderr)
                attrs = self.psql_admin(
                    scope,
                    "SELECT rolsuper OR rolcreatedb OR rolcreaterole OR rolreplication"
                    f" OR rolbypassrls, pg_has_role('{role}', 'pg_monitor', 'MEMBER'),"
                    f" rolconnlimit FROM pg_roles WHERE rolname = '{role}'",
                )
                self.assertEqual(attrs.strip(), "f|f|3")

    def test_valkey_monitor_roles_cannot_read_keys_or_config(self) -> None:
        refused = (
            ("GET", SEEDED_KEY),
            ("KEYS", "*"),
            ("SCAN", "0"),
            ("CONFIG", "GET", "*"),
            ("SLOWLOG", "GET"),
            ("SET", "k", "v"),
        )
        for scope in ("mng", "dev"):
            user = f"{scope}monitor"
            password = self.secret[f"{scope}_valkey_monitor_password"]
            with self.subTest(scope=scope):
                # Only the exporter talks to the server between the reset and
                # the read, so the log shows exactly what it is refused.
                self.valkey_admin(scope, "ACL", "LOG", "RESET")
                exporter = f"{scope}-valkey-exporter"
                self.wait(lambda e=exporter: self.metrics(e) != "")
                self.wait(
                    lambda s=scope: "object" in self.valkey_admin(s, "ACL", "LOG")
                )
                log = self.valkey_admin(scope, "ACL", "LOG", "100")
                self.assertEqual(
                    set(re.findall(r"(?m)^object\n(.+)$", log)), {"slowlog|get"}
                )
                info = self.valkey(scope, user, password, "INFO", "server")
                self.assertIn("redis_version", info)
                for command in refused:
                    out = self.valkey(scope, user, password, *command, check=False)
                    self.assertIn("NOPERM", out, command)
                wrong = self.valkey(scope, user, password + "x", "PING", check=False)
                self.assertNotIn("PONG", wrong)

    def test_wrong_password_keeps_the_exporter_up_and_reports_the_database_down(
        self,
    ) -> None:
        wrong = self.dir / "wrong"
        wrong_value = secrets.token_urlsafe(24)
        wrong.write_text(wrong_value + "\n", encoding="utf-8")
        wrong.chmod(0o644)
        for name in ("mng-pg-exporter", "mng-valkey-exporter"):
            metric = "pg_up" if "pg" in name else "redis_up"
            container = self.start_exporter(name, wrong, suffix="-wrongpw")
            try:
                self.wait(
                    lambda c=container, n=name, m=metric: (
                        self.value(self.metrics(n, c), m) == "0"
                    )
                )
                logs = docker("logs", container, check=False)
                self.assertNotIn(wrong_value, logs + self.metrics(name, container))
            finally:
                docker("rm", "-f", container, check=False)

    def test_lost_collector_grant_is_reported_and_restored_by_the_job(self) -> None:
        self.psql_admin(
            "mng",
            "REVOKE EXECUTE ON FUNCTION pg_catalog.pg_ls_waldir() FROM mng_pg_monitor",
        )
        wal = 'pg_scrape_collector_success{collector="wal"}'
        self.wait(lambda: self.value(self.metrics("mng-pg-exporter"), wal) == "0")
        self.assertEqual(self.value(self.metrics("mng-pg-exporter"), "pg_up"), "1")
        self.provision("mng")
        self.wait(lambda: self.value(self.metrics("mng-pg-exporter"), wal) == "1")

    def test_database_stop_and_recovery(self) -> None:
        for engine, metric in (("pg", "pg_up"), ("valkey", "redis_up")):
            exporter = f"dev-{engine}-exporter"
            docker("stop", f"{PREFIX}-dev-{engine}")
            try:
                self.wait(
                    lambda e=exporter, m=metric: self.value(self.metrics(e), m) == "0"
                )
            finally:
                docker("start", f"{PREFIX}-dev-{engine}")
            self.wait(
                lambda e=exporter, m=metric: self.value(self.metrics(e), m) == "1"
            )

    def test_rotation_follows_the_secret_and_refuses_the_old_password(self) -> None:
        old = self.secret["mng_pg_monitor_password"]
        self.write_secret("mng_pg_monitor_password", secrets.token_urlsafe(24))
        self.provision("mng")
        docker("restart", f"{PREFIX}-mng-pg-exporter")
        self.wait(lambda: self.value(self.metrics("mng-pg-exporter"), "pg_up") == "1")
        stale = self.psql_result("mng", "mng_pg_monitor", old, "SELECT 1")
        self.assertIn("password authentication failed", stale.stderr)
        old = self.secret["mng_valkey_monitor_password"]
        self.write_secret("mng_valkey_monitor_password", secrets.token_urlsafe(24))
        docker("restart", f"{PREFIX}-mng-valkey")
        self.wait(
            lambda: self.valkey_admin("mng", "PING", check=False).strip() == "PONG"
        )
        docker("restart", f"{PREFIX}-mng-valkey-exporter")
        self.wait(
            lambda: self.value(self.metrics("mng-valkey-exporter"), "redis_up") == "1"
        )
        self.assertNotIn(
            "PONG", self.valkey("mng", "mngmonitor", old, "PING", check=False)
        )

    def test_non_base64_monitor_secret_is_refused_before_any_change(self) -> None:
        name = "mng_pg_monitor_password"
        good, original = self.secret[name], (self.dir / name).read_bytes()
        bad = "quote'and\\backslash\"" + secrets.token_hex(8)
        self.write_secret(name, bad)
        try:
            with self.assertRaises(AssertionError):
                self.provision("mng")
            refused = self.psql_result("mng", "mng_pg_monitor", bad, "SELECT 1")
            self.assertIn("password authentication failed", refused.stderr)
        finally:
            (self.dir / name).write_bytes(original)
            self.secret[name] = good
        self.assertNotIn(bad, docker("logs", f"{PREFIX}-mng-pg", check=False))

    def test_prometheus_labels_targets_by_scope_engine_and_expected_state(
        self,
    ) -> None:
        self.wait(
            lambda: (
                len(self.scrape_states()) == 4
                and all(v[3] == "1" for v in self.scrape_states().values())
            ),
            attempts=45,
        )
        self.assertEqual(
            {job: value[:3] for job, value in self.scrape_states().items()},
            {
                "manage-postgres": ("mng", "postgresql", "on"),
                "mng-valkey-exporter": ("mng", "valkey", "on"),
                "dev-pg-exporter": ("dev", "postgresql", "on"),
                "dev-valkey-exporter": ("dev", "valkey", "on"),
            },
        )
        docker("stop", f"{PREFIX}-dev-valkey-exporter")
        try:
            self.wait(
                lambda: (
                    self.scrape_states().get("dev-valkey-exporter", "1111")[3] == "0"
                ),
                attempts=45,
            )
        finally:
            docker("start", f"{PREFIX}-dev-valkey-exporter")
        self.wait(
            lambda: self.scrape_states().get("dev-valkey-exporter", "0000")[3] == "1",
            attempts=45,
        )

    def test_promtool_accepts_the_config_and_the_alert_scenarios(self) -> None:
        rules = ROOT / "infra/06-observability/prometheus/config/alert_rules"
        scenarios = self.dir / "alerts.test.yml"
        scenarios.write_text(ALERT_TESTS, encoding="utf-8")
        scenarios.chmod(0o644)
        out = docker(
            "run", "--rm", "--entrypoint", "/bin/promtool",
            "-v", f"{rules}/alert_rules.local.datastores.yml:"
            "/t/alert_rules.local.datastores.yml:ro",
            "-v", f"{scenarios}:/t/alerts.test.yml:ro", "-w", "/t",
            PROMETHEUS, "test", "rules", "alerts.test.yml",
        )  # fmt: skip
        self.assertIn("SUCCESS", out)
        check = docker(
            "exec", f"{PREFIX}-prometheus", "promtool", "check", "config",
            "/etc/prometheus/prometheus.yml",
        )  # fmt: skip
        self.assertIn("SUCCESS", check)


if __name__ == "__main__":
    unittest.main()
