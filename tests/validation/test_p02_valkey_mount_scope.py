"""Least-privilege script mounts for the three P02 dedicated Valkey brokers."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
VALKEY_SCRIPTS = ROOT / "infra/04-data/mng-db/valkey/scripts"
RUNTIME_SCRIPTS = Path("/usr/local/lib/hy-home/valkey")


def _strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for child in value for item in _strings(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in _strings(child)]
    return []


class DedicatedValkeyMountScopeTests(unittest.TestCase):
    cases = (
        (
            "infra/07-workflow/airflow/docker-compose.yml",
            "airflow-valkey",
            "airflow_valkey_password",
        ),
        (
            "infra/07-workflow/n8n/docker-compose.yml",
            "n8n-valkey",
            "n8n_valkey_password",
        ),
        (
            "infra/02-auth/oauth2-proxy/docker-compose.yml",
            "oauth2-proxy-valkey",
            "oauth2_valkey_password",
        ),
    )

    def test_brokers_mount_only_the_two_required_scripts_and_app_secret(self) -> None:
        expected_mounts = {
            (
                (VALKEY_SCRIPTS / name).resolve(),
                RUNTIME_SCRIPTS / name,
                "ro",
            )
            for name in ("start-dedicated.sh", "render-monitor-acl.sh")
        }
        for relative_path, service_name, app_secret in self.cases:
            with self.subTest(service=service_name):
                path = ROOT / relative_path
                service = yaml.safe_load(path.read_text())["services"][service_name]
                script_mounts = set()
                for volume in service["volumes"]:
                    source, target, *options = volume.split(":")
                    target_path = Path(target)
                    if (
                        target_path == RUNTIME_SCRIPTS
                        or RUNTIME_SCRIPTS in target_path.parents
                    ):
                        script_mounts.add(
                            (
                                (path.parent / source).resolve(),
                                target_path,
                                ",".join(options),
                            )
                        )
                self.assertEqual(expected_mounts, script_mounts)
                self.assertNotIn(
                    VALKEY_SCRIPTS.resolve(),
                    {source for source, _, _ in script_mounts},
                )
                self.assertNotIn(
                    RUNTIME_SCRIPTS / "start.sh",
                    {target for _, target, _ in script_mounts},
                )

                declared = {
                    item if isinstance(item, str) else item["source"]
                    for item in service["secrets"]
                }
                self.assertEqual({app_secret}, declared)
                references = {
                    match
                    for value in _strings(service)
                    for match in re.findall(r"/run/secrets/([A-Za-z0-9_]+)", value)
                }
                self.assertEqual({app_secret}, references)


if __name__ == "__main__":
    unittest.main()
