"""LAB entrypoints stay outside the normal root (SPEC-0215)."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LABS = sorted((ROOT / "labs").glob("*.yml"))
# Synthetic, non-HOME inputs: only enough to render each LAB model.
LAB_INPUTS = {
    "LAB_DATA_DIR": "/nonexistent/lab-data",
    "LAB_SECRET_DIR": "/nonexistent/lab-secrets",
    "LAB_KAFKA_CLUSTER_ID": "synthetic-lab-cluster",
    "LAB_LOCUST_SCENARIO_DIR": "/nonexistent/locust-scenario",
    "LAB_LOCUST_RESULT_DIR": "/nonexistent/locust-results",
    "LAB_OPENSEARCH_CERT_DIR": "/nonexistent/opensearch-certs",
}


def compose(*args: str, extra_env: dict[str, str] | None = None):
    with tempfile.TemporaryDirectory() as home:
        return subprocess.run(
            ["docker", "compose", *args],
            cwd=ROOT,
            env={"PATH": os.environ["PATH"], "HOME": home, **(extra_env or {})},
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )


def render(*args: str, extra_env: dict[str, str] | None = None) -> dict:
    result = compose(*args, "config", "--format", "json", extra_env=extra_env)
    if result.returncode != 0:
        raise AssertionError(f"render failed: {' '.join(args)}\n{result.stderr}")
    return json.loads(result.stdout)


class RootClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = render("--env-file", ".env.example", "--profile", "*")
        cls.labs = {
            path.name: render(
                "--env-file",
                "labs/.env.example",
                "-f",
                str(path.relative_to(ROOT)),
                "--profile",
                "*",
                extra_env=LAB_INPUTS,
            )
            for path in LABS
        }

    def test_wildcard_root_render_selects_no_lab_service(self) -> None:
        self.assertEqual(8, len(self.labs))
        root_services = set(self.root["services"])
        for name, lab in self.labs.items():
            with self.subTest(lab=name):
                self.assertEqual(set(), root_services & set(lab["services"]))

    def test_root_declares_no_lab_network_variable_or_secret(self) -> None:
        root_networks = {net.get("name") for net in self.root["networks"].values()}
        self.assertNotIn("lab_net", root_networks)
        for name, lab in self.labs.items():
            with self.subTest(lab=name):
                lab_networks = {net.get("name") for net in lab["networks"].values()}
                self.assertEqual(set(), root_networks & lab_networks)
        for secret in self.root.get("secrets", {}).values():
            self.assertNotIn("/secrets/labs/", secret.get("file", ""))
        root_text = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertNotIn("labs/", root_text)
        self.assertNotIn("${LAB_", root_text)

    def test_a_lab_service_cannot_be_targeted_through_the_root(self) -> None:
        for name, lab in self.labs.items():
            service = sorted(lab["services"])[0]
            with self.subTest(lab=name, service=service):
                result = compose(
                    "--env-file", ".env.example", "--profile", "*", "config", service
                )
                self.assertNotEqual(0, result.returncode)
                self.assertIn("no such service", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
