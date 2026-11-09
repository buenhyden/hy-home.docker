"""ADR-0062 decision 10: no per-app dedicated Valkey broker or exporter remains."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REMOVED_SERVICES = {
    "infra/07-workflow/airflow/docker-compose.yml": "airflow-valkey",
    "infra/07-workflow/n8n/docker-compose.yml": "n8n-valkey",
    "infra/02-auth/oauth2-proxy/docker-compose.yml": "oauth2-proxy-valkey",
}
REMOVED_OVERLAYS = (
    "infra/07-workflow/airflow/docker-compose.monitor-acl.yml",
    "infra/07-workflow/n8n/docker-compose.monitor-acl.yml",
    "infra/02-auth/oauth2-proxy/docker-compose.monitor-acl.yml",
)
REMOVED_SECRETS = {
    "airflow_valkey_password",
    "airflow_valkey_monitor_password",
    "n8n_valkey_password",
    "n8n_valkey_monitor_password",
    "oauth2_valkey_monitor_password",
}


class DedicatedValkeyRemovalTests(unittest.TestCase):
    def test_leaf_compose_files_declare_no_dedicated_broker_or_exporter(self) -> None:
        for relative_path, broker in REMOVED_SERVICES.items():
            with self.subTest(service=broker):
                document = yaml.safe_load((ROOT / relative_path).read_text())
                services = document["services"]
                self.assertNotIn(broker, services)
                self.assertNotIn(broker + "-exporter", services)
                volumes = document.get("volumes") or {}
                self.assertNotIn(broker + "-data", volumes)
                self.assertNotIn("dedicated-valkey", str(document))

    def test_monitor_overlays_and_dedicated_secrets_are_gone(self) -> None:
        for relative_path in REMOVED_OVERLAYS:
            self.assertFalse((ROOT / relative_path).exists(), relative_path)
        root = yaml.safe_load((ROOT / "docker-compose.yml").read_text())
        self.assertEqual(set(), REMOVED_SECRETS & set(root["secrets"]))

    def test_apps_keep_the_shared_management_valkey(self) -> None:
        for relative_path in (
            "infra/07-workflow/airflow/docker-compose.yml",
            "infra/07-workflow/n8n/docker-compose.yml",
            "infra/02-auth/oauth2-proxy/docker-compose.yml",
        ):
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text()
                self.assertIn("mng-valkey", text)
                self.assertIn("mng_valkey_password", text)


if __name__ == "__main__":
    unittest.main()
