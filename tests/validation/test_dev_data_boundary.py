"""Static cross-file boundary for management and development data consumers."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def compose(relative):
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))["services"]


class DevDataBoundaryTests(unittest.TestCase):
    def test_management_init_does_not_create_new_business_database(self):
        service = compose("infra/04-data/mng-db/docker-compose.yml")["mng-pg-init"]
        sql = (
            ROOT / "infra/04-data/mng-db/pg/init-scripts/init_users_dbs.sql"
        ).read_text(encoding="utf-8")
        self.assertFalse(
            any(key.startswith("SERVICE_POSTGRES_") for key in service["environment"])
        )
        self.assertNotIn("service_postgres_password", service["secrets"])
        self.assertNotIn("service_postgres_db", sql)

    def test_dbt_targets_named_dev_fixture(self):
        # ADR-0062 amendment (2026-11-10): the Debezium CDC path left HOME.
        dbt = compose("labs/dbt/docker-compose.yml")
        # SPEC-0262: dbt is a LAB; the dev-pg endpoint is a required LAB input.
        dev_pg_input = "${LAB_DBT_DB_HOST:?set an approved dev-pg endpoint host}"
        self.assertEqual(dbt["dbt"]["environment"]["DBT_DB_HOST"], dev_pg_input)
        self.assertEqual(dbt["dbt-db-provision"]["environment"]["PGHOST"], dev_pg_input)
        self.assertEqual(dbt["dbt"]["environment"]["DBT_DB_NAME"], "platform_dev")
        profile = (ROOT / "labs/dbt/profiles/profiles.yml").read_text()
        self.assertIn("env_var('DBT_DB_HOST')", profile)
        self.assertIn("env_var('DBT_DB_NAME')", profile)
        self.assertNotIn("mng-pg", profile)
        self.assertNotIn("app_db", profile)

    def test_dev_consumers_do_not_read_management_postgres_variables(self):
        # dev-pg listens on a fixed internal 5432 with admin database postgres;
        # MNG POSTGRES_PORT/POSTGRES_DEFAULT_DB must not steer DEV consumers.
        consumers = 0
        for path in sorted((ROOT / "infra").rglob("docker-compose.yml")):
            text = path.read_text(encoding="utf-8")
            if "dev-pg" not in text:
                continue
            for name, service in (yaml.safe_load(text).get("services") or {}).items():
                env = service.get("environment") or {}
                if not isinstance(env, dict) or not (
                    "dev-pg" in (env.get("PGHOST"), env.get("DBT_DB_HOST"))
                    or str(env.get("DATA_SOURCE_URI", "")).startswith("dev-pg:")
                ):
                    continue
                consumers += 1
                for key, value in env.items():
                    with self.subTest(service=name, key=key):
                        self.assertNotIn("POSTGRES_PORT", str(value))
                        self.assertNotIn("POSTGRES_DEFAULT_DB", str(value))
        # SPEC-0262 moved the two dbt consumers to labs/dbt/docker-compose.yml, checked below.
        self.assertGreaterEqual(consumers, 1)
        for name, service in compose("labs/dbt/docker-compose.yml").items():
            for key, value in (service.get("environment") or {}).items():
                with self.subTest(service=name, key=key):
                    self.assertNotIn("POSTGRES_PORT", str(value))
                    self.assertNotIn("POSTGRES_DEFAULT_DB", str(value))

    def test_dev_exporters_use_monitor_accounts_not_admin(self):
        services = compose("infra/04-data/dev-db/docker-compose.yml")
        pg = services["dev-pg-exporter"]
        valkey = services["dev-valkey-exporter"]
        self.assertEqual(pg["secrets"], ["dev_pg_monitor_password"])
        self.assertEqual(pg["environment"]["DATA_SOURCE_USER"], "dev_pg_monitor")
        self.assertEqual(
            pg["depends_on"]["dev-pg-monitor-provision"]["condition"],
            "service_completed_successfully",
        )
        self.assertEqual(valkey["secrets"], ["dev_valkey_monitor_password"])
        command = "".join(valkey["command"])
        self.assertIn("-redis.user=devmonitor", command)
        self.assertIn("redis://dev-valkey:6379", command)
        self.assertNotIn("VALKEY_PORT", command)
        for flag in VALKEY_EXPORTER_FLAGS:
            self.assertIn(flag, command)
        self.assertNotIn("-redis.password", command)
        start = (ROOT / "infra/06-observability/prometheus/scripts/start.sh").read_text(
            encoding="utf-8"
        )
        for target in ("dev-pg-exporter:9187", "dev-valkey-exporter:9121"):
            with self.subTest(target=target):
                self.assertIn(target, start)

    def test_mng_monitor_job_wiring_and_sql_order(self):
        services = compose("infra/04-data/mng-db/docker-compose.yml")
        job = services["mng-pg-monitor-provision"]
        env = job["environment"]
        self.assertEqual(
            job["entrypoint"], ["/bin/sh", "/provision/run-feature-provision.sh"]
        )
        self.assertEqual(
            set(job["secrets"]), {"mng_postgres_password", "mng_pg_monitor_password"}
        )
        self.assertEqual(
            env["PROVISION_SECRETS"],
            "MNG_PG_MONITOR_PASSWORD=/run/secrets/mng_pg_monitor_password",
        )
        mounts = {m.split(":")[1]: m.split(":")[0] for m in job["volumes"]}
        base = ROOT / "infra/04-data/mng-db"
        self.assertEqual(
            (base / mounts["/provision/run-feature-provision.sh"]).resolve(),
            (base / "pg/provision/run-feature-provision.sh").resolve(),
        )
        sql_path = (base / mounts[env["PROVISION_SQL"]]).resolve()
        self.assertEqual(sql_path, (base / "pg/provision/monitor.sql").resolve())
        self.assertEqual(job["depends_on"]["mng-pg"]["condition"], "service_healthy")
        sql = sql_path.read_text(encoding="utf-8")
        self.assertIn("\\getenv monitor_secret MNG_PG_MONITOR_PASSWORD", sql)
        order = [
            "SET log_statement = 'none';",
            "AS secret_ok",
            "CREATE ROLE mng_pg_monitor NOLOGIN;",
            "'role ownership mismatch'",
            "ALTER ROLE mng_pg_monitor WITH LOGIN",
            "GRANT pg_read_all_stats, pg_read_all_settings TO mng_pg_monitor;",
            "REVOKE pg_monitor FROM mng_pg_monitor",
            "monitor role holds memberships beyond its grants",
        ]
        positions = [sql.index(part) for part in order]
        self.assertEqual(positions, sorted(positions))
        self.assertIn(
            "GRANT EXECUTE ON FUNCTION pg_catalog.pg_ls_waldir() TO mng_pg_monitor;",
            sql,
        )
        self.assertNotIn("GRANT pg_monitor", sql)
        self.assertNotIn("GRANT CONNECT", sql)
        self.assertIn("default_transaction_read_only = on", sql)

    def test_mng_exporters_use_monitor_accounts_not_admin(self):
        services = compose("infra/04-data/mng-db/docker-compose.yml")
        pg = services["mng-pg-exporter"]
        valkey = services["mng-valkey-exporter"]
        self.assertEqual(pg["secrets"], ["mng_pg_monitor_password"])
        self.assertEqual(pg["environment"]["DATA_SOURCE_USER"], "mng_pg_monitor")
        self.assertEqual(
            pg["environment"]["DATA_SOURCE_PASS_FILE"],
            "/run/secrets/mng_pg_monitor_password",
        )
        self.assertNotIn("entrypoint", pg)
        self.assertEqual(
            pg["depends_on"]["mng-pg-monitor-provision"]["condition"],
            "service_completed_successfully",
        )
        self.assertEqual(valkey["secrets"], ["mng_valkey_monitor_password"])
        command = "".join(valkey["command"])
        self.assertIn("-redis.user=mngmonitor", command)
        self.assertNotIn("-redis.password", command)
        for flag in VALKEY_EXPORTER_FLAGS:
            self.assertIn(flag, command)


# The narrowed monitor ACL grants nothing these calls would need.
VALKEY_EXPORTER_FLAGS = (
    "-config-command=-",
    "-set-client-name=false",
    "-exclude-latency-histogram-metrics",
)

DATASTORE_JOBS = (
    ("manage-postgres", "mng", "postgresql"),
    ("mng-valkey-exporter", "mng", "valkey"),
    ("dev-pg-exporter", "dev", "postgresql"),
    ("dev-valkey-exporter", "dev", "valkey"),
)


# Public DEV and MNG selectors from `.env.example`; values are synthetic.
DEV_OVERRIDES = {
    "DEV_PG_ADMIN_USER": "synthetic_dev_admin",
    "DEV_PG_HOST_PORT": "25999",
    "DEV_VALKEY_PROJECTS_FILE": "/synthetic/projects.json",
    "DEV_VALKEY_PROJECT_SECRETS_DIR": "/synthetic/secrets",
}
MNG_OVERRIDES = {
    "POSTGRES_PORT": "15432",
    "POSTGRES_HOST_PORT": "25432",
    "POSTGRES_DEFAULT_USER": "synthetic_mng_admin",
    "POSTGRES_DEFAULT_DB": "synthetic_mng_db",
    "POSTGRES_MNG_HOSTNAME": "synthetic-mng-pg",
    "POSTGRES_EXPORTER_PORT": "19187",
    "VALKEY_PORT": "16379",
    "VALKEY_MNG_HOSTNAME": "synthetic-mng-valkey",
    "VALKEY_MNG_HOST_PORT": "26999",
    "VALKEY_EXPORTER_PORT": "19121",
}


class DevMngRenderIsolationTests(unittest.TestCase):
    """Changing one side's variables must leave the other side's render intact."""

    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.base = cls.render({})

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    @classmethod
    def render(cls, overrides):
        home = Path(cls.directory.name)
        env_file = home / "public.env"
        env_file.write_bytes(
            (ROOT / ".env.example").read_bytes()
            + b"\n"
            + "".join(f"{k}={v}\n" for k, v in sorted(overrides.items())).encode()
        )
        result = subprocess.run(
            [
                "docker",
                "compose",
                "--project-directory",
                str(ROOT),
                "--env-file",
                str(env_file),
                "-f",
                str(ROOT / "docker-compose.yml"),
                "--profile",
                "*",
                "config",
                "--format",
                "json",
            ],
            cwd=ROOT,
            # One fixed HOME keeps $HOME-relative binds identical across renders.
            env={
                "COMPOSE_DISABLE_ENV_FILE": "1",
                "DOCKER_CONFIG": str(home / "docker-config"),
                "DOCKER_HOST": f"unix://{home}/no-daemon.sock",
                "HOME": str(home),
                "PATH": os.environ["PATH"],
            },
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        if result.returncode:
            raise AssertionError(result.stderr[-2000:])
        return json.loads(result.stdout)["services"]

    def changed(self, overrides):
        rendered = self.render(overrides)
        self.assertEqual(set(self.base), set(rendered))
        return {name for name in self.base if self.base[name] != rendered[name]}

    def dev_side(self):
        return {
            name
            for name, service in self.base.items()
            if name.startswith("dev-")
            or (service.get("environment") or {}).get("PGHOST") == "dev-pg"
        }

    def test_dev_variables_change_only_dev_services(self):
        changed = self.changed(DEV_OVERRIDES)
        self.assertTrue({"dev-pg", "dev-valkey"} <= changed, changed)
        self.assertEqual(set(), changed - self.dev_side())

    def test_mng_variables_leave_every_dev_service_unchanged(self):
        changed = self.changed(MNG_OVERRIDES)
        self.assertTrue({"mng-pg", "mng-valkey"} <= changed, changed)
        self.assertEqual(set(), changed & self.dev_side())
        rendered = self.render(MNG_OVERRIDES)["redisinsight"]["environment"]
        base = self.base["redisinsight"]["environment"]
        # RedisInsight reaches both tiers: only its MNG connection may follow.
        for key in ("RI_REDIS_HOST1", "RI_REDIS_PORT1", "RI_REDIS_ALIAS1"):
            with self.subTest(key=key):
                self.assertEqual(base[key], rendered[key])
        self.assertEqual("16379", rendered["RI_REDIS_PORT2"])


class DatastoreScrapeLabelTests(unittest.TestCase):
    CONFIG = ROOT / "infra/06-observability/prometheus/config"
    START = ROOT / "infra/06-observability/prometheus/scripts/start.sh"

    def render(self, state):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        env = {
            **os.environ,
            "PROMETHEUS_TARGETS_DIR": directory.name,
            "PROMETHEUS_BIN": "true",
            "OPENBAO_PORT": "8200",
        }
        env.pop("PROMETHEUS_DEV_DATA_EXPECTED", None)
        if state is not None:
            env["PROMETHEUS_DEV_DATA_EXPECTED"] = state
        result = subprocess.run(
            ["sh", str(self.START)],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        return result, Path(directory.name)

    def test_both_configs_label_every_datastore_job_by_scope_and_engine(self):
        for config in ("prometheus.yml", "prometheus.dev.yml"):
            jobs = {
                job["job_name"]: job
                for job in yaml.safe_load(
                    (self.CONFIG / config).read_text(encoding="utf-8")
                )["scrape_configs"]
            }
            for name, scope, engine in DATASTORE_JOBS:
                with self.subTest(config=config, job=name):
                    job = jobs[name]
                    if scope == "mng":
                        labels = job["static_configs"][0]["labels"]
                        self.assertEqual(labels["db_scope"], scope)
                        self.assertEqual(labels["db_engine"], engine)
                        self.assertEqual(labels["expected_state"], "on")
                    else:
                        self.assertEqual(
                            job["file_sd_configs"][0]["files"],
                            [f"/etc/prometheus/targets/{name}.yml"],
                        )

    def test_start_renders_dev_targets_with_the_declared_state(self):
        for state in ("on", "off"):
            result, directory = self.render(state)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                sorted(p.name for p in directory.iterdir()),
                [
                    "dev-pg-exporter.yml",
                    "dev-valkey-exporter.yml",
                    "keycloak.yml",
                    "openbao.yml",
                ],
            )
            openbao = yaml.safe_load((directory / "openbao.yml").read_text())[0]
            self.assertEqual(["openbao:8200"], openbao["targets"])
            keycloak = yaml.safe_load((directory / "keycloak.yml").read_text())[0]
            self.assertEqual(["keycloak-management:9000"], keycloak["targets"])
            self.assertEqual(
                {
                    "cluster": "hy-home",
                    "namespace": "hy-home",
                    "domain": "auth",
                    "container": "keycloak",
                },
                keycloak["labels"],
            )
            for name, scope, engine in DATASTORE_JOBS:
                if scope != "dev":
                    continue
                with self.subTest(state=state, job=name):
                    group = yaml.safe_load(
                        (directory / f"{name}.yml").read_text(encoding="utf-8")
                    )[0]
                    self.assertEqual(
                        group["targets"],
                        [f"{name}:{9187 if engine == 'postgresql' else 9121}"],
                    )
                    self.assertEqual(
                        group["labels"],
                        {
                            "cluster": "hy-home",
                            "namespace": "hy-home",
                            "domain": "datastores",
                            "db_scope": "dev",
                            "db_engine": engine,
                            "expected_state": state,
                        },
                    )

    def test_prometheus_can_write_the_rendered_targets(self):
        services = compose("infra/06-observability/docker-compose.yml")
        prometheus = services["prometheus"]
        self.assertEqual(
            prometheus["entrypoint"],
            ["/bin/sh", "/usr/local/libexec/prometheus/start.sh"],
        )
        # The image runs as nobody (65534); a root-owned tmpfs stops start.sh.
        self.assertIn(
            "/etc/prometheus:size=10M,uid=65534,gid=65534,mode=0755",
            prometheus["tmpfs"],
        )

    def test_start_refuses_a_missing_or_unknown_state(self):
        for state in (None, "", "ON", "true", "on\n"):
            with self.subTest(state=state):
                result, directory = self.render(state)
                self.assertEqual(result.returncode, 64)
                self.assertEqual(list(directory.iterdir()), [])

    def test_datastore_down_alerts_are_scoped_and_dev_honours_expected_state(self):
        path = self.CONFIG / "alert_rules/alert_rules.local.datastores.yml"
        rules = {
            rule["alert"]: rule
            for group in yaml.safe_load(path.read_text(encoding="utf-8"))["groups"]
            for rule in group["rules"]
        }
        expected = {
            "PostgresDown": ('pg_up{db_scope="mng",expected_state!="off"}', "critical"),
            "ValkeyDown": (
                'redis_up{db_scope="mng",expected_state!="off"}',
                "critical",
            ),
            "MngDatastoreExporterDown": (
                'up{db_scope="mng",expected_state!="off"}',
                "critical",
            ),
            "DevPostgresDown": (
                'pg_up{db_scope="dev", expected_state="on"}',
                "warning",
            ),
            "DevValkeyDown": (
                'redis_up{db_scope="dev", expected_state="on"}',
                "warning",
            ),
            "DevDatastoreExporterDown": (
                'up{db_scope="dev", expected_state="on"}',
                "warning",
            ),
        }
        for name, (selector, severity) in expected.items():
            with self.subTest(alert=name):
                self.assertIn(selector, rules[name]["expr"])
                self.assertEqual(rules[name]["labels"]["severity"], severity)
        for name, rule in rules.items():
            with self.subTest(alert=name):
                expr = " ".join(rule["expr"].split())
                if 'db_scope="dev"' in expr and "DeclaredOff" not in name:
                    self.assertIn('expected_state="on"', expr)
                # An unscoped comparison would page for DEV stopped on purpose.
                for metric in ("pg_up", "redis_up"):
                    self.assertNotIn(f"{metric} ==", expr)
        absent = rules["DatastoreScrapeTargetMissing"]["expr"]
        for job, _, _ in DATASTORE_JOBS:
            self.assertIn(f'absent(up{{job="{job}"}})', absent)


if __name__ == "__main__":
    unittest.main()
