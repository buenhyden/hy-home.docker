"""Value-preserving metadata synchronization through the public shell entrypoint."""

import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/operations/gen-secrets.sh"


class SecretMetadataSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "secrets").mkdir()
        self.example = self.root / "secrets/SENSITIVE_ENV_VARS.md.example"
        self.target = self.root / "secrets/SENSITIVE_ENV_VARS.md"
        self.example.write_text(
            "| **TEST-001** | `X` | `PW` | `(empty)` | `NEW_KEY` | `secrets/test.txt` | 2026-01-01 | New purpose |\n"
        )
        self.private = "| **TEST-001** | `O` | `PW` | `synthetic-private-value` | `OLD_KEY` | `secrets/old.txt` | 2025-01-01 | Old purpose |\n"
        self.target.write_text(self.private)
        (self.root / ".env.example").write_text("EXISTING=public\nADDED=default\n")
        (self.root / ".env").write_text(
            "# operator comment\nEXISTING=synthetic-private-env\nUNKNOWN=keep\n"
        )

    def run_mode(self, mode="--sync-metadata"):
        result = subprocess.run(
            ["bash", str(SCRIPT), mode],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotIn("synthetic-private", result.stdout + result.stderr)
        return result

    def test_preserves_values_dates_unknown_rows_and_env_bytes(self):
        unknown = "| **LOCAL-001** | `X` | `PW` | `synthetic-private-local` | `-` | | 2025-01-01 | Local |\n"
        self.target.write_text(self.private + unknown)
        result = self.run_mode()
        self.assertEqual(0, result.returncode, result.stderr)
        text = self.target.read_text()
        self.assertIn("`synthetic-private-value`", text)
        self.assertIn("2025-01-01", text)
        self.assertIn(unknown, text)
        self.assertIn("`NEW_KEY`", text)
        self.assertEqual(
            "# operator comment\nEXISTING=synthetic-private-env\nUNKNOWN=keep\nADDED=default\n",
            (self.root / ".env").read_text(),
        )
        self.assertFalse((self.root / "secrets/test.txt").exists())
        self.assertEqual(0, self.run_mode().returncode)

    def test_check_reports_drift_without_writes(self):
        before = self.target.read_bytes()
        result = self.run_mode("--sync-metadata-check")
        self.assertEqual(1, result.returncode)
        self.assertEqual(before, self.target.read_bytes())
        self.assertEqual(0, self.run_mode().returncode)
        self.assertEqual(0, self.run_mode("--sync-metadata-check").returncode)

    def test_rejects_traversal_without_any_writes(self):
        self.example.write_text(
            self.example.read_text().replace("secrets/test.txt", "secrets/../../escape")
        )
        before = self.target.read_bytes()
        self.assertEqual(2, self.run_mode().returncode)
        self.assertEqual(before, self.target.read_bytes())
        self.assertNotIn("ADDED=", (self.root / ".env").read_text())

    def test_rejects_symlink_target(self):
        outside = self.root / "outside"
        outside.write_text(self.private)
        self.target.unlink()
        self.target.symlink_to(outside)
        self.assertEqual(2, self.run_mode().returncode)
        self.assertEqual(self.private, outside.read_text())

    def test_rejects_duplicate_public_identity(self):
        self.example.write_text(self.example.read_text() * 2)
        self.assertEqual(2, self.run_mode().returncode)
        self.assertEqual(self.private, self.target.read_text())

    def test_rejects_unparseable_value_without_exposure(self):
        body = self.private.replace(
            "synthetic-private-value", "synthetic-private|ambiguous"
        )
        self.target.write_text(body)
        self.assertEqual(2, self.run_mode().returncode)
        self.assertEqual(body, self.target.read_text())

    def test_new_registry_and_env_use_public_placeholders_only(self):
        self.target.unlink()
        (self.root / ".env").unlink()
        self.assertEqual(0, self.run_mode().returncode)
        self.assertEqual(self.example.read_bytes(), self.target.read_bytes())
        self.assertEqual(0o600, self.target.stat().st_mode & 0o777)


class PublicSecretSchemaTests(unittest.TestCase):
    def test_public_ids_paths_and_env_keys_have_unique_owners(self):
        import re
        from collections import Counter

        import yaml

        root = SCRIPT.parents[2]
        text = (root / "secrets/SENSITIVE_ENV_VARS.md.example").read_text()
        rows = []
        for line in text.splitlines():
            cells = [cell.strip().strip("*`").strip() for cell in line.split("|")]
            if len(cells) == 10 and re.fullmatch(r"[A-Z][A-Z0-9_-]*-[0-9]+", cells[1]):
                rows.append(cells)
        for column in (1, 5, 6):
            counts = Counter(
                row[column] for row in rows if row[column] not in ("", "-")
            )
            self.assertEqual([], [name for name, count in counts.items() if count > 1])
        declarations = yaml.safe_load((root / "docker-compose.yml").read_text())[
            "secrets"
        ]
        expected = {
            value["file"].removeprefix("./")
            for value in declarations.values()
            if "file" in value
        }
        self.assertFalse(expected - {row[6] for row in rows})
        keys = re.findall(
            r"^([A-Za-z_][A-Za-z0-9_]*)=", (root / ".env.example").read_text(), re.M
        )
        self.assertEqual(len(keys), len(set(keys)))
        self.assertFalse(
            {row[5] for row in rows if row[5] not in ("", "-")} - set(keys)
        )
