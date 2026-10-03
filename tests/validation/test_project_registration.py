"""Synthetic, credential-free checks for external project registration."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validation/check-project-registration.py"
REF = "a" * 40


def registration():
    return {
        "schema_version": 1,
        "interface_version": "1.0",
        "project_id": "example-project",
        "environment": "development",
        "infra_ref": REF,
        "template_ref": REF,
        "project_ref": REF,
        "endpoints": {
            "same_daemon": {
                "db": {"scheme": "postgresql", "host": "dev-pg", "port": 5432, "path": "/example_db"}
            }
        },
        "allowed_networks": ["example-project-net"],
        "db": {
            "name": "example_db",
            "schema": "app",
            "owner_role": "example_owner",
            "migrator_role": "example_migrator",
            "runtime_role": "example_runtime",
            "reader_role": "example_reader",
        },
        "valkey": {"acl_user": "example_user", "acl_prefix": "example-project"},
        "s3": {"bucket": "example-project", "prefix": "example-project/objects/"},
        "oidc": {"client_id": "example-project"},
        "search": {"collection": "example-project", "authorization_path": "/projects/example-project"},
        "telemetry": {"service.name": "example-project"},
        "backup_restore": {"backup_owner": "infra", "restore_owner": "infra"},
        "secret_refs": ["example_project_db_password"],
        "quota": {"cpu_milli": 500, "memory_mib": 512, "storage_gib": 2, "requests_per_minute": 60},
        "approval": {"state": "draft", "task_ref": "SPEC-0204-TSK-0002"},
        "verification": {"state": "not_run"},
    }


class ProjectRegistrationTests(unittest.TestCase):
    def check(self, payload, *options, expected=0, reason=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registration.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(path), *options],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        if reason is not None:
            self.assertIn(f"FAIL ({reason})", result.stdout)
        self.assertNotIn("synthetic", result.stdout + result.stderr)
        return result

    def test_valid_registration_requires_explicit_secret_allowlist(self):
        self.check(registration(), "--allow-secret-ref", "example_project_db_password")
        external = registration()
        external["endpoints"] = {"external": {"api": {"scheme": "https", "host": "api.example.test", "port": 443, "path": "/v1"}}}
        self.check(external, "--allow-secret-ref", "example_project_db_password")
        self.check(registration(), expected=1, reason="explicit valid secret reference allowlist required")

    def test_missing_identity_and_unknown_fields_fail(self):
        for key in ("project_id", "environment", "infra_ref", "template_ref", "project_ref"):
            with self.subTest(key=key):
                candidate = registration()
                del candidate[key]
                self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=1)
        candidate = registration()
        candidate["password"] = "synthetic"
        self.check(
            candidate, "--allow-secret-ref", "example_project_db_password",
            expected=1, reason="schema violation",
        )

    def test_credential_endpoint_forms_fail(self):
        for changed in (
            {"host": "user@dev-pg"},
            {"host": "${DB_HOST}"},
            {"path": "/example?token=synthetic"},
            {"scheme": "postgresql://user:synthetic@dev-pg"},
            {"scheme": "http"},
            {"port": 0},
            {"path": "/../admin"},
        ):
            with self.subTest(changed=changed):
                candidate = registration()
                candidate["endpoints"]["same_daemon"]["db"].update(changed)
                self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=1)

    def test_invalid_resource_scope_and_role_reuse_fail(self):
        cases = (
            ("db", "name", "bad name"),
            ("valkey", "acl_prefix", "other-project:"),
            ("s3", "bucket", "../bad"),
            ("oidc", "client_id", "bad client"),
            ("search", "authorization_path", "https://other"),
            ("search", "authorization_path", "/projects/other-project"),
            ("s3", "prefix", "other-project/objects/"),
        )
        for section, key, value in cases:
            with self.subTest(section=section):
                candidate = registration()
                candidate[section][key] = value
                self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=1)
        candidate = registration()
        candidate["db"]["runtime_role"] = candidate["db"]["owner_role"]
        self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=1)
        candidate = registration()
        candidate["allowed_networks"] = ["host"]
        self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=1)
        candidate = registration()
        for location in ("host", "external"):
            with self.subTest(location=location):
                endpoint = {"scheme": "https", "host": "dev-pg", "port": 443, "path": "/v1"} if location == "external" else {"scheme": "postgresql", "host": "dev-pg", "port": 5432, "path": "/example_db"}
                candidate["endpoints"] = {location: {"api" if location == "external" else "db": endpoint}}
                self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=1)

    def test_endpoint_location_rejects_daemon_dns_and_nonremote_ip(self):
        host_local = registration()
        host_local["endpoints"] = {"host": {"db": {"scheme": "postgresql", "host": "localhost", "port": 5432, "path": "/example_db"}}}
        self.check(host_local, "--allow-secret-ref", "example_project_db_password")
        for host in ("db.example.test", "localhost", "12345", "0x7f000001"):
            with self.subTest(location="same_daemon", host=host):
                candidate = registration()
                candidate["endpoints"]["same_daemon"]["db"]["host"] = host
                self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=1)
        for host in ("localhost", "127.0.0.1", "127.1", "0177.0.0.1", "0.0.0.0", "169.254.2.3"):
            with self.subTest(location="external", host=host):
                candidate = registration()
                candidate["endpoints"] = {"external": {"api": {"scheme": "https", "host": host, "port": 443, "path": "/v1"}}}
                self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=1)

    def test_external_endpoint_requires_tls_and_defers_database(self):
        cases = (
            ("api", "http", 80, "/v1", 1),
            ("valkey", "redis", 6379, "/0", 1),
            ("db", "postgresql", 5432, "/example_db", 1),
            ("api", "https", 443, "/v1", 0),
            ("valkey", "rediss", 6380, "/0", 0),
        )
        for service, scheme, port, path, expected in cases:
            with self.subTest(service=service, scheme=scheme):
                candidate = registration()
                candidate["endpoints"] = {"external": {service: {"scheme": scheme, "host": "service.example.test", "port": port, "path": path}}}
                self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=expected)

    def test_dev_data_contract_matches_provisioners(self):
        self.check(registration(), "--allow-secret-ref", "example_project_db_password")
        cases = (
            ("environment", None, "production"),
            ("db", "name", "postgres"),
            ("db", "name", "app_db"),
            ("db", "name", "pg_internal"),
            ("db", "schema", "public"),
            ("db", "schema", "pg_catalog"),
            ("db", "owner_role", "postgres"),
            ("db", "owner_role", "example_db"),
            ("db", "owner_role", "app"),
            ("db", "runtime_role", "pg_internal"),
            ("valkey", "acl_user", "default"),
            ("valkey", "acl_user", "devadmin"),
            ("valkey", "acl_prefix", "example-project:"),
        )
        for section, key, value in cases:
            with self.subTest(section=section, key=key, value=value):
                candidate = registration()
                if key is None:
                    candidate[section] = value
                else:
                    candidate[section][key] = value
                    if section == "db" and key == "name":
                        candidate["endpoints"]["same_daemon"]["db"]["path"] = f"/{value}"
                self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=1)
        candidate = registration()
        candidate["endpoints"]["same_daemon"]["db"]["path"] = "/other_db"
        self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=1)

    def test_unapproved_secret_and_duplicate_json_key_fail(self):
        self.check(registration(), "--allow-secret-ref", "other_ref", expected=1, reason="secret reference not allowed")
        candidate = registration()
        candidate["secret_refs"] = ["example_project_db_password", "other_ref"]
        self.check(candidate, "--allow-secret-ref", "example_project_db_password", expected=1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            document = json.dumps(registration())
            path.write_text(document[:-1] + ',"project_id":"example-project"}', encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(path), "--allow-secret-ref", "example_project_db_password"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(1, result.returncode)


if __name__ == "__main__":
    unittest.main()
