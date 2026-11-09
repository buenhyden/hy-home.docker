"""Tier relocation regression checks; model comparisons use public inputs only."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.lib.document_governance.operations_catalog import (
    _ComposeLoader,
    conftest_source_context,
)

ROOT = Path(__file__).resolve().parents[2]
DATA = (
    "mng-db",
    "dev-db",
    "seaweedfs",
    "opensearch",
    "neo4j",
    "qdrant",
)
# Analytics packages left the root for standalone LABs (SPEC-0262).
ANALYTICS_LABS = {
    "lakehouse": (
        "lakehouse/flink",
        "lakehouse/spark",
        "lakehouse/trino",
        "lakehouse/great-expectations",
    ),
    "dbt": ("dbt",),
    "superset": ("superset",),
    "jupyterlab": ("jupyterlab",),
    "sonarqube": ("sonarqube",),
    "stalwart": ("stalwart",),
}
# ADR-0062 capability tiers; a renamed or retired tier fails here.
TIERS = (
    "01-gateway",
    "02-auth",
    "03-security",
    "04-data",
    "05-messaging",
    "06-observability",
    "07-workflow",
    "08-ai",
    "09-platform-ops",
    "10-communication",
    "11-quality",
    "12-analytics",
    "13-experience",
)


class TierLayoutTests(unittest.TestCase):
    def test_infra_has_exactly_the_registered_tiers(self):
        self.assertEqual(
            set(TIERS), {p.name for p in (ROOT / "infra").iterdir() if p.is_dir()}
        )

    def test_every_infra_service_names_its_container_and_host(self):
        # container_name and hostname equal the service key; a different
        # container_name needs a registered reason (Docker names are host-wide).
        registry = json.loads(
            (ROOT / "infra/common-optimizations.exceptions.json").read_text()
        )
        exceptions = {
            row["service"]: row["container_name"]
            for row in registry["naming_exceptions"]
            if row.get("reason")
        }
        seen = set()
        context = conftest_source_context(ROOT)
        for relative in context["regular"]:
            path = ROOT / relative
            text = path.read_text(encoding="utf-8")
            services = (yaml.load(text, Loader=_ComposeLoader) or {}).get(
                "services"
            ) or {}
            for name, service in services.items():
                seen.add(name)
                with self.subTest(file=str(path.relative_to(ROOT)), service=name):
                    # The host network namespace forbids a container hostname.
                    if service.get("network_mode") != "host":
                        self.assertEqual(name, service.get("hostname"))
                    self.assertEqual(
                        exceptions.get(name, name), service.get("container_name")
                    )
        self.assertLessEqual(set(exceptions), seen)

    def test_retired_influxdb_has_no_active_deployment(self):
        # ADR-0047: absence from the deployable model, not a repository-wide
        # string ban; history and research keep their wording.
        includes = yaml.safe_load((ROOT / "docker-compose.yml").read_text())["include"]
        self.assertFalse(any("influxdb" in str(path) for path in includes))
        self.assertFalse((ROOT / "infra/04-data/influxdb").exists())
        for path in includes:
            # Leaves use Compose-only tags (!override), so scan the source text.
            text = (ROOT / path).read_text()
            with self.subTest(path=path):
                self.assertIsNone(re.search(r"^  influxdb[\w-]*:", text, re.M))
                self.assertIsNone(re.search(r"^\s+image:\s*['\"]?influxdb", text, re.M))
                self.assertIsNone(re.search(r"^\s+- influxdb\s*$", text, re.M))

    def test_additional_packages_and_exact_labels(self):
        placements = {
            "11-quality": (
                "k6",
                "wiremock",
                "pact-broker",
                "conftest",
                "mailpit",
            ),
            "06-observability": ("dozzle",),
            "04-data": ("redisinsight",),
            "08-ai": ("open-notebook", "mlflow"),
        }
        includes = yaml.safe_load((ROOT / "docker-compose.yml").read_text())["include"]
        self.assertEqual(len(includes), len(set(includes)))
        for tier, packages in placements.items():
            for package in packages:
                with self.subTest(tier=tier, package=package):
                    leaf = ROOT / "infra" / tier / package / "docker-compose.yml"
                    self.assertTrue(leaf.is_file(), str(leaf))
                    self.assertTrue((leaf.parent / "README.md").is_file())
                    self.assertIn(str(leaf.relative_to(ROOT)), includes)
                    for service in yaml.safe_load(leaf.read_text())[
                        "services"
                    ].values():
                        self.assertEqual(
                            tier.split("-", 1)[1], service["labels"]["hy-home.tier"]
                        )
        quality = ROOT / "infra/11-quality"
        self.assertTrue(quality.is_dir())
        self.assertEqual(
            set(placements["11-quality"]),
            {p.name for p in quality.iterdir() if p.is_dir()},
        )
        locust = ROOT / "labs/locust"
        self.assertTrue((locust / "Dockerfile").is_file())
        self.assertTrue((locust / "README.md").is_file())
        self.assertTrue((ROOT / "labs/locust/docker-compose.yml").is_file())
        for package in ("opentofu", "terrakube", "registry", "renovate", "restic"):
            self.assertTrue(
                (
                    ROOT / "infra/09-platform-ops" / package / "docker-compose.yml"
                ).is_file()
            )
        self.assertTrue((ROOT / "labs/stalwart/docker-compose.yml").is_file())
        self.assertFalse((ROOT / "infra/10-communication/mailpit").exists())

    def test_transferred_hardening_retains_controls(self):
        import os

        script = "scripts/hardening/check-all-hardening.sh"
        fixtures = (
            "scripts/lib/hardening-lib.sh",
            "infra/tech-stack.versions.json",
            "infra/04-data/dev-db/docker-compose.yml",
            "labs/lakehouse/seaweedfs-table-bucket.sh",
            "infra/06-observability/docker-compose.yml",
            "infra/01-gateway/traefik/dynamic/middleware.yml",
            "infra/08-ai/ollama/docker-compose.yml",
            "infra/08-ai/open-webui/docker-compose.yml",
            "infra/04-data/redisinsight/docker-compose.yml",
            "infra/06-observability/dozzle/docker-compose.yml",
            "infra/08-ai/open-notebook/docker-compose.yml",
            "labs/sonarqube/docker-compose.yml",
            "infra/11-quality/wiremock/docker-compose.yml",
            "infra/11-quality/pact-broker/docker-compose.yml",
            "infra/11-quality/mailpit/docker-compose.yml",
        )
        cases = (
            (
                "11-quality",
                "wiremock",
                "127.0.0.1:${WIREMOCK_HOST_PORT:-18088}:8080",
                "0.0.0.0:18088:8080",
                "wiremock admin API publication must be loopback",
            ),
            (
                "11-quality",
                "pact-broker",
                "PACT_BROKER_ALLOW_PUBLIC_READ: 'false'",
                "PACT_BROKER_ALLOW_PUBLIC_READ: 'true'",
                "pact-broker public read must stay disabled",
            ),
            (
                "06-observability",
                "dozzle",
                "DOZZLE_AUTH_PROVIDER: oidc",
                "DOZZLE_AUTH_PROVIDER: none",
                "dozzle native authentication missing",
            ),
            (
                "04-data",
                "redisinsight",
                "sso-auth@file",
                "removed-auth@file",
                "redisinsight middleware chain mismatch",
            ),
            (
                "08-ai",
                "open-notebook",
                "OPEN_NOTEBOOK_PASSWORD_FILE=/run/secrets/open_notebook_password",
                "REMOVED_PASSWORD_CONTROL=true",
                "open-notebook password secret file missing",
            ),
        )
        env = {k: v for k, v in os.environ.items() if k != "HYHOME_CI_GATE_ROOT"}
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            for relative in (script, *fixtures):
                source = ROOT / relative
                self.assertTrue(source.is_file(), relative)
                target = fixture / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source.read_text())
            for tier, package, before, after, message in cases:
                with self.subTest(package=package):
                    command = ["bash", str(fixture / script), tier]
                    result = subprocess.run(
                        command,
                        cwd=fixture,
                        env=env,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(
                        0, result.returncode, result.stdout + result.stderr
                    )
                    target = fixture / "infra" / tier / package / "docker-compose.yml"
                    original = target.read_text()
                    self.assertIn(before, original)
                    target.write_text(original.replace(before, after))
                    result = subprocess.run(
                        command,
                        cwd=fixture,
                        env=env,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn(message, result.stdout + result.stderr)
                    target.write_text(original)
            for alias in ("11-laboratory", "laboratory", "lab"):
                result = subprocess.run(
                    ["bash", str(fixture / script), alias],
                    cwd=fixture,
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(2, result.returncode)
                self.assertIn("Unknown hardening tier", result.stderr)

    def test_platform_ops_layout_and_backup_unit(self):
        packages = ("opentofu", "terrakube", "registry", "renovate", "restic")
        names = set()
        for package in packages:
            path = ROOT / "infra/09-platform-ops" / package / "docker-compose.yml"
            self.assertTrue(path.is_file(), str(path))
            for name, service in yaml.safe_load(path.read_text())["services"].items():
                names.add(name)
                self.assertEqual("platform-ops", service["labels"]["hy-home.tier"])
        self.assertEqual(
            {
                "opentofu",
                "terrakube-api",
                "terrakube-ui",
                "terrakube-executor",
                "registry",
                "renovate",
                "restic",
                "restic-offsite",
                "backup-sqlite-export",
            },
            names,
        )
        relative = "infra/09-platform-ops/restic/bin/hyhome-backup.sh"
        unit = ROOT / "infra/09-platform-ops/restic/systemd/hyhome-backup.service"
        self.assertIn(
            "ExecStart=/home/hyunyoun/data/hy-home.docker/" + relative,
            unit.read_text().splitlines(),
        )
        self.assertTrue((ROOT / relative).is_file())
        includes = yaml.safe_load((ROOT / "docker-compose.yml").read_text())["include"]
        self.assertEqual(len(includes), len(set(includes)))
        for package in packages:
            self.assertIn(
                f"infra/09-platform-ops/{package}/docker-compose.yml", includes
            )

    def test_platform_ops_hardening_dispatch(self):
        import os

        script = "scripts/hardening/check-all-hardening.sh"
        paths = [
            script,
            "scripts/lib/hardening-lib.sh",
            "infra/tech-stack.versions.json",
        ]
        paths += [
            f"infra/09-platform-ops/{package}/docker-compose.yml"
            for package in ("opentofu", "terrakube", "registry", "renovate", "restic")
        ]
        env = {k: v for k, v in os.environ.items() if k != "HYHOME_CI_GATE_ROOT"}
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            for relative in paths:
                source = ROOT / relative
                self.assertTrue(source.is_file(), relative)
                target = fixture / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
            for alias in ("09-platform-ops", "platform-ops"):
                result = subprocess.run(
                    ["bash", str(fixture / script), alias],
                    cwd=fixture,
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            (fixture / "infra/09-platform-ops/registry/docker-compose.yml").unlink()
            result = subprocess.run(
                ["bash", str(fixture / script), "platform-ops"],
                cwd=fixture,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("registry/docker-compose.yml", result.stdout + result.stderr)
            for alias in ("09-tooling", "tooling"):
                result = subprocess.run(
                    ["bash", str(fixture / script), alias],
                    cwd=fixture,
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(2, result.returncode)
                self.assertIn("Unknown hardening tier", result.stderr)

    def test_certificate_script_resolves_repository_root(self):
        script = ROOT / "infra/04-data/seaweedfs/bin/gen-grpc-certs.sh"
        assignment = next(
            line
            for line in script.read_text().splitlines()
            if line.startswith("repo_root=")
        )
        relative = assignment.split(")/", 1)[1].split('"', 1)[0]
        self.assertEqual(ROOT, (script.parent / relative).resolve())

    def test_packages_include_coverage_and_labels(self):
        config = yaml.safe_load((ROOT / "docker-compose.yml").read_text())
        includes = {str(x) for x in config["include"]}
        for name in DATA:
            with self.subTest(package=name):
                path = ROOT / "infra/04-data" / name
                self.assertTrue((path / "README.md").is_file())
                relative = str((path / "docker-compose.yml").relative_to(ROOT))
                self.assertIn(relative, includes)
        for lab, packages in ANALYTICS_LABS.items():
            with self.subTest(lab=lab):
                self.assertTrue((ROOT / "labs" / lab / "docker-compose.yml").is_file())
                self.assertNotIn(f"labs/{lab}/docker-compose.yml", includes)
                for package in packages:
                    self.assertTrue((ROOT / "labs" / package / "README.md").is_file())
        for tier in ("10-communication", "12-analytics"):
            self.assertEqual(
                [], [p.name for p in (ROOT / "infra" / tier).iterdir() if p.is_dir()]
            )
        actual = {
            str(p.relative_to(ROOT))
            for p in (ROOT / "infra").rglob("docker-compose.yml")
        }
        self.assertEqual(actual, includes)

    def test_analytics_hardening_runs_and_rejects_broken_sigv4(self):
        import os

        env = {k: v for k, v in os.environ.items() if k != "HYHOME_CI_GATE_ROOT"}
        script = ROOT / "scripts/hardening/check-all-hardening.sh"
        result = subprocess.run(
            ["bash", str(script), "12-analytics"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        import shutil

        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            subprocess.run(["git", "init", "--quiet", directory], check=True)
            target = fixture / "scripts/hardening/check-all-hardening.sh"
            target.parent.mkdir(parents=True)
            shutil.copy2(script, target)
            library = fixture / "scripts/lib/hardening-lib.sh"
            library.parent.mkdir(parents=True)
            shutil.copy2(ROOT / "scripts/lib/hardening-lib.sh", library)
            for lab in ("lakehouse", "superset", "dbt"):
                shutil.copytree(ROOT / "labs" / lab, fixture / "labs" / lab)
            wrapper = fixture / "labs/lakehouse/spark/hyhome-spark.sh"
            wrapper.write_text(
                wrapper.read_text().replace(
                    "rest.auth.type sigv4", "rest.auth.type none"
                )
            )
            result = subprocess.run(
                ["bash", str(target), "12-analytics"],
                cwd=fixture,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn(
                "spark catalog must sign with SigV4", result.stdout + result.stderr
            )

    def test_experience_hardening_runs_explicitly_and_in_the_full_route(self):
        env = {k: v for k, v in os.environ.items() if k != "HYHOME_CI_GATE_ROOT"}
        script = "scripts/hardening/check-all-hardening.sh"
        compose = "infra/13-experience/storybook/docker-compose.yml"
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            for relative in (
                script,
                "scripts/lib/hardening-lib.sh",
                "docs/01.requirements/0003-security.md",
            ):
                target = fixture / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            shutil.copytree(ROOT / "infra", fixture / "infra")
            # LAB sources the full route also checks (SPEC-0262).
            shutil.copytree(ROOT / "labs", fixture / "labs")

            for alias in ("13-experience", "experience"):
                result = subprocess.run(
                    ["bash", str(fixture / script), alias],
                    cwd=fixture,
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

            target = fixture / compose
            original = target.read_text()
            target.write_text(
                original.replace(
                    "req-rate-limit@file,gateway-standard-chain@file,sso-auth@file",
                    "req-rate-limit@file,gateway-standard-chain@file",
                )
            )
            result = subprocess.run(
                ["bash", str(fixture / script), "experience"],
                cwd=fixture,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("storybook sso middleware chain missing", result.stdout)

            target.write_text(original)
            target.unlink()
            result = subprocess.run(
                ["bash", str(fixture / script)],
                cwd=fixture,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn(compose, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
