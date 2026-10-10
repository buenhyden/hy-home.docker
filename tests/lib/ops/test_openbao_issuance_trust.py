"""Offline trusted installer, receipt and interrupted-write regressions."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from .test_openbao_issuance import BASE, REV, WHEN, FakeAPI, M


class TrustedInstallTests(unittest.TestCase):
    def test_exact_committed_blobs_atomically_installed_without_overwrite(self):
        import hashlib

        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            repo = parent / "repo"
            repo.mkdir()
            source = repo / "infra/03-security/openbao/scripts"
            source.mkdir(parents=True)
            for name in (
                "issue-renderer-secret-id.sh",
                "renderer-issuance.py",
                "install-renderer-issuer.sh",
            ):
                (source / name).write_bytes((BASE / "scripts" / name).read_bytes())

            def git(*args):
                return subprocess.run(
                    ["/usr/bin/git", "-C", str(repo), *args],
                    check=True,
                    capture_output=True,
                ).stdout

            git("init", "--quiet")
            git("add", ".")
            git(
                "-c",
                "user.name=SEC01 synthetic fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "test: committed public helper fixture",
            )
            revision = git("rev-parse", "HEAD").decode().strip()
            target = parent / "reviewed-install"
            installer = parent / "approved-installer.sh"
            installer.write_bytes(
                git(
                    "show",
                    revision
                    + ":infra/03-security/openbao/scripts/install-renderer-issuer.sh",
                )
            )
            installer.chmod(0o400)
            marker = parent / "malicious-installer-executed"
            (source / "install-renderer-issuer.sh").write_text(
                "#!/bin/sh\ntouch " + str(marker) + "\nexit 1\n"
            )

            def run(target_path, rev=revision):
                return subprocess.run(
                    ["sh", str(installer), str(repo), rev, str(target_path)],
                    capture_output=True,
                    timeout=20,
                    check=False,
                )

            # Dirty source changes are deliberately excluded from the installed artifact.
            (source / "renderer-issuance.py").write_text("unreviewed working tree code")
            done = run(target)
            self.assertEqual(0, done.returncode)
            self.assertFalse(marker.exists())
            self.assertEqual(b"", done.stdout)
            self.assertEqual(b"", done.stderr)
            receipt = json.loads((target / "source-receipt.json").read_text())
            self.assertEqual(revision, receipt["source_revision"])
            for name, mode in (
                ("issue-renderer-secret-id.sh", 0o500),
                ("renderer-issuance.py", 0o400),
            ):
                blob = git(
                    "show", revision + ":infra/03-security/openbao/scripts/" + name
                )
                self.assertEqual(blob, (target / name).read_bytes())
                self.assertEqual(mode, (target / name).stat().st_mode & 0o777)
                self.assertEqual(
                    hashlib.sha256(blob).hexdigest(), receipt["sha256"][name]
                )
            self.assertNotEqual(0, run(target).returncode)
            unknown = parent / "unknown"
            unknown.mkdir(mode=0o700)
            self.assertNotEqual(0, run(unknown).returncode)
            self.assertEqual([], list(unknown.iterdir()))
            alias = parent / "alias"
            alias.symlink_to(unknown)
            self.assertNotEqual(0, run(alias).returncode)
            self.assertNotEqual(0, run(parent / "bad-revision", "bad").returncode)
            self.assertFalse((parent / "bad-revision").exists())
            public_parent = parent / "public"
            public_parent.mkdir(mode=0o755)
            self.assertNotEqual(0, run(public_parent / "unsafe-install").returncode)
            self.assertFalse((public_parent / "unsafe-install").exists())


class InterruptedAtomicUpdateTests(unittest.TestCase):
    def test_partial_write_blocks_even_with_an_older_valid_journal(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            journal.save(M.Record("1" * 32, M.utc(WHEN), M.ROLE, REV, M.MANIFEST))
            (Path(directory) / "issuance.json.pending").write_text("{")
            api = FakeAPI()
            with self.assertRaises(M.Blocked):
                M.run_issuance(api, journal, revision=REV)
            self.assertNotIn("issue", api.calls)
            self.assertTrue((Path(directory) / "issuance.json").exists())
            self.assertTrue((Path(directory) / "issuance.json.pending").exists())


class RuntimeReceiptTests(unittest.TestCase):
    def test_wrong_revision_or_tampered_snapshot_refused_before_token_read(self):
        import hashlib
        import io

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            helper = root / "renderer-issuance.py"
            wrapper = root / "issue-renderer-secret-id.sh"
            helper.write_text("approved helper")
            wrapper.write_text("approved wrapper")
            helper.chmod(0o400)
            wrapper.chmod(0o500)
            receipt = root / "source-receipt.json"

            def write_receipt():
                receipt.chmod(0o600) if receipt.exists() else None
                receipt.write_text(
                    json.dumps(
                        {
                            "source_revision": REV,
                            "sha256": {
                                p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (helper, wrapper)
                            },
                        }
                    )
                )
                receipt.chmod(0o400)

            write_receipt()
            with patch.object(M, "__file__", str(helper)):
                M.validate_receipt(REV)
                stdin = io.StringIO("synthetic-issuer\nsynthetic-cleanup\n")
                args = ["server", "volume", M.IMAGE, "agent", directory, "b" * 40]
                with patch.object(M.sys, "stdin", stdin), self.assertRaises(M.Blocked):
                    M.main(args)
                self.assertEqual(0, stdin.tell())
                helper.chmod(0o600)
                helper.write_text("tampered helper")
                helper.chmod(0o400)
                with self.assertRaises(M.Blocked):
                    M.validate_receipt(REV)
                write_receipt()
                receipt.chmod(0o600)
                with self.assertRaises(M.Blocked):
                    M.validate_receipt(REV)
                receipt.unlink()
                receipt.symlink_to(wrapper)
                with self.assertRaises(M.Blocked):
                    M.validate_receipt(REV)


if __name__ == "__main__":
    unittest.main()
