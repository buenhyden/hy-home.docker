"""Fail-closed project metadata and SQL contract for the dev PostgreSQL job."""

import hashlib
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

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


def opsflow_manifest(*, bound=True):
    password_secrets = None
    if bound:
        password_secrets = {
            "migrator": "synthetic_opsflow_migrator_password",
            "ingest": "synthetic_opsflow_ingest_password",
            "notifier": "synthetic_opsflow_notifier_password",
            "reader": "synthetic_opsflow_reader_password",
        }
    return {
        "schema_version": 2,
        "project_id": "hyhome-opsflow",
        "environment": "development",
        "database": "opsflow_dev",
        "schema": "ops_flow",
        "roles": {
            "owner": "opsflow_owner",
            "migrator": "opsflow_migrator",
            "ingest": "opsflow_ingest",
            "notifier": "opsflow_notifier",
            "reader": "opsflow_reader",
        },
        "password_secrets": password_secrets,
    }


class ProjectProvisionTests(unittest.TestCase):
    def test_function_only_rejects_cross_database_connect_before_login(self):
        sql = MODULE.sql_for(MODULE.validate(opsflow_manifest()))
        guard = sql.index("cross_database_connect_requires_cluster_review")
        self.assertLess(guard, sql.index("ALTER ROLE opsflow_migrator WITH PASSWORD"))
        self.assertIn("d.datallowconn AND d.datname<>'opsflow_dev'", sql)
        self.assertIn("has_database_privilege(r.oid,d.oid,'CONNECT')", sql)
        for role in (
            "opsflow_migrator",
            "opsflow_ingest",
            "opsflow_notifier",
            "opsflow_reader",
        ):
            self.assertIn("'" + role + "'", sql)

    def test_v1_generated_sql_is_byte_stable(self):
        sql = MODULE.sql_for(MODULE.validate(manifest())).encode()
        self.assertEqual(
            "6c5a395271102d1db425900562bbcb9651df0f36cf409ff8f3d1ca303acc3b6f",
            hashlib.sha256(sql).hexdigest(),
        )

    def test_generated_do_blocks_do_not_contain_psql_variables(self):
        for project in (manifest(), opsflow_manifest()):
            with self.subTest(schema_version=project["schema_version"]):
                sql = MODULE.sql_for(MODULE.validate(project))
                bodies = re.findall(
                    r"DO \$check\$ BEGIN\n(.*?)\nEND \$check\$;", sql, re.DOTALL
                )
                self.assertTrue(bodies)
                for body in bodies:
                    self.assertNotRegex(
                        body,
                        r"(?<!:):(?:'[A-Za-z_][A-Za-z0-9_]*'|\"[A-Za-z_][A-Za-z0-9_]*\")",
                    )

    def test_pending_opsflow_fixture_validates_but_cannot_emit_sql(self):
        fixture = SOURCE.parent / "opsflow.json"
        project = MODULE.validate(json.loads(fixture.read_text()))
        self.assertEqual(2, project["schema_version"])
        self.assertIsNone(project["password_secrets"])
        self.assertEqual(opsflow_manifest(bound=False)["roles"], project["roles"])
        with self.assertRaisesRegex(ValueError, "credential bindings pending"):
            MODULE.sql_for(project)

    def test_pending_opsflow_cli_stops_before_secret_or_sql_access(self):
        fixture = SOURCE.parent / "opsflow.json"
        with (
            mock.patch.object(sys, "argv", [str(SOURCE), str(fixture)]),
            mock.patch.object(MODULE, "read_secret") as read_secret,
        ):
            self.assertEqual(64, MODULE.main())
        read_secret.assert_not_called()

    def test_pending_opsflow_validate_only_is_structural(self):
        fixture = SOURCE.parent / "opsflow.json"
        with (
            mock.patch.object(
                sys, "argv", [str(SOURCE), str(fixture), "--validate-only"]
            ),
            mock.patch.object(MODULE, "read_secret") as read_secret,
            mock.patch("builtins.print") as output,
        ):
            self.assertEqual(0, MODULE.main())
        read_secret.assert_not_called()
        output.assert_called_once_with(
            "project manifest structurally valid; credential bindings pending"
        )

    def test_function_only_sql_has_exact_roles_and_no_broad_acl(self):
        sql = MODULE.sql_for(MODULE.validate(opsflow_manifest()))
        for kind, role in opsflow_manifest()["roles"].items():
            self.assertIn(f"CREATE ROLE {role} NOLOGIN", sql, kind)
        self.assertIn(
            "GRANT CONNECT ON DATABASE opsflow_dev TO opsflow_migrator, opsflow_ingest, opsflow_notifier, opsflow_reader;",
            sql,
        )
        self.assertIn(
            "GRANT opsflow_owner TO opsflow_migrator WITH INHERIT FALSE, SET TRUE;",
            sql,
        )
        self.assertIn(
            "GRANT USAGE ON SCHEMA ops_flow TO opsflow_ingest, opsflow_notifier, opsflow_reader;",
            sql,
        )
        for forbidden in (
            "GRANT SELECT ON ALL TABLES",
            "GRANT SELECT, INSERT, UPDATE, DELETE",
            "GRANT USAGE, SELECT ON ALL SEQUENCES",
            "ALTER DEFAULT PRIVILEGES FOR ROLE opsflow_owner IN SCHEMA ops_flow GRANT",
            "CREATE EXTENSION IF NOT EXISTS timescaledb",
        ):
            self.assertNotIn(forbidden, sql)
        self.assertIn(
            "ALTER DEFAULT PRIVILEGES FOR ROLE opsflow_owner REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;",
            sql,
        )

    def test_function_only_contract_rejects_names_shape_and_secret_reuse(self):
        base = opsflow_manifest()
        for invalid in (None, {}, {"schema_version": True}, {"schema_version": 3}):
            with (
                self.subTest(invalid=invalid),
                self.assertRaisesRegex(ValueError, "unsupported manifest schema"),
            ):
                MODULE.validate(invalid)
        changes = (
            {"database": "other_dev"},
            {"schema": "other_schema"},
            {"extra": "ignored"},
            {"roles": {**base["roles"], "runtime": "opsflow_runtime"}},
            {"roles": {**base["roles"], "notifier": "opsflow_ingest"}},
            {
                "password_secrets": {
                    **base["password_secrets"],
                    "notifier": base["password_secrets"]["ingest"],
                }
            },
            {"password_secrets": {"migrator": "synthetic_only"}},
        )
        for changed in changes:
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                MODULE.validate({**base, **changed})

    def test_function_only_sql_checks_existing_acl_before_mutation(self):
        sql = MODULE.sql_for(MODULE.validate(opsflow_manifest()))
        database_guard = sql.index("database ACL mismatch")
        schema_guard = sql.index("schema ACL mismatch")
        default_guard = sql.index("default ACL mismatch")
        public_object_guard = sql.index("public schema contains objects")
        first_login = sql.index("ALTER ROLE opsflow_migrator WITH PASSWORD")
        first_budget = sql.index("ALTER ROLE opsflow_migrator CONNECTION LIMIT")
        membership = sql.index(
            "GRANT opsflow_owner TO opsflow_migrator WITH INHERIT FALSE, SET TRUE"
        )
        role_preflight = sql.index("existing role or membership conflict")
        self.assertLess(role_preflight, sql.index("CREATE ROLE opsflow_owner"))
        self.assertLess(database_guard, sql.index("GRANT CONNECT ON DATABASE"))
        self.assertLess(schema_guard, sql.index("GRANT USAGE ON SCHEMA"))
        for guard in (
            database_guard,
            schema_guard,
            default_guard,
            public_object_guard,
        ):
            self.assertLess(guard, first_login)
            self.assertLess(guard, first_budget)
            self.assertLess(guard, membership)
        self.assertIn("unknown role membership", sql)
        self.assertIn("AS initialize_db", sql)
        self.assertIn("\\if :initialize_db", sql)
        self.assertIn("n.nspname='public' AND a.grantee<>n.nspowner", sql)
        self.assertIn("pg_type", sql)

    def test_function_only_does_not_adopt_an_unmarked_database(self):
        sql = MODULE.sql_for(MODULE.validate(opsflow_manifest()))
        self.assertNotIn("database_recoverable", sql)
        self.assertIn("\\if :create_db", sql)
        self.assertIn("unmarked database requires reviewed recovery", sql)
        branch = sql.index("\\if :create_db", sql.index("\\connect opsflow_dev"))
        comment = sql.index("COMMENT ON DATABASE opsflow_dev", branch)
        existing = sql.index("\\else", comment)
        rejection = sql.index("unmarked database requires reviewed recovery", existing)
        self.assertLess(branch, comment)
        self.assertLess(comment, existing)
        self.assertLess(existing, rejection)

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

    def test_monitor_rejects_non_postgres_connect_before_grant_or_login(self):
        sql = self.module.sql()
        guard = sql.index("monitor_cross_database_connect_requires_cluster_review")
        self.assertLess(guard, sql.index("GRANT CONNECT ON DATABASE postgres"))
        self.assertLess(guard, sql.index("ALTER ROLE dev_pg_monitor WITH LOGIN"))
        self.assertIn("d.datallowconn AND d.datname<>'postgres'", sql)
        self.assertIn("has_database_privilege('dev_pg_monitor',d.oid,'CONNECT')", sql)

    def test_monitor_role_has_collector_reads_only_and_follows_its_secret(self):
        sql = self.module.sql()
        self.assertIn(
            "GRANT pg_read_all_stats, pg_read_all_settings TO dev_pg_monitor;", sql
        )
        self.assertIn(
            "GRANT EXECUTE ON FUNCTION pg_catalog.pg_ls_waldir() TO dev_pg_monitor;",
            sql,
        )
        self.assertIn("'REVOKE pg_monitor FROM dev_pg_monitor'", sql)
        self.assertNotIn("GRANT pg_monitor", sql)
        self.assertIn("CONNECTION LIMIT 3", sql)
        self.assertIn("NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION", sql)
        self.assertIn("default_transaction_read_only = on", sql)
        self.assertIn("'dev-pg:development:monitor'", sql)
        self.assertIn("RAISE EXCEPTION 'role ownership mismatch'", sql)
        self.assertEqual(
            ["GRANT CONNECT ON DATABASE postgres TO dev_pg_monitor;"],
            [line for line in sql.splitlines() if line.startswith("GRANT CONNECT")],
        )
        # The secret is checked before any role change and applied every run,
        # so rewriting it and rerunning the job rotates the password.
        password = sql.index("ALTER ROLE dev_pg_monitor WITH LOGIN")
        self.assertLess(sql.index("\\getenv"), sql.index("AS secret_ok"))
        self.assertLess(sql.index("\\if :secret_ok"), sql.index("CREATE ROLE"))
        self.assertLess(sql.index("ownership mismatch"), password)
        self.assertNotIn("\\if :activate", sql)
        self.assertIn("[A-Za-z0-9+/=_-]{16,}", sql)
        self.assertLess(
            sql.index("'REVOKE pg_monitor FROM dev_pg_monitor'"),
            sql.index("monitor role holds memberships beyond its grants"),
        )


if __name__ == "__main__":
    unittest.main()
