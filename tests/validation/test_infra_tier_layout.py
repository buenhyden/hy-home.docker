"""Tier relocation regression checks; model comparisons use public inputs only."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DATA = (
    "mng-db",
    "dev-db",
    "supabase",
    "seaweedfs",
    "influxdb",
    "opensearch",
    "neo4j",
    "qdrant",
)
ANALYTICS = ("flink", "spark", "trino", "great-expectations", "superset", "dbt")


class TierLayoutTests(unittest.TestCase):
    def test_additional_packages_and_exact_labels(self):
        placements = {
            "11-quality": (
                "k6",
                "wiremock",
                "pact-broker",
                "sonarqube",
                "conftest",
                "mailpit",
            ),
            "06-observability": ("dozzle",),
            "04-data": ("redisinsight",),
            "08-ai": ("open-notebook", "mlflow"),
            "12-analytics": ("jupyterlab",),
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
            set(placements["11-quality"]) | {"locust"},
            {p.name for p in quality.iterdir() if p.is_dir()},
        )
        locust = quality / "locust"
        self.assertTrue((locust / "Dockerfile").is_file())
        self.assertTrue((locust / "README.md").is_file())
        self.assertFalse((locust / "docker-compose.yml").exists())
        self.assertTrue((ROOT / "labs/locust.yml").is_file())
        for package in ("opentofu", "terrakube", "registry", "renovate", "restic"):
            self.assertTrue(
                (
                    ROOT / "infra/09-platform-ops" / package / "docker-compose.yml"
                ).is_file()
            )
        self.assertTrue(
            (ROOT / "infra/10-communication/stalwart/docker-compose.yml").is_file()
        )
        self.assertFalse((ROOT / "infra/11-laboratory").exists())
        for package in placements["11-quality"]:
            self.assertFalse((ROOT / "infra/09-tooling" / package).exists())
        self.assertFalse((ROOT / "infra/10-communication/mailpit").exists())

    def test_transferred_hardening_retains_controls(self):
        import os

        script = "scripts/hardening/check-all-hardening.sh"
        fixtures = (
            "scripts/lib/hardening-lib.sh",
            "infra/tech-stack.versions.json",
            "infra/04-data/supabase/docker-compose.yml",
            "infra/04-data/dev-db/docker-compose.yml",
            "infra/04-data/seaweedfs/config/seaweedfs-table-bucket.sh",
            "infra/06-observability/docker-compose.yml",
            "infra/01-gateway/traefik/dynamic/middleware.yml",
            "infra/08-ai/ollama/docker-compose.yml",
            "infra/08-ai/open-webui/docker-compose.yml",
            "infra/04-data/redisinsight/docker-compose.yml",
            "infra/06-observability/dozzle/docker-compose.yml",
            "infra/08-ai/open-notebook/docker-compose.yml",
            "infra/11-quality/sonarqube/docker-compose.yml",
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
        self.assertFalse((ROOT / "infra/09-tooling").exists())
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
        for tier, packages in (("04-data", DATA), ("12-analytics", ANALYTICS)):
            for name in packages:
                with self.subTest(package=name):
                    path = ROOT / "infra" / tier / name
                    self.assertTrue((path / "README.md").is_file())
                    relative = str((path / "docker-compose.yml").relative_to(ROOT))
                    self.assertIn(relative, includes)
                    document = yaml.safe_load((ROOT / relative).read_text())
                    for service in document["services"].values():
                        if tier == "12-analytics":
                            self.assertEqual(
                                "analytics", service["labels"]["hy-home.tier"]
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
            shutil.copytree(ROOT / "infra/12-analytics", fixture / "infra/12-analytics")
            wrapper = fixture / "infra/12-analytics/spark/hyhome-spark.sh"
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


if __name__ == "__main__":
    unittest.main()
