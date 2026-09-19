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

    def test_preserving_mode_keeps_unparsed_environment_lines(self):
        env_text = "# operator comment\nsource local-overrides.env\nEXISTING=synthetic-private-env\n"
        (self.root / ".env").write_text(env_text)

        result = self.run_mode()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(env_text + "ADDED=default\n", (self.root / ".env").read_text())

    def test_prune_makes_public_and_private_key_sets_exact(self):
        self.example.write_text(
            self.example.read_text()
            + "| **TEST-002** | `O` | `PW` | `(empty)` | `ADDED` | `secrets/added.txt` | 2026-01-02 | Added purpose |\n"
        )
        unknown = (
            "| **LOCAL-001** | `X` | `PW` | `synthetic-private-local` | "
            "`UNKNOWN` | `secrets/local.txt` | 2025-01-03 | Local purpose |\n"
        )
        self.target.write_text("# registry comment\n" + self.private + unknown)
        secret_file = self.root / "secrets/local.txt"
        secret_file.write_text("synthetic-secret-file")
        before_retained = self.private.split("|")
        before_env_line = "EXISTING=synthetic-private-env\n"

        result = self.run_mode("--sync-metadata-prune")

        self.assertEqual(0, result.returncode, result.stderr)
        env_text = (self.root / ".env").read_text()
        self.assertEqual(
            "# operator comment\n" + before_env_line + "ADDED=default\n",
            env_text,
        )
        self.assertEqual(
            {"EXISTING", "ADDED"},
            {
                line.split("=", 1)[0]
                for line in env_text.splitlines()
                if line and not line.startswith("#")
            },
        )
        registry = self.target.read_text()
        self.assertIn("# registry comment\n", registry)
        self.assertNotIn("LOCAL-001", registry)
        rows = [
            line.split("|") for line in registry.splitlines() if line.startswith("| **")
        ]
        self.assertEqual({"TEST-001", "TEST-002"}, {row[1].strip("* ") for row in rows})
        retained = next(row for row in rows if "TEST-001" in row[1])
        self.assertEqual(before_retained[4], retained[4])
        self.assertEqual(before_retained[7], retained[7])
        self.assertEqual("NEW_KEY", retained[5].strip(" `"))
        self.assertTrue(secret_file.is_file())
        self.assertEqual("synthetic-secret-file", secret_file.read_text())

        env_before = (self.root / ".env").read_bytes()
        registry_before = self.target.read_bytes()
        self.assertEqual(0, self.run_mode("--sync-metadata-prune-check").returncode)
        self.assertEqual(0, self.run_mode("--sync-metadata-prune").returncode)
        self.assertEqual(env_before, (self.root / ".env").read_bytes())
        self.assertEqual(registry_before, self.target.read_bytes())

    def test_prune_check_reports_exact_set_drift_without_writes(self):
        registry_before = self.target.read_bytes()
        env_before = (self.root / ".env").read_bytes()

        result = self.run_mode("--sync-metadata-prune-check")

        self.assertEqual(1, result.returncode)
        self.assertEqual(registry_before, self.target.read_bytes())
        self.assertEqual(env_before, (self.root / ".env").read_bytes())
        self.assertEqual(0, self.run_mode("--sync-metadata-prune").returncode)
        self.assertEqual(0, self.run_mode("--sync-metadata-prune-check").returncode)

    def test_prune_rejects_multiline_environment_forms_before_any_write(self):
        cases = (
            'EXISTING="synthetic-private\ncontinued"\nUNKNOWN=keep\n',
            "EXISTING=synthetic-private\\\ncontinued\nUNKNOWN=keep\n",
        )
        for env_text in cases:
            with self.subTest(env_text=repr(env_text)):
                (self.root / ".env").write_text(env_text)
                registry_before = self.target.read_bytes()
                env_before = (self.root / ".env").read_bytes()

                result = self.run_mode("--sync-metadata-prune")

                self.assertEqual(2, result.returncode)
                self.assertEqual(registry_before, self.target.read_bytes())
                self.assertEqual(env_before, (self.root / ".env").read_bytes())

    def test_prune_rejects_duplicate_environment_key_before_any_write(self):
        (self.root / ".env.example").write_text(
            "EXISTING=public\nADDED=default\nEXISTING=duplicate\n"
        )
        registry_before = self.target.read_bytes()
        env_before = (self.root / ".env").read_bytes()

        result = self.run_mode("--sync-metadata-prune")

        self.assertEqual(2, result.returncode)
        self.assertEqual(registry_before, self.target.read_bytes())
        self.assertEqual(env_before, (self.root / ".env").read_bytes())

    def test_prune_rejects_malformed_registry_row_before_any_write(self):
        self.target.write_text(
            self.private
            + "| BROKEN | `X` | `PW` | `(empty)` | `-` | `-` | 2025-01-01 | Bad |\n"
        )
        registry_before = self.target.read_bytes()
        env_before = (self.root / ".env").read_bytes()

        result = self.run_mode("--sync-metadata-prune")

        self.assertEqual(2, result.returncode)
        self.assertEqual(registry_before, self.target.read_bytes())
        self.assertEqual(env_before, (self.root / ".env").read_bytes())

    def test_prune_rejects_symlink_source_before_any_write(self):
        outside = self.root / "outside-env-example"
        outside.write_text("EXISTING=public\nADDED=default\n")
        (self.root / ".env.example").unlink()
        (self.root / ".env.example").symlink_to(outside)
        registry_before = self.target.read_bytes()
        env_before = (self.root / ".env").read_bytes()

        result = self.run_mode("--sync-metadata-prune")

        self.assertEqual(2, result.returncode)
        self.assertEqual(registry_before, self.target.read_bytes())
        self.assertEqual(env_before, (self.root / ".env").read_bytes())


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
