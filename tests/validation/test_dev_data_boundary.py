"""Static cross-file boundary for management and development data consumers."""

import json
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
        self.assertIn("-config-command=-", command)
        self.assertIn("-set-client-name=false", command)
        for job in ("dev-pg-exporter:9187", "dev-valkey-exporter:9121"):
            for config in ("prometheus.yml", "prometheus.dev.yml"):
                path = ROOT / "infra/06-observability/prometheus/config" / config
                with self.subTest(config=config, job=job):
                    self.assertIn(job, path.read_text(encoding="utf-8"))

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
        self.assertIn("-config-command=-", command)
        self.assertIn("-set-client-name=false", command)


if __name__ == "__main__":
    unittest.main()
