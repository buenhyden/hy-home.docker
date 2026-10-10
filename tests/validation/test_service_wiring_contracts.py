"""Service wiring contracts found stale during SPEC-0182."""

from __future__ import annotations

import json
import re
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


class AiRuntimeContractTests(unittest.TestCase):
    """SPEC-0226: exact AI image pins and the load, queue and egress limits."""

    def setUp(self) -> None:
        self.ollama = _service("infra/08-ai/ollama/docker-compose.yml", "ollama")
        self.webui = _service("infra/08-ai/open-webui/docker-compose.yml", "open-webui")
        self.ollama_env = dict(e.split("=", 1) for e in self.ollama["environment"])

    def test_images_are_the_requested_tags_pinned_by_digest(self) -> None:
        pattern = r"^{}@sha256:[0-9a-f]{{64}}$"
        self.assertRegex(
            self.ollama["image"], pattern.format(r"ollama/ollama:0\.40\.2")
        )
        self.assertRegex(
            self.webui["image"],
            pattern.format(r"ghcr\.io/open-webui/open-webui:v0\.11\.4-cuda"),
        )

    def test_slow_loads_are_not_cut_off(self) -> None:
        # Ollama's limit is for a stalled load; Open WebUI keeps its default of
        # no total request timeout, so a long streamed answer is not cut off.
        self.assertEqual("15m", self.ollama_env["OLLAMA_LOAD_TIMEOUT"])
        self.assertNotIn("AIOHTTP_CLIENT_TIMEOUT", self.webui["environment"])

    def test_queue_is_bounded_and_cloud_is_off(self) -> None:
        self.assertEqual("${OLLAMA_MAX_QUEUE:-16}", self.ollama_env["OLLAMA_MAX_QUEUE"])
        self.assertEqual("1", self.ollama_env["OLLAMA_NO_CLOUD"])

    def test_webui_has_no_gpu_docker_socket_or_host_shell(self) -> None:
        for key in ("deploy", "gpus", "runtime", "devices", "privileged"):
            self.assertNotIn(key, self.webui)
        self.assertNotIn("docker.sock", str(self.webui["volumes"]))
        self.assertNotIn("TERMINAL_SERVER_CONNECTIONS", self.webui["environment"])
        self.assertTrue(
            self.webui["environment"]["WEBUI_SECRET_KEY_FILE"].startswith(
                "/app/backend/data/"
            )
        )

    def test_renovate_tracks_both_compose_files(self) -> None:
        renovate = json.loads((ROOT / "renovate.json5").read_text(encoding="utf-8"))
        patterns = renovate["docker-compose"]["managerFilePatterns"]
        for name in ("ollama", "open-webui"):
            path = f"infra/08-ai/{name}/docker-compose.yml"
            self.assertTrue(any(re.search(pattern[1:-1], path) for pattern in patterns))
        self.assertIn("labs/**", renovate["ignorePaths"])


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
