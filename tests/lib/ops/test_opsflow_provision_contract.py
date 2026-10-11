"""Source-only migration boundary checks; these do not execute PostgreSQL."""

import importlib.util
import json
import re
import unittest
from pathlib import Path

SQL = (
    Path(__file__).resolve().parents[3]
    / "infra/07-workflow/airflow/workloads/manifest-pipeline/sql"
)
PROVISIONER = (
    Path(__file__).resolve().parents[3] / "infra/04-data/dev-db/pg/provision/project.py"
)
SPEC = importlib.util.spec_from_file_location("opsflow_dev_pg_project", PROVISIONER)
PROJECT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROJECT)


class OpsflowProvisionContractTests(unittest.TestCase):
    def test_function_only_provisioner_matches_migration_identity(self):
        fixture = json.loads((PROVISIONER.parent / "opsflow.json").read_text())
        pending = PROJECT.validate(fixture)
        self.assertEqual(
            {
                "owner": "opsflow_owner",
                "migrator": "opsflow_migrator",
                "ingest": "opsflow_ingest",
                "notifier": "opsflow_notifier",
                "reader": "opsflow_reader",
            },
            pending["roles"],
        )
        bound = {
            **fixture,
            "password_secrets": {
                kind: f"synthetic_opsflow_{kind}_password"
                for kind in ("migrator", "ingest", "notifier", "reader")
            },
        }
        provision_sql = PROJECT.sql_for(PROJECT.validate(bound))
        migration = (SQL / "001_opsflow.sql").read_text()
        for role in pending["roles"].values():
            self.assertIn(role, provision_sql)
            self.assertIn(role, migration)
        self.assertNotRegex(
            provision_sql,
            r"GRANT\s+(?:ALL|INSERT|UPDATE|DELETE).*TO opsflow_(?:ingest|notifier|reader)",
        )

    def test_atomic_fail_closed_migration(self):
        source = (SQL / "001_opsflow.sql").read_text()
        self.assertTrue(source.startswith("\\set ON_ERROR_STOP on"))
        self.assertIn("BEGIN;", source)
        self.assertTrue(source.rstrip().endswith("COMMIT;"))
        self.assertNotRegex(source, r"(?i)IF\s+NOT\s+EXISTS|CREATE\s+OR\s+REPLACE")
        for boundary in (
            "current_database()",
            "current_user",
            "pg_default_acl",
            "migration_sha256",
            "schema_fingerprint",
        ):
            self.assertIn(boundary, source)

    def test_function_and_role_boundary(self):
        source = (SQL / "001_opsflow.sql").read_text()
        definitions = re.findall(r"CREATE FUNCTION ops_flow\.([a-z_]+)", source)
        self.assertEqual(
            set(definitions),
            {
                "publish_manifest",
                "claim_notification",
                "ack_notification",
                "retry_notification",
            },
        )
        self.assertEqual(
            source.count("SECURITY DEFINER SET search_path = pg_catalog"), 4
        )
        self.assertNotRegex(
            source,
            r"GRANT\s+(?:ALL|INSERT|UPDATE|DELETE).*TO opsflow_(?:ingest|notifier|reader)",
        )
        self.assertIn(
            "REVOKE ALL ON ALL FUNCTIONS IN SCHEMA ops_flow FROM PUBLIC", source
        )
        self.assertIn(
            "GRANT SELECT ON ops_flow.published_documents, ops_flow.delivery_status TO opsflow_reader",
            source,
        )

    def test_preflight_rejects_inherited_capabilities_before_ddl(self):
        source = (SQL / "001_opsflow.sql").read_text().split("CREATE TABLE", 1)[0]
        self.assertIn("roleid IN", source)
        self.assertIn("member IN", source)
        self.assertIn("has_database_privilege", source)
        self.assertIn("'TEMP'", source)
        self.assertNotIn("pg_catalog.coalesce", source)

    def test_receipt_checks_current_security_shape(self):
        for filename in ("001_opsflow.sql", "002_checks.sql"):
            source = (SQL / filename).read_text()
            for surface in (
                "proacl",
                "proowner",
                "relowner",
                "pg_get_viewdef",
                "pg_get_indexdef",
                "pg_get_expr",
                "nspacl",
                "datacl",
                "defaclacl",
            ):
                self.assertIn(surface, source, filename)
        source = (SQL / "002_checks.sql").read_text()
        self.assertIn(":'migration_sha256'", source)
        self.assertIn("schema_drift", source)
        self.assertIn("isolated_database_not_empty", source)

    def test_constraint_fingerprint_binds_relation_and_name(self):
        for filename in ("001_opsflow.sql", "002_checks.sql"):
            source = (SQL / filename).read_text()
            self.assertTrue("c.conrelid::pg_catalog.regclass::text" in source, filename)
            self.assertTrue("c.conname" in source, filename)

    def test_type_catalog_cannot_escape_empty_shape_or_drift_check(self):
        migration = (SQL / "001_opsflow.sql").read_text()
        preflight = migration.split("CREATE TABLE", 1)[0]
        self.assertTrue("pg_catalog.pg_type" in preflight)
        for filename in ("001_opsflow.sql", "002_checks.sql"):
            source = (SQL / filename).read_text()
            self.assertTrue("'type:'" in source, filename)
            self.assertTrue("t.typnamespace='ops_flow'" in source, filename)

    def test_public_types_are_rejected_in_empty_database(self):
        for filename in ("001_opsflow.sql", "002_checks.sql"):
            source = (SQL / filename).read_text()
            self.assertTrue(
                "typnamespace='public'::pg_catalog.regnamespace" in source, filename
            )

    def test_sequence_configuration_is_in_current_receipt(self):
        for filename in ("001_opsflow.sql", "002_checks.sql"):
            source = (SQL / filename).read_text()
            for field in (
                "seqincrement",
                "seqstart",
                "seqmin",
                "seqmax",
                "seqcache",
                "seqcycle",
            ):
                self.assertTrue(field in source, filename)

    def test_executable_checks_not_comment_claims(self):
        source = (SQL / "002_checks.sql").read_text()
        executable = "\n".join(
            line for line in source.splitlines() if not line.lstrip().startswith("--")
        )
        for assertion in (
            "has_database_privilege",
            "has_schema_privilege",
            "has_table_privilege",
            "publish_manifest",
            "claim_notification",
            "ack_notification",
            "retry_notification",
            "ROLLBACK;",
        ):
            self.assertIn(assertion, executable)
        self.assertGreaterEqual(executable.count("RAISE EXCEPTION"), 12)
        self.assertIn("SET LOCAL ROLE opsflow_ingest", executable)
        self.assertIn("SET LOCAL ROLE opsflow_notifier", executable)


if __name__ == "__main__":
    unittest.main()
