"""The operator scripts stay site-neutral and feed the unit what it reads."""

import re
import subprocess
import unittest
from pathlib import Path

WORKLOAD = Path(__file__).resolve().parents[1]
DEPLOY = WORKLOAD / "deploy"
SCRIPTS = ("install-attester.sh", "update-hermes-plugin.sh")


class DeployScriptTests(unittest.TestCase):
    def test_scripts_parse(self):
        for name in SCRIPTS:
            result = subprocess.run(
                ["bash", "-n", str(DEPLOY / name)], capture_output=True, check=False
            )
            self.assertEqual(0, result.returncode, (name, result.stderr))

    def test_scripts_carry_no_site_values(self):
        for name in SCRIPTS:
            text = (DEPLOY / name).read_text()
            self.assertNotIn("/home/", text, name)
            self.assertIsNone(re.search(r"\b\d{1,3}(\.\d{1,3}){3}\b", text), name)
            self.assertNotIn("hy.home.arpa", text, name)

    def test_environment_file_holds_what_the_attester_reads(self):
        unit = (DEPLOY / "hermes-attester.service").read_text()
        install = (DEPLOY / "install-attester.sh").read_text()
        fetch = (WORKLOAD / "publisher/source_fetch.py").read_text()
        (printf,) = re.findall(r"printf '([^']*)'.*environment\.new", install, re.S)
        written = set(re.findall(r"([A-Z_]+)=", printf))
        read = set(re.findall(r"\$\{([A-Z_]+)\}", unit))
        read |= set(re.findall(r'os\.environ\.get\("([A-Z_]+)"', fetch))
        self.assertEqual(read, written)
        self.assertIn("EnvironmentFile=/etc/hermes-attester/environment", unit)
        self.assertIn("/etc/hermes-attester/environment.new", install)

    def test_failed_install_stops_the_timer(self):
        install = (DEPLOY / "install-attester.sh").read_text()
        failure = install.split("else", 1)[1]
        self.assertIn("systemctl disable --now hermes-attester.timer", failure)


if __name__ == "__main__":
    unittest.main()
