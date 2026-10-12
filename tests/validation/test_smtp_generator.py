"""SMTP-only generator routing; every private input here is synthetic."""

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class SmtpGeneratorTests(unittest.TestCase):
    def synthetic_catalog_root(self, root):
        from scripts.lib.ops import secret_catalog
        from tests.lib.ops.test_secret_catalog import generation_model

        subprocess.run(["git", "init", "-q", str(root)], check=True)
        script = root / "scripts/operations/gen-secrets.sh"
        script.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "scripts/operations/gen-secrets.sh", script)
        library = root / "scripts/lib/ops"
        library.mkdir(parents=True)
        for name in (
            "smtp_contract.py",
            "retire_materials.py",
            "secret_catalog.py",
            "_secret_catalog_io.py",
        ):
            shutil.copyfile(ROOT / "scripts/lib/ops" / name, library / name)
        document = generation_model()
        metadata = secret_catalog.render_views(document)[secret_catalog.VIEW_NAMES[0]]
        for relative, raw in (
            (secret_catalog.CATALOG_PATH, json.dumps(document).encode()),
            (secret_catalog.SCHEMA_PATH, b"{}"),
            (secret_catalog.METADATA_PATH, metadata),
            (secret_catalog.SUPPORT_PATH, b"{}"),
            (".env.example", b""),
            ("labs/.env.example", b""),
        ):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        subprocess.run(
            [
                "git",
                "add",
                "--",
                secret_catalog.CATALOG_PATH,
                secret_catalog.SCHEMA_PATH,
                secret_catalog.METADATA_PATH,
                secret_catalog.SUPPORT_PATH,
                ".env.example",
                "labs/.env.example",
            ],
            cwd=root,
            check=True,
        )
        return script

    def run_with_root_replacement(self, mode, *, untrack_catalog=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            script = self.synthetic_catalog_root(root)
            if untrack_catalog:
                from scripts.lib.ops import secret_catalog

                subprocess.run(
                    [
                        "git",
                        "rm",
                        "--cached",
                        "-q",
                        "--",
                        secret_catalog.CATALOG_PATH,
                    ],
                    cwd=root,
                    check=True,
                )
            private = root / "secrets/SENSITIVE_ENV_VARS.md"
            private.write_text("synthetic-private-sentinel\n")
            env = root / ".env"
            env.write_text("SYNTHETIC_PRIVATE=keep\n")
            control = Path(directory) / "control"
            control.mkdir()
            fake_bin = Path(directory) / "bin"
            fake_bin.mkdir()
            real_bash = shutil.which("bash")
            self.assertIsNotNone(real_bash)
            fake_bash = fake_bin / "bash"
            fake_bash.write_text(
                "#!/bin/sh\n"
                'if [ "$1" = "-c" ] && [ -n "${HYHOME_TEST_READY:-}" ]; then\n'
                '  touch "$HYHOME_TEST_READY"\n'
                '  while [ ! -f "$HYHOME_TEST_CONTINUE" ]; do sleep 0.02; done\n'
                "fi\n"
                f'exec {real_bash} "$@"\n'
            )
            fake_bash.chmod(fake_bash.stat().st_mode | stat.S_IXUSR)
            ready = control / "ready"
            resume = control / "continue"
            command = [real_bash, str(script)] + ([mode] if mode else [])
            process = subprocess.Popen(
                command,
                cwd=root,
                env={
                    **os.environ,
                    "PATH": str(fake_bin)
                    + os.pathsep
                    + str(Path(sys.executable).parent)
                    + os.pathsep
                    + os.environ["PATH"],
                    "HYHOME_TEST_READY": str(ready),
                    "HYHOME_TEST_CONTINUE": str(resume),
                },
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            deadline = time.monotonic() + 5
            while not ready.exists():
                if process.poll() is not None:
                    stdout, stderr = process.communicate()
                    self.fail(
                        f"generator exited before replacement: {process.returncode} {stdout} {stderr}"
                    )
                if time.monotonic() >= deadline:
                    process.kill()
                    stdout, stderr = process.communicate()
                    self.fail(
                        f"generator did not reach catalog read: {stdout} {stderr}"
                    )
                time.sleep(0.01)
            displaced = root.with_name("repo-displaced")
            root.rename(displaced)
            root.mkdir()
            (root / "secrets").mkdir()
            resume.touch()
            stdout, stderr = process.communicate(timeout=20)
            self.assertNotIn("synthetic-private-sentinel", stdout + stderr)
            self.assertFalse((root / "secrets/db/example/password.txt").exists())
            self.assertFalse((root / "secrets/SENSITIVE_ENV_VARS.md").exists())
            self.assertFalse((root / ".env").exists())
            if untrack_catalog:
                self.assertEqual(2, process.returncode, stdout + stderr)
                self.assertFalse(
                    (displaced / "secrets/db/example/password.txt").exists()
                )
            elif process.returncode == 0:
                if mode:
                    self.assertTrue(
                        (displaced / "secrets/SENSITIVE_ENV_VARS.md").exists()
                    )
                else:
                    self.assertTrue(
                        (displaced / "secrets/db/example/password.txt").exists()
                    )
            else:
                self.assertEqual(2, process.returncode, stdout + stderr)

    def test_run_generation_root_replacement_does_not_mutate_replacement(self):
        self.run_with_root_replacement("")

    def test_sync_metadata_root_replacement_does_not_mutate_replacement(self):
        self.run_with_root_replacement("--sync-metadata")

    def test_prune_metadata_root_replacement_does_not_mutate_replacement(self):
        self.run_with_root_replacement("--sync-metadata-prune")

    def test_run_generation_untracked_catalog_rejects_after_root_replacement(self):
        self.run_with_root_replacement("", untrack_catalog=True)

    def test_sync_metadata_untracked_catalog_rejects_after_root_replacement(self):
        self.run_with_root_replacement("--sync-metadata", untrack_catalog=True)

    def test_prune_metadata_untracked_catalog_rejects_after_root_replacement(self):
        self.run_with_root_replacement("--sync-metadata-prune", untrack_catalog=True)

    def test_retirement_check_uses_helper_without_touching_other_domains(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "scripts/operations/gen-secrets.sh"
            destination.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "scripts/operations/gen-secrets.sh", destination)
            library = root / "scripts/lib/ops/smtp_contract.py"
            library.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "scripts/lib/ops/smtp_contract.py", library)
            shutil.copyfile(
                ROOT / "scripts/lib/ops/retire_materials.py",
                library.parent / "retire_materials.py",
            )
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
                "retire_materials.py",
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
