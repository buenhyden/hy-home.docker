"""Failing-case coverage for the two Compose baseline gates.

Both gates run in CI through `.github/workflow-contract.yml` and neither had a
covering test, so nothing proved they could go red. Each script resolves the
repository root with `git rev-parse --show-toplevel` and reads its subject from
`docker compose config --format json`, so the fixtures here are a throwaway Git
repository plus a `docker` shim on `PATH` that prints a crafted document.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUICKWIN = ROOT / "scripts/validation/check-quickwin-baseline.sh"
TEMPLATE_SECURITY = ROOT / "scripts/validation/check-template-security-baseline.sh"

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
        )


class QuickwinBaselineTests(BaselineGateHarness):
    def test_the_tracked_script_runs(self) -> None:
        self.write_config(compliant_config("alpha"))
        result = subprocess.run(
            ["bash", os.fspath(QUICKWIN)],
            cwd=self.root,
            capture_output=True,
            text=True,
            env=self.gate_env(),
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


if __name__ == "__main__":
    unittest.main()
