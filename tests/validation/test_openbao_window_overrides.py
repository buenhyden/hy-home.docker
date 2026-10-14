"""SPEC-0243 W6 scoped override and hourly logrotate drop-in contracts."""

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DROP_IN = ROOT / "infra/03-security/openbao/config/systemd/logrotate-hourly.conf"
# service: (overlay, base Compose file, CA mount target)
BASE = {
    "traefik": (
        "infra/01-gateway/traefik/compose.window-ca.override.yml",
        "infra/01-gateway/traefik/docker-compose.yml",
        "/openbao-ca/ca.pem",
    ),
    "prometheus": (
        "infra/06-observability/compose.window-ca.override.yml",
        "infra/06-observability/docker-compose.yml",
        "/etc/prometheus/openbao-ca.pem",
    ),
}
PINNED = re.compile(r"[a-z0-9./-]+:v[0-9.]+@sha256:[a-f0-9]{64}")


class WindowOverrideTests(unittest.TestCase):
    def test_each_overlay_changes_only_its_service_image(self):
        for name, (overlay, compose, target) in BASE.items():
            with self.subTest(service=name):
                model = yaml.safe_load((ROOT / overlay).read_text())
                self.assertEqual(set(model), {"x-hyhome-overlay", "services"})
                self.assertEqual(
                    model["x-hyhome-overlay"], {"version": 1, "base": compose}
                )
                self.assertEqual(set(model["services"]), {name})
                override = model["services"][name]
                self.assertEqual(set(override), {"image"})
                self.assertRegex(override["image"], PINNED)
                base = yaml.safe_load((ROOT / compose).read_text())["services"][name]
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
