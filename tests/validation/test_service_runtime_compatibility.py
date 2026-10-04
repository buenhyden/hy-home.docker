"""SPEC-0204 service runtime declarations that must agree before HOME rollout."""

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
N8N = ROOT / "infra/07-workflow/n8n"


def compose(path: str) -> dict:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


class RuntimeCompatibilityTests(unittest.TestCase):
    def test_n8n_instances_and_runners_share_version_and_supported_timeout(self):
        services = compose("infra/07-workflow/n8n/docker-compose.yml")["services"]
        versions = {
            services[name]["build"]["args"]["N8N_VERSION"]
            for name in ("n8n", "n8n-worker")
        }
        versions.update(
            services[name]["image"].split(":", 1)[1].removesuffix("-local")
            for name in (
                "n8n",
                "n8n-worker",
                "n8n-task-runner",
                "n8n-task-runner-worker",
            )
        )
        for dockerfile in ("Dockerfile", "dev.Dockerfile"):
            match = re.search(
                r"^ARG N8N_VERSION=(\S+)$", (N8N / dockerfile).read_text(), re.M
            )
            self.assertIsNotNone(match, dockerfile)
            versions.add(match.group(1))

        self.assertEqual(1, len(versions), f"n8n/runner version mismatch: {versions}")
        for name in ("n8n", "n8n-worker", "n8n-task-runner", "n8n-task-runner-worker"):
            environment = services[name]["environment"]
            self.assertEqual(300, environment["N8N_RUNNERS_TASK_TIMEOUT"])
            self.assertNotIn("N8N_RUNNER_TASK_TIMEOUT", environment)

    def test_n8n_consumes_selected_broker_secret_and_runner_token(self):
        services = compose("infra/07-workflow/n8n/docker-compose.yml")["services"]
        for name in ("n8n", "n8n-worker"):
            environment = services[name]["environment"]
            self.assertIn(
                "${N8N_VALKEY_SECRET:-mng_valkey_password}",
                environment["QUEUE_BULL_REDIS_PASSWORD_FILE"],
            )
            self.assertIn("N8N_VALKEY_SECRET", environment)
            self.assertEqual(
                "${N8N_VALKEY_SECRET:-mng_valkey_password}",
                services[name]["secrets"][0],
            )
            self.assertNotIn("n8n_valkey_password", services[name]["secrets"])
        for entrypoint in ("docker-entrypoint.sh", "docker-entrypoint.dev.sh"):
            script = (N8N / entrypoint).read_text(encoding="utf-8")
            self.assertIn("N8N_VALKEY_SECRET", script, entrypoint)
            result = subprocess.run(["sh", "-n", str(N8N / entrypoint)], check=False)
            self.assertEqual(0, result.returncode, entrypoint)
        for name in ("n8n-task-runner", "n8n-task-runner-worker"):
            runner = services[name]
            self.assertIn("n8n_runner_auth_token", runner["secrets"])
            self.assertNotIn("N8N_RUNNERS_AUTH_TOKEN_FILE", runner["environment"])
            self.assertEqual(["tini", "--", "/bin/sh", "-ec"], runner["entrypoint"])
            command = runner["command"]
            launcher = command if isinstance(command, str) else " ".join(command)
            self.assertIn("/run/secrets/n8n_runner_auth_token", launcher)
            self.assertIn("N8N_RUNNERS_AUTH_TOKEN", launcher)
            self.assertIn("/usr/local/bin/task-runner-launcher", launcher)
            result = subprocess.run(
                ["sh", "-n"], input=launcher, text=True, check=False
            )
            self.assertEqual(0, result.returncode, name)
            with tempfile.TemporaryDirectory() as temporary:
                secret = Path(temporary) / "token"
                stub = Path(temporary) / "launcher"
                stub.write_text(
                    '#!/bin/sh\ntest "$N8N_RUNNERS_AUTH_TOKEN" = synthetic-token\n',
                    encoding="utf-8",
                )
                stub.chmod(0o700)
                simulated = (
                    launcher.replace("$$", "$")
                    .replace("/run/secrets/n8n_runner_auth_token", str(secret))
                    .replace("/usr/local/bin/task-runner-launcher", str(stub))
                )
                for value, expected in (
                    (None, False),
                    ("", False),
                    ("synthetic-token", True),
                ):
                    if value is None:
                        secret.unlink(missing_ok=True)
                    else:
                        secret.write_text(value, encoding="utf-8")
                    result = subprocess.run(
                        ["sh", "-ec", simulated],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(expected, result.returncode == 0, (name, value))
                    self.assertNotIn("synthetic-token", result.stdout + result.stderr)

    def test_n8n_entrypoints_reject_wrong_or_empty_selected_broker_secret(self):
        for entrypoint in ("docker-entrypoint.sh", "docker-entrypoint.dev.sh"):
            source = (N8N / entrypoint).read_text(encoding="utf-8")
            guard = source[: source.index("if [ -d /opt/custom-certificates ]")]
            with tempfile.TemporaryDirectory() as temporary:
                mount = Path(temporary)
                guard = guard.replace("/run/secrets", str(mount))
                for name in (
                    "n8n_db_password",
                    "n8n_encryption_key",
                    "n8n_runner_auth_token",
                ):
                    (mount / name).write_text("synthetic", encoding="utf-8")
                for host, selected, value, success in (
                    ("mng-valkey", "mng_valkey_password", "synthetic", True),
                    ("n8n-valkey", "n8n_valkey_password", "synthetic", True),
                    ("mng-valkey", "n8n_valkey_password", "synthetic", False),
                    ("mng-valkey", "mng_valkey_password", "", False),
                    ("mng-valkey", "mng_valkey_password", None, False),
                ):
                    for name in ("mng_valkey_password", "n8n_valkey_password"):
                        (mount / name).unlink(missing_ok=True)
                    if value is not None:
                        (mount / selected).write_text(value, encoding="utf-8")
                    environment = os.environ.copy()
                    environment.update(N8N_VALKEY_HOST=host, N8N_VALKEY_SECRET=selected)
                    result = subprocess.run(
                        ["sh", "-c", guard],
                        env=environment,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(
                        success, result.returncode == 0, (entrypoint, host, selected)
                    )
                    self.assertNotIn("synthetic", result.stdout + result.stderr)

    def test_openbao_sealed_status_is_not_ready(self):
        openbao = compose("infra/03-security/openbao/docker-compose.yml")["services"][
            "openbao"
        ]
        health = openbao["healthcheck"]["test"][1]
        self.assertIn("bao status", health)
        with tempfile.TemporaryDirectory() as temporary:
            stub = Path(temporary) / "bao"
            stub.write_text('#!/bin/sh\nexit "$BAO_SYNTHETIC_RC"\n', encoding="utf-8")
            stub.chmod(0o700)
            for status, expected in ((0, 0), (1, 1), (2, 1)):
                environment = os.environ.copy()
                environment["PATH"] = f"{temporary}:{environment['PATH']}"
                environment["BAO_SYNTHETIC_RC"] = str(status)
                result = subprocess.run(
                    ["sh", "-c", health.replace("$$", "$")],
                    env=environment,
                    check=False,
                )
                self.assertEqual(expected == 0, result.returncode == 0, status)

    def test_crawl4ai_security_pin_and_isolated_optional_network(self):
        data = compose("infra/08-ai/crawl4ai/docker-compose.yml")
        crawler = data["services"]["crawl4ai"]
        version = crawler["image"].rsplit(":", 1)[1].split("@", 1)[0]
        self.assertGreaterEqual(tuple(map(int, version.split("."))), (0, 9, 4))
        self.assertEqual(["crawl4ai"], crawler["profiles"])
        self.assertEqual(["crawl4ai_net"], crawler["networks"])
        self.assertEqual("false", crawler["labels"]["traefik.enable"])

    def test_cassandra_remains_an_independent_official_image_lab(self):
        lab = compose("labs/cassandra.yml")
        service = lab["services"]["cassandra-node1"]
        self.assertTrue(service["image"].startswith("cassandra:"))
        self.assertEqual("hy-home-lab-cassandra", lab["name"])
        self.assertIn(
            "cassandra-node1-volume:/var/lib/cassandra:rw", service["volumes"]
        )
        self.assertIn(
            "${LAB_DATA_DIR:?set isolated LAB data root}",
            lab["volumes"]["cassandra-node1-volume"]["driver_opts"]["device"],
        )
        self.assertTrue(lab["networks"]["lab_cassandra_core_net"]["internal"])


if __name__ == "__main__":
    unittest.main()
