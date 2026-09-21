"""Compose baseline gates and PostgreSQL initialization contracts.

Both gates run in CI through `.github/workflow-contract.yml` and neither had a
covering test, so nothing proved they could go red. Each script resolves the
repository root with `git rev-parse --show-toplevel` and reads its subject from
`docker compose config --format json`, so the fixtures here are a throwaway Git
repository plus a `docker` shim on `PATH` that prints a crafted document.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUICKWIN = ROOT / "scripts/validation/check-quickwin-baseline.sh"
TEMPLATE_SECURITY = ROOT / "scripts/validation/check-template-security-baseline.sh"
VALIDATE_COMPOSE = ROOT / "scripts/validation/validate-docker-compose.sh"

COMPLIANT_SERVICE = {
    "restart": "unless-stopped",
    "healthcheck": {"test": ["CMD", "true"]},
    "security_opt": ["no-new-privileges:true"],
    "cpus": "1.0",
    "mem_limit": "512m",
    "secrets": ["example_secret"],
    "cap_drop": ["ALL"],
}

EMPTY_EXCEPTIONS = {
    "quickwin_baseline": {"healthcheck_exceptions": [], "secrets_exceptions": []},
    "template_adoption": {
        "required_reference": "common-optimizations.yml",
        "file_exceptions": [],
    },
    "security_baseline": {
        "no_new_privileges_exceptions": [],
        "cap_drop_all_exceptions": [],
    },
}


def compliant_config(*names: str) -> dict[str, dict[str, dict[str, object]]]:
    return {"services": {name: dict(COMPLIANT_SERVICE) for name in names}}


class BaselineGateHarness(unittest.TestCase):
    """A disposable repository the gates can be pointed at."""

    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        subprocess.run(
            ["git", "init", "--quiet"],
            cwd=self.root,
            check=True,
            capture_output=True,
        )
        (self.root / ".env.example").write_text("EXAMPLE=1\n", encoding="utf-8")
        (self.root / "infra").mkdir()
        self.write_exceptions(EMPTY_EXCEPTIONS)
        self.write_compose_file(
            "infra/docker-compose.yml", "include: common-optimizations.yml\n"
        )
        self.bin = self.root / "fakebin"
        self.bin.mkdir()
        self.config_path = self.root / "compose-config.json"
        docker = self.bin / "docker"
        docker.write_text(
            '#!/usr/bin/env bash\nset -eu\ncat "$FAKE_COMPOSE_CONFIG"\n',
            encoding="utf-8",
        )
        docker.chmod(0o755)

    def write_exceptions(self, payload: object) -> None:
        path = self.root / "infra/common-optimizations.exceptions.json"
        path.write_text(json.dumps(payload), encoding="utf-8")

    def write_compose_file(self, relative: str, body: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")

    def gate_env(self) -> dict[str, str]:
        return {
            **os.environ,
            "PATH": os.fspath(self.bin) + os.pathsep + os.environ["PATH"],
            "FAKE_COMPOSE_CONFIG": os.fspath(self.config_path),
        }

    def write_config(self, config: object) -> None:
        self.config_path.write_text(json.dumps(config), encoding="utf-8")

    def run_gate(
        self, script: Path, config: object
    ) -> subprocess.CompletedProcess[str]:
        """Run the tracked script itself, against the disposable repository.

        Each gate resolves its own root with `git rev-parse --show-toplevel`,
        so invoking the real file with `cwd` set to the fixture points it at
        the fixture without copying it. A copy would leave these tests passing
        while the tracked script rotted.
        """

        self.write_config(config)
        return subprocess.run(
            ["bash", os.fspath(script)],
            cwd=self.root,
            capture_output=True,
            text=True,
            env=self.gate_env(),
            check=False,
        )


class ComposeSelectionValidationTests(unittest.TestCase):
    def _run_port_matrix(
        self, services: dict[str, dict[str, object]]
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(
                ["git", "init", "--quiet"],
                cwd=root,
                check=True,
                capture_output=True,
            )
            (root / ".env.example").write_text("EXAMPLE=1\n", encoding="utf-8")
            policy = (
                root / "docs/05.operations/catalog/00-workspace/"
                "0078-compose-profile-vocabulary/policy.md"
            )
            policy.parent.mkdir(parents=True)
            policy.write_text(
                "| Named selection | Profiles | Forbidden categories |\n"
                "| --- | --- | --- |\n"
                "| HOME | `alpha`, `beta` | "
                "`automation`, `lifecycle`, `topology` |\n",
                encoding="utf-8",
            )
            fakebin = root / "fakebin"
            fakebin.mkdir()
            docker = fakebin / "docker"
            docker.write_text(
                """#!/usr/bin/env python3
import json
import os
import sys

args = sys.argv[1:]
if "--profiles" in args:
    print("alpha")
    print("beta")
    raise SystemExit(0)
profiles = [
    args[index + 1]
    for index, value in enumerate(args)
    if value == "--profile"
]
all_services = json.loads(os.environ["FAKE_COMPOSE_SERVICES"])
services = {profile: all_services[profile] for profile in profiles}
if "--services" in args:
    print("\\n".join(services))
else:
    print(json.dumps({"services": services}))
""",
                encoding="utf-8",
            )
            docker.chmod(0o755)
            return subprocess.run(
                ["bash", os.fspath(VALIDATE_COMPOSE)],
                cwd=root,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    "PATH": os.fspath(fakebin) + os.pathsep + os.environ["PATH"],
                    "FAKE_COMPOSE_SERVICES": json.dumps(services),
                },
                check=False,
            )

    def test_default_mode_checks_home_union_for_cross_profile_port_collisions(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(
                ["git", "init", "--quiet"],
                cwd=root,
                check=True,
                capture_output=True,
            )
            (root / ".env.example").write_text("EXAMPLE=1\n", encoding="utf-8")
            policy = (
                root / "docs/05.operations/catalog/00-workspace/"
                "0078-compose-profile-vocabulary/policy.md"
            )
            policy.parent.mkdir(parents=True)
            policy.write_text(
                "| Named selection | Profiles | Forbidden categories |\n"
                "| --- | --- | --- |\n"
                "| HOME | `alpha`, `beta` | "
                "`automation`, `lifecycle`, `topology` |\n",
                encoding="utf-8",
            )
            fakebin = root / "fakebin"
            fakebin.mkdir()
            docker = fakebin / "docker"
            docker.write_text(
                """#!/usr/bin/env python3
import json
import sys

args = sys.argv[1:]
if "--profiles" in args:
    print("alpha")
    print("beta")
    raise SystemExit(0)
profiles = [
    args[index + 1]
    for index, value in enumerate(args)
    if value == "--profile"
]
services = {
    profile: {
        "ports": [
            {
                "host_ip": "127.0.0.1",
                "published": "18080",
                "protocol": "tcp",
            }
        ]
    }
    for profile in profiles
}
if "--services" in args:
    print("\\n".join(services))
elif "--format" in args:
    print(json.dumps({"services": services}))
else:
    print(json.dumps({"services": services}))
""",
                encoding="utf-8",
            )
            docker.chmod(0o755)
            result = subprocess.run(
                ["bash", os.fspath(VALIDATE_COMPOSE)],
                cwd=root,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    "PATH": os.fspath(fakebin) + os.pathsep + os.environ["PATH"],
                },
                check=False,
            )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL: HOME:", result.stdout)

    def test_ipv4_wildcard_and_omitted_host_overlap_specific_address(self) -> None:
        for wildcard in ({"host_ip": "0.0.0.0"}, {}):
            with self.subTest(wildcard=wildcard):
                result = self._run_port_matrix(
                    {
                        "alpha": {
                            "ports": [
                                {
                                    **wildcard,
                                    "published": "18080",
                                    "protocol": "tcp",
                                }
                            ]
                        },
                        "beta": {
                            "ports": [
                                {
                                    "host_ip": "127.0.0.1",
                                    "published": "18080",
                                    "protocol": "tcp",
                                }
                            ]
                        },
                    }
                )
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("FAIL: HOME:", result.stdout)

    def test_ipv6_wildcard_overlaps_specific_ipv6_address(self) -> None:
        result = self._run_port_matrix(
            {
                "alpha": {
                    "ports": [
                        {
                            "host_ip": "::",
                            "published": "18080",
                            "protocol": "tcp",
                        }
                    ]
                },
                "beta": {
                    "ports": [
                        {
                            "host_ip": "::1",
                            "published": "18080",
                            "protocol": "tcp",
                        }
                    ]
                },
            }
        )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL: HOME:", result.stdout)

    def test_omitted_or_empty_host_overlaps_specific_ipv6_address(self) -> None:
        for implicit in ({}, {"host_ip": ""}):
            with self.subTest(implicit=implicit):
                result = self._run_port_matrix(
                    {
                        "alpha": {
                            "ports": [
                                {
                                    **implicit,
                                    "published": "18080",
                                    "protocol": "tcp",
                                }
                            ]
                        },
                        "beta": {
                            "ports": [
                                {
                                    "host_ip": "::1",
                                    "published": "18080",
                                    "protocol": "tcp",
                                }
                            ]
                        },
                    }
                )
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("FAIL: HOME:", result.stdout)

    def test_ipv4_mapped_ipv6_addresses_overlap_native_ipv4_bindings(self) -> None:
        cases = (
            ("same specific address", "::ffff:127.0.0.1", "127.0.0.1"),
            ("mapped wildcard", "::ffff:0.0.0.0", "127.0.0.1"),
        )
        for label, mapped, native in cases:
            with self.subTest(case=label):
                result = self._run_port_matrix(
                    {
                        "alpha": {
                            "ports": [
                                {
                                    "host_ip": mapped,
                                    "published": "18080",
                                    "protocol": "tcp",
                                }
                            ]
                        },
                        "beta": {
                            "ports": [
                                {
                                    "host_ip": native,
                                    "published": "18080",
                                    "protocol": "tcp",
                                }
                            ]
                        },
                    }
                )
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("FAIL: HOME:", result.stdout)

    def test_nonoverlapping_address_family_and_protocol_bindings_pass(self) -> None:
        cases = (
            ("distinct IPv4", "127.0.0.1", "127.0.0.2", "tcp", "tcp"),
            ("distinct IPv6", "::1", "2001:db8::1", "tcp", "tcp"),
            ("separate families", "0.0.0.0", "::", "tcp", "tcp"),
            ("separate protocols", "0.0.0.0", "127.0.0.1", "tcp", "udp"),
        )
        for label, first_host, second_host, first_protocol, second_protocol in cases:
            with self.subTest(case=label):
                result = self._run_port_matrix(
                    {
                        "alpha": {
                            "ports": [
                                {
                                    "host_ip": first_host,
                                    "published": "18080",
                                    "protocol": first_protocol,
                                }
                            ]
                        },
                        "beta": {
                            "ports": [
                                {
                                    "host_ip": second_host,
                                    "published": "18080",
                                    "protocol": second_protocol,
                                }
                            ]
                        },
                    }
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn("Docker Compose validation passed", result.stdout)

    def test_invalid_host_ip_fails_closed(self) -> None:
        result = self._run_port_matrix(
            {
                "alpha": {
                    "ports": [
                        {
                            "host_ip": "not-an-ip",
                            "published": "18080",
                            "protocol": "tcp",
                        }
                    ]
                },
                "beta": {"ports": []},
            }
        )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("invalid host IP", result.stdout + result.stderr)


class QuickwinBaselineTests(BaselineGateHarness):
    def test_the_tracked_script_runs(self) -> None:
        self.write_config(compliant_config("alpha"))
        result = subprocess.run(
            ["bash", os.fspath(QUICKWIN)],
            cwd=self.root,
            capture_output=True,
            text=True,
            env=self.gate_env(),
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_compliant_services_pass(self) -> None:
        result = self.run_gate(QUICKWIN, compliant_config("alpha", "beta"))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: baseline enforced", result.stdout)

    def test_every_required_control_can_fail_independently(self) -> None:
        for key, label in (
            ("restart", "restart"),
            ("healthcheck", "healthcheck"),
            ("security_opt", "no-new-privileges"),
            ("cpus", "cpus"),
            ("mem_limit", "mem_limit"),
            ("secrets", "secrets"),
        ):
            with self.subTest(control=key):
                config = compliant_config("alpha")
                del config["services"]["alpha"][key]
                result = self.run_gate(QUICKWIN, config)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("FAIL: baseline violations detected", result.stdout)
                self.assertIn(f"alpha: {label}", result.stdout)

    def test_one_noncompliant_service_fails_a_compliant_pair(self) -> None:
        config = compliant_config("alpha", "beta")
        del config["services"]["beta"]["mem_limit"]
        result = self.run_gate(QUICKWIN, config)
        self.assertEqual(1, result.returncode)
        self.assertIn("beta: mem_limit", result.stdout)
        self.assertNotIn("alpha:", result.stdout.split("FAIL:")[1])

    def test_registered_exceptions_are_honoured(self) -> None:
        self.write_exceptions(
            {
                **EMPTY_EXCEPTIONS,
                "quickwin_baseline": {
                    "healthcheck_exceptions": [{"service": "alpha"}],
                    "secrets_exceptions": [{"service": "alpha"}],
                },
            }
        )
        config = compliant_config("alpha")
        del config["services"]["alpha"]["healthcheck"]
        del config["services"]["alpha"]["secrets"]
        result = self.run_gate(QUICKWIN, config)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: baseline enforced", result.stdout)

    def test_an_exception_covers_only_the_service_it_names(self) -> None:
        self.write_exceptions(
            {
                **EMPTY_EXCEPTIONS,
                "quickwin_baseline": {
                    "healthcheck_exceptions": [{"service": "alpha"}],
                    "secrets_exceptions": [],
                },
            }
        )
        config = compliant_config("alpha", "beta")
        del config["services"]["beta"]["healthcheck"]
        result = self.run_gate(QUICKWIN, config)
        self.assertEqual(1, result.returncode)
        self.assertIn("beta: healthcheck", result.stdout)

    def test_missing_exceptions_registry_fails_closed(self) -> None:
        (self.root / "infra/common-optimizations.exceptions.json").unlink()
        result = self.run_gate(QUICKWIN, compliant_config("alpha"))
        self.assertEqual(2, result.returncode)
        self.assertIn("exceptions registry not found", result.stderr)

    def test_empty_service_set_fails_rather_than_passing_vacuously(self) -> None:
        result = self.run_gate(QUICKWIN, {"services": {}})
        self.assertEqual(1, result.returncode)
        self.assertIn("service count is 0", result.stderr)


class TemplateSecurityBaselineTests(BaselineGateHarness):
    def test_the_tracked_script_runs(self) -> None:
        self.write_config(compliant_config("alpha"))
        result = subprocess.run(
            ["bash", os.fspath(TEMPLATE_SECURITY)],
            cwd=self.root,
            capture_output=True,
            text=True,
            env=self.gate_env(),
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_compliant_repository_passes(self) -> None:
        result = self.run_gate(TEMPLATE_SECURITY, compliant_config("alpha"))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: template adoption", result.stdout)

    def test_compose_file_without_the_required_reference_fails(self) -> None:
        self.write_compose_file("infra/docker-compose.extra.yml", "services: {}\n")
        result = self.run_gate(TEMPLATE_SECURITY, compliant_config("alpha"))
        self.assertEqual(1, result.returncode)
        self.assertIn("template adoption missing", result.stdout)
        self.assertIn("infra/docker-compose.extra.yml", result.stdout)

    def test_missing_no_new_privileges_fails(self) -> None:
        config = compliant_config("alpha")
        config["services"]["alpha"]["security_opt"] = []
        result = self.run_gate(TEMPLATE_SECURITY, config)
        self.assertEqual(1, result.returncode)
        self.assertIn("no-new-privileges missing", result.stdout)
        self.assertIn("- alpha", result.stdout)

    def test_missing_cap_drop_all_fails(self) -> None:
        config = compliant_config("alpha")
        config["services"]["alpha"]["cap_drop"] = ["NET_RAW"]
        result = self.run_gate(TEMPLATE_SECURITY, config)
        self.assertEqual(1, result.returncode)
        self.assertIn("cap_drop ALL missing", result.stdout)

    def test_registered_exceptions_are_honoured(self) -> None:
        self.write_compose_file("infra/docker-compose.extra.yml", "services: {}\n")
        self.write_exceptions(
            {
                **EMPTY_EXCEPTIONS,
                "template_adoption": {
                    "required_reference": "common-optimizations.yml",
                    "file_exceptions": ["infra/docker-compose.extra.yml"],
                },
                "security_baseline": {
                    "no_new_privileges_exceptions": [{"service": "alpha"}],
                    "cap_drop_all_exceptions": [{"service": "alpha"}],
                },
            }
        )
        config = compliant_config("alpha")
        config["services"]["alpha"]["security_opt"] = []
        config["services"]["alpha"]["cap_drop"] = []
        result = self.run_gate(TEMPLATE_SECURITY, config)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: template adoption", result.stdout)

    def test_yaml_suffixed_compose_files_are_reported_as_excluded(self) -> None:
        self.write_compose_file("infra/docker-compose.legacy.yaml", "services: {}\n")
        result = self.run_gate(TEMPLATE_SECURITY, compliant_config("alpha"))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("compose_yaml_files_excluded=1", result.stdout)
        self.assertIn("infra/docker-compose.legacy.yaml", result.stdout)

    def test_missing_exceptions_registry_fails_closed(self) -> None:
        (self.root / "infra/common-optimizations.exceptions.json").unlink()
        result = self.run_gate(TEMPLATE_SECURITY, compliant_config("alpha"))
        self.assertEqual(2, result.returncode)
        self.assertIn("exceptions registry not found", result.stderr)

    def test_empty_service_set_fails_rather_than_passing_vacuously(self) -> None:
        result = self.run_gate(TEMPLATE_SECURITY, {"services": {}})
        self.assertEqual(1, result.returncode)
        self.assertIn("service count is 0", result.stderr)


class PostgresInitializationContractTests(unittest.TestCase):
    # Connection targeting checks without accessing a PostgreSQL runtime.
    def init_scripts(self) -> list[str]:
        return [
            (ROOT / path).read_text(encoding="utf-8")
            for path in (
                "infra/04-data/operational/mng-db/pg/init-scripts/init_users_dbs.sql",
                "infra/04-data/relational/postgresql-cluster/init-scripts/init_users_dbs.sql",
            )
        ]

    def test_schema_permissions_follow_a_direct_fail_closed_connection(self) -> None:
        for index, sql in enumerate(self.init_scripts()):
            with self.subTest(script=index):
                self.assertTrue(sql.startswith("\\set ON_ERROR_STOP on\n"))
                self.assertNotRegex(sql, r"SELECT format\('[^']*\\connect")
                self.assertIn(
                    "\\gset\n\\connect -reuse-previous=on :service_postgres_conninfo\n",
                    sql,
                )
                self.assertLess(
                    sql.index(
                        "\\connect -reuse-previous=on :service_postgres_conninfo"
                    ),
                    sql.index("'ALTER SCHEMA public OWNER TO %I'"),
                )

    def test_database_names_are_escaped_as_one_libpq_value(self) -> None:
        cases = (
            ("service", "dbname='service'"),
            ("Mixed Case", "dbname='Mixed Case'"),
            ("owner's db", "dbname='owner\\'s db'"),
            (r"path\db", r"dbname='path\\db'"),
            ('a"b', "dbname='a\"b'"),
            ("-", "dbname='-'"),
            ("host=other dbname=postgres", "dbname='host=other dbname=postgres'"),
            ("postgresql://other/db", "dbname='postgresql://other/db'"),
            ("x' host=other", "dbname='x\\' host=other'"),
            ("한글\nname", "dbname='한글\nname'"),
        )
        for index, sql in enumerate(self.init_scripts()):
            with self.subTest(script=index):
                query = re.search(
                    r"(SELECT 'dbname='''[\s\S]*?AS service_postgres_conninfo)\s*\\gset",
                    sql,
                )
                self.assertIsNotNone(
                    query, "database switch must build a quoted conninfo value"
                )
                assert query is not None
                # Evaluate the actual portable string expression, not a copy.
                # SQLite does not emulate PostgreSQL/psql or prove readiness.
                expression = query.group(1).replace(":'service_postgres_db'", "?")
                with sqlite3.connect(":memory:") as connection:
                    connection.create_function("chr", 1, chr)
                    for database, expected in cases:
                        with self.subTest(database=database):
                            actual = connection.execute(
                                expression, (database,)
                            ).fetchone()[0]
                            self.assertEqual(expected, actual)


class ServiceConfigurationPathTests(unittest.TestCase):
    def test_openbao_agent_config_argument_is_a_mounted_file(self) -> None:
        import yaml

        path = ROOT / "infra/03-security/openbao/docker-compose.yml"
        agent = yaml.safe_load(path.read_text())["services"]["openbao-agent"]
        configs = [
            arg.removeprefix("-config=")
            for arg in agent["command"]
            if arg.startswith("-config=")
        ]
        targets = {mount.split(":")[1] for mount in agent["volumes"]}
        self.assertEqual(1, len(configs))
        self.assertIn(configs[0], targets)

    def test_openbao_rendered_credentials_are_on_persistent_mount(self) -> None:
        import yaml

        path = ROOT / "infra/03-security/openbao/docker-compose.yml"
        agent = yaml.safe_load(path.read_text())["services"]["openbao-agent"]
        targets = [
            mount.split(":")[1] for mount in agent["volumes"] if mount.endswith(":rw")
        ]
        destinations = re.findall(
            r'destination\s*=\s*"([^\"]+)"',
            (path.parent / "config/agent.hcl").read_text(),
        )
        self.assertTrue(destinations)
        for destination in destinations:
            self.assertTrue(
                any(destination.startswith(target + "/") for target in targets),
                destination,
            )


class MailpitHealthContractTests(unittest.TestCase):
    def test_native_healthcheck_and_custom_ui_port_contract(self):
        import yaml

        text = (ROOT / "infra/10-communication/mailpit/docker-compose.yml").read_text()
        for ui_port in (8025, 18025):
            with self.subTest(ui_port=ui_port):
                rendered = text.replace("${MAILPIT_UI_PORT:-8025}", str(ui_port))
                service = yaml.safe_load(rendered)["services"]["mailpit"]
                self.assertEqual(
                    ["CMD", "/mailpit", "readyz"],
                    service.get("healthcheck", {}).get("test"),
                )
                self.assertEqual(
                    f"0.0.0.0:{ui_port}", service["environment"]["MP_UI_BIND_ADDR"]
                )
                self.assertEqual(
                    str(ui_port),
                    str(
                        service["labels"][
                            "traefik.http.services.mailpit-ui.loadbalancer.server.port"
                        ]
                    ),
                )
                self.assertTrue(
                    any(port.endswith(f":{ui_port}") for port in service["ports"])
                )
                self.assertEqual(
                    {
                        "interval": "15s",
                        "start_period": "10s",
                        "timeout": "5s",
                        "retries": 3,
                    },
                    {
                        key: service["healthcheck"][key]
                        for key in ("interval", "start_period", "timeout", "retries")
                    },
                )

    def test_real_hardening_rejects_missing_or_shell_healthcheck(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (
                "scripts/hardening/check-all-hardening.sh",
                "scripts/lib/hardening-lib.sh",
                "infra/10-communication/stalwart/docker-compose.yml",
                "infra/10-communication/mailpit/docker-compose.yml",
            ):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text((ROOT / name).read_text())
            target = root / "infra/10-communication/mailpit/docker-compose.yml"
            original = target.read_text()
            for test in (
                None,
                ["CMD-SHELL", "curl -f http://localhost:8025/readyz"],
                ["CMD", "true"],
            ):
                # Keep unrelated hardening string guards byte-stable.
                body = re.sub(r"    healthcheck:\n(?:      .*\n)+", "", original)
                if test is not None:
                    body = body.replace(
                        "    networks:\n",
                        "    healthcheck:\n      test: "
                        + json.dumps(test)
                        + "\n    networks:\n",
                    )
                target.write_text(body)
                env = {
                    key: value
                    for key, value in os.environ.items()
                    if key != "HYHOME_CI_GATE_ROOT"
                }
                result = subprocess.run(
                    [
                        "bash",
                        str(root / "scripts/hardening/check-all-hardening.sh"),
                        "10-communication",
                    ],
                    cwd=root,
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn("mailpit", result.stdout.lower())


class OllamaPortContractTests(unittest.TestCase):
    def test_public_render_keeps_direct_api_local_with_distinct_ports(self):
        with tempfile.TemporaryDirectory() as home:
            result = subprocess.run(
                [
                    "docker",
                    "compose",
                    "--env-file",
                    str(ROOT / ".env.example"),
                    "--profile",
                    "ollama",
                    "config",
                    "--format",
                    "json",
                ],
                cwd=ROOT,
                env={
                    "PATH": os.environ["PATH"],
                    "HOME": home,
                    "OLLAMA_HOST_PORT": "21434",
                    "OLLAMA_PORT": "12434",
                },
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
        self.assertEqual(0, result.returncode, "public Compose render failed")
        services = json.loads(result.stdout)["services"]
        self.assertEqual(
            "0.0.0.0:12434", services["ollama"]["environment"]["OLLAMA_HOST"]
        )
        published = services["ollama"]["ports"]
        self.assertEqual(1, len(published))
        self.assertEqual("127.0.0.1", published[0].get("host_ip", "0.0.0.0"))
        self.assertEqual("21434", published[0]["published"])
        self.assertEqual(12434, published[0]["target"])
        self.assertEqual(
            "12434",
            services["ollama"]["labels"][
                "traefik.http.services.ollama.loadbalancer.server.port"
            ],
        )
        self.assertEqual(
            "ollama:12434", services["ollama-exporter"]["environment"]["OLLAMA_HOST"]
        )


MNG_DB_COMPOSE = "infra/04-data/operational/mng-db/docker-compose.yml"
PG_CLUSTER_COMPOSE = "infra/04-data/relational/postgresql-cluster/docker-compose.yml"
PROVISION_RUNNER = (
    "infra/04-data/operational/mng-db/pg/provision/run-feature-provision.sh"
)
# Feature-owned mng-pg provisioning jobs: (compose file, job, SQL file, profiles).
FEATURE_JOBS = (
    (
        "infra/11-laboratory/mlflow/docker-compose.yml",
        "mlflow-db-provision",
        "infra/11-laboratory/mlflow/provisioning/mng-pg.sql",
        {"mlops", "data-science"},
    ),
    (
        "infra/09-tooling/dbt/docker-compose.yml",
        "dbt-db-provision",
        "infra/09-tooling/dbt/provisioning/mng-pg.sql",
        {"analytics-engineering"},
    ),
    (
        "infra/05-messaging/kafka/docker-compose.yml",
        "debezium-db-provision",
        "infra/05-messaging/kafka/connect/debezium/provisioning/mng-pg.sql",
        {"cdc"},
    ),
)
FEATURE_SECRETS = {
    "mlflow_db_password",
    "dbt_db_password",
    "debezium_postgres_password",
    "mlflow_s3_password",
}


def _compose_service(path: str, name: str) -> dict:
    import yaml

    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))["services"][name]


def _runner_text(service: dict) -> str:
    parts = []
    for key in ("entrypoint", "command"):
        value = service.get(key) or []
        parts.extend([value] if isinstance(value, str) else value)
    return "\n".join(parts)


def _psql_variables(sql: str) -> set[str]:
    # :'name' and :name interpolations; :{?name} is a definedness test.
    return set(re.findall(r"(?<![:\w]):'?([a-z_][a-z0-9_]*)'?(?![\w(])", sql)) - {
        "gset",
        "gexec",
    }


def _default(value: str) -> str:
    match = re.fullmatch(r"\$\{[A-Z_]+:-(.*)\}", value)
    return _default(match.group(1)) if match else value


class FeatureProvisioningContractTests(unittest.TestCase):
    """Base DB bootstrap and feature provisioning stay separate and complete."""

    def test_base_init_passes_every_psql_variable_its_sql_reads(self) -> None:
        # Regression: SQL appended to init_users_dbs.sql read :'mlflow_db_password'
        # while mng-pg-init never passed -v mlflow_db_password (syntax error).
        for compose, job, sql in (
            (
                MNG_DB_COMPOSE,
                "mng-pg-init",
                "infra/04-data/operational/mng-db/pg/init-scripts/init_users_dbs.sql",
            ),
            (
                PG_CLUSTER_COMPOSE,
                "pg-cluster-init",
                "infra/04-data/relational/postgresql-cluster/init-scripts/init_users_dbs.sql",
            ),
        ):
            with self.subTest(job=job):
                runner = _runner_text(_compose_service(compose, job))
                passed = set(re.findall(r"-v ([a-z_][a-z0-9_]*)=", runner))
                used = _psql_variables((ROOT / sql).read_text(encoding="utf-8"))
                used -= {"service_postgres_conninfo"}  # produced by \gset
                self.assertEqual(set(), used - passed)

    def test_base_init_never_requires_feature_credentials(self) -> None:
        for compose, job in (
            (MNG_DB_COMPOSE, "mng-pg-init"),
            (PG_CLUSTER_COMPOSE, "pg-cluster-init"),
        ):
            with self.subTest(job=job):
                service = _compose_service(compose, job)
                # Feature profiles may select the base job for dependency
                # closure; it must still never read feature credentials.
                self.assertEqual(
                    set(), set(service.get("secrets", [])) & FEATURE_SECRETS
                )
                self.assertNotRegex(_runner_text(service), r"mlflow|dbt|debezium")

    def test_feature_jobs_supply_every_input_without_argv_secrets(self) -> None:
        for compose, job, sql_path, profiles in FEATURE_JOBS:
            with self.subTest(job=job):
                service = _compose_service(compose, job)
                env = service["environment"]
                self.assertEqual(profiles, set(service["profiles"]))
                self.assertEqual(
                    ["/bin/sh", "/provision/run-feature-provision.sh"],
                    service["entrypoint"],
                )
                self.assertNotIn("command", service)
                secret_pairs = dict(
                    pair.split("=", 1) for pair in env["PROVISION_SECRETS"].split()
                )
                for file in secret_pairs.values():
                    self.assertIn(
                        file.removeprefix("/run/secrets/"), service["secrets"]
                    )
                self.assertIn("mng_postgres_password", service["secrets"])
                for name in env["PROVISION_IDENTIFIERS"].split():
                    self.assertIn(name, env)
                sql = (ROOT / sql_path).read_text(encoding="utf-8")
                wanted = set(re.findall(r"\\getenv [a-z_]+ ([A-Z_]+)", sql))
                self.assertTrue(wanted)
                self.assertEqual(set(), wanted - set(env) - set(secret_pairs))
                mounts = {m.split(":")[1]: m.split(":")[0] for m in service["volumes"]}
                runner = (ROOT / compose).parent / mounts[
                    "/provision/run-feature-provision.sh"
                ]
                self.assertEqual((ROOT / PROVISION_RUNNER).resolve(), runner.resolve())
                self.assertEqual(
                    (ROOT / sql_path).resolve(),
                    (
                        (ROOT / compose).parent / mounts["/provision/mng-pg.sql"]
                    ).resolve(),
                )
                self.assertEqual(
                    "service_completed_successfully",
                    service["depends_on"]["mng-pg-init"]["condition"],
                )

    def test_debezium_connector_matches_provisioned_names_and_allowed_path(
        self,
    ) -> None:
        connector = json.loads(
            (
                ROOT
                / "infra/05-messaging/kafka/connect/debezium/postgres-connector.json"
            ).read_text(encoding="utf-8")
        )
        env = _compose_service(
            "infra/05-messaging/kafka/docker-compose.yml", "debezium-db-provision"
        )["environment"]
        self.assertEqual(env["DEBEZIUM_DB_USER"], connector["database.user"])
        self.assertEqual(
            _default(env["DEBEZIUM_DB_NAME"]), connector["database.dbname"]
        )
        self.assertEqual(
            {env["DEBEZIUM_SCHEMA"], env["DEBEZIUM_HEARTBEAT_SCHEMA"]},
            set(connector["schema.include.list"].split(",")),
        )
        self.assertIn(
            env["DEBEZIUM_HEARTBEAT_SCHEMA"] + ".heartbeat",
            connector["heartbeat.action.query"],
        )
        self.assertEqual(env["DEBEZIUM_PUBLICATION"], connector["publication.name"])
        self.assertEqual("disabled", connector["publication.autocreate.mode"])
        example = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn(f'SERVICE_POSTGRES_DB="{connector["database.dbname"]}"', example)
        worker = _compose_service(
            "infra/05-messaging/kafka/docker-compose.yml", "kafka-connect"
        )
        allowed = worker["environment"][
            "CONNECT_CONFIG_PROVIDERS_FILE_PARAM_ALLOWED_PATHS"
        ]
        match = re.fullmatch(
            r"\$\{file:([^:]+):password\}", connector["database.password"]
        )
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(allowed, str(Path(match.group(1)).parent))
        renderer = (
            ROOT / "infra/05-messaging/kafka/connect/render-connect-secrets.sh"
        ).read_text()
        self.assertIn(f"dir={allowed}\n", renderer)
        self.assertIn("debezium_postgres_password", worker["secrets"])

    def test_properties_escaping_matches_java_properties_rules(self) -> None:
        # Execute the renderer's escaping lines, then parse like Properties.load.
        script = (
            ROOT / "infra/05-messaging/kafka/connect/render-connect-secrets.sh"
        ).read_text()
        lines = script.splitlines()
        start = next(
            n
            for n, line in enumerate(lines)
            if line.strip().startswith('value="${value//')
        )
        end = next(n for n in range(start, len(lines)) if lines[n].strip() == "esac")
        # Execute the renderer's own escaping block: backslash, then leading blank.
        escaping = "\n".join(lines[start : end + 1])
        self.assertIn("case", escaping)
        for raw in (
            "plain",
            r"back\slash",
            " leading",
            "\tleading-tab",
            "\fleading-ff",
            "a=b:c#!",
            "tail\\",
        ):
            with self.subTest(raw=raw):
                out = subprocess.run(
                    [
                        "bash",
                        "-c",
                        f'value="$1"\n{escaping}\nprintf "%s" "$value"',
                        "_",
                        raw,
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout
                # java.util.Properties: skip unescaped leading blanks, then unescape.
                parsed, index = [], 0
                while index < len(out) and out[index] in " \t\f":
                    index += 1
                while index < len(out):
                    char = out[index]
                    if char == "\\" and index + 1 < len(out):
                        parsed.append(out[index + 1])
                        index += 2
                        continue
                    parsed.append(char)
                    index += 1
                self.assertEqual(raw, "".join(parsed))


@unittest.skipUnless(
    os.environ.get("HYHOME_PG_REHEARSAL") == "1",
    "set HYHOME_PG_REHEARSAL=1 to run the disposable PostgreSQL rehearsal (needs Docker)",
)
class FeatureProvisioningRehearsalTests(unittest.TestCase):
    """Run base init and feature SQL against a throwaway PostgreSQL 18 server.

    The server has no published port, joins an internal network created for
    this test, receives synthetic credentials only and is removed afterwards.
    """

    IMAGE = "postgres:18.6-alpine"

    @classmethod
    def setUpClass(cls) -> None:
        cls.tag = f"hyrehearsal{os.getpid()}"
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.secrets = Path(cls.tmp.name)
        subprocess.run(
            ["docker", "network", "create", "--internal", cls.tag],
            check=True,
            capture_output=True,
        )
        cls.addClassCleanup(
            subprocess.run, ["docker", "network", "rm", cls.tag], capture_output=True
        )
        cls.addClassCleanup(
            subprocess.run, ["docker", "rm", "-f", f"{cls.tag}-db"], capture_output=True
        )
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--name",
                f"{cls.tag}-db",
                "--network",
                cls.tag,
                "-e",
                "POSTGRES_USER=admin",
                "-e",
                "POSTGRES_PASSWORD=synthetic-admin",
                "-e",
                "POSTGRES_DB=postgres",
                cls.IMAGE,
                "postgres",
                "-c",
                "wal_level=logical",
            ],
            check=True,
            capture_output=True,
        )
        for _ in range(60):
            ready = subprocess.run(
                [
                    "docker",
                    "exec",
                    f"{cls.tag}-db",
                    "pg_isready",
                    "-h",
                    "127.0.0.1",
                    "-U",
                    "admin",
                ],
                capture_output=True,
                check=False,
            )
            if ready.returncode == 0:
                break
            subprocess.run(["sleep", "1"], check=True)
        cls.write_secret("mng_postgres_password", "synthetic-admin")
        for name, value in {
            "n8n_db_password": "a",
            "keycloak_db_password": "b",
            "airflow_db_password": "c",
            "terrakube_db_password": "d",
            "sonarqube_db_password": "e",
            "service_postgres_password": "f",
            "mlflow_db_password": "ml'quote\\slash pw",
            "dbt_db_password": "dbt-synthetic",
            "debezium_postgres_password": "dbz-synthetic",
        }.items():
            cls.write_secret(name, value)
        cls.base_init()

    @classmethod
    def write_secret(cls, name: str, value: str) -> None:
        path = cls.secrets / name
        path.write_text(value, encoding="utf-8")
        path.chmod(0o644)

    @classmethod
    def base_init(cls) -> None:
        runner = _runner_text(_compose_service(MNG_DB_COMPOSE, "mng-pg-init"))
        args = re.findall(r"-v ([a-z0-9_]+)=\"\$\$([A-Z0-9_]+)\"", runner)
        values = {
            "N8N_DB_PASSWORD": "a",
            "KEYCLOAK_DB_PASSWORD": "b",
            "AIRFLOW_DB_PASSWORD": "c",
            "TERRAKUBE_DB_PASSWORD": "d",
            "SONARQUBE_DB_PASSWORD": "e",
            "SERVICE_POSTGRES_USERNAME": "app_user",
            "SERVICE_DB_PASSWORD": "f",
            "SERVICE_POSTGRES_DB": "app_db",
        }
        command = [
            "psql",
            "-X",
            "-h",
            f"{cls.tag}-db",
            "-U",
            "admin",
            "-d",
            "postgres",
            "-v",
            "ON_ERROR_STOP=1",
        ]
        for variable, env_name in args:
            command += ["-v", f"{variable}={values[env_name]}"]
        command += ["-f", "/work/init.sql"]
        result = cls.docker_run(
            command,
            {"PGPASSWORD": "synthetic-admin"},
            extra=[
                "-v",
                f"{ROOT / 'infra/04-data/operational/mng-db/pg/init-scripts/init_users_dbs.sql'}:/work/init.sql:ro",
            ],
        )
        assert result.returncode == 0, result.stderr

    @classmethod
    def docker_run(cls, command: list[str], env: dict[str, str], extra: list[str] = ()):  # type: ignore[assignment]
        argv = [
            "docker",
            "run",
            "--rm",
            "--network",
            cls.tag,
            "-v",
            f"{cls.secrets}:/run/secrets:ro",
        ]
        for key, value in env.items():
            argv += ["-e", f"{key}={value}"]
        argv += [*extra, cls.IMAGE, *command]
        return subprocess.run(
            argv, capture_output=True, text=True, timeout=180, check=False
        )

    def provision(self, job: str, **overrides: str):
        compose, sql_path = next(
            (source, sql) for source, name, sql, _ in FEATURE_JOBS if name == job
        )
        service = _compose_service(compose, job)
        env = {
            key: _default(str(value)) for key, value in service["environment"].items()
        }
        env.update(
            PGHOST=f"{self.tag}-db",
            PGPORT="5432",
            PGUSER="admin",
            PGDATABASE="postgres",
        )
        env.update(overrides)
        return self.docker_run(
            ["/bin/sh", "/provision/run-feature-provision.sh"],
            env,
            extra=[
                "-v",
                f"{ROOT / PROVISION_RUNNER}:/provision/run-feature-provision.sh:ro",
                "-v",
                f"{ROOT / sql_path}:/provision/mng-pg.sql:ro",
            ],
        )

    def sql(
        self,
        query: str,
        database: str = "postgres",
        user: str = "admin",
        password: str = "synthetic-admin",
    ) -> subprocess.CompletedProcess:
        return self.docker_run(
            [
                "psql",
                "-X",
                "-At",
                "-h",
                f"{self.tag}-db",
                "-U",
                user,
                "-d",
                database,
                "-v",
                "ON_ERROR_STOP=1",
                "-c",
                query,
            ],
            {"PGPASSWORD": password},
        )

    def test_1_fresh_provisioning_and_idempotent_rerun(self) -> None:
        self.sql(
            "CREATE TABLE public.orders(id int primary key)", "app_db", "app_user", "f"
        )
        for _ in range(2):
            for job in (
                "mlflow-db-provision",
                "dbt-db-provision",
                "debezium-db-provision",
            ):
                with self.subTest(job=job):
                    result = self.provision(job)
                    self.assertEqual(0, result.returncode, result.stderr)
        roles = self.sql(
            "SELECT string_agg(rolname||':'||rolsuper||rolreplication||rolcreatedb, ',' ORDER BY rolname)"
            " FROM pg_roles WHERE rolname IN ('mlflow','dbt','debezium')"
        ).stdout.strip()
        self.assertEqual(
            "dbt:falsefalsefalse,debezium:falsetruefalse,mlflow:falsefalsefalse", roles
        )
        # The feature role logs in with a password containing quote/backslash.
        self.assertEqual(
            "mlflow",
            self.sql(
                "SELECT current_user", "mlflow", "mlflow", "ml'quote\\slash pw"
            ).stdout.strip(),
        )
        self.assertEqual(
            0,
            self.sql(
                "CREATE TABLE t(i int)", "mlflow", "mlflow", "ml'quote\\slash pw"
            ).returncode,
        )
        # Other logins lost PUBLIC CONNECT on the MLflow database.
        self.assertNotEqual(
            0, self.sql("SELECT 1", "mlflow", "app_user", "f").returncode
        )
        # dbt reads the source, writes only its target schema.
        self.assertEqual(
            0,
            self.sql(
                "SELECT count(*) FROM public.orders", "app_db", "dbt", "dbt-synthetic"
            ).returncode,
        )
        self.assertEqual(
            0,
            self.sql(
                "CREATE VIEW analytics.v AS SELECT 1 AS x",
                "app_db",
                "dbt",
                "dbt-synthetic",
            ).returncode,
        )
        self.assertNotEqual(
            0,
            self.sql(
                "CREATE TABLE public.x(i int)", "app_db", "dbt", "dbt-synthetic"
            ).returncode,
        )
        # Tables created later by the owner are readable through default privileges.
        self.sql(
            "CREATE TABLE public.later(id int primary key)", "app_db", "app_user", "f"
        )
        self.assertEqual(
            0,
            self.sql(
                "SELECT count(*) FROM public.later",
                "app_db",
                "debezium",
                "dbz-synthetic",
            ).returncode,
        )
        self.assertNotEqual(
            0,
            self.sql(
                "INSERT INTO public.orders VALUES (1)",
                "app_db",
                "debezium",
                "dbz-synthetic",
            ).returncode,
        )
        publication = self.sql(
            "SELECT count(*) FROM pg_publication_tables WHERE pubname='hyhome_app_publication'"
            " AND tablename IN ('orders','later','heartbeat')",
            "app_db",
        ).stdout.strip()
        self.assertEqual("3", publication)
        # The heartbeat action query succeeds; other schemas stay read-only.
        heartbeat = json.loads(
            (
                ROOT
                / "infra/05-messaging/kafka/connect/debezium/postgres-connector.json"
            ).read_text()
        )["heartbeat.action.query"]
        self.assertEqual(
            0, self.sql(heartbeat, "app_db", "debezium", "dbz-synthetic").returncode
        )
        # A service role this job did not create is never altered.
        result = self.provision("dbt-db-provision", DBT_DB_USER="app_user")
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            "1", self.sql("SELECT 1", "app_db", "app_user", "f").stdout.strip()
        )

    def test_2_invalid_inputs_fail_before_any_change(self) -> None:
        cases = {
            "bad identifier": dict(MLFLOW_DB_USER="Robert'); DROP"),
            "multi-line identifier": dict(MLFLOW_DB_USER="ml_new\nx"),
            "missing secret file": dict(
                PROVISION_SECRETS="MLFLOW_DB_PASSWORD=/run/secrets/absent"
            ),
            "empty secret": dict(
                PROVISION_SECRETS="MLFLOW_DB_PASSWORD=/run/secrets/empty"
            ),
            "multi-line secret": dict(
                PROVISION_SECRETS="MLFLOW_DB_PASSWORD=/run/secrets/twolines"
            ),
        }
        self.write_secret("empty", "")
        self.write_secret("twolines", "one\ntwo")
        for label, override in cases.items():
            with self.subTest(case=label):
                inputs = {
                    "MLFLOW_DB_USER": "ml_new",
                    "MLFLOW_DB_NAME": "ml_new",
                    **override,
                }
                result = self.provision("mlflow-db-provision", **inputs)
                self.assertEqual(64, result.returncode, result.stderr)
        self.assertEqual(
            "0",
            self.sql(
                "SELECT count(*) FROM pg_roles WHERE rolname IN ('ml_new','Robert')"
            ).stdout.strip(),
        )

    def test_3_non_default_names_and_foreign_owner_refusal(self) -> None:
        result = self.provision(
            "mlflow-db-provision", MLFLOW_DB_USER="ml_x", MLFLOW_DB_NAME="ml_store"
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            "ml_x",
            self.sql(
                "SELECT pg_get_userbyid(datdba) FROM pg_database WHERE datname='ml_store'"
            ).stdout.strip(),
        )
        # An existing database owned by someone else is never taken over.
        self.sql("CREATE DATABASE foreign_ml OWNER app_user")
        result = self.provision(
            "mlflow-db-provision", MLFLOW_DB_USER="ml_y", MLFLOW_DB_NAME="foreign_ml"
        )
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            "0",
            self.sql(
                "SELECT count(*) FROM pg_roles WHERE rolname='ml_y'"
            ).stdout.strip(),
        )
        # An administrator role is never demoted.
        result = self.provision(
            "mlflow-db-provision", MLFLOW_DB_USER="admin", MLFLOW_DB_NAME="ml_admin"
        )
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            "t",
            self.sql(
                "SELECT rolsuper FROM pg_roles WHERE rolname='admin'"
            ).stdout.strip(),
        )

    def test_4_mid_run_failure_is_not_rolled_back_but_rerun_converges(self) -> None:
        # Target DB check passes, source schema check fails after role/CONNECT
        # were already committed: ON_ERROR_STOP stops without rollback.
        result = self.provision(
            "dbt-db-provision", DBT_DB_USER="dbt_mid", DBT_SOURCE_SCHEMA="missing_src"
        )
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            "1",
            self.sql(
                "SELECT count(*) FROM pg_roles WHERE rolname='dbt_mid'"
            ).stdout.strip(),
        )
        self.sql("CREATE SCHEMA missing_src AUTHORIZATION app_user", "app_db")
        result = self.provision(
            "dbt-db-provision",
            DBT_DB_USER="dbt_mid",
            DBT_SOURCE_SCHEMA="missing_src",
            DBT_SCHEMA="analytics_mid",
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_5_concurrent_runs_serialize(self) -> None:
        procs = [
            subprocess.Popen(
                [
                    "docker",
                    "run",
                    "--rm",
                    "--network",
                    self.tag,
                    "-v",
                    f"{self.secrets}:/run/secrets:ro",
                    "-v",
                    f"{ROOT / PROVISION_RUNNER}:/provision/run-feature-provision.sh:ro",
                    "-v",
                    f"{ROOT / 'infra/11-laboratory/mlflow/provisioning/mng-pg.sql'}:/provision/mng-pg.sql:ro",
                    "-e",
                    f"PGHOST={self.tag}-db",
                    "-e",
                    "PGPORT=5432",
                    "-e",
                    "PGUSER=admin",
                    "-e",
                    "PGDATABASE=postgres",
                    "-e",
                    "PROVISION_ADMIN_PASSWORD_FILE=/run/secrets/mng_postgres_password",
                    "-e",
                    "PROVISION_SQL=/provision/mng-pg.sql",
                    "-e",
                    "PROVISION_IDENTIFIERS=MLFLOW_DB_USER MLFLOW_DB_NAME",
                    "-e",
                    "PROVISION_SECRETS=MLFLOW_DB_PASSWORD=/run/secrets/mlflow_db_password",
                    "-e",
                    "MLFLOW_DB_USER=ml_race",
                    "-e",
                    "MLFLOW_DB_NAME=ml_race",
                    self.IMAGE,
                    "/bin/sh",
                    "/provision/run-feature-provision.sh",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
            for _ in range(3)
        ]
        codes = [proc.wait(timeout=180) for proc in procs]
        self.assertEqual([0, 0, 0], codes)
        self.assertEqual(
            "1",
            self.sql(
                "SELECT count(*) FROM pg_database WHERE datname='ml_race'"
            ).stdout.strip(),
        )


if __name__ == "__main__":
    unittest.main()
