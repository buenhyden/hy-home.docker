"""Service wiring contracts found stale during SPEC-0182."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path, PurePosixPath

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


class OptionalIntegrationContractTests(unittest.TestCase):
    def test_explicit_targets_close_companions_for_direct_and_dependency_starts(self):
        from scripts.lib.document_governance.operations_catalog import _compose_mapping

        root = yaml.safe_load((ROOT / "docker-compose.yml").read_text())
        services = {
            name: service
            for path in root["include"]
            for name, service in _compose_mapping(ROOT, PurePosixPath(path))[
                "services"
            ].items()
        }
        pairs = {
            "mng-pg": {"mng-pg-monitor-provision", "mng-pg-exporter"},
            "mng-valkey": {"mng-valkey-exporter"},
            "dev-pg": {"dev-pg-monitor-provision", "dev-pg-exporter"},
            "dev-valkey": {"dev-valkey-exporter"},
            "kafka-1": {"kafka-exporter"},
            "ollama": {"ollama-exporter"},
        }

        def missing_companions(targets):
            selected, pending = frozenset(), frozenset(targets)
            while pending:
                selected = selected | pending
                pending = (
                    frozenset(
                        dependency
                        for name in pending
                        for dependency, rule in services[name]
                        .get("depends_on", {})
                        .items()
                        if rule.get("required", True)
                    )
                    - selected
                )
            return (
                frozenset(
                    companion
                    for producer, companions in pairs.items()
                    if producer in selected
                    for companion in companions
                )
                - selected
            )

        policy = (
            ROOT
            / "docs/05.operations/policies/01-common/0078-compose-profile-vocabulary.md"
        ).read_text()
        for producer in pairs:
            match = re.search(
                r"^\| `" + re.escape(producer) + r"` \| `([^`]+)` \|$", policy, re.M
            )
            self.assertIsNotNone(match, producer)
            self.assertFalse(missing_companions(match[1].split()), producer)
            self.assertTrue(missing_companions({producer}), producer)
        self.assertIn("mng-pg-exporter", missing_companions({"mng-pg-init"}))
        self.assertIn("kafka-exporter", missing_companions({"kafka-connect"}))

    def test_every_producer_profile_selects_its_existing_exporter_and_provisioner(self):
        for path, producer, companions in (
            (
                "infra/04-data/mng-db/docker-compose.yml",
                "mng-valkey",
                ("mng-valkey-exporter",),
            ),
            (
                "infra/04-data/mng-db/docker-compose.yml",
                "mng-pg",
                ("mng-pg-monitor-provision", "mng-pg-exporter"),
            ),
            (
                "infra/04-data/dev-db/docker-compose.yml",
                "dev-pg",
                ("dev-pg-monitor-provision", "dev-pg-exporter"),
            ),
            (
                "infra/04-data/dev-db/docker-compose.yml",
                "dev-valkey",
                ("dev-valkey-exporter",),
            ),
            (
                "infra/05-messaging/kafka/docker-compose.yml",
                "kafka-1",
                ("kafka-exporter",),
            ),
            ("infra/08-ai/ollama/docker-compose.yml", "ollama", ("ollama-exporter",)),
        ):
            producer_profiles = set(_service(path, producer)["profiles"])
            for companion in companions:
                with self.subTest(producer=producer, companion=companion):
                    self.assertEqual(
                        producer_profiles, set(_service(path, companion)["profiles"])
                    )
                    self.assertNotIn(
                        companion, _service(path, producer).get("depends_on", {})
                    )

    def test_named_account_mount_is_optional_and_ollama_only_adds_the_worker(self):
        root = yaml.safe_load((ROOT / "docker-compose.yml").read_text())
        self.assertEqual(
            "./secrets/db/mng-valkey/n8n_password.txt",
            root["secrets"]["mng_valkey_n8n_password"]["file"],
        )
        self.assertNotIn(
            "mng_valkey_n8n_password",
            _service("infra/04-data/mng-db/docker-compose.yml", "mng-valkey")[
                "secrets"
            ],
        )
        acl = yaml.safe_load(
            (ROOT / "infra/04-data/mng-db/docker-compose.n8n-acl.yml").read_text()
        )
        self.assertEqual(
            {"version": 1, "base": "infra/04-data/mng-db/docker-compose.yml"},
            acl["x-hyhome-overlay"],
        )
        self.assertEqual({"mng-valkey"}, set(acl["services"]))
        self.assertEqual(
            "1",
            str(acl["services"]["mng-valkey"]["environment"]["MNG_VALKEY_N8N_ENABLED"]),
        )
        overlay = yaml.safe_load(
            (ROOT / "infra/07-workflow/n8n/docker-compose.ollama-local.yml").read_text()
        )
        self.assertEqual(
            {"version": 1, "base": "docker-compose.yml"}, overlay["x-hyhome-overlay"]
        )
        self.assertEqual({"n8n_ollama_net": {"internal": True}}, overlay["networks"])
        self.assertEqual({"n8n-worker", "ollama"}, set(overlay["services"]))
        for service in overlay["services"].values():
            self.assertEqual({"networks": {"n8n_ollama_net": {}}}, service)

    @unittest.skipUnless(shutil.which("docker"), "docker CLI not available")
    def test_public_render_preserves_defaults_and_adds_only_opted_in_connections(self):
        def render(*overlays: str, named: bool = False):
            with tempfile.TemporaryDirectory() as directory:
                env = {
                    "PATH": os.environ["PATH"],
                    "COMPOSE_DISABLE_ENV_FILE": "1",
                    "DOCKER_CONFIG": directory,
                }
                if named:
                    env |= {
                        "N8N_VALKEY_USERNAME": "n8n",
                        "N8N_VALKEY_SECRET": "mng_valkey_n8n_password",
                    }
                args = [
                    "docker",
                    "compose",
                    "--env-file",
                    ".env.example",
                    "-f",
                    "docker-compose.yml",
                ]
                for overlay in overlays:
                    args.extend(("-f", overlay))
                args.extend(
                    (
                        "--profile",
                        "mng",
                        "--profile",
                        "workflow-n8n",
                        "--profile",
                        "ollama",
                        "config",
                        "--format",
                        "json",
                    )
                )
                result = subprocess.run(
                    args,
                    cwd=ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=60,
                )
                return json.loads(result.stdout)

        base = render()
        optional = render(
            "infra/04-data/mng-db/docker-compose.n8n-acl.yml",
            "infra/07-workflow/n8n/docker-compose.ollama-local.yml",
            named=True,
        )
        self.assertEqual(set(base["services"]), set(optional["services"]))
        for name in ("n8n", "n8n-worker"):
            normal = base["services"][name]["environment"]
            named = optional["services"][name]["environment"]
            self.assertEqual("mng-valkey", normal["QUEUE_BULL_REDIS_HOST"])
            self.assertEqual("", normal["QUEUE_BULL_REDIS_USERNAME"])
            self.assertEqual("0", normal["QUEUE_BULL_REDIS_DB"])
            self.assertEqual("n8n", named["QUEUE_BULL_REDIS_USERNAME"])
            self.assertEqual("0", named["QUEUE_BULL_REDIS_DB"])
            self.assertEqual(
                "/run/secrets/mng_valkey_n8n_password",
                named["QUEUE_BULL_REDIS_PASSWORD_FILE"],
            )
        for name, service in optional["services"].items():
            old = set(base["services"][name].get("networks", {}))
            expected = (
                old | {"n8n_ollama_net"} if name in ("n8n-worker", "ollama") else old
            )
            self.assertEqual(expected, set(service.get("networks", {})), name)
        self.assertTrue(optional["networks"]["n8n_ollama_net"]["internal"])


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
            self.ollama["image"], pattern.format(r"ollama/ollama:0\.40\.6")
        )
        self.assertRegex(
            self.webui["image"],
            pattern.format(r"ghcr\.io/open-webui/open-webui:v0\.12\.0-cuda"),
        )

    def test_cuda_libraries_are_warmed_before_gpu_discovery(self) -> None:
        # SPEC-0246: a cold read from the HDD outlasted the 30 s discovery watchdog.
        script = self.ollama["entrypoint"][-1]
        self.assertTrue(
            script.startswith("cat /usr/lib/ollama/cuda_v12/* > /dev/null;")
        )
        self.assertTrue(script.endswith("exec /bin/ollama serve"))

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
