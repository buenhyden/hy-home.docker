"""The attester systemd units carry the hardening and flags, and no secrets."""

import configparser
import unittest
from pathlib import Path

DEPLOY = Path(__file__).resolve().parents[1] / "deploy"


def parse(name):
    parser = configparser.ConfigParser(strict=False, interpolation=None)
    parser.optionxform = str
    text = (DEPLOY / name).read_text(encoding="utf-8")
    parser.read_string(text)
    return parser, text


class DeployUnitTests(unittest.TestCase):
    def test_service_is_hardened_and_least_privilege(self):
        unit, _ = parse("hermes-attester.service")
        service = unit["Service"]
        for key, value in {
            "Type": "oneshot",
            "User": "hermes-attester",
            "Group": "hermes-attester",
            "NoNewPrivileges": "yes",
            "ProtectSystem": "strict",
            "ProtectHome": "yes",
            "PrivateTmp": "yes",
            "PrivateDevices": "yes",
            "RestrictAddressFamilies": "AF_INET AF_INET6 AF_UNIX",
            "StateDirectory": "hermes-attester/state hermes-attester/evidence",
            "StateDirectoryMode": "0700",
            "CapabilityBoundingSet": "",
            "ProtectKernelTunables": "yes",
            "ProtectKernelModules": "yes",
            "ProtectControlGroups": "yes",
            "UMask": "0077",
        }.items():
            self.assertEqual(value, service[key], key)

    def test_exec_start_runs_the_isolated_attester(self):
        unit, _ = parse("hermes-attester.service")
        argv = unit["Service"]["ExecStart"].split()
        self.assertTrue(argv[0].endswith("/venv/bin/python"))
        self.assertEqual(["-I", "-m", "publisher.cli", "attest-queue"], argv[1:5])
        flags = dict(zip(argv[5::2], argv[6::2], strict=True))
        self.assertEqual(
            {
                "--gateway": "${HERMES_GATEWAY_URL}",
                "--auth-header-file": "/etc/hermes-attester/auth-header",
                "--signing-key": "/etc/hermes-attester/signing-key",
                "--key-id": "hermes-attester-1",
                "--state-dir": "/var/lib/hermes-attester/state",
                "--evidence-dir": "/var/lib/hermes-attester/evidence",
            },
            flags,
        )

    def test_site_values_come_from_a_required_environment_file(self):
        # No "-" prefix: a missing file stops the unit instead of running blind.
        unit, _ = parse("hermes-attester.service")
        self.assertEqual(
            "/etc/hermes-attester/environment", unit["Service"]["EnvironmentFile"]
        )

    def test_timer_runs_every_five_minutes(self):
        unit, _ = parse("hermes-attester.timer")
        self.assertEqual("2min", unit["Timer"]["OnBootSec"])
        self.assertEqual("5min", unit["Timer"]["OnUnitActiveSec"])
        self.assertNotIn("Persistent", unit["Timer"])
        self.assertEqual("timers.target", unit["Install"]["WantedBy"])

    def test_no_secret_value_in_units(self):
        for name in ("hermes-attester.service", "hermes-attester.timer"):
            _, text = parse(name)
            for marker in ("Bearer ", "PRIVATE KEY", "Authorization:", "Environment="):
                self.assertNotIn(marker, text, name)


if __name__ == "__main__":
    unittest.main()
