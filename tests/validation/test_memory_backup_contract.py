"""Registered mutation entrypoints use host memory-capacity admission."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESTIC = ROOT / "infra/09-platform-ops/restic"


class BackupContractTests(unittest.TestCase):
    def test_generic_local_cmd_refuses_backup_before_restic(self):
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "restic"
            executable.write_text("#!/bin/sh\necho unexpected-restic\n")
            executable.chmod(0o700)
            result = subprocess.run(
                ["sh", str(RESTIC / "backup.sh"), "cmd", "state", "backup", "/fixture"],
                capture_output=True,
                text=True,
                env={**os.environ, "PATH": directory + ":" + os.environ["PATH"]},
                check=False,
            )
            self.assertEqual(result.returncode, 64)
            self.assertNotIn("unexpected-restic", result.stdout)

    def test_direct_backup_refuses_missing_admission(self):
        result = subprocess.run(
            ["sh", str(RESTIC / "backup.sh"), "backup"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 64)
        self.assertIn("backup-run", result.stderr)

    def test_internal_backup_refuses_forged_digest(self):
        result = subprocess.run(
            ["sh", str(RESTIC / "backup.sh"), "budget-backup"],
            input="forged\n",
            capture_output=True,
            text=True,
            env={**os.environ, "HYHOME_MEMORY_ADMISSION_SHA256": "0" * 64},
            check=False,
        )
        self.assertEqual(result.returncode, 64)

    def test_daily_local_and_offsite_mutations_use_same_host_cli(self):
        script = (RESTIC / "bin/hyhome-backup.sh").read_text()
        self.assertIn("backup-run --target state", script)
        self.assertIn("backup-run --target offsite", script)
        self.assertNotIn('"${compose[@]}" run --rm --no-deps restic backup', script)
        self.assertIn("offsite_repo_bytes", script)


if __name__ == "__main__":
    unittest.main()
