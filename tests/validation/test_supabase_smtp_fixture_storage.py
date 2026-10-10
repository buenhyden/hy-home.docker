"""Security regressions for the isolated SMTP fixture's local files."""

from __future__ import annotations

import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import ANY, patch

from tests.validation import _supabase_smtp_fixture_storage as storage
from tests.validation._supabase_smtp_fixture_storage import (
    PUBLIC_SYNTHETIC_DB_PASSWORD,
    PUBLIC_SYNTHETIC_JWT,
    PUBLIC_SYNTHETIC_SIGNUP_EMAILS,
    PUBLIC_SYNTHETIC_SIGNUP_PASSWORD,
    PUBLIC_SYNTHETIC_SMTP_PASSWORD,
    PUBLIC_SYNTHETIC_WRONG_SMTP_PASSWORD,
)
from tests.validation.test_supabase_smtp_rehearsal import SMTPFixture


class SMTPFixtureStorageTests(unittest.TestCase):
    def setUp(self):
        self.fixture = SMTPFixture()

    def tearDown(self):
        self.fixture.scratch.cleanup()

    def test_fixture_directory_is_private(self):
        mode = stat.S_IMODE(self.fixture.directory.stat().st_mode)
        self.assertEqual(0o700, mode)

    def test_non_private_fixture_directory_is_rejected(self):
        self.fixture.directory.chmod(0o755)
        with self.assertRaises(PermissionError):
            self.fixture.write("smtp-password", "public-synthetic-value")
        self.assertFalse((self.fixture.directory / "smtp-password").exists())

    def test_existing_file_is_not_replaced(self):
        path = self.fixture.write("smtp-password", "first\n")
        with self.assertRaises(FileExistsError):
            self.fixture.write("smtp-password", "second\n")
        self.assertEqual(b"first\n", path.read_bytes())

    def test_symlink_is_not_followed(self):
        with tempfile.TemporaryDirectory(prefix="smtp01-outside-") as outside:
            target = Path(outside) / "target"
            target.write_bytes(b"unchanged\n")
            (self.fixture.directory / "smtp-password").symlink_to(target)
            with self.assertRaises(FileExistsError):
                self.fixture.write("smtp-password", "replacement\n")
            self.assertEqual(b"unchanged\n", target.read_bytes())

    def test_traversal_and_non_basename_names_are_rejected(self):
        for name in ("../escape", "nested/file", ".", ""):
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.fixture.write(name, "public-synthetic-value")

    def test_invalid_content_and_modes_are_rejected(self):
        with self.assertRaises(TypeError):
            self.fixture.write("fixture", b"public-synthetic-value")
        for mode in (True, -1, 0o1000):
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.fixture.write("fixture", "public-synthetic-value", mode)

    def test_fixed_public_synthetic_credentials_and_exact_mode(self):
        self.assertEqual(PUBLIC_SYNTHETIC_SMTP_PASSWORD, self.fixture.smtp_password)
        self.assertEqual(PUBLIC_SYNTHETIC_DB_PASSWORD, self.fixture.db_password)
        self.assertEqual(PUBLIC_SYNTHETIC_JWT, self.fixture.jwt)
        path = self.fixture.write("mode-check", "public-synthetic-value", 0o640)
        self.assertEqual(b"public-synthetic-value", path.read_bytes())
        self.assertEqual(0o640, stat.S_IMODE(path.stat().st_mode))

    def test_restrictive_umask_does_not_change_final_mode(self):
        previous = os.umask(0o077)
        try:
            paths = {
                mode: self.fixture.write(
                    f"umask-{mode:o}", "public-synthetic-value", mode
                )
                for mode in (0o640, 0o644, 0o755)
            }
        finally:
            os.umask(previous)
        for mode, path in paths.items():
            with self.subTest(mode=oct(mode)):
                self.assertEqual(b"public-synthetic-value", path.read_bytes())
                self.assertEqual(mode, stat.S_IMODE(path.stat().st_mode))

    def test_creation_is_private_before_descriptor_sets_final_mode(self):
        with (
            patch.object(storage.os, "open", wraps=os.open) as open_call,
            patch.object(storage.os, "fchmod", wraps=os.fchmod) as chmod_call,
        ):
            self.fixture.write("mode-order", "public-synthetic-value", 0o644)
        leaf_call = next(call for call in open_call.call_args_list if call.kwargs)
        self.assertEqual(0o600, leaf_call.args[2])
        chmod_call.assert_called_once_with(ANY, 0o644)

    def test_signup_uses_bounded_public_synthetic_inputs(self):
        requests = []
        self.fixture.docker = lambda *args, **kwargs: subprocess.CompletedProcess(
            args, 0, stdout=b"t\n", stderr=b""
        )
        self.fixture.http = lambda url, payload: (
            requests.append((url, payload))
            or (
                200,
                False,
                0,
            )
        )
        self.fixture.signup("http://synthetic.invalid")
        self.assertEqual(
            [
                (
                    "http://synthetic.invalid/signup",
                    {
                        "email": PUBLIC_SYNTHETIC_SIGNUP_EMAILS[0],
                        "password": PUBLIC_SYNTHETIC_SIGNUP_PASSWORD,
                    },
                )
            ],
            requests,
        )

    def test_prepared_credential_files_have_exact_public_bytes(self):
        self.fixture.build_http_peer = lambda: None
        self.fixture.docker = lambda *args, **kwargs: subprocess.CompletedProcess(
            args, 0, stdout=b"", stderr=b""
        )
        self.fixture.certificates = lambda: None
        self.fixture._prepare_fixture_files()
        expected = {
            "smtp-password": (PUBLIC_SYNTHETIC_SMTP_PASSWORD + "\n").encode(),
            "wrong-password": (PUBLIC_SYNTHETIC_WRONG_SMTP_PASSWORD + "\n").encode(),
            "db-password": PUBLIC_SYNTHETIC_DB_PASSWORD.encode(),
            "smtp-auth": ("fixture:" + PUBLIC_SYNTHETIC_SMTP_PASSWORD + "\n").encode(),
        }
        for name, content in expected.items():
            with self.subTest(name=name):
                self.assertEqual(content, (self.fixture.directory / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
