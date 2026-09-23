"""`mng-pg-init` bootstrap SQL, executed against a real PostgreSQL.

`tests/validation/test_compose_baseline_gates.py` proves statically that the job
passes every `psql` variable the script reads. Nothing proved the script runs:
it is full of `\\gexec` and `\\connect` meta-commands that only `psql` executes,
and `mng-pg-init` reruns on every `core` start, so a non-idempotent statement
would fail the stack rather than a gate.

Opt-in. The suite skips unless `HYHOME_INTEGRATION=1` and Testcontainers is
installed (`pip install -r tests/requirements-integration.txt`), so repository
discovery stays runnable without a Docker daemon.
"""

from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path

import yaml

try:  # Optional: see the module docstring.
    from testcontainers.postgres import PostgresContainer
except ImportError:  # pragma: no cover - exercised by the skip below.
    PostgresContainer = None

COMPOSE = Path("infra/04-data/operational/mng-db/docker-compose.yml")
INIT_SQL = Path("infra/04-data/operational/mng-db/pg/init-scripts/init_users_dbs.sql")

BOOTSTRAP_USER = "hyhome_admin"
BOOTSTRAP_DB = "postgres"
SERVICE_USERNAME = "app_user"
SERVICE_DB = "app_db"

# Not a credential. PostgreSQL rejects an empty password, so every role in this
# throwaway container gets the same visible placeholder.
PLACEHOLDER = "placeholder-not-a-credential"

FEATURE_ROLES = ("n8n", "keycloak", "airflow", "terrakube", "sonarqube")


def repository_root() -> Path:
    return Path(
        subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )


def init_job_image(root: Path) -> str:
    """The pin the job itself declares, so the test cannot drift from it."""
    document = yaml.safe_load((root / COMPOSE).read_text(encoding="utf-8"))
    return document["services"]["mng-pg-init"]["image"]


@unittest.skipUnless(
    os.environ.get("HYHOME_INTEGRATION") == "1",
    "set HYHOME_INTEGRATION=1 to run integration tests against a Docker daemon",
)
@unittest.skipIf(
    PostgresContainer is None,
    "install tests/requirements-integration.txt to run integration tests",
)
class MngPgInitSqlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = repository_root()
        cls.container = PostgresContainer(
            image=init_job_image(cls.root),
            username=BOOTSTRAP_USER,
            password=PLACEHOLDER,
            dbname=BOOTSTRAP_DB,
        ).with_volume_mapping(str(cls.root / INIT_SQL.parent), "/work", "ro")
        cls.container.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.container.stop()

    def psql(self, *arguments: str) -> tuple[int, str]:
        exit_code, output = self.container.get_wrapped_container().exec_run(
            ["psql", "-U", BOOTSTRAP_USER, "-d", BOOTSTRAP_DB, *arguments],
            user="postgres",
        )
        return exit_code, output.decode("utf-8", "replace")

    def run_init_sql(self) -> tuple[int, str]:
        return self.psql(
            "-v",
            "ON_ERROR_STOP=1",
            *[
                argument
                for role in FEATURE_ROLES
                for argument in ("-v", f"{role}_db_password={PLACEHOLDER}")
            ],
            "-v",
            f"service_postgres_username={SERVICE_USERNAME}",
            "-v",
            f"service_postgres_password={PLACEHOLDER}",
            "-v",
            f"service_postgres_db={SERVICE_DB}",
            "-f",
            f"/work/{INIT_SQL.name}",
        )

    def query(self, sql: str) -> list[str]:
        exit_code, output = self.psql("-tAc", sql)
        self.assertEqual(exit_code, 0, output)
        return [line for line in output.splitlines() if line]

    def test_init_sql_creates_every_role_and_database_and_reruns_cleanly(self) -> None:
        for attempt in ("first", "second"):
            with self.subTest(run=attempt):
                exit_code, output = self.run_init_sql()
                self.assertEqual(exit_code, 0, output)

        expected = sorted((*FEATURE_ROLES, SERVICE_USERNAME))
        self.assertEqual(
            sorted(
                self.query(
                    "SELECT rolname FROM pg_roles"
                    f" WHERE rolname IN ({', '.join(repr(n) for n in expected)})"
                )
            ),
            expected,
        )

        expected_databases = sorted((*FEATURE_ROLES, SERVICE_DB))
        self.assertEqual(
            sorted(
                self.query(
                    "SELECT datname FROM pg_database"
                    f" WHERE datname IN ({', '.join(repr(n) for n in expected_databases)})"
                )
            ),
            expected_databases,
        )

    def test_every_created_database_is_owned_by_its_own_role(self) -> None:
        self.assertEqual(self.run_init_sql()[0], 0)

        owners = dict(
            line.split("|", 1)
            for line in self.query(
                "SELECT datname || '|' || pg_get_userbyid(datdba) FROM pg_database"
                " WHERE datname NOT IN ('postgres', 'template0', 'template1')"
            )
        )
        for role in FEATURE_ROLES:
            self.assertEqual(owners.get(role), role)
        self.assertEqual(owners.get(SERVICE_DB), SERVICE_USERNAME)


if __name__ == "__main__":
    unittest.main()
