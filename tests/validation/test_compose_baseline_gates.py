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


if __name__ == "__main__":
    unittest.main()
