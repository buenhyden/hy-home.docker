"""SMTP-only generator routing; every private input here is synthetic."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class SmtpGeneratorTests(unittest.TestCase):
    def test_retirement_check_uses_helper_without_touching_other_domains(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "scripts/operations/gen-secrets.sh"
            destination.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "scripts/operations/gen-secrets.sh", destination)
            library = root / "scripts/lib/ops/smtp_contract.py"
            library.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "scripts/lib/ops/smtp_contract.py", library)
            canonical = root / "secrets/communication/smtp/smtp_password.txt"
            canonical.parent.mkdir(parents=True)
            canonical.write_text("synthetic-password")
            old = root / "secrets/communication/supabase/supabase_smtp_password.txt"
            old.parent.mkdir(parents=True)
            old.write_text("synthetic-password")
            metadata = root / "secrets/SENSITIVE_ENV_VARS.md"
            metadata.write_text(
                "| COMM-002 | X | PW | private-fixture | - | "
                "secrets/communication/smtp/smtp_password.txt | date | purpose |\n"
                "| COMM-003 | X | PW | private-fixture | - | "
                "secrets/communication/supabase/supabase_smtp_password.txt | date | purpose |\n"
            )
            (root / ".env").write_text("operator-untouched\n")
            (root / "labs").mkdir()
            (root / "labs/.env").write_text("lab-untouched\n")
            tracked = [canonical, old, metadata, root / ".env", root / "labs/.env"]
            before = [path.read_bytes() for path in tracked]
            result = subprocess.run(
                ["bash", str(destination), "--retire-supabase-smtp-check"],
                cwd=root,
                env={"PATH": os.environ["PATH"]},
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn('"status": "pending"', result.stdout)
            for sentinel in (
                "synthetic-password",
                "private-fixture",
                "operator-untouched",
                "lab-untouched",
            ):
                self.assertNotIn(sentinel, result.stdout + result.stderr)
            self.assertEqual(before, [path.read_bytes() for path in tracked])

    def test_dry_run_never_generates_retired_value_owner(self):
        result = subprocess.run(
            ["bash", "scripts/operations/gen-secrets.sh", "--dry-run"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(0, result.returncode)
        self.assertNotIn("supabase_smtp_password.txt", result.stdout)
        self.assertNotIn("id=COMM-003", result.stdout)
        self.assertNotIn("id=Retired ID", result.stdout)


if __name__ == "__main__":
    unittest.main()
