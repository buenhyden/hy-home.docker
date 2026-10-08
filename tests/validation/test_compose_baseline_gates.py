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
import shutil
import sqlite3
import subprocess
import tempfile
import time
import unittest
import uuid
from pathlib import Path

from scripts.lib.document_governance.operations_catalog import _ComposeLoader

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_SECURITY = ROOT / "scripts/validation/check-template-security-baseline.sh"
CONTROLS = ROOT / "scripts/validation/compose_controls.py"
VALIDATE_COMPOSE = ROOT / "scripts/validation/validate-docker-compose.sh"


class ComposeSelectionValidationTests(unittest.TestCase):
    def _run_port_matrix(
        self,
        services: dict[str, dict[str, object]],
        volumes: dict[str, object] | None = None,
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
                root / "docs/05.operations/policies/0078-compose-profile-vocabulary.md"
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
volumes = json.loads(os.environ["FAKE_COMPOSE_VOLUMES"])
if "--services" in args:
    print("\\n".join(services))
else:
    print(json.dumps({"services": services, "volumes": volumes}))
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
                    "FAKE_COMPOSE_VOLUMES": json.dumps(volumes or {}),
                },
                check=False,
            )

    def test_preflight_reads_data_roots_from_compose_not_shell(self) -> None:
        # An unquoted value with spaces is valid for Compose but not for `. .env`.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(
                ["git", "init", "--quiet"], cwd=root, check=True, capture_output=True
            )
            (root / ".env").write_text(
                "COMFYUI_ARGS=--listen 0.0.0.0\n", encoding="utf-8"
            )
            for name in ("rootCA.pem", "cert.pem", "key.pem"):
                path = root / "secrets/certs" / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("synthetic", encoding="utf-8")
            data = root / "data"
            for name in ("mount", "auth", "data", "broker", "obs"):
                (data / name).mkdir(parents=True)
            fakebin = root / "fakebin"
            fakebin.mkdir()
            docker = fakebin / "docker"
            docker.write_text(
                f"""#!/usr/bin/env python3
import json
import sys

args = sys.argv[1:]
if args[:1] == ["network"]:
    raise SystemExit(1)
if "--environment" in args:
    for key, name in (
        ("DEFAULT_MOUNT_VOLUME_PATH", "mount"),
        ("DEFAULT_AUTH_DIR", "auth"),
        ("DEFAULT_DATA_DIR", "data"),
        ("DEFAULT_MESSAGE_BROKER_DIR", "broker"),
        ("DEFAULT_OBSERVABILITY_DIR", "obs"),
    ):
        print(key + "={data}/" + name)
    print("COMFYUI_ARGS=--listen 0.0.0.0")
elif "--format" in args:
    print(json.dumps({{"services": {{"a": {{}}}}, "volumes": {{}}}}))
""",
                encoding="utf-8",
            )
            docker.chmod(0o755)
            result = subprocess.run(
                ["bash", os.fspath(VALIDATE_COMPOSE), "--preflight"],
                cwd=root,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    "PATH": os.fspath(fakebin) + os.pathsep + os.environ["PATH"],
                },
                check=False,
            )
        output = result.stdout + result.stderr
        self.assertEqual(0, result.returncode, output)
        self.assertNotIn("command not found", output)
        self.assertIn(f"dir exists: {data}/data", output)

    def test_named_volume_devices_must_be_distinct_and_not_nested(self) -> None:
        services = {"alpha": {}, "beta": {}}

        def bind(path: str) -> dict[str, object]:
            return {"driver_opts": {"type": "none", "o": "bind", "device": path}}

        cases = {
            "nested": ({"a": bind("/srv/data/pg"), "b": bind("/srv/data/pg/x")}, 1),
            "shared": ({"a": bind("/srv/data/pg"), "b": bind("/srv/data/pg/")}, 1),
            "empty root": ({"a": bind("/dev-pg")}, 1),
            "relative": ({"a": bind("data/pg")}, 1),
            "siblings": ({"a": bind("/srv/data/pg"), "b": bind("/srv/data/pg2")}, 0),
            "named only": ({"a": {"driver": "local"}}, 0),
        }
        for label, (volumes, expected) in cases.items():
            with self.subTest(case=label):
                result = self._run_port_matrix(services, volumes)
                self.assertEqual(
                    expected, result.returncode, result.stdout + result.stderr
                )
                if expected:
                    self.assertIn("named volume host paths overlap", result.stdout)

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
                root / "docs/05.operations/policies/0078-compose-profile-vocabulary.md"
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


def _controls():
    import importlib.util

    spec = importlib.util.spec_from_file_location("compose_controls", CONTROLS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COMPLIANT = {
    "restart": "unless-stopped",
    "init": True,
    "healthcheck": {"test": ["CMD", "true"]},
    "security_opt": ["no-new-privileges:true"],
    "cap_drop": ["ALL"],
    "cpus": "1.0",
    "mem_limit": "512m",
}
REGISTERED = {
    "no_new_privileges": "",
    "cap_drop_all": "",
    "cap_add": "",
    "privileged": "",
    "restart": "",
    "healthcheck": "",
    "cpus": "",
    "mem_limit": "",
}


class ComposeControlsTests(unittest.TestCase):
    """compose_controls.check over synthetic rendered models (SPEC-0218)."""

    TODAY = __import__("datetime").date(2026, 10, 9)

    def setUp(self) -> None:
        self.module = _controls()

    def models(self, **services: dict) -> dict:
        root = {
            name: spec for name, spec in services.items() if not name.startswith("lab_")
        }
        lab = {
            name[4:]: spec for name, spec in services.items() if name.startswith("lab_")
        }
        return {
            "root": ({"services": root}, {n: "infra/x/docker-compose.yml" for n in root}, ("/repo/secrets/",)),
            "lab:x": ({"services": lab}, {n: "labs/x.yml" for n in lab}, ("/lab-secrets/",)),
        }  # fmt: skip

    def entry(self, **overrides: object) -> dict:
        row = {
            "scope": "root", "compose_file": "infra/x/docker-compose.yml", "service": "a",
            "control": "cap_add", "allowed_value": ["NET_BIND_SERVICE"], "kind": "compatibility",
            "owner": "@o", "reason": "r", "impact": "i", "mitigation": "m", "verification": "v",
            "reviewed": "2026-10-09", "review_by": "2027-01-01", "release_condition": "c",
        }  # fmt: skip
        return {**row, **overrides}

    def check(self, models: dict, *rows: dict) -> list[str]:
        registry = {"controls": REGISTERED, "exceptions": list(rows)}
        return self.module.check(registry, models, self.TODAY)

    def test_compliant_daemon_passes(self) -> None:
        self.assertEqual([], self.check(self.models(a=dict(COMPLIANT))))

    def test_every_enforced_control_fails_independently(self) -> None:
        cases = {
            "no_new_privileges": {"security_opt": []},
            "cap_drop_all": {"cap_drop": []},
            "cap_add": {"cap_add": ["SYS_ADMIN"]},
            "privileged": {"privileged": True},
            "restart": {"restart": "on-failure"},
            "healthcheck": {"healthcheck": {"disable": True}},
            "cpus": {"cpus": None},
            "mem_limit": {"mem_limit": None},
        }
        for control, change in cases.items():
            with self.subTest(control=control):
                findings = self.check(self.models(a={**COMPLIANT, **change}))
                self.assertEqual(1, len(findings), findings)
                self.assertIn(f"root/a: {control}", findings[0])

    def test_a_job_needs_no_healthcheck_and_no_service_needs_a_secret(self) -> None:
        job = {**COMPLIANT, "restart": "no"}
        job.pop("healthcheck")
        self.assertEqual([], self.check(self.models(a=job)))

    def test_unregistered_controls_are_reported_but_not_enforced(self) -> None:
        service = {**COMPLIANT, "init": False}
        self.assertEqual([], self.check(self.models(a=service)))
        self.assertEqual(
            {"init": False, "pids_limit": None}, self.module.deviations(service, ())
        )

    def test_an_exact_exception_passes_and_a_changed_value_fails(self) -> None:
        models = self.models(a={**COMPLIANT, "cap_add": ["NET_BIND_SERVICE"]})
        self.assertEqual([], self.check(models, self.entry()))
        wider = self.models(
            a={**COMPLIANT, "cap_add": ["NET_BIND_SERVICE", "SYS_ADMIN"]}
        )
        findings = self.check(wider, self.entry())
        self.assertTrue(any("differs" in f for f in findings), findings)

    def test_registry_defects_are_findings(self) -> None:
        models = self.models(a={**COMPLIANT, "cap_add": ["NET_BIND_SERVICE"]})
        cases = {
            "missing reason": (self.entry(reason=""), "missing reason"),
            "wildcard": (self.entry(service="*"), "wildcards"),
            "unregistered": (self.entry(control="tmpfs"), "unregistered control"),
            "expired": (self.entry(review_by="2026-10-01"), "expired"),
            "too long": (self.entry(review_by="2028-01-01"), "more than a year"),
            "orphan": (self.entry(service="gone"), "no such service"),
            "wrong file": (
                self.entry(compose_file="infra/y/docker-compose.yml"),
                "declared in",
            ),
            "bad kind": (self.entry(kind="temporary"), "kind must be"),
            "unknown field": (self.entry(note="x"), "unknown fields"),
        }
        for label, (row, expected) in cases.items():
            with self.subTest(case=label):
                findings = self.check(models, row)
                self.assertTrue(any(expected in f for f in findings), findings)
        duplicate = self.check(models, self.entry(), self.entry())
        self.assertTrue(any("duplicate" in f for f in duplicate), duplicate)

    def test_an_exception_for_a_conforming_service_is_stale(self) -> None:
        findings = self.check(self.models(a=dict(COMPLIANT)), self.entry())
        self.assertTrue(any("retire the exception" in f for f in findings), findings)

    def test_root_and_lab_services_of_one_name_are_distinct(self) -> None:
        models = self.models(
            a=dict(COMPLIANT), lab_a={**COMPLIANT, "cap_add": ["IPC_LOCK"]}
        )
        root_entry = self.entry(allowed_value=["IPC_LOCK"])
        findings = self.check(models, root_entry)
        self.assertTrue(any("lab:x/a: cap_add" in f for f in findings), findings)
        lab_entry = self.entry(
            scope="lab:x", compose_file="labs/x.yml", allowed_value=["IPC_LOCK"]
        )
        self.assertEqual([], self.check(models, lab_entry))

    def test_the_secrets_group_follows_secret_reads(self) -> None:
        group = {**COMPLIANT, "group_add": ["1000"]}
        self.assertEqual(
            "unneeded",
            self.module.deviations(group, ("/repo/secrets/",))["secrets_group"],
        )
        reader = {**group, "secrets": [{"source": "s"}]}
        self.assertNotIn(
            "secrets_group", self.module.deviations(reader, ("/repo/secrets/",))
        )
        bind = {**group, "volumes": [{"type": "bind", "source": "/repo/secrets/certs"}]}
        self.assertNotIn(
            "secrets_group", self.module.deviations(bind, ("/repo/secrets/",))
        )
        self.assertEqual(
            "missing",
            self.module.deviations({**COMPLIANT, "secrets": [{}]}, ())["secrets_group"],
        )

    def test_the_gate_entrypoint_runs_this_validator(self) -> None:
        script = TEMPLATE_SECURITY.read_text(encoding="utf-8")
        self.assertIn("scripts/validation/compose_controls.py", script)


class PostgresInitializationContractTests(unittest.TestCase):
    # Connection targeting checks without accessing a PostgreSQL runtime.
    def init_scripts(self) -> list[str]:
        return [
            (ROOT / path).read_text(encoding="utf-8")
            for path in (
                "infra/04-data/postgresql-cluster/init-scripts/init_users_dbs.sql",
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

        text = (ROOT / "infra/11-quality/mailpit/docker-compose.yml").read_text()
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
                "infra/11-quality/sonarqube/docker-compose.yml",
                "infra/11-quality/wiremock/docker-compose.yml",
                "infra/11-quality/pact-broker/docker-compose.yml",
                "infra/11-quality/mailpit/docker-compose.yml",
            ):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text((ROOT / name).read_text())
            target = root / "infra/11-quality/mailpit/docker-compose.yml"
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
                        "11-quality",
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


MNG_DB_COMPOSE = "infra/04-data/mng-db/docker-compose.yml"
PG_CLUSTER_COMPOSE = "labs/postgresql-ha.yml"
PROVISION_RUNNER = "infra/04-data/mng-db/pg/provision/run-feature-provision.sh"
# Feature-owned mng-pg provisioning jobs: (compose file, job, SQL file, profiles).
FEATURE_JOBS = (
    (
        "infra/08-ai/mlflow/docker-compose.yml",
        "mlflow-db-provision",
        "infra/08-ai/mlflow/provisioning/mng-pg.sql",
        {"mlops", "data-science"},
    ),
    (
        "infra/12-analytics/dbt/docker-compose.yml",
        "dbt-db-provision",
        "infra/12-analytics/dbt/provisioning/dev-pg.sql",
        {"analytics-engineering"},
    ),
    (
        "infra/05-messaging/kafka/docker-compose.yml",
        "debezium-db-provision",
        "infra/05-messaging/kafka/connect/debezium/provisioning/dev-pg.sql",
        {"cdc"},
    ),
    (
        "infra/11-quality/pact-broker/docker-compose.yml",
        "pact-broker-db-provision",
        "infra/11-quality/pact-broker/provisioning/mng-pg.sql",
        {"contract-testing"},
    ),
    (
        "infra/12-analytics/superset/docker-compose.yml",
        "superset-db-provision",
        "infra/12-analytics/superset/provisioning/mng-pg.sql",
        {"bi"},
    ),
)
FEATURE_SECRETS = {
    "mlflow_db_password",
    "dbt_db_password",
    "debezium_postgres_password",
    "seaweedfs_s3_mlflow_secret_key",
    "pact_broker_db_password",
    "superset_db_password",
}


def _compose_service(path: str, name: str) -> dict:
    import yaml

    return yaml.load((ROOT / path).read_text(encoding="utf-8"), Loader=_ComposeLoader)[
        "services"
    ][name]


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
                "infra/04-data/mng-db/pg/init-scripts/init_users_dbs.sql",
            ),
            (
                PG_CLUSTER_COMPOSE,
                "pg-cluster-init",
                "infra/04-data/postgresql-cluster/init-scripts/init_users_dbs.sql",
            ),
        ):
            with self.subTest(job=job):
                runner = _runner_text(_compose_service(compose, job))
                passed = set(re.findall(r"-v ([a-z_][a-z0-9_]*)=", runner))
                passed.update(re.findall(r"\\set ([a-z_][a-z0-9_]*)", runner))
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
                self.assertNotRegex(
                    _runner_text(service), r"mlflow|dbt|debezium|pact|superset"
                )

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
                admin_secret = Path(env["PROVISION_ADMIN_PASSWORD_FILE"]).name
                self.assertIn(admin_secret, service["secrets"])
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
                    ((ROOT / compose).parent / mounts[env["PROVISION_SQL"]]).resolve(),
                )
                self.assertEqual(
                    "service_completed_successfully",
                    service["depends_on"][
                        "dev-platform-provision"
                        if job in {"dbt-db-provision", "debezium-db-provision"}
                        else "mng-pg-init"
                    ]["condition"],
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
        self.assertIn("DEV_PG_ADMIN_USER=", example)
        self.assertEqual("platform_dev", connector["database.dbname"])
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
    """Rehearse mng metadata and dev source grants on disposable PG18 servers.

    Neither server publishes a port. Both join one temporary internal network,
    receive synthetic credentials only, and are removed afterwards.
    """

    IMAGE = "postgres:18.6-alpine"
    DEV_IMAGE = re.search(
        r"^FROM (\S+)",
        (ROOT / "infra/04-data/dev-db/pg/Dockerfile").read_text(encoding="utf-8"),
        re.MULTILINE,
    ).group(1)

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
        cls.addClassCleanup(
            subprocess.run,
            ["docker", "rm", "-f", f"{cls.tag}-dev"],
            capture_output=True,
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
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--name",
                f"{cls.tag}-dev",
                "--network",
                cls.tag,
                "-e",
                "POSTGRES_USER=admin",
                "-e",
                "POSTGRES_PASSWORD=synthetic-dev-admin",
                "-e",
                "POSTGRES_DB=postgres",
                cls.DEV_IMAGE,
                "postgres",
                "-c",
                "wal_level=logical",
                "-c",
                "shared_preload_libraries=timescaledb",
            ],
            check=True,
            capture_output=True,
        )
        for server in ("db", "dev"):
            for _ in range(60):
                ready = subprocess.run(
                    [
                        "docker",
                        "exec",
                        f"{cls.tag}-{server}",
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
            else:
                raise AssertionError(f"disposable {server} server did not become ready")
        cls.write_secret("mng_postgres_password", "synthetic-admin")
        cls.write_secret("dev_pg_admin_password", "synthetic-dev-admin")
        for name, value in {
            "n8n_db_password": "a",
            "keycloak_db_password": "b",
            "airflow_db_password": "c",
            "terrakube_db_password": "d",
            "sonarqube_db_password": "e",
            "dev_pg_platform_migrator_password": "platform-migrator-synthetic",
            "dev_pg_platform_runtime_password": "platform-runtime-synthetic",
            "dev_pg_platform_reader_password": "platform-reader-synthetic",
            "mlflow_db_password": "ml'quote\\slash pw",
            "dbt_db_password": "dbt-synthetic",
            "debezium_postgres_password": "dbz-synthetic",
            "superset_db_password": "ss'quote\\slash@pw",
            "superset_secret_key": "synthetic-superset-signing-key",
            "superset_oidc_client_secret": "synthetic-oidc",
            "rootCA.pem": "not used offline",
        }.items():
            cls.write_secret(name, value)
        cls.base_init()
        cls.platform_init()

    @classmethod
    def write_secret(cls, name: str, value: str) -> None:
        path = cls.secrets / name
        path.write_text(value, encoding="utf-8")
        path.chmod(0o600)

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
                f"{ROOT / 'infra/04-data/mng-db/pg/init-scripts/init_users_dbs.sql'}:/work/init.sql:ro",
            ],
        )
        assert result.returncode == 0, result.stderr

    @classmethod
    def platform_init(cls) -> None:
        manifest = json.loads(
            (ROOT / "infra/04-data/dev-db/pg/provision/platform.json").read_text(
                encoding="utf-8"
            )
        )
        project = __import__("runpy").run_path(
            str(ROOT / "infra/04-data/dev-db/pg/provision/project.py")
        )
        sql_path = cls.secrets / "platform.sql"
        sql_path.write_text(project["sql_for"](manifest), encoding="utf-8")
        sql_path.chmod(0o600)
        result = cls.docker_run(
            [
                "psql",
                "-X",
                "-h",
                f"{cls.tag}-dev",
                "-U",
                "admin",
                "-d",
                "postgres",
                "-v",
                "ON_ERROR_STOP=1",
                "-f",
                "/work/platform.sql",
            ],
            {
                "PGPASSWORD": "synthetic-dev-admin",
                "DEV_MIGRATOR_PASSWORD": "platform-migrator-synthetic",
                "DEV_RUNTIME_PASSWORD": "platform-runtime-synthetic",
                "DEV_READER_PASSWORD": "platform-reader-synthetic",
            },
            extra=["-v", f"{sql_path}:/work/platform.sql:ro"],
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
        dev_job = job in {"dbt-db-provision", "debezium-db-provision"}
        env.update(
            PGHOST=f"{self.tag}-{'dev' if dev_job else 'db'}",
            PGPORT="5432",
            PGUSER="admin",
            PGDATABASE="postgres",
            PROVISION_ADMIN_PASSWORD_FILE=(
                "/run/secrets/dev_pg_admin_password"
                if dev_job
                else "/run/secrets/mng_postgres_password"
            ),
        )
        env.update(overrides)
        return self.docker_run(
            ["/bin/sh", "/provision/run-feature-provision.sh"],
            env,
            extra=[
                "-v",
                f"{ROOT / PROVISION_RUNNER}:/provision/run-feature-provision.sh:ro",
                "-v",
                f"{ROOT / sql_path}:/provision/{'dev-pg' if dev_job else 'mng-pg'}.sql:ro",
            ],
        )

    def sql(
        self,
        query: str,
        database: str = "postgres",
        user: str = "admin",
        password: str | None = None,
        host: str = "mng",
    ) -> subprocess.CompletedProcess:
        if database == "platform_dev":
            host = "dev"
        password = password or (
            "synthetic-dev-admin" if host == "dev" else "synthetic-admin"
        )
        return self.docker_run(
            [
                "psql",
                "-X",
                "-At",
                "-h",
                f"{self.tag}-{'dev' if host == 'dev' else 'db'}",
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
        created = self.sql(
            "SET ROLE platform_owner; CREATE TABLE app.orders(id int primary key)",
            "platform_dev",
        )
        self.assertEqual(0, created.returncode, created.stderr)
        for _ in range(2):
            for job in (
                "mlflow-db-provision",
                "dbt-db-provision",
                "debezium-db-provision",
            ):
                with self.subTest(job=job):
                    result = self.provision(job)
                    self.assertEqual(0, result.returncode, result.stderr)
        mng_roles = self.sql(
            "SELECT string_agg(rolname||':'||rolsuper||rolreplication||rolcreatedb, ',' ORDER BY rolname)"
            " FROM pg_roles WHERE rolname='mlflow'"
        ).stdout.strip()
        dev_roles = self.sql(
            "SELECT string_agg(rolname||':'||rolsuper||rolreplication||rolcreatedb, ',' ORDER BY rolname)"
            " FROM pg_roles WHERE rolname IN ('dbt','debezium')",
            host="dev",
        ).stdout.strip()
        self.assertEqual("mlflow:falsefalsefalse", mng_roles)
        self.assertEqual("dbt:falsefalsefalse,debezium:falsetruefalse", dev_roles)
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
        self.assertNotEqual(0, self.sql("SELECT 1", "mlflow", "n8n", "a").returncode)
        # The platform roles have distinct data and DDL rights.
        self.assertEqual(
            0,
            self.sql(
                "SELECT count(*) FROM app.orders",
                "platform_dev",
                "platform_reader",
                "platform-reader-synthetic",
            ).returncode,
        )
        self.assertNotEqual(
            0,
            self.sql(
                "INSERT INTO app.orders VALUES (1)",
                "platform_dev",
                "platform_reader",
                "platform-reader-synthetic",
            ).returncode,
        )
        self.assertNotEqual(
            0,
            self.sql(
                "CREATE TABLE app.reader_x(i int)",
                "platform_dev",
                "platform_reader",
                "platform-reader-synthetic",
            ).returncode,
        )
        self.assertEqual(
            0,
            self.sql(
                "INSERT INTO app.orders VALUES (1)",
                "platform_dev",
                "platform_runtime",
                "platform-runtime-synthetic",
            ).returncode,
        )
        self.assertNotEqual(
            0,
            self.sql(
                "CREATE TABLE app.runtime_x(i int)",
                "platform_dev",
                "platform_runtime",
                "platform-runtime-synthetic",
            ).returncode,
        )
        # dbt reads the source and writes only its target schema.
        self.assertEqual(
            0,
            self.sql(
                "SELECT count(*) FROM app.orders",
                "platform_dev",
                "dbt",
                "dbt-synthetic",
            ).returncode,
        )
        self.assertEqual(
            0,
            self.sql(
                "CREATE VIEW analytics.v AS SELECT 1 AS x",
                "platform_dev",
                "dbt",
                "dbt-synthetic",
            ).returncode,
        )
        self.assertNotEqual(
            0,
            self.sql(
                "CREATE TABLE app.x(i int)", "platform_dev", "dbt", "dbt-synthetic"
            ).returncode,
        )
        # Tables created later by the owner are readable through default privileges.
        later = self.sql(
            "SET ROLE platform_owner; CREATE TABLE app.later(id int primary key)",
            "platform_dev",
        )
        self.assertEqual(0, later.returncode, later.stderr)
        self.assertEqual(
            0,
            self.sql(
                "SELECT count(*) FROM app.later",
                "platform_dev",
                "debezium",
                "dbz-synthetic",
            ).returncode,
        )
        self.assertNotEqual(
            0,
            self.sql(
                "INSERT INTO app.orders VALUES (2)",
                "platform_dev",
                "debezium",
                "dbz-synthetic",
            ).returncode,
        )
        publication = self.sql(
            "SELECT count(*) FROM pg_publication_tables WHERE pubname='hyhome_platform_publication'"
            " AND tablename IN ('orders','later','heartbeat')",
            "platform_dev",
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
            0,
            self.sql(heartbeat, "platform_dev", "debezium", "dbz-synthetic").returncode,
        )
        # A service role this job did not create is never altered.
        result = self.provision("dbt-db-provision", DBT_DB_USER="platform_runtime")
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            "1",
            self.sql(
                "SELECT 1",
                "platform_dev",
                "platform_runtime",
                "platform-runtime-synthetic",
            ).stdout.strip(),
        )

    def test_6_superset_migrates_and_serves_on_its_own_database(self) -> None:
        # SPEC-0180 S16: provisioning, the init job's own command twice, then
        # the web server; the password carries a quote, a backslash and an @.
        self.assertEqual(0, self.provision("superset-db-provision").returncode)
        compose = "infra/12-analytics/superset/docker-compose.yml"
        init = _compose_service(compose, "superset-init")
        image = init["image"]
        built = subprocess.run(
            [
                "docker",
                "build",
                "-q",
                "-t",
                image,
                str(ROOT / "infra/12-analytics/superset"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, built.returncode, built.stderr)
        env = {key: _default(str(value)) for key, value in init["environment"].items()}
        env.update(DEFAULT_URL="rehearsal.invalid", SUPERSET_DB_HOST=f"{self.tag}-db")
        base = [
            "docker",
            "run",
            "--network",
            self.tag,
            "--read-only",
            "--tmpfs",
            "/tmp",
            "--tmpfs",
            "/app/superset_home:uid=1000,gid=1000",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "-v",
            f"{self.secrets}:/run/secrets:ro",
            "-v",
            f"{self.secrets / 'rootCA.pem'}:/etc/ssl/certs/hy-home-rootCA.pem:ro",
            "-v",
            f"{ROOT / compose.rsplit('/', 1)[0]}/superset_config.py:/app/pythonpath/superset_config.py:ro",
        ]
        for key, value in env.items():
            base += ["-e", f"{key}={value}"]
        for _ in range(2):
            ran = subprocess.run(
                [
                    *base[:2],
                    "--rm",
                    *base[2:],
                    "--entrypoint",
                    init["entrypoint"][0],
                    image,
                    *init["entrypoint"][1:],
                    *init["command"],
                ],
                capture_output=True,
                text=True,
                timeout=600,
                check=False,
            )
            self.assertEqual(0, ran.returncode, ran.stdout[-2000:] + ran.stderr[-2000:])
        self.assertEqual(
            "lakehouse|trino://superset@trino:8080/lakehouse",
            self.sql(
                "SELECT database_name, sqlalchemy_uri FROM dbs",
                "superset",
                "superset",
                "ss'quote\\slash@pw",
            ).stdout.strip(),
        )
        web = f"{self.tag}-superset"
        self.addCleanup(
            subprocess.run, ["docker", "rm", "-f", web], capture_output=True
        )
        started = subprocess.run(
            [*base[:2], "-d", "--name", web, *base[2:], image],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, started.returncode, started.stderr)

        def curl(path: str) -> str:
            return subprocess.run(
                [
                    "docker",
                    "exec",
                    web,
                    "curl",
                    "-s",
                    "-o",
                    "/dev/null",
                    "-w",
                    "%{http_code}",
                    f"http://localhost:8088{path}",
                ],
                capture_output=True,
                text=True,
                check=False,
            ).stdout

        for _ in range(60):
            if curl("/health") == "200":
                break
            subprocess.run(["sleep", "3"], check=True)
        self.assertEqual("200", curl("/health"))
        self.assertEqual("401", curl("/api/v1/database/"))
        login = subprocess.run(
            ["docker", "exec", web, "curl", "-s", "http://localhost:8088/login/"],
            capture_output=True,
            text=True,
            check=False,
        ).stdout
        self.assertIn("keycloak", login)
        environ = subprocess.run(
            ["docker", "exec", web, "env"], capture_output=True, text=True, check=False
        ).stdout
        self.assertNotIn("slash@pw", environ)
        self.assertNotIn("synthetic-oidc", environ)

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
        self.sql("CREATE DATABASE foreign_ml OWNER n8n")
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
                "SELECT count(*) FROM pg_roles WHERE rolname='dbt_mid'",
                host="dev",
            ).stdout.strip(),
        )
        schema = self.sql(
            "CREATE SCHEMA missing_src AUTHORIZATION platform_owner", "platform_dev"
        )
        self.assertEqual(0, schema.returncode, schema.stderr)
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
                    f"{ROOT / 'infra/08-ai/mlflow/provisioning/mng-pg.sql'}:/provision/mng-pg.sql:ro",
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


RESTIC_COMPOSE = "infra/09-platform-ops/restic/docker-compose.yml"
PGBACKREST_DIR = "infra/04-data/mng-db/pg/backup"
RESTIC_DIR = "infra/09-platform-ops/restic"


def _compose_command(service: dict) -> list[str]:
    command = service.get("command", [])
    return command if isinstance(command, list) else command.split()


class BackupContractTests(unittest.TestCase):
    """Static contracts for pgBackRest in mng-pg and the Restic job (S03)."""

    def test_mng_pg_archives_wal_through_pgbackrest_in_the_server(self) -> None:
        service = _compose_service(MNG_DB_COMPOSE, "mng-pg")
        self.assertEqual("./pg/backup", service["build"]["context"])
        command = _compose_command(service)
        self.assertIn("archive_mode=on", command)
        self.assertIn(
            "archive_command=pgbackrest --stanza=mng archive-push %p", command
        )
        repo = [
            volume
            for volume in service["volumes"]
            if isinstance(volume, dict)
            and volume.get("target") == "/var/lib/pgbackrest"
        ]
        self.assertEqual(1, len(repo))
        self.assertIn("BACKUP_STATE_REPO_DIR", repo[0]["source"])
        self.assertIs(False, repo[0]["bind"]["create_host_path"])
        self.assertIn("pgbackrest_cipher_pass", service["secrets"])
        environment = service["environment"]
        self.assertFalse(any("CIPHER" in key for key in environment))
        self.assertTrue(
            environment["PGBACKREST_CONFIG_INCLUDE_PATH"].startswith("/tmp/")
        )

    def test_pgbackrest_image_pins_package_and_restores_default_umask(self) -> None:
        dockerfile = (ROOT / PGBACKREST_DIR / "Dockerfile").read_text(encoding="utf-8")
        self.assertRegex(
            dockerfile, r"apk add --no-cache pgbackrest=\d+\.\d+\.\d+-r\d+"
        )
        entrypoint = (ROOT / PGBACKREST_DIR / "entrypoint.sh").read_text(
            encoding="utf-8"
        )
        # umask 077 leaking into the official entrypoint left PGDATA's parent
        # untraversable for the postgres user (rehearsal, 2026-09-22).
        before_exec = entrypoint.split("exec docker-entrypoint.sh")[0]
        self.assertEqual("umask 022", before_exec.strip().splitlines()[-1])
        config = (ROOT / PGBACKREST_DIR / "pgbackrest.conf").read_text(encoding="utf-8")
        self.assertIn("repo1-cipher-type=aes-256-cbc", config)
        self.assertIn("archive-push-queue-max=", config)
        self.assertIn("must be a single line", entrypoint)
        self.assertNotIn("repo1-cipher-pass", config)

    def test_restic_job_reads_sources_read_only_and_has_no_network(self) -> None:
        service = _compose_service(RESTIC_COMPOSE, "restic")
        self.assertEqual(["backup"], service["profiles"])
        self.assertEqual("none", service["network_mode"])
        self.assertEqual(["snapshots"], service["command"])
        self.assertEqual(["DAC_OVERRIDE"], service["cap_add"])
        writable = {"/repo/state", "/repo/host"}
        for volume in service["volumes"]:
            if isinstance(volume, str):
                self.assertTrue(volume.endswith(":ro"), volume)
                continue
            if volume["target"] in writable:
                self.assertIs(False, volume["bind"]["create_host_path"])
            else:
                self.assertIs(True, volume.get("read_only"), volume["target"])

    def test_restic_state_set_is_an_allowlist_without_live_engines(self) -> None:
        lines = (ROOT / RESTIC_DIR / "sets/state-include.txt").read_text(
            encoding="utf-8"
        )
        allowed = [
            line for line in lines.splitlines() if line and not line.startswith("#")
        ]
        self.assertTrue(allowed)
        for rel in allowed:
            self.assertFalse(rel.startswith("/") or ".." in rel, rel)
        live = (
            "management/pg",
            "management/valkey",
            "security/openbao",
            "obs/",
            "message_broker",
            "data/",
            "ai/ollama",
            "ai/comfyui/models",
            "workflow/airflow/logs",
            "workflow/airflow/airflow-valkey",
        )
        # SeaweedFS needle and master trees are read live on purpose: needles
        # are append-only and the filer metadata export is taken first (S06).
        # The live filer store is never copied.
        seaweedfs = {"data/seaweedfs/volume", "data/seaweedfs/master"}
        self.assertLessEqual(seaweedfs, set(allowed))
        for rel in set(allowed) - seaweedfs:
            self.assertFalse(
                any(rel == x.rstrip("/") or rel.startswith(x) for x in live), rel
            )
        self.assertFalse(any(rel.startswith("data/seaweedfs/filer") for rel in allowed))
        script = (ROOT / RESTIC_DIR / "backup.sh").read_text(encoding="utf-8")
        self.assertIn("--files-from-verbatim", script)

    def test_destructive_restic_actions_need_explicit_confirmation(self) -> None:
        script = (ROOT / RESTIC_DIR / "backup.sh").read_text(encoding="utf-8")
        prune = script.split("forget-prune)")[1].split(";;")[0]
        self.assertIn('"${HYHOME_PRUNE_CONFIRM:-}" != "delete-old-snapshots"', prune)
        init = script.split("    init)")[1].split(";;")[0]
        self.assertIn("already initialized; skipped", init)
        passthrough = script.split("    cmd)")[1]
        self.assertIn("forget | prune)", passthrough)

    def test_orchestrator_never_sources_env_and_checks_disk_separation(self) -> None:
        script = (ROOT / RESTIC_DIR / "bin/hyhome-backup.sh").read_text(
            encoding="utf-8"
        )
        self.assertNotRegex(script, r"(^|\s)(source|\.)\s+\S*\.env")
        self.assertIn("flock -n 9", script)
        self.assertIn('device_of "$state_repo"', script)
        self.assertIn('device_of "$host_repo"', script)
        self.assertIn("over the ${max_gib} GiB budget; Restic backup skipped", script)
        # The budget check follows pgBackRest (whose expire shrinks the repository).
        self.assertLess(
            script.index("pgbackrest --stanza=mng"), script.index("state_kib=")
        )
        self.assertIn("is inside backed-up source", script)
        # Repository contents belong to UID 70 and root; the host user cannot
        # measure them (live findings, 2026-09-22), so a read-only container does.
        self.assertIn('-v "$1:/m:ro" --entrypoint du "$restic_image"', script)
        self.assertNotIn("du -sk --", script)
        self.assertNotIn(
            "workflow/airflow\n",
            (ROOT / RESTIC_DIR / "sets/state-include.txt").read_text(),
        )
        cleanup = script[
            script.index("cleanup() {") : script.index("trap cleanup EXIT")
        ]
        self.assertIn('find "$staging" -mindepth 1 -delete', cleanup)
        self.assertIn("volume.vacuum.enable", cleanup)
        # A stalled RDB export must not hold the run until the unit timeout
        # (2026-09-26 to 09-29): the limit runs inside the container, so the
        # export process ends there too, and a partial file is not backed up.
        export = script[
            script.index("if running mng-valkey; then") : script.index(
                "backup-sqlite-export"
            )
        ]
        self.assertIn("timeout 300 valkey-cli --no-auth-warning --rdb -", export)
        self.assertIn('rm -f "$staging/mng-valkey.rdb"', export)
        # DEV queues get the same bounded snapshot, as the admin ACL user;
        # a stopped DEV is skipped, a failed export is dropped and fails.
        dev = script[
            script.index("if running dev-valkey; then") : script.index(
                "backup-sqlite-export"
            )
        ]
        self.assertIn("--user devadmin", dev)
        self.assertIn("timeout 300 valkey-cli --no-auth-warning", dev)
        self.assertIn('rm -f "$staging/dev-valkey.rdb"', dev)
        self.assertIn("status=1", dev)
        # OpenBao: a snapshot-only token on stdin (never argv), renewed each
        # run; a failed or empty snapshot is dropped and fails the run.
        bao = script[
            script.index("# OpenBao Raft snapshot") : script.index(
                "backup-sqlite-export"
            )
        ]
        self.assertIn('<"$bao_token"', bao)
        self.assertNotIn("BAO_TOKEN=$(cat", bao)
        self.assertNotIn("-token=", bao)
        self.assertIn("bao token renew", bao)
        self.assertIn('rm -f "$staging/openbao-raft.snap"', bao)
        self.assertIn('[[ ! -s "$staging/openbao-raft.snap" ]]', bao)
        policy = (
            ROOT / "infra/03-security/openbao/config/policies/backup-snapshot.hcl"
        ).read_text(encoding="utf-8")
        self.assertEqual(
            ['"sys/storage/raft/snapshot"'], re.findall(r"path (\S+)", policy)
        )
        self.assertIn('capabilities = ["read"]', policy)
        service = (ROOT / RESTIC_DIR / "systemd/hyhome-backup.service").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("[Install]", service.splitlines())
        timer = (ROOT / RESTIC_DIR / "systemd/hyhome-backup.timer").read_text(
            encoding="utf-8"
        )
        self.assertIn("Persistent=true", timer)

    def test_offsite_job_is_the_only_backup_egress_and_reads_repos_read_only(
        self,
    ) -> None:
        import yaml

        document = yaml.safe_load((ROOT / RESTIC_COMPOSE).read_text(encoding="utf-8"))
        service = document["services"]["restic-offsite"]
        local = document["services"]["restic"]
        self.assertEqual(["backup"], service["profiles"])
        self.assertEqual(local["image"], service["image"])
        self.assertNotIn("network_mode", service)
        self.assertEqual(["restic_offsite_net"], service["networks"])
        network = document["networks"]["restic_offsite_net"]
        self.assertFalse(network.get("internal", False))
        self.assertEqual(["snapshots"], service["command"])
        self.assertEqual(["DAC_READ_SEARCH"], service["cap_add"])
        self.assertEqual(
            {
                "restic_password",
                "restic_offsite_password",
                "r2_access_key_id",
                "r2_secret_access_key",
            },
            set(service["secrets"]),
        )
        environment = service["environment"]
        # Credentials arrive only as secret files; the script exports them.
        self.assertFalse(any(key.startswith("AWS_ACCESS") for key in environment))
        self.assertFalse(any(key.startswith("AWS_SECRET") for key in environment))
        self.assertEqual(
            "/run/secrets/restic_offsite_password", environment["RESTIC_PASSWORD_FILE"]
        )
        self.assertEqual(
            "/run/secrets/restic_password", environment["RESTIC_FROM_PASSWORD_FILE"]
        )
        mounts = {}
        for volume in service["volumes"]:
            if isinstance(volume, str):
                self.assertTrue(volume.endswith(":ro"), volume)
                continue
            mounts[volume["target"]] = volume
            self.assertIs(True, volume.get("read_only"), volume["target"])
        self.assertEqual({"/repo/state", "/repo/host"}, set(mounts))
        root = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
        for name in service["secrets"]:
            self.assertTrue(
                root["secrets"][name]["file"].startswith("./secrets/backup/"), name
            )

    def test_state_set_carries_the_pgbackrest_repository_offsite(self) -> None:
        # Owner decision 2026-09-25: pgBackRest reaches R2 inside the state
        # Restic repository, not through a direct pgBackRest S3 repository.
        service = _compose_service(RESTIC_COMPOSE, "restic")
        mount = [
            volume
            for volume in service["volumes"]
            if isinstance(volume, dict) and volume["target"] == "/src/state/pgbackrest"
        ]
        self.assertEqual(1, len(mount))
        self.assertTrue(mount[0]["source"].endswith("/pgbackrest"))
        self.assertIs(True, mount[0]["read_only"])
        script = (ROOT / RESTIC_DIR / "backup.sh").read_text(encoding="utf-8")
        self.assertIn('echo /src/state/pgbackrest >>"$list"', script)
        exclude = (ROOT / RESTIC_DIR / "sets/state-exclude.txt").read_text(
            encoding="utf-8"
        )
        self.assertIn("*.pgbackrest.tmp", exclude)
        mng_pg = _compose_service(MNG_DB_COMPOSE, "mng-pg")
        self.assertNotIn("repo2", " ".join(_compose_command(mng_pg)))

    def test_dev_repository_mount_and_scheduler_failure_contract(self) -> None:
        service = _compose_service(RESTIC_COMPOSE, "restic")
        mount = next(
            v
            for v in service["volumes"]
            if isinstance(v, dict) and v["target"] == "/src/state/dev-pgbackrest"
        )
        self.assertTrue(mount["source"].endswith("/dev-pgbackrest"))
        self.assertIs(True, mount["read_only"])
        self.assertIs(False, mount["bind"]["create_host_path"])
        script = (ROOT / RESTIC_DIR / "bin/hyhome-backup.sh").read_text()
        block = script[
            script.index("# Development backup contract.") : script.index(
                "if running mng-valkey; then"
            )
        ]
        with tempfile.TemporaryDirectory() as directory:
            staging = Path(directory)
            for failure in ("none", "check", "backup", "globals", "schema", "stopped"):
                with self.subTest(failure=failure):
                    harness = """set -euo pipefail
status=0
running() { [[ "$FAILURE" != stopped ]]; }
docker() {
  printf '%s\n' "$*" >>"$staging/calls"
  case "$*" in
    *pgbackrest*check*) [[ "$FAILURE" != check ]] ;;
    *pgbackrest*backup*) [[ "$FAILURE" != backup ]] ;;
    *globals-only*) echo synthetic; [[ "$FAILURE" != globals ]] ;;
    *schema-only*) echo synthetic; [[ "$FAILURE" != schema ]] ;;
    *) echo synthetic ;;
  esac
}
"""
                    (staging / "dev-pg-globals.sql").write_text(
                        "stale synthetic export"
                    )
                    result = subprocess.run(
                        ["bash", "-c", harness + block + "exit $status"],
                        check=False,
                        env={**os.environ, "staging": str(staging), "FAILURE": failure},
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(0 if failure == "none" else 1, result.returncode)
                    if failure in ("check", "backup"):
                        self.assertFalse((staging / "dev-pg-globals.sql").exists())
                    if failure in ("globals", "schema"):
                        self.assertFalse((staging / f"dev-pg-{failure}.sql").exists())
                    for artifact in staging.iterdir():
                        artifact.unlink()
        self.assertIn("timeout 1800 pgbackrest --stanza=dev", block)
        self.assertIn("timeout 300 pg_dumpall", block)
        self.assertLess(
            script.index("# Development backup contract."), script.index("state_kib=")
        )
        self.assertIn(
            'echo /src/state/dev-pgbackrest >>"$list"',
            (ROOT / RESTIC_DIR / "backup.sh").read_text(),
        )

    def test_offsite_script_copies_without_deleting_and_samples_remote_data(
        self,
    ) -> None:
        script = (ROOT / RESTIC_DIR / "offsite.sh").read_text(encoding="utf-8")
        self.assertIn("--copy-chunker-params", script)
        self.assertIn("--read-data-subset", script)
        self.assertIn("already initialized; skipped", script)
        # Local repositories are mounted read-only, so the source is not locked.
        self.assertIn("copy --no-lock --from-repo", script)
        self.assertNotIn("set -x", script)
        self.assertIn("forget | prune | unlock)", script)
        # Remote deletion lives only in the confirmed forget-prune action, and
        # keeps every snapshot inside the 30-day bucket lock.
        prune = script.split("forget-prune)")[1].split(";;")[0]
        self.assertIn(
            '"${HYHOME_PRUNE_CONFIRM:-}" != "delete-old-remote-snapshots"', prune
        )
        self.assertIn("--keep-within 30d", prune)
        outside = script.replace(prune, "")
        self.assertNotRegex(outside, r"\brestic (forget|prune|unlock)\b")
        # copy reports the stored size for the free-tier alert.
        self.assertIn("stats --mode raw-data --json", script)
        self.assertIn("R2 repository size:", script)

    def test_orchestrator_copies_offsite_after_local_restic_succeeds(self) -> None:
        script = (ROOT / RESTIC_DIR / "bin/hyhome-backup.sh").read_text(
            encoding="utf-8"
        )
        copy = script.index("restic-offsite copy")
        self.assertLess(script.index("restic check || "), copy)
        self.assertIn("offsite copy not configured", script)
        self.assertIn('[[ "$restic_ok" == true ]]', script)
        self.assertRegex(script, r"restic-offsite copy\)\" \|\| \{[^}]*status=1")
        self.assertIn("restic-offsite check", script)
        self.assertIn("hyhome_backup_offsite_repo_bytes", script)
        rules = (
            ROOT
            / "infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("hyhome_backup_offsite_repo_bytes > 8e9", rules)
        # Plaintext exports are gone and SeaweedFS vacuum resumes before upload.
        self.assertLess(script.rindex("\ncleanup\n"), copy)


CDC_KAFKA_COMPOSE = ROOT / "infra/05-messaging/kafka/docker-compose.yml"
CDC_CONNECTOR = (
    ROOT / "infra/05-messaging/kafka/connect/debezium/postgres-connector.json"
)


def _cdc_docker(*args, check=True, timeout=180, **kw):
    return subprocess.run(
        ["docker", *args],
        capture_output=True,
        text=True,
        check=check,
        timeout=timeout,
        **kw,
    )


def _cdc_after(record):
    # Avro JSON wraps the nullable row in its union branch, named after the
    # record ("hyhome.platform.app.orders.Value").
    ((branch, row),) = record["after"].items()
    assert branch.endswith(".Value"), branch
    return row


SSO_MIDDLEWARE = Path(
    os.environ.get(
        "SSO_MIDDLEWARE", ROOT / "infra/01-gateway/traefik/dynamic/middleware.yml"
    )
)
SSO_PROXY_CFG = ROOT / "infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg"
SSO_SUBNET, SSO_TRAEFIK_IP = "10.250.199.0/24", "10.250.199.2"


def _sso_docker(*args, check=True, timeout=180, **kw):
    return subprocess.run(["docker", *args], capture_output=True, text=True,
                          check=check, timeout=timeout, **kw)  # fmt: skip


def _sso_image(compose, service):
    import yaml

    spec = yaml.safe_load((ROOT / compose).read_text())["services"][service]
    return spec["image"]


SSO_REALM = {
    "realm": "r",
    "enabled": True,
    "groups": [{"name": "admins"}],
    "clients": [{
        "clientId": "proxy", "enabled": True, "publicClient": False,
        "standardFlowEnabled": True, "implicitFlowEnabled": False,
        "directAccessGrantsEnabled": False, "serviceAccountsEnabled": False,
        "redirectUris": ["https://auth.hy.test/oauth2/callback"],
        "attributes": {"pkce.code.challenge.method": "S256",
                       "post.logout.redirect.uris": "https://app.hy.test/*"},
    }],
    "users": [
        {"username": name, "enabled": True, "email": f"{name}@example.test",
         "emailVerified": True, "firstName": name, "lastName": "Synthetic",
         "credentials": [{"type": "password", "value": f"{name}-synthetic",
                          "temporary": False}],
         "groups": groups}
        for name, groups in (("alice", ["/admins"]), ("bob", []))
    ],
}  # fmt: skip

SSO_ROUTERS = """
http:
  routers:
    app:
      rule: Host(`app.hy.test`)
      entryPoints: [websecure]
      tls: {}
      middlewares: [sso-protected-chain@file]
      service: app-svc
    oauth2:
      rule: Host(`auth.hy.test`) && PathPrefix(`/oauth2`)
      entryPoints: [websecure]
      tls: {}
      middlewares: [gateway-standard-chain@file]
      service: oauth2-proxy-svc
  services:
    app-svc:
      loadBalancer:
        servers:
          - url: "http://upstream:8000"
"""

SSO_UPSTREAM = """
import http.server, json
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"user": self.headers.get("X-Auth-Request-User"),
                           "email": self.headers.get("X-Auth-Request-Email")}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.end_headers(); self.wfile.write(body)
http.server.HTTPServer(("0.0.0.0", 8000), H).serve_forever()
"""

# Runs inside the client container: one browser-like session per invocation.
SSO_CLIENT = r"""
import http.cookiejar, json, re, ssl, sys, urllib.parse, urllib.request
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx),
                                     urllib.request.HTTPCookieProcessor(jar), NoRedirect())
def req(url, data=None, accept="text/html"):
    r = urllib.request.Request(url, data=data, headers={"Accept": accept})
    try:
        resp = opener.open(r, timeout=20)
    except urllib.error.HTTPError as e:
        resp = e
    return (resp.status, resp.headers.get("Location") or "",
            resp.headers.get("Content-Type") or "", resp.read().decode("utf-8", "replace"))
def login(user):
    status, loc, _, _ = req("https://app.hy.test/")
    assert status == 302 and "/protocol/openid-connect/auth" in loc, (status, loc)
    query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(loc).query))
    status, _, _, page = req(loc)
    action = re.search(r'action="([^"]+)"', page).group(1).replace("&amp;", "&")
    form = urllib.parse.urlencode({"username": user, "password": user + "-synthetic"}).encode()
    status, loc, _, _ = req(action, form)
    assert status == 302 and loc.startswith("https://auth.hy.test/oauth2/callback"), (status, loc)
    callback = req(loc)[0]
    cookies = {c.name: {"domain": c.domain, "secure": c.secure,
                        "httponly": c.has_nonstandard_attr("HttpOnly")}
               for c in jar}
    return query, cookies, callback
mode = sys.argv[1]
out = {}
if mode == "anonymous":
    for accept in ("text/html", "application/json"):
        status, loc, ctype, _ = req("https://app.hy.test/api/v1/data", accept=accept)
        out[accept] = {"status": status, "location": loc.split("?")[0], "type": ctype}
else:
    query, cookies, callback = login(mode)
    out["callback"] = callback
    keys = ("client_id", "redirect_uri", "code_challenge_method", "response_type")
    out["authorize"] = {k: query.get(k) for k in keys}
    out["state_and_challenge"] = bool(query.get("state")) and bool(query.get("code_challenge"))
    out["cookies"] = cookies
    status, _, _, body = req("https://app.hy.test/", accept="application/json")
    out["app"] = {"status": status, "body": body[:300]}
    status, _, _, _ = req("https://auth.hy.test/oauth2/sign_out?rd=https%3A%2F%2Fapp.hy.test%2F")
    out["sign_out"] = status
    status, loc, _, _ = req("https://app.hy.test/")
    out["after_sign_out"] = {"status": status, "location": loc.split("?")[0]}
print(json.dumps(out))
"""


@unittest.skipUnless(
    os.environ.get("HYHOME_SSO_REHEARSAL") == "1",
    "set HYHOME_SSO_REHEARSAL=1 to run the disposable SSO rehearsal (needs Docker)",
)
class SsoRehearsalTests(unittest.TestCase):
    """Traefik, oauth2-proxy and Keycloak on an internal network: synthetic
    realm, two users and the tracked middleware and proxy config."""

    @classmethod
    def setUpClass(cls):
        cls.tag = f"hysso{os.getpid()}"
        cls.proxy_image = f"hy-home/oauth2-proxy:rehearsal-{cls.tag}"
        _sso_docker("build", "-q", "-t", cls.proxy_image, "-f",
                    str(ROOT / "infra/02-auth/oauth2-proxy/dev.Dockerfile"),
                    str(ROOT / "infra/02-auth/oauth2-proxy"), timeout=900)  # fmt: skip
        cls.addClassCleanup(_sso_docker, "image", "rm", cls.proxy_image, check=False)
        cls.tmp = Path(tempfile.mkdtemp(prefix="hysso"))
        cls.addClassCleanup(shutil.rmtree, cls.tmp, True)
        (cls.tmp / "dynamic").mkdir()
        shutil.copy(SSO_MIDDLEWARE, cls.tmp / "dynamic/middleware.yml")
        (cls.tmp / "dynamic/routers.yml").write_text(SSO_ROUTERS)
        (cls.tmp / "import").mkdir()
        # Random, synthetic and removed with the temporary directory; the
        # containers read them as mounted files, as on HOME.
        client_value = os.urandom(16).hex()
        realm = json.loads(json.dumps(SSO_REALM))
        realm["clients"][0]["secret"] = client_value
        (cls.tmp / "import/r.json").write_text(json.dumps(realm))
        (cls.tmp / "secrets").mkdir()
        (cls.tmp / "secrets/client").write_text(client_value)
        (cls.tmp / "secrets/cookie").write_text(os.urandom(16).hex())
        for path in [cls.tmp, *cls.tmp.rglob("*")]:
            path.chmod(0o755 if path.is_dir() else 0o644)
        _sso_docker("network", "create", "--internal", "--subnet", SSO_SUBNET, cls.tag)
        cls.addClassCleanup(_sso_docker, "network", "rm", cls.tag, check=False)
        for name in ("keycloak", "upstream", "proxy", "traefik", "client"):
            cls.addClassCleanup(
                _sso_docker, "rm", "-f", f"{cls.tag}-{name}", check=False
            )
        net = ["--network", cls.tag]
        # Traefik first, so no dynamic address takes its fixed one.
        _sso_docker("run", "-d", "--name", f"{cls.tag}-traefik", *net, "--ip", SSO_TRAEFIK_IP,
               "--network-alias", "app.hy.test", "--network-alias", "auth.hy.test",
               "-v", f"{cls.tmp}/dynamic:/dynamic:ro", _sso_image("infra/01-gateway/traefik/docker-compose.yml", "traefik"),
               "--entrypoints.websecure.address=:443", "--providers.file.directory=/dynamic",
               "--log.level=ERROR")  # fmt: skip
        _sso_docker("run", "-d", "--name", f"{cls.tag}-keycloak", *net, "--network-alias", "keycloak",
               "-e", "KC_BOOTSTRAP_ADMIN_USERNAME=admin",
               "-e", "KC_BOOTSTRAP_ADMIN_PASSWORD=synthetic-admin",
               "-v", f"{cls.tmp}/import:/opt/keycloak/data/import:ro",
               _sso_image("infra/02-auth/keycloak/docker-compose.yml", "keycloak"),
               "start-dev", "--import-realm", "--http-port=8080",
               "--hostname=http://keycloak:8080")  # fmt: skip
        _sso_docker("run", "-d", "--name", f"{cls.tag}-upstream", *net, "--network-alias", "upstream",
               "python:3.13.15-alpine", "python", "-c", SSO_UPSTREAM)  # fmt: skip
        _sso_docker("run", "-d", "--name", f"{cls.tag}-client", *net,
               "python:3.13.15-alpine", "sleep", "infinity")  # fmt: skip
        cls.wait(cls.fetch_ok("http://keycloak:8080/realms/r"), "keycloak", tries=150)
        cls.add_group_mapper()
        # The tracked config; only deployment-specific values are replaced.
        env = {
            "OAUTH2_PROXY_CLIENT_ID": "proxy",
            "OAUTH2_PROXY_OIDC_ISSUER_URL": "http://keycloak:8080/realms/r",
            "OAUTH2_PROXY_REDIRECT_URL": "https://auth.hy.test/oauth2/callback",
            "OAUTH2_PROXY_COOKIE_DOMAINS": ".hy.test",
            "OAUTH2_PROXY_WHITELIST_DOMAINS": ".hy.test",
            "OAUTH2_PROXY_TRUSTED_PROXY_IPS": f"{SSO_TRAEFIK_IP}/32",
            "OAUTH2_PROXY_SESSION_STORE_TYPE": "cookie",
            "OAUTH2_PROXY_SCOPE": "openid email profile",
        }
        args = [x for key, value in env.items() for x in ("-e", f"{key}={value}")]
        _sso_docker("run", "-d", "--name", f"{cls.tag}-proxy", *net, "--network-alias", "oauth2-proxy",
               *args, "-v", f"{SSO_PROXY_CFG}:/etc/oauth2-proxy.cfg:ro",
               "-v", f"{cls.tmp}/secrets/client:/run/secrets/oauth2_proxy_client_secret:ro",
               "-v", f"{cls.tmp}/secrets/cookie:/run/secrets/oauth2_proxy_cookie_secret:ro",
               cls.proxy_image)  # fmt: skip
        cls.wait(
            cls.fetch_ok("http://oauth2-proxy:4180/ping"), "oauth2-proxy", tries=60
        )

    @classmethod
    def fetch_ok(cls, url):
        code = f"import urllib.request;urllib.request.urlopen({url!r},timeout=5)"
        return lambda: _sso_docker("exec", f"{cls.tag}-client", "python", "-c", code,
                              check=False).returncode == 0  # fmt: skip

    @classmethod
    def add_group_mapper(cls):
        # Group paths in the tokens, as the HOME realm gives allowed_groups.
        script = (
            "cd /tmp && export HOME=/tmp && K=/opt/keycloak/bin/kcadm.sh && "
            "$K config credentials --server http://localhost:8080 --realm master "
            "--user admin --password synthetic-admin >/dev/null && "
            "ID=$($K get clients -r r -q clientId=proxy --fields id --format csv --noquotes) && "
            "$K create clients/$ID/protocol-mappers/models -r r -s name=groups "
            "-s protocol=openid-connect -s protocolMapper=oidc-group-membership-mapper "
            "-s 'config.\"full.path\"=true' -s 'config.\"id.token.claim\"=true' "
            "-s 'config.\"access.token.claim\"=true' -s 'config.\"userinfo.token.claim\"=true' "
            "-s 'config.\"claim.name\"=groups' >/dev/null"
        )
        _sso_docker("exec", f"{cls.tag}-keycloak", "bash", "-c", script)

    @classmethod
    def wait(cls, probe, what, tries=60):
        for _ in range(tries):
            if probe():
                return
            time.sleep(2)
        logs = _sso_docker("logs", "--tail", "20", f"{cls.tag}-proxy", check=False)
        raise AssertionError(
            f"{what} not ready\n{logs.stdout[-2000:]}{logs.stderr[-2000:]}"
        )

    def browse(self, mode):
        out = _sso_docker("exec", f"{self.tag}-client", "python", "-c", SSO_CLIENT, mode,
                     check=False, timeout=120)  # fmt: skip
        self.assertEqual(0, out.returncode, out.stderr[-2000:])
        print(mode, out.stdout.strip())
        return json.loads(out.stdout)

    def test_anonymous_browser_is_redirected_and_machine_client_is_refused(self):
        out = self.browse("anonymous")
        browser = out["text/html"]
        self.assertEqual(302, browser["status"])
        self.assertTrue(
            browser["location"].endswith("/realms/r/protocol/openid-connect/auth")
        )
        # A login page is not an API answer: a JSON client gets 401.
        self.assertEqual(401, out["application/json"]["status"], out)

    def test_member_signs_in_with_pkce_and_signs_out(self):
        out = self.browse("alice")
        self.assertEqual("S256", out["authorize"]["code_challenge_method"])
        self.assertEqual(
            "https://auth.hy.test/oauth2/callback", out["authorize"]["redirect_uri"]
        )
        self.assertTrue(out["state_and_challenge"])
        cookie = out["cookies"]["__Secure-sso-cookie"]
        self.assertEqual(".hy.test", cookie["domain"])
        self.assertTrue(cookie["secure"] and cookie["httponly"])
        self.assertEqual(200, out["app"]["status"])
        self.assertIn("alice", out["app"]["body"])
        self.assertEqual(302, out["after_sign_out"]["status"])

    def test_non_member_is_denied(self):
        # oauth2-proxy refuses the session at the callback (allowed_groups), so
        # no SSO cookie exists and the application never answers.
        out = self.browse("bob")
        self.assertEqual(403, out["callback"], out)
        self.assertNotIn("__Secure-sso-cookie", out["cookies"])
        self.assertNotEqual(200, out["app"]["status"])


@unittest.skipUnless(
    os.environ.get("HYHOME_CDC_REHEARSAL") == "1",
    "set HYHOME_CDC_REHEARSAL=1 to run the disposable CDC stream rehearsal (needs Docker)",
)
class CdcStreamRehearsalTests(unittest.TestCase):
    """Rehearse the tracked connector end to end on synthetic data only.

    Every container joins one temporary internal network under the aliases the
    tracked connector names, publishes no port, and is removed afterwards.
    """

    # A password with Properties-significant characters proves the renderer.
    SPECIAL_VALUE = " lead\\back#hash=eq:colon!é"

    @classmethod
    def image(cls, service):
        import yaml

        return yaml.safe_load(CDC_KAFKA_COMPOSE.read_text())["services"][service][
            "image"
        ]

    @classmethod
    def setUpClass(cls):
        cls.tag = f"hycdc{os.getpid()}"
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        secret = Path(cls.tmp.name) / "debezium_postgres_password"
        secret.write_text(cls.SPECIAL_VALUE)
        secret.chmod(0o644)
        _cdc_docker("network", "create", "--internal", cls.tag)
        cls.addClassCleanup(_cdc_docker, "network", "rm", cls.tag, check=False)
        dev_image = re.search(
            r"^FROM (\S+)",
            (ROOT / "infra/04-data/dev-db/pg/Dockerfile").read_text(),
            re.M,
        ).group(1)
        run = ["run", "-d", "--network", cls.tag]
        specs = {
            "pg": (["--network-alias", "dev-pg", "-e", "POSTGRES_USER=admin",
                    "-e", "POSTGRES_PASSWORD=synthetic-admin", dev_image, "postgres",
                    "-c", "wal_level=logical", "-c", "shared_preload_libraries=timescaledb"]),
            "kafka": (["--network-alias", "kafka-1",
                       "-e", "CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qg",
                       "-e", "KAFKA_NODE_ID=1",
                       "-e", "KAFKA_PROCESS_ROLES=broker,controller",
                       "-e", "KAFKA_CONTROLLER_QUORUM_VOTERS=1@kafka-1:9093",
                       "-e", "KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:19092,CONTROLLER://0.0.0.0:9093",
                       "-e", "KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka-1:19092",
                       "-e", "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT",
                       "-e", "KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER",
                       "-e", "KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT",
                       "-e", "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1",
                       "-e", "KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1",
                       "-e", "KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1",
                       "-e", "KAFKA_AUTO_CREATE_TOPICS_ENABLE=false",
                       "-e", "KAFKA_HEAP_OPTS=-Xms256M -Xmx512M",
                       cls.image("kafka-1")]),
            "sr": (["--network-alias", "schema-registry",
                    "-e", "SCHEMA_REGISTRY_HOST_NAME=schema-registry",
                    "-e", "SCHEMA_REGISTRY_LISTENERS=http://0.0.0.0:8081",
                    "-e", "SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS=PLAINTEXT://kafka-1:19092",
                    "-e", "SCHEMA_REGISTRY_KAFKASTORE_TOPIC_REPLICATION_FACTOR=1",
                    cls.image("schema-registry")]),
            "client": (["python:3.13.15-alpine", "sleep", "infinity"]),
        }  # fmt: skip
        for name, args in specs.items():
            cls.addClassCleanup(
                _cdc_docker, "rm", "-f", f"{cls.tag}-{name}", check=False
            )
            _cdc_docker(*run, "--name", f"{cls.tag}-{name}", *args)
        cls.addClassCleanup(_cdc_docker, "rm", "-f", f"{cls.tag}-connect", check=False)
        cls.start_connect(secret)
        cls.wait(
            lambda: cls.sql("SELECT 1", db="postgres") == "1",
            "postgres",
            tries=150,
            container="pg",
        )
        cls.provision()
        cls.wait(cls.connect_ready, "kafka connect", tries=120)

    @classmethod
    def start_connect(cls, secret):
        import yaml

        env = yaml.safe_load(CDC_KAFKA_COMPOSE.read_text())["services"][
            "kafka-connect"
        ]["environment"]
        args = []
        for key, value in env.items():
            if key == "KAFKA_OPTS":
                continue  # the JMX agent jar is not mounted here
            value = re.sub(r"\$\{[A-Z_]+:-([^}]*)\}", r"\1", str(value))
            args += ["-e", f"{key}={value}"]
        _cdc_docker(
            "run", "-d", "--name", f"{cls.tag}-connect", "--network", cls.tag,
            "--network-alias", "kafka-connect",
            "-v", f"{secret}:/run/secrets/debezium_postgres_password:ro",
            "-v", f"{ROOT}/infra/05-messaging/kafka/connect/render-connect-secrets.sh:/usr/local/bin/render-connect-secrets.sh:ro",
            *args, cls.image("kafka-connect"),
            "/bin/bash", "/usr/local/bin/render-connect-secrets.sh",
        )  # fmt: skip

    @classmethod
    def wait(cls, probe, what, tries=60, container="connect"):
        for _ in range(tries):
            try:
                if probe():
                    return
            except Exception:
                pass
            time.sleep(2)
        logs = _cdc_docker(
            "logs", "--tail", "25", f"{cls.tag}-{container}", check=False
        )
        raise AssertionError(
            f"{what} not ready\n{logs.stdout[-3000:]}{logs.stderr[-3000:]}"
        )

    @classmethod
    def sql(cls, query, db="platform_dev"):
        out = _cdc_docker(
            "exec", f"{cls.tag}-pg", "psql", "-h", "127.0.0.1", "-v", "ON_ERROR_STOP=1", "-U", "admin",
            "-d", db, "-Atc", query,
        )  # fmt: skip
        return out.stdout.strip()

    CLIENT = """
import sys, urllib.request
method, url = sys.argv[1], sys.argv[2]
data = sys.stdin.buffer.read() or None
req = urllib.request.Request(url, data=data, method=method,
                             headers={"Content-Type": "application/json"})
try:
    print(urllib.request.urlopen(req, timeout=20).read().decode())
except urllib.error.HTTPError as error:
    print(error.read().decode())
"""

    @classmethod
    def http(cls, method, url, body=None):
        # Neither the Connect nor the Registry image ships curl.
        return _cdc_docker(
            "exec", "-i", f"{cls.tag}-client", "python", "-c", cls.CLIENT, method, url,
            input=body or "", check=False,
        ).stdout  # fmt: skip

    @classmethod
    def connect_ready(cls):
        return cls.http("GET", "http://kafka-connect:8083/connectors").startswith("[")

    @classmethod
    def provision(cls):
        cls.sql("CREATE ROLE platform_owner NOLOGIN", db="postgres")
        cls.sql("CREATE DATABASE platform_dev OWNER platform_owner", db="postgres")
        cls.sql("CREATE SCHEMA app AUTHORIZATION platform_owner")
        cls.sql(
            "CREATE TABLE app.orders (id int PRIMARY KEY, item text NOT NULL);"
            "ALTER TABLE app.orders OWNER TO platform_owner;"
            "INSERT INTO app.orders VALUES (1, 'snapshot-a'), (2, 'snapshot-b')"
        )
        env = {
            "DEBEZIUM_DB_USER": "debezium",
            "DEBEZIUM_DB_NAME": "platform_dev",
            "DEBEZIUM_SCHEMA": "app",
            "DEBEZIUM_HEARTBEAT_SCHEMA": "debezium_heartbeat",
            "DEBEZIUM_PUBLICATION": "hyhome_platform_publication",
            "DEBEZIUM_SOURCE_OWNER": "platform_owner",
            "DEBEZIUM_DB_PASSWORD": cls.SPECIAL_VALUE,
        }
        args = ["exec", "-i"]
        for key, value in env.items():
            args += ["-e", f"{key}={value}"]
        sql = ROOT / "infra/05-messaging/kafka/connect/debezium/provisioning/dev-pg.sql"
        _cdc_docker(
            *args, f"{cls.tag}-pg", "psql", "-h", "127.0.0.1", "-q", "-U", "admin", "-d", "postgres",
            "-f", "-", input=sql.read_text(),
        )  # fmt: skip

    def consume(self, count):
        out = _cdc_docker(
            "exec", f"{self.tag}-sr", "kafka-avro-console-consumer",
            "--bootstrap-server", "kafka-1:19092", "--topic", "hyhome.platform.app.orders",
            "--from-beginning", "--max-messages", str(count), "--timeout-ms", "60000",
            "--property", "schema.registry.url=http://localhost:8081",
            "--group", f"rehearsal-{uuid.uuid4().hex[:8]}",
            check=False, timeout=120,
        ).stdout  # fmt: skip
        return [json.loads(line) for line in out.splitlines() if line.startswith("{")]

    def running(self):
        status = json.loads(
            self.http(
                "GET", "http://kafka-connect:8083/connectors/hyhome-platform/status"
            )
        )
        tasks = status.get("tasks") or [{}]
        return status["connector"]["state"] == tasks[0].get("state") == "RUNNING"

    def slot(self, column):
        return self.sql(
            f"SELECT {column} FROM pg_replication_slots"
            " WHERE slot_name = 'hyhome_platform_slot'"
        )

    def test_1_stream_decode_evolve_and_resume(self):
        config = json.loads(CDC_CONNECTOR.read_text())
        config = config.get("config", config)
        body = self.http(
            "PUT",
            "http://kafka-connect:8083/connectors/hyhome-platform/config",
            json.dumps(config),
        )
        self.assertIn('"name":"hyhome-platform"', body.replace(" ", ""), body[:400])
        self.wait(self.running, "connector RUNNING", tries=90)
        # The connector created the slot; provisioning never does.
        self.wait(lambda: self.slot("active") == "t", "active slot")

        rows = self.consume(2)
        self.assertEqual(
            ["snapshot-a", "snapshot-b"], sorted(_cdc_after(r)["item"] for r in rows)
        )

        # A streamed row, then an additive column: a second registered version.
        self.sql("INSERT INTO app.orders VALUES (3, 'stream-c')")
        self.sql("ALTER TABLE app.orders ADD COLUMN note text")
        self.sql("INSERT INTO app.orders VALUES (4, 'stream-d', 'evolved')")
        # Three partitions (topic.creation.default.partitions) order only per
        # key, so rows are compared by primary key.
        rows = {_cdc_after(r)["id"]: _cdc_after(r) for r in self.consume(4)}
        self.assertEqual({1, 2, 3, 4}, set(rows))
        self.assertEqual("stream-d", rows[4]["item"])
        self.assertIn("evolved", json.dumps(rows[4]["note"]))
        versions = self.http(
            "GET",
            "http://schema-registry:8081/subjects/hyhome.platform.app.orders-value/versions",
        )
        self.assertEqual([1, 2], json.loads(versions))

        # A restarted worker resumes from its stored offset without a second
        # snapshot: exactly one new event follows the four already read.
        _cdc_docker("restart", f"{self.tag}-connect")
        self.wait(self.connect_ready, "kafka connect after restart", tries=120)
        self.wait(self.running, "connector RUNNING after restart", tries=90)
        self.sql("INSERT INTO app.orders VALUES (5, 'after-restart', NULL)")
        ids = sorted(_cdc_after(r)["id"] for r in self.consume(6))
        self.assertEqual([1, 2, 3, 4, 5], ids)

    def test_2_heartbeat_writes_and_advances_the_slot(self):
        before = self.slot("confirmed_flush_lsn")
        time.sleep(75)  # the tracked heartbeat.interval.ms is 60000
        beats = self.sql(
            "SELECT count(*) FROM debezium_heartbeat.heartbeat"
            " WHERE beat_at > now() - interval '2 minutes'"
        )
        self.assertEqual("1", beats)
        self.assertNotEqual(before, self.slot("confirmed_flush_lsn"))


@unittest.skipUnless(
    os.environ.get("HYHOME_BACKUP_REHEARSAL") == "1",
    "set HYHOME_BACKUP_REHEARSAL=1 to run the disposable backup rehearsal (needs Docker)",
)
class BackupRestoreRehearsalTests(unittest.TestCase):
    """pgBackRest full/diff/PITR and Restic round trips on synthetic data only.

    Everything runs on an internal network with bind mounts under a temporary
    directory; no named volume, host port or HOME container is touched.
    """

    RESTIC_IMAGE = "restic/restic:0.19.1"

    @classmethod
    def setUpClass(cls) -> None:
        cls.tag = f"hybackup{os.getpid()}"
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.dir = Path(cls.tmp.name)
        # Containers leave files owned by UID 70 or root; hand them back before
        # the temporary directory is removed (cleanups run last-in, first-out).
        cls.addClassCleanup(
            subprocess.run,
            [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{cls.dir}:/w",
                "--entrypoint",
                "chown",
                cls.RESTIC_IMAGE,
                "-R",
                f"{os.getuid()}:{os.getgid()}",
                "/w",
            ],
            capture_output=True,
        )
        cls.image = f"hy-home/mng-pg:rehearsal-{cls.tag}"
        subprocess.run(
            ["docker", "build", "-q", "-t", cls.image, str(ROOT / PGBACKREST_DIR)],
            check=True,
            capture_output=True,
        )
        cls.addClassCleanup(
            subprocess.run, ["docker", "image", "rm", cls.image], capture_output=True
        )
        subprocess.run(
            ["docker", "network", "create", "--internal", cls.tag],
            check=True,
            capture_output=True,
        )
        cls.addClassCleanup(
            subprocess.run, ["docker", "network", "rm", cls.tag], capture_output=True
        )
        # The repository is written by UID 70; the restore target gets the
        # runbook's 0755 so the rehearsal cannot hide a traversal failure.
        for name, mode in (("repo", 0o777), ("restore", 0o755), ("sec", 0o755)):
            (cls.dir / name).mkdir()
            (cls.dir / name).chmod(mode)
        cls.secret("pgbackrest_cipher_pass", "synthetic-cipher-pass")
        cls.secret("pw", "synthetic-admin")

    @classmethod
    def secret(cls, name: str, value: str) -> Path:
        path = cls.dir / "sec" / name
        path.write_text(value, encoding="utf-8")
        path.chmod(0o644)
        return path

    def docker(
        self, *args: str, check: bool = True
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["docker", *args], check=check, capture_output=True, text=True, timeout=600
        )

    def start_server(
        self, name: str, data: Path, *extra: str, pg_args: tuple[str, ...] = ()
    ) -> None:
        self.addCleanup(self.docker, "rm", "-f", name, check=False)
        self.docker(
            "run",
            "-d",
            "--name",
            name,
            "--network",
            self.tag,
            "-e",
            "POSTGRES_USER=admin",
            "-e",
            "POSTGRES_PASSWORD_FILE=/run/secrets/pw",
            "-e",
            "PGDATA=/var/lib/postgresql/data/pgdata",
            "-e",
            "PGBACKREST_PG1_USER=admin",
            "-e",
            "PGBACKREST_CONFIG_INCLUDE_PATH=/tmp/pgbackrest/conf.d",
            "-v",
            f"{self.dir}/sec/pgbackrest_cipher_pass:/run/secrets/pgbackrest_cipher_pass:ro",
            "-v",
            f"{self.dir}/sec/pw:/run/secrets/pw:ro",
            "-v",
            f"{data}:/var/lib/postgresql/data",
            *extra,
            self.image,
            "postgres",
            *pg_args,
        )
        self.start_server_ready(name)

    def start_server_ready(self, name: str) -> None:
        for _ in range(90):
            ready = self.docker(
                "exec",
                name,
                "psql",
                "-U",
                "admin",
                "-d",
                "postgres",
                "-Atc",
                "select 1",
                check=False,
            )
            if ready.returncode == 0:
                return
            subprocess.run(["sleep", "1"], check=True)
        self.fail(self.docker("logs", name, check=False).stderr[-2000:])

    def sql(self, name: str, query: str) -> str:
        return self.docker(
            "exec", name, "psql", "-U", "admin", "-d", "postgres", "-Atc", query
        ).stdout.strip()

    def pgbackrest(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return self.docker(
            "exec", "-u", "postgres", name, "pgbackrest", "--stanza=mng", *args
        )

    def test_full_diff_and_point_in_time_restore(self) -> None:
        source = self.dir / "src-data"
        source.mkdir()
        source.chmod(0o755)
        db = f"{self.tag}-db"
        self.start_server(
            db,
            source,
            "-v",
            f"{self.dir}/repo:/var/lib/pgbackrest",
            pg_args=(
                "-c",
                "archive_mode=on",
                "-c",
                "archive_command=pgbackrest --stanza=mng archive-push %p",
                "-c",
                "archive_timeout=60",
            ),
        )
        self.pgbackrest(db, "stanza-create")
        self.pgbackrest(db, "check")
        self.pgbackrest(db, "--type=full", "backup")
        self.sql(
            db, "create table t(id int); insert into t select generate_series(1,100)"
        )
        self.pgbackrest(db, "--type=diff", "backup")
        self.sql(db, "insert into t select generate_series(101,150)")
        subprocess.run(["sleep", "1"], check=True)
        target = self.sql(db, "select now()")
        subprocess.run(["sleep", "1"], check=True)
        self.sql(db, "insert into t select generate_series(151,999)")
        self.sql(db, "select pg_switch_wal()")
        subprocess.run(["sleep", "3"], check=True)
        info = self.pgbackrest(db, "info").stdout
        self.assertIn("status: ok", info)
        self.assertIn("diff backup", info)

        restored = self.dir / "restore"
        self.docker(
            "run",
            "--rm",
            "--network",
            self.tag,
            "-v",
            f"{self.dir}/sec/pgbackrest_cipher_pass:/run/secrets/pgbackrest_cipher_pass:ro",
            "-v",
            f"{self.dir}/repo:/var/lib/pgbackrest:ro",
            "-v",
            f"{restored}:/var/lib/postgresql/data",
            "--entrypoint",
            "sh",
            self.image,
            "-ec",
            "mkdir -p /tmp/pgbackrest/conf.d; "
            'printf "[global]\\nrepo1-cipher-pass=%s\\n" "$(cat /run/secrets/pgbackrest_cipher_pass)"'
            " > /tmp/pgbackrest/conf.d/cipher.conf; chown -R postgres /tmp/pgbackrest; "
            "install -d -o postgres -g postgres -m 0700 /var/lib/postgresql/data/pgdata; "
            "gosu postgres pgbackrest --config-include-path=/tmp/pgbackrest/conf.d "
            f"--stanza=mng --type=time '--target={target}' --target-action=promote "
            "--archive-mode=off restore",
        )
        # Recovery runs archive-get, so the restored server needs the image
        # entrypoint, the read-only repository and the cipher secret.
        self.start_server(
            f"{self.tag}-restored",
            restored,
            "-v",
            f"{self.dir}/repo:/var/lib/pgbackrest:ro",
        )
        self.assertEqual(
            "150|150",
            self.sql(f"{self.tag}-restored", "select count(*), max(id) from t"),
        )

    def test_empty_cipher_secret_fails_before_start(self) -> None:
        empty = self.secret("empty", "  ")
        result = self.docker(
            "run",
            "--rm",
            "-v",
            f"{empty}:/run/secrets/pgbackrest_cipher_pass:ro",
            self.image,
            check=False,
        )
        self.assertEqual(64, result.returncode)

    def test_restic_round_trip_excludes_and_guards(self) -> None:
        base = self.dir / "restic"
        for sub in (
            "repo-state",
            "repo-host",
            "pgbackrest",
            "dev-pgbackrest",
            "vol/ai/comfyui/input",
            "vol/management/pg",
            "staging",
            "secrets",
            "out",
        ):
            (base / sub).mkdir(parents=True)
        (base / "out").chmod(0o777)
        (base / "vol/ai/comfyui/input/a.txt").write_text("payload", encoding="utf-8")
        (base / "vol/management/pg/PG_VERSION").write_text("18", encoding="utf-8")
        (base / "secrets/x.txt").write_text("synthetic-secret", encoding="utf-8")
        (base / "dev-pgbackrest/backup.info").write_text(
            "synthetic-backup", encoding="utf-8"
        )
        (base / "env").write_text("K=v\n", encoding="utf-8")
        (base / "pw").write_text("synthetic-restic-pw", encoding="utf-8")
        (base / "pw").chmod(0o644)
        restic_dir = ROOT / RESTIC_DIR

        def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
            return self.docker(
                "run",
                "--rm",
                "-u",
                "0:0",
                "--cap-drop",
                "ALL",
                "--cap-add",
                "DAC_OVERRIDE",
                "--security-opt",
                "no-new-privileges:true",
                "--read-only",
                "--tmpfs",
                "/tmp",
                "--network",
                "none",
                "-e",
                "RESTIC_PASSWORD_FILE=/run/secrets/restic_password",
                "-e",
                "RESTIC_CACHE_DIR=/tmp/c",
                "-v",
                f"{base}/pw:/run/secrets/restic_password:ro",
                "-v",
                f"{restic_dir}/backup.sh:/opt/hyhome/backup.sh:ro",
                "-v",
                f"{restic_dir}/sets:/opt/hyhome/sets:ro",
                "-v",
                f"{base}/repo-state:/repo/state",
                "-v",
                f"{base}/repo-host:/repo/host",
                "-v",
                f"{base}/vol:/src/state/volumes:ro",
                "-v",
                f"{base}/staging:/src/state/exports:ro",
                "-v",
                f"{base}/pgbackrest:/src/state/pgbackrest:ro",
                "-v",
                f"{base}/dev-pgbackrest:/src/state/dev-pgbackrest:ro",
                "-v",
                f"{base}/secrets:/src/host/secrets:ro",
                "-v",
                f"{base}/env:/src/host/env/.env:ro",
                "-v",
                f"{base}/out:/out",
                "--entrypoint",
                "/bin/sh",
                self.RESTIC_IMAGE,
                "/opt/hyhome/backup.sh",
                *args,
                check=check,
            )

        self.assertEqual(65, run("backup", check=False).returncode)
        run("init")
        self.assertIn("already initialized; skipped", run("init").stdout)
        run("backup")
        run("check")
        listing = run("cmd", "state", "ls", "latest").stdout
        self.assertIn("/src/state/volumes/ai/comfyui/input/a.txt", listing)
        self.assertNotIn("PG_VERSION", listing)
        self.assertIn("/src/state/dev-pgbackrest/backup.info", listing)
        # Restore runs in a plain container (RUN-0021): the hardened job has no
        # CHOWN/FOWNER to reapply ownership and must never write a source.
        self.docker(
            "run",
            "--rm",
            "-e",
            "RESTIC_PASSWORD_FILE=/pw",
            "-v",
            f"{base}/pw:/pw:ro",
            "-v",
            f"{base}/repo-host:/repo:ro",
            "-v",
            f"{base}/out:/out",
            self.RESTIC_IMAGE,
            "-r",
            "/repo",
            "--no-lock",
            "restore",
            "latest",
            "--target",
            "/out",
        )
        restored = self.docker(
            "run",
            "--rm",
            "-v",
            f"{base}/out:/r:ro",
            "--entrypoint",
            "cat",
            self.RESTIC_IMAGE,
            "/r/src/host/secrets/x.txt",
        ).stdout
        self.assertEqual("synthetic-secret", restored)
        self.assertEqual(64, run("forget-prune", check=False).returncode)
        self.assertEqual(
            64, run("cmd", "state", "forget", "latest", check=False).returncode
        )
        (base / "pw").write_text("wrong", encoding="utf-8")
        wrong = run("cmd", "state", "snapshots", check=False)
        self.assertNotEqual(0, wrong.returncode)
        self.assertIn("wrong password", wrong.stderr)


SEAWEEDFS_DIR = "infra/04-data/seaweedfs"
FLINK_SERVICES = ("flink-jobmanager", "flink-taskmanager")
SEAWEEDFS_SERVICES = (
    "seaweedfs-master",
    "seaweedfs-volume",
    "seaweedfs-filer",
    "seaweedfs-s3",
)


class SeaweedfsContractTests(unittest.TestCase):
    """Static S06 contracts; SeaweedfsRehearsalTests proves them at runtime."""

    def test_nginx_cdn_is_a_read_only_prefix_to_cdn_bucket(self) -> None:
        conf = (ROOT / "infra/01-gateway/nginx/config/nginx.conf").read_text(
            encoding="utf-8"
        )
        block = conf[conf.index("location ^~ /cdn/ {") :]
        block = block[: block.index("\n        }\n")]
        self.assertIn("limit_except GET HEAD { deny all; }", block)
        self.assertIn("proxy_pass http://seaweedfs_s3/cdn-bucket/;", block)
        self.assertNotIn("minio", conf)

    def services(self) -> dict[str, dict]:
        import yaml

        path = ROOT / SEAWEEDFS_DIR / "docker-compose.yml"
        return yaml.safe_load(path.read_text(encoding="utf-8"))["services"]

    def test_every_component_starts_through_the_security_script(self) -> None:
        services = self.services()
        for name in SEAWEEDFS_SERVICES:
            service = services[name]
            self.assertEqual("1000:1000", service["user"], name)
            self.assertEqual(
                ["/bin/sh", "/opt/hyhome/hyhome-seaweedfs.sh"],
                service["entrypoint"],
                name,
            )
            self.assertIn("seaweedfs_jwt_filer_key", service["secrets"], name)

    def test_state_is_persistent_and_only_s3_is_routed(self) -> None:
        services = self.services()
        commands = {
            name: " ".join(services[name]["command"]) for name in SEAWEEDFS_SERVICES
        }
        self.assertIn("-mdir=/data", commands["seaweedfs-master"])
        self.assertIn("-dir=/data", commands["seaweedfs-volume"])
        for name in ("seaweedfs-master", "seaweedfs-volume", "seaweedfs-filer"):
            self.assertTrue(
                any(str(v).endswith(":/data:rw") for v in services[name]["volumes"]),
                name,
            )
            self.assertNotIn("traefik.enable=true", _labels(services[name]), name)
            # The master issues write JWTs and deletes collections for any
            # caller, so these three are reachable only on the internal network.
            self.assertEqual(
                {"seaweed_internal"}, set(services[name]["networks"]), name
            )
            self.assertEqual("/etc/seaweedfs", services[name]["working_dir"], name)
        # The Iceberg REST catalog (S12) is on; like S3 it has no host port,
        # and the only route still targets the S3 port.
        for flag in (
            "-port.iceberg=${SEAWEEDFS_ICEBERG_PORT:-8181}",
            "-port.lance=0",
            "-iam=false",
        ):
            self.assertIn(flag, commands["seaweedfs-s3"])
        self.assertNotIn("ports", services["seaweedfs-s3"])
        self.assertIn(
            "traefik.http.services.s3.loadbalancer.server.port="
            "${seaweedfs_s3_http_port:-8333}",
            _labels(services["seaweedfs-s3"]),
        )


@unittest.skipUnless(
    os.environ.get("HYHOME_SEAWEEDFS_REHEARSAL") == "1",
    "set HYHOME_SEAWEEDFS_REHEARSAL=1 to run the disposable SeaweedFS rehearsal (needs Docker)",
)
class SeaweedfsRehearsalTests(unittest.TestCase):
    """The rendered SeaweedFS services on disposable data (SPEC-0180 S06).

    The real Compose model is rendered, then only its container names, networks
    (two internal ones), volume and secret sources are moved under a temporary
    directory; commands, images, users, mounts of the start script and health
    checks are the ones HOME uses. Tests run in name order.
    """

    AWS_IMAGE = "amazon/aws-cli:2.36.50"
    PROBE_IMAGE = "python:3.13.15-alpine"
    ACCESS = "rehearsaladmin"

    @classmethod
    def setUpClass(cls) -> None:
        cls.tag = f"hysw{os.getpid()}"
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.dir = Path(cls.tmp.name)
        cls.secret_key = "Rehearsal" + os.urandom(6).hex()
        for sub in (
            "data/seaweedfs/master",
            "data/seaweedfs/volume",
            "data/seaweedfs/filer",
            "io",
            "backup",
            "data/flink/checkpoints",
        ):
            (cls.dir / sub).mkdir(parents=True)
        (cls.dir / "io").chmod(0o777)
        # As RUN-0094 creates it: operator-owned, setgid, written by the
        # image user through its SECRETS_GID supplementary group.
        (cls.dir / "data/flink/checkpoints").chmod(0o2770)
        subprocess.run(
            [
                "bash",
                str(ROOT / SEAWEEDFS_DIR / "bin/gen-grpc-certs.sh"),
                str(cls.dir / "certs/seaweedfs"),
            ],
            check=True,
            capture_output=True,
            env={**os.environ, "SECRETS_GID": str(os.getgid())},
        )
        secrets = {
            "seaweedfs_jwt_volume_key": "Volume" + os.urandom(6).hex(),
            "seaweedfs_jwt_filer_key": "Filer" + os.urandom(6).hex(),
            "seaweedfs_s3_admin_secret_key": cls.secret_key,
            **{
                f"seaweedfs_s3_{name}_secret_key": name.title() + os.urandom(6).hex()
                for name in ("loki", "tempo", "mlflow", "terrakube", "lakehouse")
            },
        }
        cls.consumer_secret = {
            name: secrets[f"seaweedfs_s3_{name}_secret_key"]
            for name in ("loki", "tempo", "mlflow", "terrakube", "lakehouse")
        }
        for name, value in secrets.items():
            path = cls.dir / f"{name}.txt"
            path.write_text(value + "\n", encoding="utf-8")
            path.chmod(0o640)  # as on HOME: group SECRETS_GID via group_add
        env = {
            **os.environ,
            "DEFAULT_DATA_DIR": str(cls.dir / "data"),
            "DEFAULT_CERT_DIR": str(cls.dir / "certs"),
            "SEAWEEDFS_S3_ADMIN_ACCESS_KEY": cls.ACCESS,
            # Flink (UID 9999) reads secrets and checkpoints through this group.
            "SECRETS_GID": str(os.getgid()),
        }
        rendered = json.loads(
            subprocess.run(
                [
                    "docker",
                    "compose",
                    "--env-file",
                    ".env.example",
                    "--profile",
                    "seaweedfs",
                    "--profile",
                    "lakehouse",
                    "config",
                    "--format",
                    "json",
                    *SEAWEEDFS_SERVICES,
                    "seaweedfs-buckets",
                    "seaweedfs-table-bucket",
                    "trino",
                    "great-expectations",
                    *FLINK_SERVICES,
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
        )
        services = {
            name: rendered["services"][name]
            for name in (
                *SEAWEEDFS_SERVICES,
                "seaweedfs-buckets",
                "seaweedfs-table-bucket",
                "trino",
                "great-expectations",
                *FLINK_SERVICES,
            )
        }
        for name, service in services.items():
            service["container_name"] = f"{cls.tag}-{name}"
            service["labels"] = {
                k: v
                for k, v in service.get("labels", {}).items()
                if not k.startswith("traefik.")
            }
            service["networks"] = (
                {"sw": {}, "client": {}}
                if name == "seaweedfs-s3"
                else {"client": {}}
                if name
                in (
                    "seaweedfs-buckets",
                    "seaweedfs-table-bucket",
                    "trino",
                    "great-expectations",
                    *FLINK_SERVICES,
                )
                else {"sw": {}}
            )
            service.pop("ports", None)
            service.pop("profiles", None)
        volumes = rendered["volumes"]
        for volume in volumes.values():
            volume.pop("name", None)
        cls.model = {
            "name": cls.tag,
            "services": services,
            "networks": {"sw": {"internal": True}, "client": {"internal": True}},
            "volumes": {
                name: volumes[name]
                for name in (
                    "seaweedfs-master-data",
                    "seaweedfs-volume-data",
                    "seaweedfs-filer-data",
                    "flink-checkpoints",
                )
            },
            "secrets": {
                name: {"file": str(cls.dir / f"{name}.txt")} for name in secrets
            },
        }
        (cls.dir / "compose.json").write_text(json.dumps(cls.model), encoding="utf-8")
        # Checkpoint files belong to the Flink image user; delete them as that
        # user once the containers are gone, before the temporary directory.
        cls.addClassCleanup(
            subprocess.run,
            [
                "docker",
                "run",
                "--rm",
                "--user",
                "9999:9999",
                "--group-add",
                str(os.getgid()),
                "--entrypoint",
                "find",
                "-v",
                f"{cls.dir / 'data/flink/checkpoints'}:/c",
                services["flink-jobmanager"]["image"],
                "/c",
                "-mindepth",
                "1",
                "-delete",
            ],
            capture_output=True,
        )
        cls.addClassCleanup(cls.compose, "down", "-v", "--timeout", "5")
        cls.up()
        for job in ("seaweedfs-buckets", "seaweedfs-table-bucket"):
            result = cls.compose("run", "--rm", "--no-deps", job)
            if result.returncode != 0:
                raise AssertionError(result.stdout + result.stderr)

    @classmethod
    def compose(
        cls, *args: str, check: bool = False
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "docker",
                "compose",
                "-p",
                cls.tag,
                "-f",
                str(cls.dir / "compose.json"),
                *args,
            ],
            check=check,
            capture_output=True,
            text=True,
        )

    @classmethod
    def up(cls) -> None:
        result = cls.compose(
            "up", "-d", "--wait", "--wait-timeout", "180", *SEAWEEDFS_SERVICES
        )
        if result.returncode != 0:
            logs = cls.compose("logs", "--no-color", "--tail", "40").stdout
            raise AssertionError(result.stderr + logs)

    def aws(
        self, *args: str, secret: str | None = None, access: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--network",
                f"{self.tag}_client",
                "-e",
                f"AWS_ACCESS_KEY_ID={access or self.ACCESS}",
                "-e",
                f"AWS_SECRET_ACCESS_KEY={secret or self.secret_key}",
                "-e",
                "AWS_DEFAULT_REGION=us-east-1",
                "-e",
                "AWS_EC2_METADATA_DISABLED=true",
                "-v",
                f"{self.dir / 'io'}:/io",
                self.AWS_IMAGE,
                "--endpoint-url",
                "http://seaweedfs-s3:8333",
                *args,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def probe(self, network: str, code: str) -> str:
        return subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--network",
                f"{self.tag}_{network}",
                self.PROBE_IMAGE,
                "python3",
                "-c",
                code,
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def shell(self, commands: str) -> str:
        out = subprocess.run(
            [
                "docker",
                "exec",
                "-i",
                f"{self.tag}-seaweedfs-master",
                "/bin/sh",
                "/opt/hyhome/hyhome-seaweedfs.sh",
                "shell",
                "-master=localhost:9333",
                "-filer=seaweedfs-filer:8888",
            ],
            input=commands,
            check=True,
            capture_output=True,
            text=True,
        )
        text = out.stdout + out.stderr
        # hyhome-backup.sh also treats this text as failure.
        self.assertNotRegex(text.lower(), r"error|fail", commands)
        return text

    STATUS = (
        "import urllib.request as u, urllib.error as e\n"
        "def status(method, url, data=None):\n"
        "    try:\n"
        "        return u.urlopen(u.Request(url, data=data, method=method), timeout=10).status\n"
        "    except e.HTTPError as err:\n"
        "        return err.code\n"
    )

    def test_1_anonymous_and_wrong_credentials_are_refused(self) -> None:
        codes = self.probe(
            "client",
            self.STATUS + "print(status('PUT', 'http://seaweedfs-s3:8333/anon'),"
            " status('GET', 'http://seaweedfs-s3:8333/'))",
        )
        self.assertEqual("403 403", codes)
        wrong = self.aws("s3api", "list-buckets", secret="wrong" + self.secret_key)
        self.assertNotEqual(0, wrong.returncode)
        self.assertIn("SignatureDoesNotMatch", wrong.stderr)

    def test_2_filer_and_volume_http_need_a_jwt(self) -> None:
        codes = self.probe(
            "sw",
            self.STATUS + "import json\n"
            "fid = json.load(u.urlopen('http://seaweedfs-master:9333/dir/assign', timeout=10))\n"
            "print(status('GET', 'http://seaweedfs-filer:8888/'),"
            " status('PUT', 'http://seaweedfs-filer:8888/x', b'x'),"
            " status('POST', 'http://' + fid['url'] + '/' + fid['fid'], b'x'))",
        )
        self.assertEqual("401 401 401", codes)

    def test_2_grpc_requires_a_client_certificate(self) -> None:
        # A TLS server that demands a client certificate fails the handshake
        # with an alert; a plaintext listener would fail with a version error.
        result = self.probe(
            "sw",
            "import socket, ssl\n"
            "ctx = ssl.create_default_context()\n"
            "ctx.check_hostname = False\n"
            "ctx.verify_mode = ssl.CERT_NONE\n"
            "out = []\n"
            "for host, port in (('seaweedfs-master', 19333), ('seaweedfs-filer', 18888), ('seaweedfs-volume', 18085), ('seaweedfs-s3', 18333)):\n"
            "    try:\n"
            "        with ctx.wrap_socket(socket.create_connection((host, port), timeout=10)) as tls:\n"
            "            tls.send(b'PRI * HTTP/2.0\\r\\n\\r\\nSM\\r\\n\\r\\n')\n"
            "            tls.recv(1)\n"
            "        out.append('accepted')\n"
            "    except ssl.SSLError as err:\n"
            "        out.append(str(err.reason))\n"
            "    except OSError as err:\n"
            "        out.append(type(err).__name__)\n"
            "print(' '.join(out))",
        )
        self.assertEqual(
            ["TLSV13_ALERT_CERTIFICATE_REQUIRED"] * 4, result.split(), result
        )
        # S3 clients cannot resolve or reach the master, volume or filer.
        reach = self.probe(
            "client",
            "import socket\n"
            "out = []\n"
            "for host in ('seaweedfs-master', 'seaweedfs-volume', 'seaweedfs-filer'):\n"
            "    try:\n"
            "        socket.create_connection((host, 9333), timeout=5).close()\n"
            "        out.append('reached')\n"
            "    except OSError:\n"
            "        out.append('unreachable')\n"
            "print(' '.join(out))",
        )
        self.assertEqual("unreachable unreachable unreachable", reach)
        # A failed shell command must be visible to hyhome-backup.sh through
        # the exit status or error text (it checks both).
        failed = subprocess.run(
            [
                "docker",
                "exec",
                "-i",
                f"{self.tag}-seaweedfs-master",
                "/bin/sh",
                "/opt/hyhome/hyhome-seaweedfs.sh",
                "shell",
                "-master=localhost:9333",
                "-filer=seaweedfs-filer:8888",
            ],
            input="fs.meta.load /nonexistent.meta\n",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertTrue(
            failed.returncode != 0
            or re.search(r"error|fail", (failed.stdout + failed.stderr).lower()),
            failed,
        )

    def catalog(self, path: str, access: str, secret: str) -> str:
        return subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--network",
                f"{self.tag}_client",
                "--entrypoint",
                "curl",
                self.AWS_IMAGE,
                "-s",
                "--aws-sigv4",
                "aws:amz:us-east-1:s3",
                "--user",
                f"{access}:{secret}",
                f"http://seaweedfs-s3:8181{path}",
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    def test_3_lakehouse_catalog_is_scoped_to_its_identity(self) -> None:
        lakehouse = {"access": "lakehouse", "secret": self.consumer_secret["lakehouse"]}
        # seaweedfs-table-bucket created the bucket, its policy and namespaces.
        listed = json.loads(self.catalog("/v1/lakehouse/namespaces", **lakehouse))
        self.assertEqual({"dev", "test"}, {".".join(ns) for ns in listed["namespaces"]})
        # Another identity cannot even see the table bucket.
        self.assertIn(
            '"code":404',
            self.catalog(
                "/v1/lakehouse/namespaces", "loki", self.consumer_secret["loki"]
            ),
        )
        # The identity is limited to its bucket on the S3 side as well.
        self.assertNotEqual(
            0, self.aws("s3", "ls", "s3://loki-bucket", **lakehouse).returncode
        )
        self.assertNotEqual(
            0,
            self.aws(
                "s3tables", "create-table-bucket", "--name", "other", **lakehouse
            ).returncode,
        )
        # The policy grants table work, not control of the bucket itself.
        arn = self.aws(
            "s3tables",
            "list-table-buckets",
            "--query",
            "tableBuckets[?name=='lakehouse'].arn | [0]",
            "--output",
            "text",
        ).stdout.strip()
        for command in (
            (
                "put-table-bucket-policy",
                "--resource-policy",
                '{"Version":"2012-10-17","Statement":[]}',
            ),
            ("delete-table-bucket",),
        ):
            self.assertNotEqual(
                0,
                self.aws(
                    "s3tables",
                    command[0],
                    "--table-bucket-arn",
                    arn,
                    *command[1:],
                    **lakehouse,
                ).returncode,
                command[0],
            )

    def test_3_trino_reads_and_writes_the_lakehouse_catalog(self) -> None:
        # SPEC-0180 S13: the HOME catalog file and wrapper, on the scoped identity.
        started = self.compose(
            "up", "-d", "--no-deps", "--wait", "--wait-timeout", "240", "trino"
        )
        self.addCleanup(self.compose, "rm", "-sf", "trino")
        self.assertEqual(0, started.returncode, started.stderr)

        def sql(statement: str) -> str:
            result = self.compose(
                "exec", "-T", "trino", "trino", "--execute", statement
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            return result.stdout

        table = "lakehouse.test.s13_rehearsal"
        sql(f"CREATE TABLE {table} (id bigint, name varchar)")
        sql(f"INSERT INTO {table} VALUES (1, 'a'), (2, 'b')")
        sql(f"UPDATE {table} SET name = 'c' WHERE id = 2")
        sql(f"ALTER TABLE {table} EXECUTE optimize")
        self.assertEqual(
            '"1","a"\n"2","c"', sql(f"SELECT id, name FROM {table} ORDER BY id").strip()
        )
        self.assertIn('"s13_rehearsal"', sql("SHOW TABLES FROM lakehouse.test"))
        sql(f"DROP TABLE {table}")
        self.assertNotIn("s13_rehearsal", sql("SHOW TABLES FROM lakehouse.test"))

    def test_3_flink_writes_the_lakehouse_catalog(self) -> None:
        # SPEC-0180 S14: the HOME image, wrapper and catalog statement, on the
        # scoped identity; batch and checkpointed streaming inserts both commit.
        started = self.compose(
            "up", "-d", "--no-deps", "--wait", "--wait-timeout", "240", *FLINK_SERVICES
        )
        self.addCleanup(self.compose, "rm", "-sf", *FLINK_SERVICES)
        self.assertEqual(0, started.returncode, started.stderr)

        def sql(script: str) -> str:
            result = subprocess.run(
                [
                    "docker",
                    "compose",
                    "-p",
                    self.tag,
                    "-f",
                    str(self.dir / "compose.json"),
                    "exec",
                    "-T",
                    "flink-jobmanager",
                    "bash",
                    "-c",
                    "cat >/tmp/job.sql && bash /opt/hyhome/hyhome-flink.sh"
                    " /opt/flink/bin/sql-client.sh -i /tmp/lakehouse.sql -f /tmp/job.sql",
                ],
                input="SET 'table.dml-sync' = 'true';\n"
                "SET 'sql-client.execution.result-mode' = 'tableau';\n" + script,
                capture_output=True,
                text=True,
                check=False,
                timeout=300,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertNotIn("[ERROR]", result.stdout)
            return result.stdout

        table = "`test`.s14_rehearsal"
        sql(f"CREATE TABLE {table} (id BIGINT, name STRING);\n")
        self.addCleanup(sql, f"DROP TABLE IF EXISTS {table};\n")
        sql(
            "SET 'execution.runtime-mode' = 'batch';\n"
            f"INSERT INTO {table} VALUES (1, 'a'), (2, 'b');\n"
        )
        sql(
            "SET 'execution.runtime-mode' = 'streaming';\n"
            "SET 'execution.checkpointing.interval' = '2s';\n"
            "CREATE TEMPORARY TABLE gen (id BIGINT) WITH ("
            "'connector' = 'datagen', 'number-of-rows' = '5', 'rows-per-second' = '2',"
            " 'fields.id.kind' = 'sequence', 'fields.id.start' = '10',"
            " 'fields.id.end' = '14');\n"
            f"INSERT INTO {table} SELECT id, 's' FROM gen;\n"
        )
        out = sql(
            "SET 'execution.runtime-mode' = 'batch';\n"
            f"SELECT COUNT(*) AS n, SUM(id) AS s FROM {table};\n"
        )
        self.assertRegex(out, r"\|\s+7\s+\|\s+63\s+\|")

    def test_3_great_expectations_passes_and_fails_through_trino(self) -> None:
        # SPEC-0180 S15: the HOME image and the tracked rehearsal suite; a
        # duplicate key turns the same suite into exit 1.
        started = self.compose(
            "up", "-d", "--no-deps", "--wait", "--wait-timeout", "240", "trino"
        )
        self.addCleanup(self.compose, "rm", "-sf", "trino")
        self.assertEqual(0, started.returncode, started.stderr)

        def sql(statement: str) -> None:
            result = self.compose(
                "exec", "-T", "trino", "trino", "--execute", statement
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

        def gx() -> subprocess.CompletedProcess[str]:
            return self.compose(
                "run",
                "--rm",
                "--no-deps",
                "great-expectations",
                "validate",
                "lakehouse-rehearsal",
            )

        table = "lakehouse.test.gx_rehearsal"
        sql(f"CREATE TABLE {table} (id bigint, name varchar)")
        self.addCleanup(sql, f"DROP TABLE IF EXISTS {table}")
        sql(f"INSERT INTO {table} VALUES (1, 'a'), (2, 'b')")
        passed = gx()
        self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)
        self.assertIn('"table": "test.gx_rehearsal", "success": true', passed.stdout)
        sql(f"INSERT INTO {table} VALUES (2, 'c')")
        failed = gx()
        self.assertEqual(1, failed.returncode, failed.stdout + failed.stderr)
        self.assertIn(
            '"expectation": "expect_column_values_to_be_unique"', failed.stdout
        )
        self.assertIn('"success": false}', failed.stdout)

    def test_3_s3_api_used_by_consumers(self) -> None:
        io = self.dir / "io"
        (io / "small.txt").write_bytes(b"0123456789hello")
        (io / "big.bin").write_bytes(os.urandom(20 * 1024 * 1024))
        self.assertEqual(
            0, self.aws("s3api", "create-bucket", "--bucket", "rehearsal").returncode
        )
        put = self.aws(
            "s3api",
            "put-object",
            "--bucket",
            "rehearsal",
            "--key",
            "dir/space name+plus.txt",
            "--body",
            "/io/small.txt",
            "--content-type",
            "text/plain",
            "--metadata",
            "owner=s06",
            "--tagging",
            "tier=test",
        )
        self.assertEqual(0, put.returncode, put.stderr)
        head = json.loads(
            self.aws(
                "s3api",
                "head-object",
                "--bucket",
                "rehearsal",
                "--key",
                "dir/space name+plus.txt",
            ).stdout
        )
        self.assertEqual("text/plain", head["ContentType"])
        self.assertEqual({"owner": "s06"}, head["Metadata"])
        tags = json.loads(
            self.aws(
                "s3api",
                "get-object-tagging",
                "--bucket",
                "rehearsal",
                "--key",
                "dir/space name+plus.txt",
            ).stdout
        )
        self.assertEqual([{"Key": "tier", "Value": "test"}], tags["TagSet"])
        ranged = self.aws(
            "s3api",
            "get-object",
            "--bucket",
            "rehearsal",
            "--key",
            "dir/space name+plus.txt",
            "--range",
            "bytes=10-14",
            "/io/range.out",
        )
        self.assertEqual(0, ranged.returncode, ranged.stderr)
        self.assertEqual(b"hello", (io / "range.out").read_bytes())
        big = self.aws("s3", "cp", "/io/big.bin", "s3://rehearsal/big.bin")
        self.assertEqual(0, big.returncode, big.stderr)
        etag = json.loads(
            self.aws(
                "s3api", "head-object", "--bucket", "rehearsal", "--key", "big.bin"
            ).stdout
        )["ETag"]
        self.assertRegex(etag, r'-\d+"$')  # multipart ETag, not an MD5
        self.assertEqual(
            0, self.aws("s3", "cp", "s3://rehearsal/big.bin", "/io/big.out").returncode
        )
        self.assertEqual((io / "big.bin").read_bytes(), (io / "big.out").read_bytes())
        listing = json.loads(
            self.aws(
                "s3api", "list-objects-v2", "--bucket", "rehearsal", "--prefix", "dir/"
            ).stdout
        )
        self.assertEqual(
            ["dir/space name+plus.txt"], [item["Key"] for item in listing["Contents"]]
        )
        url = self.aws(
            "s3",
            "presign",
            "s3://rehearsal/dir/space name+plus.txt",
            "--expires-in",
            "300",
        ).stdout.strip()
        body = self.probe(
            "client",
            f"import urllib.request as u; print(u.urlopen({url!r}, timeout=10).read().decode())",
        )
        self.assertEqual("0123456789hello", body)
        # A key that is also another key's prefix: record what the store does.
        self.assertEqual(
            0,
            self.aws(
                "s3api",
                "put-object",
                "--bucket",
                "rehearsal",
                "--key",
                "a",
                "--body",
                "/io/small.txt",
            ).returncode,
        )
        nested = self.aws(
            "s3api",
            "put-object",
            "--bucket",
            "rehearsal",
            "--key",
            "a/b",
            "--body",
            "/io/small.txt",
        )
        self.assertEqual(0, nested.returncode, nested.stderr)
        # Both keys stay readable with their own bytes (SeaweedFS keeps `a` as a
        # file entry and `a/` as a directory entry).
        (io / "small2.txt").write_bytes(b"nested")
        self.assertEqual(
            0,
            self.aws(
                "s3api",
                "put-object",
                "--bucket",
                "rehearsal",
                "--key",
                "a/b",
                "--body",
                "/io/small2.txt",
            ).returncode,
        )
        self.assertEqual(
            0,
            self.aws(
                "s3api",
                "get-object",
                "--bucket",
                "rehearsal",
                "--key",
                "a/b",
                "/io/ab.out",
            ).returncode,
        )
        self.assertEqual(b"nested", (io / "ab.out").read_bytes())
        self.assertEqual(
            0,
            self.aws(
                "s3api",
                "get-object",
                "--bucket",
                "rehearsal",
                "--key",
                "a",
                "/io/a.out",
            ).returncode,
        )
        self.assertEqual(b"0123456789hello", (io / "a.out").read_bytes())
        self.assertEqual(
            0,
            self.aws(
                "s3api", "delete-object", "--bucket", "rehearsal", "--key", "a"
            ).returncode,
        )
        gone = self.aws("s3api", "head-object", "--bucket", "rehearsal", "--key", "a")
        self.assertNotEqual(0, gone.returncode)

    def test_4_restart_keeps_objects(self) -> None:
        data = self.dir / "data/seaweedfs"
        self.assertTrue(
            list((data / "volume").glob("*.dat")), "needles are not on the volume bind"
        )
        self.assertTrue(
            (data / "filer/filerldb2").is_dir(), "filer store is not on its bind"
        )
        self.assertTrue(
            any((data / "master").iterdir()), "master state is not on its bind"
        )
        # With the volume server down a read fails instead of returning bytes.
        self.compose("stop", "--timeout", "10", "seaweedfs-volume", check=True)
        down = self.aws("s3", "cp", "s3://rehearsal/big.bin", "/io/while-down.out")
        self.assertNotEqual(0, down.returncode)
        self.compose("stop", "--timeout", "10", check=True)
        self.up()
        self.assertEqual(
            0,
            self.aws(
                "s3", "cp", "s3://rehearsal/big.bin", "/io/after-restart.out"
            ).returncode,
        )
        self.assertEqual(
            (self.dir / "io/big.bin").read_bytes(),
            (self.dir / "io/after-restart.out").read_bytes(),
        )

    def test_5_backup_set_restores_into_empty_stores(self) -> None:
        import shutil

        # The orchestrator's order: pause vacuum, save filer metadata, then copy
        # the volume and master trees while the servers run.
        self.shell("lock\nvolume.vacuum.disable\nunlock\n")
        self.shell("fs.meta.save -o /tmp/filer.meta /\n")
        meta = subprocess.run(
            [
                "docker",
                "exec",
                f"{self.tag}-seaweedfs-master",
                "cat",
                "/tmp/filer.meta",
            ],
            check=True,
            capture_output=True,
        ).stdout
        self.assertGreater(len(meta), 0)
        backup = self.dir / "backup"
        (backup / "filer.meta").write_bytes(meta)
        data = self.dir / "data/seaweedfs"
        for sub in ("volume", "master"):
            shutil.copytree(data / sub, backup / sub)
        self.compose("down", "--timeout", "10", check=True)
        for sub in ("volume", "master", "filer"):
            shutil.rmtree(data / sub)
        shutil.copytree(backup / "volume", data / "volume")
        shutil.copytree(backup / "master", data / "master")
        (data / "filer").mkdir()
        self.up()
        subprocess.run(
            [
                "docker",
                "cp",
                str(backup / "filer.meta"),
                f"{self.tag}-seaweedfs-master:/tmp/restore.meta",
            ],
            check=True,
            capture_output=True,
        )
        self.shell("fs.meta.load /tmp/restore.meta\n")
        restored = self.aws("s3", "cp", "s3://rehearsal/big.bin", "/io/restored.out")
        self.assertEqual(0, restored.returncode, restored.stderr)
        self.assertEqual(
            (self.dir / "io/big.bin").read_bytes(),
            (self.dir / "io/restored.out").read_bytes(),
        )
        self.compose("restart", "--timeout", "10", check=True)
        self.up()
        small = self.aws(
            "s3api",
            "get-object",
            "--bucket",
            "rehearsal",
            "--key",
            "dir/space name+plus.txt",
            "/io/restored-small.out",
        )
        self.assertEqual(0, small.returncode, small.stderr)
        self.assertEqual(
            b"0123456789hello", (self.dir / "io/restored-small.out").read_bytes()
        )

    def test_6_consumer_identities_are_bucket_scoped(self) -> None:
        io = self.dir / "io"
        (io / "scope.txt").write_bytes(b"scope")
        for bucket in (
            "loki-bucket",
            "tempo-bucket",
            "mlflow-artifacts",
            "tfstate",
            "cdn-bucket",
        ):
            self.assertEqual(
                0,
                self.aws("s3api", "head-bucket", "--bucket", bucket).returncode,
                bucket,
            )
        loki = {"access": "loki", "secret": self.consumer_secret["loki"]}
        own = self.aws(
            "s3api",
            "put-object",
            "--bucket",
            "loki-bucket",
            "--key",
            "k",
            "--body",
            "/io/scope.txt",
            **loki,
        )
        self.assertEqual(0, own.returncode, own.stderr)
        for args in (
            (
                "s3api",
                "put-object",
                "--bucket",
                "tempo-bucket",
                "--key",
                "k",
                "--body",
                "/io/scope.txt",
            ),
            ("s3api", "list-objects-v2", "--bucket", "tempo-bucket"),
            ("s3api", "create-bucket", "--bucket", "loki-extra"),
        ):
            denied = self.aws(*args, **loki)
            self.assertNotEqual(0, denied.returncode, args)
            self.assertIn("AccessDenied", denied.stderr, args)
        put = self.aws(
            "s3api",
            "put-object",
            "--bucket",
            "cdn-bucket",
            "--key",
            "asset.txt",
            "--body",
            "/io/scope.txt",
            "--content-type",
            "text/plain",
        )
        self.assertEqual(0, put.returncode, put.stderr)
        codes = self.probe(
            "client",
            self.STATUS
            + "print(status('GET', 'http://seaweedfs-s3:8333/cdn-bucket/asset.txt'),"
            " status('GET', 'http://seaweedfs-s3:8333/cdn-bucket?list-type=2'),"
            " status('PUT', 'http://seaweedfs-s3:8333/cdn-bucket/x', b'x'),"
            " status('DELETE', 'http://seaweedfs-s3:8333/cdn-bucket/asset.txt'),"
            " status('GET', 'http://seaweedfs-s3:8333/loki-bucket/k'))",
        )
        self.assertEqual("200 403 403 403 403", codes)


def _labels(service: dict) -> set[str]:
    labels = service.get("labels") or {}
    if isinstance(labels, dict):
        labels = [f"{key}={value}" for key, value in labels.items()]
    return {label.lower() for label in labels}


class NetworkSegmentationContractTests(unittest.TestCase):
    """Fixed flows of the segmented networks (SPEC-0180 S05, AD-0026)."""

    @staticmethod
    def _services() -> dict[str, dict]:
        import yaml

        services: dict[str, dict] = {}
        for path in sorted((ROOT / "infra").rglob("docker-compose*.y*ml")):
            document = (
                yaml.load(path.read_text(encoding="utf-8"), Loader=_ComposeLoader) or {}
            )
            for name, service in (document.get("services") or {}).items():
                if name in services:
                    raise AssertionError(f"service {name} is declared twice")
                services[name] = service
        return services

    def test_routed_services_join_edge_net(self) -> None:
        missing = [
            name
            for name, service in self._services().items()
            if "traefik.enable=true" in _labels(service)
            and name != "storybook"
            and "edge_net" not in (service.get("networks") or {})
        ]
        self.assertEqual([], missing)

    def test_storybook_uses_only_dedicated_internal_ingress(self) -> None:
        import yaml

        services = self._services()
        storybook = services["storybook"]
        self.assertEqual({"experience_ingress_net"}, set(storybook["networks"]))
        self.assertIn("experience_ingress_net", services["traefik"]["networks"])
        self.assertEqual(
            {"storybook", "traefik"},
            {
                name
                for name, service in services.items()
                if "experience_ingress_net" in (service.get("networks") or {})
            },
        )
        root = yaml.load(
            (ROOT / "docker-compose.yml").read_text(encoding="utf-8"),
            Loader=_ComposeLoader,
        )
        self.assertTrue(root["networks"]["experience_ingress_net"]["internal"])
        self.assertFalse(storybook.get("ports"))
        self.assertEqual(
            "experience_ingress_net",
            storybook["labels"]["traefik.docker.network"],
        )
        self.assertEqual(
            "req-rate-limit@file,gateway-standard-chain@file,sso-auth@file",
            storybook["labels"]["traefik.http.routers.storybook.middlewares"],
        )

    def test_prometheus_scrape_targets_are_services_on_obs_net(self) -> None:
        services = self._services()
        config = ROOT / "infra/06-observability/prometheus/config"
        hosts = {
            host
            for path in config.glob("prometheus*.yml")
            for host in re.findall(
                r"[\"'\s\[/]([a-z][a-z0-9_.-]*):\d{2,5}\b",
                path.read_text(encoding="utf-8"),
            )
        } - {"localhost"}
        self.assertIn("traefik", hosts)
        self.assertEqual([], sorted(hosts - services.keys()))
        # seaweedfs-s3 is scraped over edge_net (shared with Prometheus) so the
        # S3 API does not also join obs_net; see POL-0024 "Metrics".
        edge_scraped = {"seaweedfs-s3"}
        missing = [
            name
            for name in sorted(hosts)
            if ("edge_net" if name in edge_scraped else "obs_net")
            not in (services[name].get("networks") or {})
        ]
        self.assertEqual([], missing)

    def test_traefik_edge_address_is_the_trusted_proxy(self) -> None:
        edge = _compose_service(
            "infra/01-gateway/traefik/docker-compose.yml", "traefik"
        )["networks"]["edge_net"]
        self.assertEqual("10.250.1.2", edge["ipv4_address"])
        self.assertEqual(
            {"keycloak.${DEFAULT_URL}", "auth.${DEFAULT_URL}"}, set(edge["aliases"])
        )
        oauth2 = (
            ROOT / "infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg"
        ).read_text(encoding="utf-8")
        self.assertRegex(oauth2, r'trusted_proxy_ips = \[[^]]*"10\.250\.1\.2/32"')
        airflow = self._services()["airflow-apiserver"]["environment"]
        self.assertIn("10.250.1.2", airflow["FORWARDED_ALLOW_IPS"].split(","))

    def test_no_service_pins_keycloak_to_the_host_gateway(self) -> None:
        # Traefik publishes only on HOST_LAN_BIND_IP, so host-gateway has no
        # listener on 443; containers reach Keycloak through the edge_net alias.
        pinned = sorted(
            name
            for name, service in self._services().items()
            if any(
                "keycloak." in str(host) or "auth." in str(host)
                for host in service.get("extra_hosts") or []
            )
        )
        self.assertEqual([], pinned)

    def test_servers_do_not_bind_to_one_network_address(self) -> None:
        # A multi-homed server bound to its own name listens only on the
        # network that name happens to resolve on.
        for name, service in self._services().items():
            command = service.get("command") or ""
            command = command if isinstance(command, str) else " ".join(command)
            for bind in re.findall(r"-ip\.bind=(\S+?)'?(?:\s|$)", command):
                self.assertEqual("0.0.0.0", bind, name)

    def test_opensearch_nodes_use_only_the_standalone_lab_network(self) -> None:
        import yaml

        normal = self._services()
        lab = yaml.safe_load((ROOT / "labs/opensearch-cluster.yml").read_text())
        for index in (1, 2, 3):
            name = f"opensearch-node{index}"
            self.assertNotIn(name, normal)
            self.assertEqual(
                {"lab_opensearch_core_net"}, set(lab["services"][name]["networks"])
            )


class ConftestPolicyGateTests(unittest.TestCase):
    """The Conftest CI gate runs the declared job, and the job stays isolated."""

    COMPOSE = "infra/11-quality/conftest/docker-compose.yml"

    def test_job_reads_infra_only_without_network_or_root(self) -> None:
        service = _compose_service(self.COMPOSE, "conftest")
        self.assertEqual("none", service["network_mode"])
        self.assertEqual("1000:1000", service["user"])
        self.assertEqual(["../..:/project/infra:ro"], service["volumes"])
        self.assertNotIn("secrets", service)
        self.assertEqual(["policy-check"], service["profiles"])

    def test_gate_script_runs_the_declared_job(self) -> None:
        script = (ROOT / "scripts/validation/check-conftest-policy.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn(f"-f {self.COMPOSE}", script)
        self.assertIn("run --rm conftest", script)

    def test_gate_modes_are_closed_and_preserve_the_combined_default(self) -> None:
        gate = (ROOT / "scripts/validation/check-conftest-policy.sh").read_text(
            encoding="utf-8"
        )
        runner = (ROOT / "infra/11-quality/conftest/run.sh").read_text(encoding="utf-8")
        self.assertIn("--mode", gate)
        self.assertIn("verify|corpus|all", gate)
        self.assertIn('mode="all"', gate)
        self.assertIn("mode=${1-all}", runner)
        self.assertIn("verify|corpus|all", runner)
        self.assertIn('if [ "$mode" != corpus ]', runner)
        self.assertIn('if [ "$mode" != verify ]', runner)

    def test_invalid_gate_mode_is_rejected_before_docker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker = root / "docker-called"
            docker = root / "docker"
            docker.write_text(
                '#!/bin/sh\n: >"$DOCKER_MARKER"\nexit 0\n',
                encoding="utf-8",
            )
            docker.chmod(0o755)
            result = subprocess.run(
                [
                    str(ROOT / "scripts/validation/check-conftest-policy.sh"),
                    "--mode",
                    "invalid",
                ],
                cwd=ROOT,
                env={
                    "DOCKER_MARKER": str(marker),
                    "PATH": f"{root}:{os.defpath}",
                },
                capture_output=True,
                text=True,
                check=False,
            )
            docker_called = marker.exists()
        self.assertEqual(2, result.returncode)
        self.assertIn("verify|corpus|all", result.stderr)
        self.assertFalse(docker_called)

    def test_container_modes_execute_only_their_owned_checks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            command_log = root / "conftest.log"
            find_log = root / "find.log"
            conftest = root / "conftest"
            conftest.write_text(
                '#!/bin/sh\nprintf "%s|%s\\n" "$PWD" "$*" >>"$CONFTEST_LOG"\n',
                encoding="utf-8",
            )
            find = root / "find"
            find.write_text(
                '#!/bin/sh\nprintf "%s\\n" "$*" >>"$FIND_LOG"\n',
                encoding="utf-8",
            )
            conftest.chmod(0o755)
            find.chmod(0o755)
            environment = {
                "CONFTEST_LOG": str(command_log),
                "FIND_LOG": str(find_log),
                "PATH": f"{root}:{os.defpath}",
            }
            script = ROOT / "infra/11-quality/conftest/run.sh"

            verify = subprocess.run(
                ["/bin/sh", str(script), "verify"],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, verify.returncode, verify.stderr)
            self.assertEqual(
                f"{ROOT}|verify --policy infra/11-quality/conftest/policy\n",
                command_log.read_text(encoding="utf-8"),
            )
            self.assertFalse(find_log.exists())

            command_log.unlink()
            corpus = subprocess.run(
                ["/bin/sh", str(script), "corpus"],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, corpus.returncode, corpus.stderr)
            commands = command_log.read_text(encoding="utf-8").splitlines()
            self.assertEqual(2, len(commands))
            self.assertTrue(
                all(command.startswith(f"{ROOT}|test ") for command in commands)
            )
            self.assertNotIn("verify", "\n".join(commands))
            # infra Compose files, LAB entrypoints (SPEC-0218) and Dockerfiles.
            finds = find_log.read_text(encoding="utf-8").splitlines()
            self.assertEqual(3, len(finds))
            self.assertTrue(any(line.startswith("labs ") for line in finds), finds)

            command_log.unlink()
            find_log.unlink()
            for arguments in (("all",), ()):
                combined = subprocess.run(
                    ["/bin/sh", str(script), *arguments],
                    cwd=ROOT,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, combined.returncode, combined.stderr)
                commands = command_log.read_text(encoding="utf-8").splitlines()
                self.assertEqual(3, len(commands))
                self.assertTrue(commands[0].startswith(f"{ROOT}|verify "))
                self.assertTrue(
                    all(command.startswith(f"{ROOT}|test ") for command in commands[1:])
                )
                self.assertEqual(
                    3, len(find_log.read_text(encoding="utf-8").splitlines())
                )
                command_log.unlink()
                find_log.unlink()

            for arguments in (("",), ("unknown",), ("verify", "extra")):
                rejected = subprocess.run(
                    ["/bin/sh", str(script), *arguments],
                    cwd=ROOT,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(2, rejected.returncode)
                self.assertFalse(command_log.exists())
                self.assertFalse(find_log.exists())

    def test_every_policy_has_unit_tests(self) -> None:
        policy = ROOT / "infra/11-quality/conftest/policy"
        rules = {p.stem for p in policy.glob("*.rego") if not p.stem.endswith("_test")}
        tests = {p.stem.removesuffix("_test") for p in policy.glob("*_test.rego")}
        self.assertEqual(rules, tests)


@unittest.skipUnless(
    os.environ.get("HYHOME_MAIL_REHEARSAL") == "1",
    "set HYHOME_MAIL_REHEARSAL=1 to run the disposable Stalwart rehearsal (needs Docker)",
)
class StalwartRehearsalTests(unittest.TestCase):
    """SPEC-0180 S17: the rendered HOME services on an internal network."""

    SERVICES = ("stalwart", "stalwart-config")

    @classmethod
    def setUpClass(cls) -> None:
        cls.tag = f"hymail{os.getpid()}"
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.dir = Path(cls.tmp.name)
        (cls.dir / "data/stalwart/data").mkdir(parents=True)
        # The datastore belongs to the image user; delete it as that user
        # after the containers are gone (cleanups run last-in, first-out).
        cls.addClassCleanup(
            subprocess.run,
            [
                "docker",
                "run",
                "--rm",
                "--entrypoint",
                "find",
                "-v",
                f"{cls.dir / 'data/stalwart'}:/d",
                "stalwartlabs/stalwart:v0.16.22",
                "/d/data",
                "-mindepth",
                "1",
                "-delete",
            ],
            capture_output=True,
            check=False,
        )
        cls.secret = "Rehearsal" + os.urandom(6).hex()
        (cls.dir / "stalwart_password.txt").write_text(
            cls.secret + "\n", encoding="utf-8"
        )
        (cls.dir / "stalwart_password.txt").chmod(0o640)
        env = {
            **os.environ,
            "DEFAULT_COMMUNICATION_DIR": str(cls.dir / "data"),
            "DEFAULT_URL": "rehearsal.test",
            "SECRETS_GID": str(os.getgid()),
        }
        rendered = json.loads(
            subprocess.run(
                [
                    "docker",
                    "compose",
                    "--env-file",
                    ".env.example",
                    "--profile",
                    "mail-server",
                    "config",
                    "--format",
                    "json",
                    *cls.SERVICES,
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
        )
        services = {name: rendered["services"][name] for name in cls.SERVICES}
        for name, service in services.items():
            service["container_name"] = f"{cls.tag}-{name}"
            service["labels"] = {}
            service["networks"] = {"mail": {}}
            service.pop("profiles", None)
        volume = rendered["volumes"]["stalwart-data"]
        volume.pop("name", None)
        cls.model = {
            "name": cls.tag,
            "services": services,
            "networks": {"mail": {"internal": True}},
            "volumes": {"stalwart-data": volume},
            "secrets": {
                "stalwart_password": {"file": str(cls.dir / "stalwart_password.txt")}
            },
        }
        (cls.dir / "compose.json").write_text(json.dumps(cls.model), encoding="utf-8")
        cls.addClassCleanup(cls.compose, "down", "-v", "--timeout", "5")
        started = cls.compose("up", "-d", "--wait", "--wait-timeout", "120", "stalwart")
        if started.returncode != 0:
            raise AssertionError(
                started.stderr + cls.compose("logs", "--tail", "40").stdout
            )

    @classmethod
    def compose(cls, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "docker",
                "compose",
                "-p",
                cls.tag,
                "-f",
                str(cls.dir / "compose.json"),
                *args,
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=600,
        )

    def listening(self) -> set[int]:
        table = self.compose(
            "exec", "-T", "stalwart", "cat", "/proc/net/tcp", "/proc/net/tcp6"
        ).stdout
        ports = set()
        for line in table.splitlines()[1:]:
            fields = line.split()
            if (
                len(fields) > 3
                and fields[3] == "0A"
                and not fields[1].startswith("0100007F")
            ):
                if fields[1].startswith("0B00007F"):
                    continue
                ports.add(int(fields[1].rsplit(":", 1)[1], 16))
        return ports

    def smtp(self, *rcpt: str) -> str:
        script = "".join(
            ["EHLO sender.rehearsal.test\r\n", "MAIL FROM:<a@example.org>\r\n"]
            + [f"RCPT TO:<{r}>\r\n" for r in rcpt]
            + ["QUIT\r\n"]
        )
        return subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "-i",
                "--network",
                f"{self.tag}_mail",
                "alpine:3",
                "nc",
                "-w",
                "5",
                f"{self.tag}-stalwart",
                "25",
            ],
            input=script,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        ).stdout

    def test_plan_makes_the_server_internal_only(self) -> None:
        for _ in range(2):  # the second run must converge, not fail
            applied = self.compose("run", "--rm", "--no-deps", "stalwart-config")
            self.assertEqual(0, applied.returncode, applied.stdout + applied.stderr)
            self.assertIn("(0 failed)", applied.stdout + applied.stderr)
        restarted = self.compose("restart", "stalwart")
        self.assertEqual(0, restarted.returncode, restarted.stderr)
        self.assertEqual(
            0,
            self.compose(
                "up", "-d", "--wait", "--wait-timeout", "120", "stalwart"
            ).returncode,
        )
        self.assertEqual({25, 587, 993, 8080}, self.listening())
        replies = self.smtp("x@example.com", "nobody@rehearsal.test")
        self.assertIn("220 mail.rehearsal.test", replies)
        self.assertIn("550 5.1.2 Relay not allowed", replies)
        self.assertIn("Mailbox does not exist", replies)
        logs = self.compose("logs", "--no-color").stdout
        self.assertNotIn(self.secret, logs)


# SPEC-0180 S18: every routed service without the SSO ForwardAuth chain must
# name its own authentication. Keep in step with the route matrix in GDE-0079.
ROUTES_WITHOUT_SSO = {
    # Native OIDC (POL-0079 native list)
    "airflow": "native-oidc",
    "dozzle": "native-oidc",
    "gatus": "native-oidc",
    "grafana": "native-oidc",
    "kafka-ui": "native-oidc",
    "open-webui": "native-oidc",
    "openbao": "native-oidc",
    "superset": "native-oidc",
    # The identity provider and the ForwardAuth service themselves
    "keycloak": "identity-provider",
    "oauth2-proxy": "identity-provider",
    # Application or gateway credentials
    "dashboard": "gateway-basic-auth",
    "neo4j": "app-credentials",
    "open-notebook": "app-password-and-ip-allowlist",
    "opensearch": "security-plugin",
    "opensearch-dashboards": "security-plugin",
    "prometheus-api": "gateway-basic-auth",
    # Signed machine API
    "s3": "sigv4",
    # Two static files (favicon, robots.txt)
    "grafana-static": "static-only",
}


class RouteAuthContractTests(unittest.TestCase):
    @staticmethod
    def routers() -> list[tuple[str, str, set[str] | None]]:
        """Every HTTP/TCP router declaration as (source, name, chain).

        Declarations are kept apart: two services may declare the same router
        name, and a merged chain would hide one that lost its middleware.
        A TCP router has chain None.
        """
        import yaml

        found: list[tuple[str, str, set[str] | None]] = []
        for path in sorted((ROOT / "infra").rglob("docker-compose.yml")):
            data = (
                yaml.load(path.read_text(encoding="utf-8"), Loader=_ComposeLoader) or {}
            )
            for service_name, service in (data.get("services") or {}).items():
                labels = service.get("labels") or {}
                if isinstance(labels, list):
                    labels = dict(item.split("=", 1) for item in labels if "=" in item)
                chains: dict[str, set[str] | None] = {}
                for key, value in labels.items():
                    parts = key.split(".")
                    if len(parts) > 4 and parts[:3] == ["traefik", "http", "routers"]:
                        chain = chains.setdefault(parts[3], set())
                        if parts[4:] == ["middlewares"]:
                            chain.update(str(value).split(","))
                    elif len(parts) > 4 and parts[:3] == ["traefik", "tcp", "routers"]:
                        chains["tcp:" + parts[3]] = None
                source = f"{path.relative_to(ROOT)}:{service_name}"
                found += [(source, name, chain) for name, chain in chains.items()]
        dynamic = ROOT / "infra/01-gateway/traefik/dynamic"
        for path in sorted([*dynamic.glob("*.yml"), *dynamic.glob("*.yaml")]):
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            source = str(path.relative_to(ROOT))
            for name, router in ((data.get("http") or {}).get("routers") or {}).items():
                found.append((source, name, set(router.get("middlewares") or [])))
            for name in (data.get("tcp") or {}).get("routers") or {}:
                found.append((source, "tcp:" + name, None))
        return found

    def test_every_router_is_behind_sso_or_names_its_authentication(self) -> None:
        routers = self.routers()
        tcp = [(src, name) for src, name, chain in routers if chain is None]
        self.assertEqual([], tcp, "TCP routes cannot use ForwardAuth")
        unexplained = sorted(
            (src, name)
            for src, name, chain in routers
            if "sso-auth@file" not in chain and name not in ROUTES_WITHOUT_SSO
        )
        self.assertEqual([], unexplained)
        exempt = {name for _, name, chain in routers if "sso-auth@file" not in chain}
        self.assertEqual([], sorted(set(ROUTES_WITHOUT_SSO) - exempt), "stale entries")
        bare = sorted(
            (src, name)
            for src, name, chain in routers
            if not chain and ROUTES_WITHOUT_SSO.get(name) != "static-only"
        )
        self.assertEqual([], bare)

    def test_sso_redirects_browsers_and_refuses_machine_clients(self) -> None:
        """The proxy root sends a browser to Keycloak and answers an
        Accept: application/json client with 401; a login page is never a
        machine answer. SsoRehearsalTests proves this at runtime."""
        import yaml

        path = ROOT / "infra/01-gateway/traefik/dynamic/middleware.yml"
        middlewares = yaml.safe_load(path.read_text(encoding="utf-8"))["http"][
            "middlewares"
        ]
        self.assertEqual(
            "http://oauth2-proxy:4180/",
            middlewares["sso-auth"]["forwardAuth"]["address"],
        )
        errors = middlewares["sso-errors"]["errors"]
        self.assertEqual(["403"], errors["status"])
        self.assertNotIn("statusRewrites", errors)
        cfg = (ROOT / "infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg").read_text()
        self.assertIn('upstreams = [ "static://200" ]', cfg)
        self.assertIn("skip_provider_button = true", cfg)


class QdrantApiKeyContractTests(unittest.TestCase):
    def test_qdrant_requires_its_keys_and_prometheus_sends_the_read_only_one(
        self,
    ) -> None:
        import yaml

        compose = ROOT / "infra/04-data/qdrant/docker-compose.yml"
        services = yaml.safe_load(compose.read_text(encoding="utf-8"))["services"]
        service = services["qdrant"]
        self.assertIn("qdrant_api_key", service["secrets"])
        script = service["command"][-1]
        self.assertIn("</run/secrets/qdrant_api_key", script)
        self.assertIn("export QDRANT__SERVICE__API_KEY", script)
        self.assertIn("qdrant_read_only_api_key", service["secrets"])
        self.assertIn("</run/secrets/qdrant_read_only_api_key", script)
        self.assertIn("export QDRANT__SERVICE__READ_ONLY_API_KEY", script)
        self.assertIn('!= "$$QDRANT__SERVICE__API_KEY"', script)
        self.assertIn("exec ./entrypoint.sh", script)
        root = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
        self.assertIn("qdrant_api_key", root["secrets"])
        self.assertIn("qdrant_read_only_api_key", root["secrets"])
        observability = ROOT / "infra/06-observability/docker-compose.yml"
        prometheus = yaml.safe_load(observability.read_text(encoding="utf-8"))
        granted = prometheus["services"]["prometheus"]["secrets"]
        self.assertIn("qdrant_read_only_api_key", granted)
        self.assertNotIn("qdrant_api_key", granted)
        for name in ("prometheus.yml", "prometheus.dev.yml"):
            config = ROOT / "infra/06-observability/prometheus/config" / name
            text = config.read_text(encoding="utf-8")
            self.assertNotIn("qdrant_api_key", text, name)
            jobs = yaml.safe_load(text)["scrape_configs"]
            job = next(j for j in jobs if j["job_name"] == "qdrant")
            key_file = job.get("bearer_token_file")
            self.assertEqual("/run/secrets/qdrant_read_only_api_key", key_file, name)


class SeaweedfsS3MetricsContractTests(unittest.TestCase):
    def test_only_s3_serves_metrics_and_prometheus_scrapes_and_alerts_on_it(
        self,
    ) -> None:
        import yaml

        compose = ROOT / "infra/04-data/seaweedfs/docker-compose.yml"
        services = yaml.safe_load(compose.read_text(encoding="utf-8"))["services"]
        for name, service in services.items():
            has_metrics = any(
                "-metricsPort" in str(arg) for arg in service.get("command") or []
            )
            self.assertEqual(name == "seaweedfs-s3", has_metrics, name)
        self.assertIn("-metricsPort=9327", services["seaweedfs-s3"]["command"])
        config_dir = ROOT / "infra/06-observability/prometheus/config"
        for name in ("prometheus.yml", "prometheus.dev.yml"):
            jobs = yaml.safe_load((config_dir / name).read_text(encoding="utf-8"))[
                "scrape_configs"
            ]
            job = next(j for j in jobs if j["job_name"] == "seaweedfs-s3")
            self.assertEqual(
                ["seaweedfs-s3:9327"], job["static_configs"][0]["targets"], name
            )
        rules = yaml.safe_load(
            (config_dir / "alert_rules/alert_rules.local.datastores.yml").read_text(
                encoding="utf-8"
            )
        )
        exprs = [r.get("expr", "") for g in rules["groups"] for r in g["rules"]]
        self.assertIn('up{job="seaweedfs-s3"} == 0', exprs)
        self.assertTrue(any("node_filesystem_avail_bytes" in e for e in exprs))


class BackupAndHostAlertingContractTests(unittest.TestCase):
    """Stale backups, a filling system disk and an n8n without its database
    each went unalerted on 2026-09-26 to 09-29 (SPEC-0192)."""

    def test_only_a_successful_run_writes_the_timestamp_atomically(self) -> None:
        script = (ROOT / RESTIC_DIR / "bin/hyhome-backup.sh").read_text(
            encoding="utf-8"
        )
        tail = script[script.index("repository sizes:") :]
        self.assertIn("if (( status == 0 )); then", tail)
        self.assertIn("hyhome_backup_last_success_timestamp_seconds", tail)
        self.assertIn('chmod 0644 "$metrics_tmp"', tail)
        self.assertIn('mv -f "$metrics_tmp" "$metrics_dir/hyhome_backup.prom"', tail)

    def test_node_exporter_reads_the_metrics_directory_read_only(self) -> None:
        import yaml

        compose = ROOT / "infra/06-observability/docker-compose.yml"
        service = yaml.safe_load(compose.read_text(encoding="utf-8"))["services"][
            "node-exporter"
        ]
        self.assertIn("--collector.textfile.directory=/textfile", service["command"])
        mount = next(
            v
            for v in service["volumes"]
            if isinstance(v, dict) and v.get("target") == "/textfile"
        )
        self.assertTrue(mount["read_only"])
        self.assertFalse(mount["bind"]["create_host_path"])
        self.assertTrue(mount["source"].startswith("${BACKUP_STATE_REPO_DIR"))
        self.assertTrue(mount["source"].endswith("}/metrics"))

    def test_backup_staleness_and_system_disk_rules(self) -> None:
        import yaml

        rules = yaml.safe_load(
            (
                ROOT
                / "infra/06-observability/prometheus/config/alert_rules"
                / "alert_rules.local.infra.yml"
            ).read_text(encoding="utf-8")
        )
        by_name = {
            r["alert"]: r for g in rules["groups"] for r in g["rules"] if "alert" in r
        }
        stale = by_name["HyhomeBackupStale"]["expr"]
        self.assertIn(
            "time() - hyhome_backup_last_success_timestamp_seconds > 26 * 3600", stale
        )
        self.assertIn("absent(hyhome_backup_last_success_timestamp_seconds)", stale)
        disk = by_name["HostSystemDiskLow"]
        self.assertIn('mountpoint="/"', disk["expr"])
        self.assertIn("< 25 * 1024 * 1024 * 1024", disk["expr"])
        self.assertEqual("15m", disk["for"])

    def test_n8n_health_check_needs_the_database(self) -> None:
        import yaml

        compose = ROOT / "infra/07-workflow/n8n/docker-compose.yml"
        services = yaml.safe_load(compose.read_text(encoding="utf-8"))["services"]
        self.assertIn(
            "/healthz/readiness", " ".join(services["n8n"]["healthcheck"]["test"])
        )


class ObservabilityDashboardContractTests(unittest.TestCase):
    """One provisioned dashboard per role, every service covered, and alerts
    that link their runbooks (SPEC-0193)."""

    OBS = ROOT / "infra/06-observability"
    DASHBOARDS = OBS / "grafana/dashboards"

    def _dashboards(self) -> dict[str, dict]:
        return {
            str(path.relative_to(self.DASHBOARDS))[: -len(".json")]: json.loads(
                path.read_text(encoding="utf-8")
            )
            for path in sorted(self.DASHBOARDS.rglob("*.json"))
        }

    @staticmethod
    def _queries(dashboard: dict) -> set[str]:
        found: set[str] = set()

        def walk(node) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    if key in ("expr", "rawSql") and isinstance(value, str):
                        found.add(re.sub(r"\s+", "", value))
                    else:
                        walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(dashboard.get("panels", []) + dashboard.get("rows", []))
        return found

    def test_dashboards_have_unique_uids_resolved_datasources_and_a_source(
        self,
    ) -> None:
        dashboards = self._dashboards()
        uids = [d["uid"] for d in dashboards.values()]
        self.assertEqual(len(uids), len(set(uids)))
        for name, dashboard in dashboards.items():
            self.assertNotIn("__inputs", dashboard, name)
            variables = {
                v.get("name") for v in dashboard.get("templating", {}).get("list", [])
            }
            for placeholder in set(
                re.findall(r"\$\{(DS_[A-Z0-9_]+)\}", json.dumps(dashboard))
            ):
                self.assertIn(placeholder, variables, name)
            self.assertRegex(
                dashboard.get("description", ""), r"^(Source: |Local dashboard)", name
            )

    def test_no_two_dashboards_share_half_their_queries(self) -> None:
        queries = {n: self._queries(d) for n, d in self._dashboards().items()}
        names = sorted(n for n in queries if queries[n])
        for i, first in enumerate(names):
            for second in names[i + 1 :]:
                shared = len(queries[first] & queries[second])
                smaller = min(len(queries[first]), len(queries[second]))
                self.assertLess(shared / smaller, 0.5, (first, second))

    def test_readme_covers_every_service_every_job_and_every_dashboard(self) -> None:
        import yaml

        readme = (self.OBS / "grafana/README.md").read_text(encoding="utf-8")
        section = readme[
            readme.index("### Service Coverage") : readme.index("### Dashboard Sources")
        ]
        rows = [
            [cell.strip() for cell in line.strip("|").split("|")]
            for line in section.splitlines()
            if line.startswith("| ") and not line.startswith(("| Layer", "| ---"))
        ]
        services = {
            name
            for path in (ROOT / "infra").rglob("docker-compose*.yml")
            for name in (
                yaml.load(path.read_text(encoding="utf-8"), Loader=_ComposeLoader) or {}
            ).get("services", {})
            or {}
        }
        listed = [row[1].strip("`") for row in rows]
        self.assertEqual(sorted(services), sorted(listed))
        jobs = {
            job["job_name"]
            for job in yaml.safe_load(
                (self.OBS / "prometheus/config/prometheus.dev.yml").read_text(
                    encoding="utf-8"
                )
            )["scrape_configs"]
        }
        named_jobs = {j for row in rows for j in re.findall(r"`([a-z0-9-]+)`", row[2])}
        self.assertEqual(jobs, named_jobs)
        referenced = {
            d for row in rows for d in re.findall(r"`([A-Z]\w+/[a-z0-9-]+)`", row[3])
        }
        lab_section = readme[
            readme.index("### LAB Dashboard Coverage") : readme.index(
                "### Dashboard Sources"
            )
        ]
        lab_referenced = set(re.findall(r"`([A-Z]\w+/[a-z0-9-]+)`", lab_section))
        self.assertEqual(set(self._dashboards()), referenced | lab_referenced)

    def test_both_prometheus_files_hold_one_labelled_scrape_set(self) -> None:
        import yaml

        config = self.OBS / "prometheus/config"
        dev, prod = (
            yaml.safe_load((config / name).read_text(encoding="utf-8"))
            for name in ("prometheus.dev.yml", "prometheus.yml")
        )
        self.assertEqual(dev["scrape_configs"], prod["scrape_configs"])
        seen: set[str] = set()
        for job in dev["scrape_configs"]:
            for static in job["static_configs"]:
                self.assertEqual(
                    "hy-home", static["labels"]["cluster"], job["job_name"]
                )
                self.assertEqual(
                    "hy-home", static["labels"]["namespace"], job["job_name"]
                )
                for target in static["targets"]:
                    self.assertNotIn(target, seen, job["job_name"])
                    seen.add(target)

    def test_every_alert_rule_links_an_existing_runbook(self) -> None:
        import yaml

        prefix = "https://github.com/buenhyden/hy-home.docker/blob/main/"
        for path in sorted(
            (self.OBS / "prometheus/config/alert_rules").glob("alert_rules*.yml")
        ):
            for group in yaml.safe_load(path.read_text(encoding="utf-8"))["groups"]:
                for rule in group["rules"]:
                    if "alert" not in rule:
                        continue
                    url = rule["annotations"]["runbook_url"]
                    self.assertTrue(
                        url.startswith(prefix + "docs/05.operations/runbooks/"),
                        rule["alert"],
                    )
                    self.assertFalse(url.endswith("README.md"), rule["alert"])
                    self.assertTrue(
                        (ROOT / url[len(prefix) :]).is_file(), rule["alert"]
                    )


if __name__ == "__main__":
    unittest.main()
