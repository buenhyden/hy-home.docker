"""Each installer role ships a module set that actually imports and runs."""

import configparser
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

WORKLOAD = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install", WORKLOAD / "install.py")
install = importlib.util.module_from_spec(spec)
spec.loader.exec_module(install)

ATTESTER_ONLY = {"attestation", "attester", "source_check", "source_fetch"}


def release(role):
    """A directory holding exactly the files the installer ships for a role."""
    root = Path(tempfile.mkdtemp())
    for name in install.role_files(role):
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(WORKLOAD / name, target)
    return root


def run(root, code):
    return subprocess.run(
        [sys.executable, "-I", "-c", f"import sys; sys.path.insert(0, {str(root)!r}); {code}"],
        capture_output=True,
        check=False,
        text=True,
    )  # fmt: skip


class ReleaseRoleTests(unittest.TestCase):
    def test_publisher_role_keeps_signing_and_fetching_out(self):
        shipped = {Path(n).stem for n in install.role_files("publisher")}
        self.assertFalse(shipped & ATTESTER_ONLY)

    def test_attester_role_adds_only_the_attester_modules(self):
        publisher = install.role_files("publisher")
        attester = install.role_files("attester")
        self.assertEqual(
            {f"publisher/{m}.py" for m in ATTESTER_ONLY}, attester - publisher
        )

    def test_default_prefix_per_role(self):
        self.assertEqual(Path("/opt/hermes-publisher"), install.PREFIX["publisher"])
        self.assertEqual(Path("/opt/hermes-attester"), install.PREFIX["attester"])

    def test_publisher_release_imports_its_cli(self):
        root = release("publisher")
        self.addCleanup(shutil.rmtree, root)
        result = run(root, "import publisher.cli")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_publisher_release_refuses_attest_queue_without_traceback(self):
        root = release("publisher")
        self.addCleanup(shutil.rmtree, root)
        result = run(
            root,
            "import publisher.cli as c; raise SystemExit(c.main(["
            "'attest-queue', '--gateway', 'https://g.example', '--auth-header-file', 'a',"
            " '--signing-key', 'k', '--key-id', 'x', '--state-dir', 's',"
            " '--evidence-dir', 'e']))",
        )
        self.assertNotEqual(0, result.returncode)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("operation_rejected", result.stdout)

    def test_attester_release_offers_attest_queue(self):
        root = release("attester")
        self.addCleanup(shutil.rmtree, root)
        result = run(
            root, "import publisher.cli as c; c.main(['attest-queue', '--help'])"
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("--signing-key", result.stdout)

    def test_service_unit_runs_the_attester_release(self):
        unit = configparser.ConfigParser(strict=False, interpolation=None)
        unit.optionxform = str
        unit.read(WORKLOAD / "deploy/hermes-attester.service")
        self.assertTrue(
            unit["Service"]["ExecStart"].startswith(
                "/opt/hermes-attester/current/venv/bin/python -I -m publisher.cli"
            )
        )


if __name__ == "__main__":
    unittest.main()
