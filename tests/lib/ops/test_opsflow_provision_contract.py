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
    def test_v1_bootstrap_preserves_structural_contract(self):
        source = (SQL / "001_opsflow.sql").read_text()
        self.assertEqual(
            ["runs", "documents", "current_runs", "outbox", "schema_version"],
            re.findall(r"CREATE TABLE ops_flow\.([a-z_]+)", source),
        )
        for signature in (
            "publish_manifest(p_source text,p_run text,p_sha text,p_time timestamptz,p_rows jsonb,p_artifact text)",
            "claim_notification()",
            "ack_notification(p_id bigint,p_token uuid)",
            "retry_notification(p_id bigint,p_token uuid)",
        ):
            self.assertIn(f"CREATE FUNCTION ops_flow.{signature}", source)
        self.assertIn(
            "schema_version(version integer PRIMARY KEY CHECK(version=1)", source
        )

    def test_fingerprints_cast_internal_char_catalog_fields(self):
        fingerprint = re.compile(
            r"FROM \(\n(  SELECT 'column:'.*?)\n \) shape;", re.DOTALL
        )
        fields = (
            "t.typtype",
            "t.typcategory",
            "c.relkind",
            "c.relpersistence",
            "r.ev_enabled",
            "t.tgenabled",
            "p.polcmd",
            "d.defaclobjtype",
        )
        for filename, expected_blocks in (
            ("001_opsflow.sql", 1),
            ("002_checks.sql", 1),
            ("003_business_date.sql", 2),
        ):
            blocks = fingerprint.findall((SQL / filename).read_text())
            self.assertEqual(expected_blocks, len(blocks), filename)
            for block in blocks:
                for field in fields:
                    self.assertIn(f"||{field}::text", block, (filename, field))
                    self.assertNotRegex(
                        block, rf"\|\|{re.escape(field)}(?!::text)", (filename, field)
                    )

    def test_relation_acl_fingerprint_is_restore_stable_without_losing_rights(self):
        fingerprint = re.compile(
            r"FROM \(\n(  SELECT 'column:'.*?)\n \) shape;", re.DOTALL
        )
        for filename, expected_blocks in (
            ("001_opsflow.sql", 1),
            ("002_checks.sql", 1),
            ("003_business_date.sql", 2),
        ):
            blocks = fingerprint.findall((SQL / filename).read_text())
            self.assertEqual(expected_blocks, len(blocks), filename)
            for block in blocks:
                relation = next(
                    line for line in block.splitlines() if "SELECT 'relation:'" in line
                )
                for boundary in (
                    "c.relkind IN ('r','p','v','m','f','S')",
                    "CASE WHEN c.relacl IS NULL THEN pg_catalog.acldefault(",
                    "CASE WHEN c.relkind='S' THEN 's'::\"char\" ELSE 'r'::\"char\" END",
                    "pg_catalog.aclexplode",
                    "pg_catalog.pg_get_userbyid(a.grantor)",
                    "CASE WHEN a.grantee=0 THEN 'PUBLIC' ELSE pg_catalog.pg_get_userbyid(a.grantee) END",
                    "a.privilege_type",
                    "a.is_grantable",
                    "ELSE COALESCE(c.relacl::text,'') END",
                ):
                    self.assertIn(boundary, relation, (filename, boundary))
                self.assertNotIn(
                    "||COALESCE(c.relacl::text,'') FROM pg_catalog.pg_class",
                    relation,
                    filename,
                )

    def test_checks_verify_latest_supported_migration_receipt(self):
        source = (SQL / "002_checks.sql").read_text()
        for boundary in (
            "current_version integer",
            "SELECT max(version) INTO current_version",
            "current_version NOT IN (1,2)",
            "count(*) FROM ops_flow.schema_version) <> current_version",
            "82a4762a8962832c7fdd05826df3b97cf02cc4f96c974a328e42e4493143b18f",
            "WHERE version=current_version AND migration_sha256=",
            "WHERE version=current_version)",
        ):
            self.assertIn(boundary, source)
        self.assertNotIn("WHERE version=1 AND migration_sha256=", source)

    def test_business_date_migration_is_fail_closed(self):
        source = (SQL / "003_business_date.sql").read_text()
        self.assertTrue(source.startswith("\\set ON_ERROR_STOP on"))
        self.assertIn("BEGIN;", source)
        self.assertTrue(source.rstrip().endswith("COMMIT;"))
        for boundary in (
            "current_database()",
            "current_user",
            "session_user",
            "SET LOCAL lock_timeout = '10s'",
            "SET LOCAL statement_timeout = '60s'",
            "82a4762a8962832c7fdd05826df3b97cf02cc4f96c974a328e42e4493143b18f",
            "pg_advisory_xact_lock",
            "LOCK TABLE ops_flow.runs, ops_flow.documents, ops_flow.current_runs, ops_flow.outbox, ops_flow.schema_version IN ACCESS EXCLUSIVE MODE",
            "schema_fingerprint",
            "existing_source_business_date_conflict",
        ):
            self.assertIn(boundary, source)
        before_index = source.split(
            "CREATE UNIQUE INDEX runs_source_business_date_uidx", 1
        )[0]
        self.assertIn("GROUP BY source", before_index)
        self.assertIn("AT TIME ZONE 'UTC'", before_index)
        self.assertNotIn("CREATE OR REPLACE FUNCTION", source)
        self.assertNotRegex(source, r"(?i)\b(?:DELETE|TRUNCATE|DROP INDEX)\b")

    def test_business_date_migration_versions_receipt_and_named_index(self):
        source = (SQL / "003_business_date.sql").read_text()
        self.assertIn(
            "CREATE UNIQUE INDEX runs_source_business_date_uidx\n ON ops_flow.runs (source, ((captured_at AT TIME ZONE 'UTC')::date))",
            source,
        )
        self.assertIn("CHECK(version IN (1,2))", source)
        self.assertIn("INSERT INTO ops_flow.schema_version SELECT 2", source)
        self.assertNotRegex(source, r"(?i)UPDATE\s+ops_flow\.schema_version")
        for surface in (
            "pg_get_functiondef",
            "pg_get_constraintdef",
            "pg_get_viewdef",
            "pg_get_indexdef",
            "pg_get_expr",
            "proacl",
            "proowner",
            "relowner",
            "nspacl",
            "datacl",
            "defaclacl",
            "seqincrement",
            "seqstart",
            "seqmin",
            "seqmax",
            "seqcache",
            "seqcycle",
        ):
            self.assertIn(surface, source)

    def test_business_date_migration_reuses_v1_fingerprint(self):
        fingerprint = re.compile(
            r"FROM \(\n(  SELECT 'column:'.*?)\n \) shape;", re.DOTALL
        )
        baseline = fingerprint.findall((SQL / "001_opsflow.sql").read_text())
        checker = fingerprint.findall((SQL / "002_checks.sql").read_text())
        migration = fingerprint.findall((SQL / "003_business_date.sql").read_text())
        self.assertEqual(1, len(baseline))
        self.assertEqual(baseline, checker)
        self.assertEqual([baseline[0], baseline[0]], migration)

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
