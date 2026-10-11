"""SMTP-only generator routing; every private input here is synthetic."""

import json
import os
import shutil
import subprocess
import sys
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
        from scripts.lib.ops import secret_catalog
        from tests.lib.ops.test_secret_catalog import model as synthetic_catalog_model

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            script = root / "scripts/operations/gen-secrets.sh"
            script.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "scripts/operations/gen-secrets.sh", script)
            library = root / "scripts/lib/ops"
            library.mkdir(parents=True)
            for name in (
                "smtp_contract.py",
                "secret_catalog.py",
                "_secret_catalog_io.py",
            ):
                shutil.copyfile(ROOT / "scripts/lib/ops" / name, library / name)
            document = synthetic_catalog_model()
            metadata = secret_catalog.render_views(document)[
                secret_catalog.VIEW_NAMES[0]
            ]
            for relative, raw in (
                (secret_catalog.CATALOG_PATH, json.dumps(document).encode()),
                (
                    secret_catalog.SCHEMA_PATH,
                    (ROOT / secret_catalog.SCHEMA_PATH).read_bytes(),
                ),
                (secret_catalog.METADATA_PATH, metadata),
                (secret_catalog.SUPPORT_PATH, b"{}"),
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            subprocess.run(
                [
                    "git",
                    "add",
                    "--",
                    secret_catalog.CATALOG_PATH,
                    secret_catalog.SCHEMA_PATH,
                    secret_catalog.METADATA_PATH,
                    secret_catalog.SUPPORT_PATH,
                ],
                cwd=root,
                check=True,
            )
            # Metadata-only mode must not inspect these private synthetic inputs.
            private = root / "secrets/SENSITIVE_ENV_VARS.md"
            private.write_text("synthetic-private-sentinel\n")
            env = root / ".env"
            env.write_text("synthetic-private-dotenv-sentinel\n")
            before = private.read_bytes(), env.read_bytes()
            result = subprocess.run(
                ["bash", str(script), "--dry-run"],
                cwd=root,
                env={
                    **os.environ,
                    "PATH": str(Path(sys.executable).parent)
                    + os.pathsep
                    + os.environ["PATH"],
                },
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertNotIn("supabase_smtp_password.txt", result.stdout)
            self.assertNotIn("id=COMM-003", result.stdout)
            self.assertNotIn("id=Retired ID", result.stdout)
            self.assertNotIn("synthetic-private", result.stdout + result.stderr)
            self.assertEqual(before, (private.read_bytes(), env.read_bytes()))
            self.assertFalse(
                (root / "secrets/communication/smtp/smtp_password.txt").exists()
            )


if __name__ == "__main__":
    unittest.main()
