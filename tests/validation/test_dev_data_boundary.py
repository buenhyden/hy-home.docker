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


if __name__ == "__main__":
    unittest.main()
