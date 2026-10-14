"""SPEC-0243 W6 scoped override and hourly logrotate drop-in contracts."""

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OVERRIDE = ROOT / "infra/03-security/openbao/window/compose.window-ca.override.yml"
DROP_IN = ROOT / "infra/03-security/openbao/config/logrotate/logrotate-hourly.conf"
BASE = {
    "traefik": (
        ROOT / "infra/01-gateway/traefik/docker-compose.yml",
        "/openbao-ca/ca.pem",
    ),
    "prometheus": (
        ROOT / "infra/06-observability/docker-compose.yml",
        "/etc/prometheus/openbao-ca.pem",
    ),
}
PINNED = re.compile(r"[a-z0-9./-]+:v[0-9.]+@sha256:[a-f0-9]{64}")


class WindowOverrideTests(unittest.TestCase):
    def test_override_changes_only_the_image_of_two_services(self):
        services = yaml.safe_load(OVERRIDE.read_text())
        self.assertEqual(set(services), {"services"})
        self.assertEqual(set(services["services"]), set(BASE))
        for name, (compose, target) in BASE.items():
            with self.subTest(service=name):
                override = services["services"][name]
                self.assertEqual(set(override), {"image"})
                self.assertRegex(override["image"], PINNED)
                base = yaml.safe_load(compose.read_text())["services"][name]
                # The pin keeps the running image, which differs from Compose's.
                self.assertNotEqual(override["image"], base["image"])
                self.assertEqual(
                    override["image"].split(":")[0], base["image"].split(":")[0]
                )
                # Recreating deploys the CA mount the base already declares.
                self.assertIn(
                    target,
                    [v.get("target") for v in base["volumes"] if isinstance(v, dict)],
                )

    def test_drop_in_only_reschedules_the_shared_logrotate_timer(self):
        lines = [
            line
            for line in DROP_IN.read_text().splitlines()
            if line and not line.startswith("#")
        ]
        self.assertEqual(
            lines, ["[Timer]", "OnCalendar=", "OnCalendar=hourly", "AccuracySec=5m"]
        )


if __name__ == "__main__":
    unittest.main()
