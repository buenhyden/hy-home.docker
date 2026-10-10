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

    def test_dbt_and_cdc_target_named_dev_fixture(self):
        dbt = compose("infra/12-analytics/dbt/docker-compose.yml")
        kafka = compose("infra/05-messaging/kafka/docker-compose.yml")
        connector = json.loads(
            (
                ROOT
                / "infra/05-messaging/kafka/connect/debezium/postgres-connector.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(dbt["dbt"]["environment"]["DBT_DB_HOST"], "dev-pg")
        self.assertEqual(dbt["dbt"]["environment"]["DBT_DB_NAME"], "platform_dev")
        profile = (ROOT / "infra/12-analytics/dbt/profiles/profiles.yml").read_text()
        self.assertIn("env_var('DBT_DB_HOST')", profile)
        self.assertIn("env_var('DBT_DB_NAME')", profile)
        self.assertNotIn("mng-pg", profile)
        self.assertNotIn("app_db", profile)
        self.assertEqual(
            kafka["debezium-db-provision"]["environment"]["PGHOST"], "dev-pg"
        )
        self.assertEqual(connector["database.hostname"], "dev-pg")
        self.assertEqual(connector["database.dbname"], "platform_dev")
        self.assertEqual(connector["slot.name"], "hyhome_platform_slot")
        self.assertEqual(connector["publication.name"], "hyhome_platform_publication")
        publication_sql = (
            ROOT / "infra/05-messaging/kafka/connect/debezium/provisioning/dev-pg.sql"
        ).read_text()
        self.assertIn("p.puballtables", publication_sql)
        self.assertIn("pg_catalog.pg_publication_rel", publication_sql)
        self.assertIn("pg_catalog.pg_publication_namespace", publication_sql)
        self.assertIn("Timescale hypertable internal chunks are", publication_sql)
        self.assertIn(
            "unsupported until a separate source/connector contract", publication_sql
        )
        self.assertEqual(connector["topic.prefix"], "hyhome.platform")
        self.assertEqual(
            connector["value.converter.schema.registry.url"],
            "http://schema-registry:8081",
        )

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
        self.assertGreaterEqual(consumers, 4)

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
                ["dev-pg-exporter.yml", "dev-valkey-exporter.yml", "openbao.yml"],
            )
            openbao = yaml.safe_load((directory / "openbao.yml").read_text())[0]
            self.assertEqual(["openbao:8200"], openbao["targets"])
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
            "PostgresDown": ('pg_up{db_scope="mng"}', "critical"),
            "ValkeyDown": ('redis_up{db_scope="mng"}', "critical"),
            "MngDatastoreExporterDown": ('up{db_scope="mng"}', "critical"),
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
