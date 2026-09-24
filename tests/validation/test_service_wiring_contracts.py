"""Service wiring contracts found stale during SPEC-0182."""

from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _service(path: str, name: str) -> dict:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))["services"][name]


class N8nValkeyExporterTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("docker"), "docker CLI not available")
    def test_rendered_exporter_targets_the_declared_valkey(self) -> None:
        rendered = subprocess.run(
            [
                "docker",
                "compose",
                "--env-file",
                ".env.example",
                "-f",
                "docker-compose.yml",
                "--profile",
                "dedicated-valkey",
                "config",
                "--format",
                "json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
        services = json.loads(rendered.stdout)["services"]
        command = " ".join(services["n8n-valkey-exporter"]["command"])
        self.assertIn("-redis.addr=redis://n8n-valkey:6379", command)
        self.assertIn("n8n-valkey", services)


class OpenWebUiVectorStoreTests(unittest.TestCase):
    def test_no_vector_db_url_without_a_selected_vector_db(self) -> None:
        env = _service("infra/08-ai/open-webui/docker-compose.yml", "open-webui")[
            "environment"
        ]
        if "VECTOR_DB_URL" in env:
            self.assertIn("VECTOR_DB", env)


class ComposeCoreReadinessExampleTests(unittest.TestCase):
    def test_example_holds_only_what_the_harness_reads(self) -> None:
        example = ROOT / "examples/operations/compose-core-readiness"
        self.assertEqual(
            {"compose.core-runtime.override.yml", "env.runtime.example"},
            {p.name for p in example.iterdir()},
        )
        for path in example.iterdir():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("INFRA_SUBNET", text, path.name)
            self.assertNotIn("INFRA_GATEWAY", text, path.name)


if __name__ == "__main__":
    unittest.main()
