"""Guard LAB credential paths against regressions into process arguments."""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


class LabCredentialArgvTest(unittest.TestCase):
    def test_haproxy_password_is_not_passed_to_sed_argv(self):
        compose = yaml.safe_load((ROOT / "labs/postgresql-ha.yml").read_text())
        command = compose["services"]["pg-router"]["command"][2]
        fixture_value = "HAp9+#%"

        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            secret = work / "password"
            template = work / "haproxy.cfg.tpl"
            output = work / "haproxy.cfg"
            sed_script = work / "haproxy-secret.sed"
            args_log = work / "sed.argv"
            fake_sed = work / "sed"
            secret.write_text(fixture_value)
            template.write_text("stats auth admin:${HAPROXY_STATS_PASSWORD}\n")
            real_sed = shutil.which("sed")
            self.assertIsNotNone(real_sed)
            fake_sed.write_text(
                '#!/bin/sh\nprintf \'%s\\n\' "$@" > "$SED_ARGS_LOG"\n'
                f'exec {real_sed} "$@"\n'
            )
            fake_sed.chmod(0o700)
            command = (
                command.replace(
                    "/run/secrets/lab_pg_haproxy_stats_password", str(secret)
                )
                .replace("/tmp/haproxy.cfg.tpl", str(template))
                .replace("/tmp/haproxy-secret.sed", str(sed_script))
                .replace("/tmp/haproxy.cfg", str(output))
                .replace("exec haproxy -W -db -f " + str(output), "exit 0")
                .replace("$$", "$")
            )
            env = {
                **os.environ,
                "PATH": f"{work}:{os.environ['PATH']}",
                "SED_ARGS_LOG": str(args_log),
            }
            result = subprocess.run(
                ["sh", "-ec", command],
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn(fixture_value, args_log.read_text())
            self.assertEqual(output.read_text(), f"stats auth admin:{fixture_value}\n")
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            self.assertFalse(sed_script.exists())

    def test_postgres_password_sql_suppresses_statement_logging(self):
        for relative_path in (
            "infra/04-data/mng-db/pg/init-scripts/init_users_dbs.sql",
            "infra/04-data/postgresql-cluster/init-scripts/init_users_dbs.sql",
        ):
            with self.subTest(path=relative_path):
                sql = (ROOT / relative_path).read_text()
                for session in re.split(r"(?m)^\\connect .*$", sql):
                    if "PASSWORD" not in session:
                        continue
                    with self.subTest(session=session[:40]):
                        self.assertIn("SET log_statement = 'none';", session)
                        self.assertIn("SET log_min_error_statement = 'panic';", session)
                        self.assertLess(
                            session.index("SET log_min_error_statement"),
                            session.index("PASSWORD"),
                        )

    def test_opensearch_hashing_uses_supported_environment_input(self):
        entrypoint = (
            ROOT / "infra/04-data/opensearch/opensearch/opensearch-entrypoint.sh"
        ).read_text()

        self.assertNotIn('hash.sh" -p', entrypoint)
        self.assertIn('hash.sh" -env OPENSEARCH_HASH_PASSWORD', entrypoint)

    def test_passwords_do_not_enter_cli_arguments(self):
        valkey = (ROOT / "labs/valkey-cluster.yml").read_text()
        mongo = (ROOT / "labs/mongodb.yml").read_text()
        pg = (ROOT / "labs/postgresql-ha.yml").read_text()
        couch = (ROOT / "labs/couchdb.yml").read_text()
        opensearch = (ROOT / "labs/opensearch-cluster.yml").read_text()
        valkey_start = (
            ROOT / "infra/04-data/valkey-cluster/scripts/valkey-start.sh"
        ).read_text()
        valkey_init = (
            ROOT / "infra/04-data/valkey-cluster/scripts/valkey-cluster-init.sh"
        ).read_text()
        couch_init = (ROOT / "labs/couchdb-cluster-init.sh").read_text()

        self.assertNotIn("valkey-cli -a", valkey + valkey_init)
        self.assertNotIn('--requirepass "$password"', valkey_start)
        self.assertIn('exec valkey-server "$config"', valkey_start)
        self.assertNotIn("-redis.password=", valkey)
        self.assertNotIn(" -p $$MONGO_ROOT_PASSWORD", mongo)
        self.assertNotIn("$${MONGO_ROOT_PASSWORD}@", mongo)
        # The init reads the password from the secret into env, not argv;
        # the exporter that took MONGODB_PASSWORD is retired (SPEC-0215).
        self.assertIn("process.env.MONGO_ROOT_PASSWORD", mongo)
        self.assertNotIn("mongodb_exporter", mongo)
        self.assertNotIn("-v patroni_exporter_password=", pg)
        self.assertNotIn("-v service_postgres_password=", pg)
        self.assertIn("DATA_SOURCE_PASS_FILE", pg)
        self.assertNotIn("COUCHDB_PASSWORD@", couch + couch_init)
        self.assertIn("--config /tmp/couch-auth.conf", couch_init)
        self.assertNotIn("curl -fsSk -u", opensearch)
        self.assertIn("curl -fsSk --config -", opensearch)

    def test_couch_system_database_replay_accepts_existing_and_fails_other_errors(self):
        source = (ROOT / "labs/couchdb-cluster-init.sh").read_text()
        function = (
            "ensure_system_databases() {"
            + source.split("ensure_system_databases() {", 1)[1].split("\n}\n", 1)[0]
            + "\n}\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake_curl = root / "curl"
            fake_curl.write_text(
                '#!/bin/sh\nprintf \'%s\\n\' "$*" >> "$CALLS_FILE"\n'
                "case \"$*\" in *'_replicator'*) "
                "printf '%s' \"${REPLICATOR_STATUS:-412}\" ;; "
                "*) printf '%s' 201 ;; esac\n"
            )
            fake_curl.chmod(0o700)
            program = (
                "set -eu\nbase=http://example.invalid\n"
                + function
                + "ensure_system_databases\n"
            )
            env = {
                **os.environ,
                "PATH": f"{root}:{os.environ['PATH']}",
                "CALLS_FILE": str(root / "calls"),
            }
            result = subprocess.run(
                ["sh", "-c", program],
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len((root / "calls").read_text().splitlines()), 3)
            env["REPLICATOR_STATUS"] = "500"
            result = subprocess.run(
                ["sh", "-c", program],
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("_replicator (HTTP 500)", result.stderr)

    def test_lab_image_and_restart_boundaries(self):
        cassandra = (ROOT / "labs/cassandra.yml").read_text()
        mongo = (ROOT / "labs/mongodb.yml").read_text()
        couch_init = (ROOT / "labs/couchdb-cluster-init.sh").read_text()
        valkey_init = (
            ROOT / "infra/04-data/valkey-cluster/scripts/valkey-cluster-init.sh"
        ).read_text()

        self.assertIn("cassandra-node1-volume:/var/lib/cassandra:rw", cassandra)
        self.assertNotIn("/bitnami/cassandra", cassandra)
        self.assertNotIn("CASSANDRA_PASSWORD_FILE", cassandra)
        self.assertNotIn("bitnami/cassandra-exporter", cassandra)
        self.assertIn("network_mode: none", mongo)
        self.assertNotIn("apk add", mongo)
        self.assertIn("require('crypto').randomBytes", mongo)
        self.assertIn("mongodb-arbiter:\n        condition: service_healthy", mongo)
        self.assertIn(
            "ensure_system_databases\n  echo 'LAB CouchDB cluster is already configured'",
            couch_init,
        )
        self.assertIn("ensure_system_databases\nrm -f", couch_init)
        self.assertIn("cluster state is not healthy", valkey_init)
        self.assertNotIn("Skipping destructive re-init.\n  exit 0", valkey_init)


if __name__ == "__main__":
    unittest.main()
