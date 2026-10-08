"""Fail-closed project metadata and SQL contract for the dev PostgreSQL job."""

import importlib.util
import json
import sys
import unittest
from pathlib import Path

SOURCE = (
    Path(__file__).resolve().parents[2] / "infra/04-data/dev-db/pg/provision/project.py"
)
SPEC = importlib.util.spec_from_file_location("dev_pg_project", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def manifest():
    return {
        "schema_version": 1,
        "project_id": "hyhome-platform",
        "environment": "development",
        "database": "platform_dev",
        "schema": "app",
        "roles": {
            "owner": "platform_owner",
            "migrator": "platform_migrator",
            "runtime": "platform_runtime",
            "reader": "platform_reader",
        },
        "password_secrets": {
            "migrator": "dev_pg_platform_migrator_password",
            "runtime": "dev_pg_platform_runtime_password",
            "reader": "dev_pg_platform_reader_password",
        },
    }


class ProjectProvisionTests(unittest.TestCase):
    def test_login_roles_get_connection_budgets_on_every_run(self):
        sql = MODULE.sql_for(MODULE.validate(manifest()))
        for role, limit in (
            ("platform_migrator", 2),
            ("platform_runtime", 10),
            ("platform_reader", 5),
        ):
            statement = f"ALTER ROLE {role} CONNECTION LIMIT {limit};"
            self.assertEqual(1, sql.count(statement))
            # Outside the activation branch, so reruns reapply the budget.
            self.assertLess(
                sql.index("\\endif", sql.index(f"activate_{role.split('_')[1]}")),
                sql.index(statement),
            )
        self.assertNotIn("platform_owner CONNECTION LIMIT", sql)

    def test_fixture_has_distinct_roles_and_no_default_business_database(self):
        project = MODULE.validate(manifest())
        sql = MODULE.sql_for(project)
        self.assertIn("CREATE DATABASE platform_dev OWNER platform_owner", sql)
        self.assertIn("CREATE ROLE platform_owner NOLOGIN", sql)
        self.assertIn("REVOKE ALL ON DATABASE platform_dev FROM PUBLIC", sql)
        self.assertIn("REVOKE ALL ON SCHEMA public FROM PUBLIC", sql)
        self.assertIn(
            "GRANT SELECT ON ALL TABLES IN SCHEMA app TO platform_reader", sql
        )
        self.assertIn("REVOKE ALL ON ALL FUNCTIONS IN SCHEMA app FROM PUBLIC", sql)
        self.assertIn("REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC", sql)
        self.assertNotIn("GRANT CREATE ON SCHEMA app TO platform_runtime", sql)
        self.assertNotIn("app_db", sql)

    def test_unknown_fields_and_unsafe_identifiers_fail_before_sql(self):
        for changed in (
            {"database": "app_db; DROP DATABASE postgres"},
            {"schema": "public"},
            {"project_id": "../outside"},
            {"extra": "ignored"},
            {"roles": {**manifest()["roles"], "reader": "platform_runtime"}},
            {
                "password_secrets": {
                    **manifest()["password_secrets"],
                    "reader": "../key",
                }
            },
        ):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                MODULE.validate({**manifest(), **changed})

    def test_no_unapproved_hypertable_or_retention_policy(self):
        sql = MODULE.sql_for(MODULE.validate(manifest())).lower()
        self.assertIn("create extension if not exists timescaledb", sql)
        self.assertNotIn("create_hypertable", sql)
        self.assertNotIn("add_retention_policy", sql)

    def test_wal_archive_is_bounded_and_retained(self):
        compose = (SOURCE.parents[2] / "docker-compose.yml").read_text()
        backup = (SOURCE.parents[1] / "backup/pgbackrest.conf").read_text()
        entrypoint = (SOURCE.parents[1] / "backup/entrypoint.sh").read_text()
        self.assertIn("archive_mode=on", compose)
        self.assertNotIn("archive_mode=off", compose)
        self.assertIn(
            "archive_command=pgbackrest --stanza=dev archive-push %p", compose
        )
        self.assertIn("repo1-retention-full=2", backup)
        self.assertIn("repo1-retention-diff=6", backup)
        self.assertIn("archive-push-queue-max=2GiB", backup)
        self.assertNotIn("repo1-cipher-pass", backup)
        # Only the repository root changes owner; existing backups are untouched.
        self.assertIn('chown postgres:postgres "$repo"', entrypoint)
        self.assertNotIn('chown -R postgres:postgres "$repo"', entrypoint)
        # A read-only restore mount must start: change only when it differs.
        self.assertIn('if [ "$(stat -c', entrypoint)

    def test_tracked_fixture_matches_validated_contract(self):
        fixture = SOURCE.parent / "platform.json"
        self.assertEqual(
            MODULE.validate(json.loads(fixture.read_text())),
            MODULE.validate(manifest()),
        )

    def test_other_environment_and_secret_reuse_fail(self):
        for changed in (
            {"environment": "production"},
            {
                "password_secrets": {
                    **manifest()["password_secrets"],
                    "reader": "dev_pg_platform_runtime_password",
                }
            },
        ):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                MODULE.validate({**manifest(), **changed})

    def test_partial_create_recovery_is_scoped(self):
        sql = MODULE.sql_for(MODULE.validate(manifest()))
        for kind, role in manifest()["roles"].items():
            with self.subTest(kind=kind):
                created = sql.index(f"CREATE ROLE {role} NOLOGIN")
                marked = sql.index(f"COMMENT ON ROLE {role} IS")
                checked = sql.index("RAISE EXCEPTION 'role ownership mismatch'", marked)
                self.assertLess(created, marked)
                self.assertLess(marked, checked)
                self.assertIn(
                    f"shobj_description(r.oid, 'pg_authid') = 'dev-pg:development:hyhome-platform:{kind}'",
                    sql[marked:checked],
                )
        created = sql.index("CREATE DATABASE platform_dev OWNER platform_owner")
        marked = sql.index("COMMENT ON DATABASE platform_dev IS")
        checked = sql.index("RAISE EXCEPTION 'database ownership mismatch'")
        self.assertLess(created, marked)
        self.assertLess(marked, checked)
        self.assertIn("shobj_description(d.oid, 'pg_database')", sql[marked:checked])
        self.assertIn("AS database_recoverable", sql)
        self.assertIn("d.datacl IS NULL", sql)
        self.assertIn("pg_get_userbyid(d.datdba) = 'platform_owner'", sql)
        self.assertIn("n.nspname = 'public'", sql)
        self.assertIn("manual review required", sql)
        for kind, role in manifest()["roles"].items():
            with self.subTest(kind=kind):
                before = sql[: sql.index(f"CREATE ROLE {role} NOLOGIN")]
                after = sql[sql.index(f"CREATE ROLE {role} NOLOGIN") :]
                self.assertGreater(before.rindex("BEGIN;"), before.rfind("COMMIT;"))
                self.assertLess(
                    after.index(f"COMMENT ON ROLE {role}"), after.index("COMMIT;")
                )

    def test_both_connections_take_database_scoped_advisory_lock(self):
        sql = MODULE.sql_for(MODULE.validate(manifest()))
        lock = "SELECT pg_advisory_lock(hashtext('dev-pg:platform_dev'));"
        self.assertEqual(2, sql.count(lock))
        first, second = (i for i in range(len(sql)) if sql.startswith(lock, i))
        self.assertLess(first, sql.index("CREATE ROLE platform_owner"))
        self.assertLess(sql.index("\\connect platform_dev"), second)
        self.assertLess(second, sql.index("COMMENT ON DATABASE platform_dev"))
        self.assertLess(second, sql.index("CREATE SCHEMA IF NOT EXISTS app"))

    def test_existing_objects_are_bound_to_project_metadata(self):
        sql = MODULE.sql_for(MODULE.validate(manifest()))
        self.assertIn("pg_advisory_lock", sql)
        self.assertEqual(2, sql.count("pg_advisory_lock"))
        self.assertLess(
            sql.index("\\connect platform_dev"), sql.rindex("pg_advisory_lock")
        )
        self.assertIn("role ownership mismatch", sql)
        self.assertIn("\\if :create_owner", sql)
        self.assertIn("\\gexec", sql)
        self.assertIn("ALTER ROLE platform_runtime WITH PASSWORD", sql)
        self.assertLess(
            sql.index("SET log_statement = 'none'"),
            sql.index("ALTER ROLE platform_runtime WITH PASSWORD"),
        )
        self.assertLess(
            sql.index("SET log_min_error_statement = 'panic'"),
            sql.index("ALTER ROLE platform_runtime WITH PASSWORD"),
        )
        self.assertIn("activate_runtime", sql)
        self.assertIn("default privileges", sql.lower())
        self.assertIn("shobj_description", sql)
        self.assertIn("database ownership mismatch", sql)
        self.assertIn("role ownership mismatch", sql)
        self.assertIn("schema ownership mismatch", sql)
        self.assertIn("\\connect platform_dev", sql)
        self.assertIn("CREATE EXTENSION IF NOT EXISTS timescaledb", sql)


class MonitorProvisionTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(SOURCE.parent))
        self.addCleanup(sys.path.remove, str(SOURCE.parent))
        spec = importlib.util.spec_from_file_location(
            "dev_pg_monitor", SOURCE.parent / "monitor.py"
        )
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_monitor_role_is_pg_monitor_only_and_never_rotated(self):
        sql = self.module.sql()
        self.assertIn("GRANT pg_monitor TO dev_pg_monitor;", sql)
        self.assertIn("CONNECTION LIMIT 3", sql)
        self.assertIn("NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION", sql)
        self.assertIn("'dev-pg:development:monitor'", sql)
        self.assertIn("RAISE EXCEPTION 'role ownership mismatch'", sql)
        # The password is set only while the role cannot log in yet.
        activate = sql.index("\\if :activate")
        self.assertLess(activate, sql.index("WITH PASSWORD"))
        self.assertNotIn("GRANT CONNECT", sql)
        self.assertLess(sql.index("\\getenv"), sql.index("WITH PASSWORD"))


if __name__ == "__main__":
    unittest.main()
