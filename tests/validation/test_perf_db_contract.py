"""Static contract tests for the shared performance-result database."""

import importlib.util
import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PERF = ROOT / "infra/04-data/dev-db/pg/perf"
SOURCE = PERF / "register.py"
SPEC = importlib.util.spec_from_file_location("perf_db_register", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def manifest():
    return {
        "schema_version": 1,
        "project_id": "example-quality",
        "roles": {
            "reader": "example_quality_reader",
            "writer": "example_quality_writer",
            "verdict": "example_quality_verdict",
        },
    }


class PerfDatabaseContractTests(unittest.TestCase):
    def test_project_registration_uses_distinct_non_login_roles(self):
        project = MODULE.validate(manifest())
        sql = MODULE.sql_for(project)

        for kind, role in project["roles"].items():
            with self.subTest(kind=kind):
                self.assertIn(f"CREATE ROLE {role} NOLOGIN", sql)
                self.assertIn(f"dev-pg:development:perf_db:example-quality:{kind}", sql)
                self.assertIn("FROM pg_auth_members", sql)
        self.assertNotIn(" PASSWORD ", sql)
        self.assertNotIn(" LOGIN", sql)
        self.assertIn("perf_db:project-registration", sql)
        self.assertIn("INSERT INTO quality.projects", sql)
        self.assertIn("project role already assigned", sql)

    def test_project_roles_receive_only_their_quality_authority(self):
        sql = MODULE.sql_for(MODULE.validate(manifest()))

        self.assertIn(
            "GRANT SELECT ON quality.run_attempts, quality.artifacts, "
            "quality.metric_summaries, quality.verdict_events",
            sql,
        )
        self.assertIn(
            "GRANT EXECUTE ON FUNCTION quality.import_payload(jsonb, bytea)", sql
        )
        self.assertIn(
            "GRANT INSERT (decision_id, run_id, attempt, project_id, verdict, reason)",
            sql,
        )
        self.assertNotIn("GRANT INSERT ON quality.verdict_events", sql)
        self.assertNotIn("GRANT INSERT ON quality.run_attempts", sql)
        self.assertNotIn("claim_run_attempt(uuid", sql)
        self.assertNotIn("GRANT UPDATE", sql)
        self.assertNotIn("GRANT DELETE", sql)
        self.assertNotIn(
            "GRANT INSERT ON quality.verdict_events TO example_quality_writer", sql
        )
        self.assertNotIn("GRANT perf_owner", sql)

    def test_manifest_rejects_implicit_or_unsafe_authority(self):
        for changed in (
            {"extra": "ignored"},
            {"project_id": "../other"},
            {"roles": {**manifest()["roles"], "reader": "perf_owner"}},
            {
                "roles": {
                    **manifest()["roles"],
                    "verdict": "example_quality_writer",
                }
            },
            {"schema_version": 2},
        ):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                MODULE.validate({**manifest(), **changed})

    def test_tracked_example_is_valid_but_does_not_issue_credentials(self):
        fixture = json.loads((PERF / "project.example.json").read_text())
        self.assertEqual(MODULE.validate(fixture), MODULE.validate(manifest()))
        self.assertNotIn("password", json.dumps(fixture).lower())

    def test_schema_forces_project_rls_and_immutable_result_rows(self):
        sql = (PERF / "schema.sql").read_text()

        for table in (
            "run_attempts",
            "artifacts",
            "metric_summaries",
            "verdict_events",
        ):
            with self.subTest(table=table):
                self.assertIn(
                    f"ALTER TABLE quality.{table} ENABLE ROW LEVEL SECURITY", sql
                )
                self.assertIn(
                    f"ALTER TABLE quality.{table} FORCE ROW LEVEL SECURITY", sql
                )
        self.assertIn("quality.has_project_access", sql)
        self.assertIn("quality.claim_run_attempt", sql)
        self.assertIn("quality.import_payload", sql)
        self.assertIn("DROP FUNCTION IF EXISTS quality.import_payload(jsonb)", sql)
        self.assertIn("hyhome.quality-import/v1", sql)
        self.assertIn("sha256(p_unsigned_payload)", sql)
        self.assertIn("p_payload - 'payload_sha256'", sql)
        self.assertIn("jsonb_array_elements(p_payload->'artifacts')", sql)
        self.assertIn("jsonb_array_elements(p_payload->'metrics')", sql)
        self.assertIn("RAISE EXCEPTION 'run attempt identity conflict'", sql)
        self.assertIn("PRIMARY KEY (run_id, attempt)", sql)
        self.assertIn("reported_verdict", sql)
        self.assertIn("CREATE TABLE IF NOT EXISTS quality.verdict_events", sql)
        self.assertNotIn("GRANT UPDATE", sql)
        self.assertNotIn("GRANT DELETE", sql)
        self.assertIn("security_invoker = true", sql)

    def test_schema_rejects_false_complete_or_invalid_summary_shapes(self):
        sql = (PERF / "schema.sql").read_text()

        self.assertIn("samples > 0", sql)
        self.assertIn("execution_state = 'completed'", sql)
        self.assertIn("jsonb_typeof(values) = 'object'", sql)
        self.assertIn("jsonb_typeof(thresholds) = 'object'", sql)
        self.assertIn("bytes >= 0", sql)
        self.assertIn("execution_state = 'interrupted'", sql)
        self.assertIn("reported_verdict NOT IN ('passed', 'failed_threshold')", sql)
        self.assertIn("reported_verdict = 'incomplete'", sql)
        self.assertIn("ALTER COLUMN started_at DROP NOT NULL", sql)
        self.assertIn("run_attempts_timestamp_consistency", sql)
        self.assertIn("VALIDATE CONSTRAINT run_attempts_incomplete_consistency", sql)
        self.assertIn("VALUES (1), (2)", sql)
        self.assertIn("octet_length(p_unsigned_payload) > 1048576", sql)
        self.assertIn("started_at IS NULL AND ended_at IS NULL", sql)
        self.assertIn("started_at IS NOT NULL", sql)
        self.assertIn("ended_at >= started_at", sql)

    def test_bootstrap_is_fixed_name_idempotent_and_secret_free(self):
        sql = (PERF / "bootstrap.sql").read_text()

        self.assertIn("CREATE ROLE perf_owner NOLOGIN", sql)
        self.assertIn("CREATE ROLE perf_migrator NOLOGIN", sql)
        self.assertIn("CREATE DATABASE perf_db OWNER perf_owner", sql)
        self.assertIn("\\ir schema.sql", sql)
        self.assertIn("role ownership mismatch", sql)
        self.assertIn("database ownership mismatch", sql)
        self.assertIn("FROM pg_auth_members", sql)
        self.assertNotIn("PASSWORD", sql.upper())
        self.assertNotIn("/run/secrets", sql)

    def test_quality_results_profile_consumes_perf_bootstrap_as_one_shot_job(self):
        compose = yaml.safe_load((PERF.parents[1] / "docker-compose.yml").read_text())
        services = compose["services"]
        dev_pg = services["dev-pg"]
        job = services["dev-perf-provision"]

        self.assertIn("quality-results", dev_pg["profiles"])
        self.assertNotIn("testing", dev_pg["profiles"])
        self.assertEqual(["quality-results"], job["profiles"])
        self.assertEqual("no", job["restart"])
        self.assertEqual(["python3", "/work/perf/provision.py"], job["entrypoint"])
        self.assertEqual("1", job["environment"]["PYTHONDONTWRITEBYTECODE"])
        self.assertEqual(["./pg/perf:/work/perf:ro"], job["volumes"])
        self.assertEqual(["dev_pg_admin_password"], job["secrets"])
        self.assertEqual("service_healthy", job["depends_on"]["dev-pg"]["condition"])
        self.assertEqual({"dev_data_net": {}}, job["networks"])
        self.assertNotIn("ports", job)

    def test_compose_provisioner_holds_cluster_lock_without_secret_argv(self):
        source = (PERF / "provision.py").read_text()

        self.assertIn("pg_try_advisory_lock", source)
        self.assertIn("subprocess.Popen", source)
        self.assertIn('env["PGPASSWORD"]', source)
        self.assertIn('"/work/perf/bootstrap.sql"', source)
        self.assertNotIn("PGPASSWORD=", source)


if __name__ == "__main__":
    unittest.main()
