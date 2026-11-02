"""Bounded Airflow _CMD credentials using synthetic private files only."""

from __future__ import annotations

import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "infra/07-workflow/airflow/connection_uri.py"


def load_helper():
    spec = importlib.util.spec_from_file_location("airflow_connection_uri", HELPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConnectionUriTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="p04-uri-")
        self.addCleanup(self.temporary.cleanup)
        self.secrets = Path(self.temporary.name)
        self.password = " p04-synthetic @:/?#%40+ 한글 "  # gitleaks:allow -- synthetic fixture; never deployed
        for name in (
            "airflow_db_password",
            "mng_valkey_password",
            "airflow_valkey_password",
        ):
            self.write_secret(name, self.password.encode())

    def write_secret(self, name, value):
        path = self.secrets / name
        path.write_bytes(value)
        path.chmod(0o600)
        return path

    def test_special_credentials_round_trip_without_double_decoding(self):
        module = load_helper()
        original = {"POSTGRES_PORT": "55432", "VALKEY_PORT": "16379"}
        for mode, host, port, scheme in (
            ("metadata", "mng-pg", 55432, "postgresql+psycopg2"),
            ("result", "mng-pg", 55432, "db+postgresql+psycopg2"),
            ("broker", "mng-valkey", 16379, "redis"),
        ):
            with self.subTest(mode=mode):
                result = module.render(mode, original, secrets_dir=self.secrets)
                parsed = urlsplit(result)
                self.assertEqual(
                    (scheme, host, port), (parsed.scheme, parsed.hostname, parsed.port)
                )
                self.assertEqual(self.password, unquote(parsed.password))
                self.assertIn("%2540", result)
                self.assertEqual("", parsed.query)
                self.assertEqual("", parsed.fragment)
        self.assertEqual({"POSTGRES_PORT": "55432", "VALKEY_PORT": "16379"}, original)

    def test_optional_single_terminal_lf_is_framing_and_spaces_survive(self):
        module = load_helper()
        self.write_secret("airflow_db_password", (self.password + "\n").encode())
        parsed = urlsplit(module.render("metadata", {}, secrets_dir=self.secrets))
        self.assertEqual(self.password, unquote(parsed.password))
        self.assertEqual(5432, parsed.port)

    def test_dedicated_broker_selects_matching_secret_and_port(self):
        module = load_helper()
        dedicated = "p04-dedicated-synthetic"
        self.write_secret("airflow_valkey_password", dedicated.encode())
        result = module.render(
            "broker",
            {
                "AIRFLOW_VALKEY_HOST": "airflow-valkey",
                "AIRFLOW_VALKEY_SECRET": "airflow_valkey_password",
                "VALKEY_PORT": "16380",
            },
            secrets_dir=self.secrets,
        )
        parsed = urlsplit(result)
        self.assertEqual(
            ("airflow-valkey", 16380, "/0"), (parsed.hostname, parsed.port, parsed.path)
        )
        self.assertEqual(dedicated, unquote(parsed.password))

    def test_database_preserves_literal_carriage_return_and_tab(self):
        module = load_helper()
        value = " p04\tvalue\r "
        self.write_secret("airflow_db_password", value.encode())
        result = module.render("metadata", {}, secrets_dir=self.secrets)
        self.assertEqual(value, unquote(urlsplit(result).password))

    def test_broker_rejects_existing_acl_control_characters(self):
        module = load_helper()
        for character in ("\r", "\t", "\x01", "\x1f", "\x7f"):
            with self.subTest(code=ord(character)):
                self.write_secret("mng_valkey_password", ("p04" + character).encode())
                with self.assertRaises(module.ConnectionError):
                    module.render("broker", {}, secrets_dir=self.secrets)

    def test_invalid_secret_bytes_fail_without_value_in_error(self):
        module = load_helper()
        for value in (
            b"",
            b"\n",
            b"p04\ninside",
            b"p04\n\n",
            b"p04\0",
            b"\xff",
            b"x" * 4097,
        ):
            with self.subTest(size=len(value)):
                self.write_secret("airflow_db_password", value)
                with self.assertRaises(module.ConnectionError) as failure:
                    module.render("metadata", {}, secrets_dir=self.secrets)
                self.assertEqual(module.ERROR, str(failure.exception))
                self.assertIsNone(failure.exception.__cause__)
                self.assertIsNone(failure.exception.__context__)

    def test_maximum_size_and_nonascii_singleline_are_supported(self):
        module = load_helper()
        for value in (b"x" * 4096, ("한글+%40" + "\n").encode()):
            self.write_secret("airflow_db_password", value)
            result = module.render("metadata", {}, secrets_dir=self.secrets)
            self.assertEqual(
                value.removesuffix(b"\n").decode(), unquote(urlsplit(result).password)
            )

    def test_invalid_ports_are_rejected_before_secret_read(self):
        module = load_helper()
        for key, mode in (("POSTGRES_PORT", "metadata"), ("VALKEY_PORT", "broker")):
            for port in (
                "",
                "0",
                "65536",
                "-1",
                "+1",
                "1.0",
                " 5432",
                "123456",
                "１２",
                None,
                5432,
            ):
                with self.subTest(key=key, value=port):
                    with patch.object(
                        module,
                        "_read_secret",
                        side_effect=AssertionError("must not read"),
                    ):
                        with self.assertRaises(module.ConnectionError):
                            module.render(mode, {key: port}, secrets_dir=self.secrets)

    def test_port_range_edges_and_dev_variables_do_not_change_metadata(self):
        module = load_helper()
        for port in ("1", "65535"):
            result = module.render(
                "metadata",
                {
                    "POSTGRES_PORT": port,
                    "DEV_PG_HOST_PORT": "25433",
                    "DEV_PG_PORT": "1234",
                },
                secrets_dir=self.secrets,
            )
            parsed = urlsplit(result)
            self.assertEqual(
                ("mng-pg", int(port), "/airflow"),
                (parsed.hostname, parsed.port, parsed.path),
            )

    def test_invalid_mode_and_broker_pair_do_not_read_a_secret(self):
        module = load_helper()
        invalid = (
            ("unknown", {}),
            ("broker", {"AIRFLOW_VALKEY_HOST": "airflow-valkey"}),
            ("broker", {"AIRFLOW_VALKEY_SECRET": "airflow_valkey_password"}),
            ("broker", {"AIRFLOW_VALKEY_HOST": "localhost"}),
            ("broker", {"AIRFLOW_VALKEY_SECRET": "../../private"}),
        )
        for mode, environment in invalid:
            with patch.object(
                module, "_read_secret", side_effect=AssertionError("must not read")
            ):
                with self.assertRaises(module.ConnectionError):
                    module.render(mode, environment, secrets_dir=self.secrets)

    def test_nonmapping_environment_has_only_a_value_free_error(self):
        module = load_helper()
        for environment in (None, [], "p04-synthetic-private-value"):
            with self.assertRaises(module.ConnectionError) as failure:
                module.render("metadata", environment, secrets_dir=self.secrets)
            self.assertEqual(module.ERROR, str(failure.exception))
            self.assertIsNone(failure.exception.__context__)

    def test_unsafe_secret_permissions_are_refused(self):
        module = load_helper()
        path = self.secrets / "airflow_db_password"
        for mode in (0o000, 0o644, 0o660, 0o666, 0o777):
            with self.subTest(mode=oct(mode)):
                path.chmod(mode)
                with self.assertRaises(module.ConnectionError):
                    module.render("metadata", {}, secrets_dir=self.secrets)

    def test_protected_owner_and_shared_group_read_modes_work(self):
        module = load_helper()
        path = self.secrets / "airflow_db_password"
        for mode in (0o400, 0o600, 0o440, 0o640):
            path.chmod(mode)
            self.assertEqual(
                self.password,
                unquote(
                    urlsplit(
                        module.render("metadata", {}, secrets_dir=self.secrets)
                    ).password
                ),
            )

    def test_untrusted_owner_without_readable_group_is_rejected(self):
        module = load_helper()
        with patch.object(module.os, "geteuid", return_value=987654):
            with self.assertRaises(module.ConnectionError):
                module.render("metadata", {}, secrets_dir=self.secrets)

    def test_shared_group_allows_a_protected_file_from_another_owner(self):
        module = load_helper()
        path = self.secrets / "airflow_db_password"
        path.chmod(0o640)
        with patch.object(module.os, "geteuid", return_value=987654):
            result = module.render("metadata", {}, secrets_dir=self.secrets)
        self.assertEqual(self.password, unquote(urlsplit(result).password))

    def test_symlink_hardlink_and_nonregular_input_are_rejected(self):
        module = load_helper()
        path = self.secrets / "airflow_db_password"
        original = path.read_bytes()
        path.unlink()
        path.symlink_to(self.secrets / "mng_valkey_password")
        with self.assertRaises(module.ConnectionError):
            module.render("metadata", {}, secrets_dir=self.secrets)
        path.unlink()
        os.link(self.secrets / "mng_valkey_password", path)
        with self.assertRaises(module.ConnectionError):
            module.render("metadata", {}, secrets_dir=self.secrets)
        path.unlink()
        path.mkdir()
        with self.assertRaises(module.ConnectionError):
            module.render("metadata", {}, secrets_dir=self.secrets)
        path.rmdir()
        os.mkfifo(path, 0o600)
        with self.assertRaises(module.ConnectionError):
            module.render("metadata", {}, secrets_dir=self.secrets)
        path.unlink()
        self.write_secret(path.name, original)

    def test_missing_file_symlink_parent_and_relative_root_are_rejected(self):
        module = load_helper()
        link = self.secrets / "linked"
        link.symlink_to(self.secrets, target_is_directory=True)
        for directory in (link, Path("relative-secrets")):
            with self.assertRaises(module.ConnectionError):
                module.render("metadata", {}, secrets_dir=directory)
        (self.secrets / "airflow_db_password").unlink()
        with self.assertRaises(module.ConnectionError):
            module.render("metadata", {}, secrets_dir=self.secrets)

    def test_group_writable_secret_directory_is_rejected(self):
        module = load_helper()
        self.secrets.chmod(0o770)
        with self.assertRaises(module.ConnectionError):
            module.render("metadata", {}, secrets_dir=self.secrets)

    def test_read_denial_and_interruption_are_redacted(self):
        module = load_helper()
        for failure in (
            PermissionError("sensitive fixture detail"),
            InterruptedError("private fixture detail"),
        ):
            with patch.object(module.os, "read", side_effect=failure):
                with self.assertRaises(module.ConnectionError) as raised:
                    module.render("metadata", {}, secrets_dir=self.secrets)
                self.assertEqual(module.ERROR, str(raised.exception))

    def test_modification_during_read_is_rejected(self):
        module = load_helper()
        read = os.read
        path = self.secrets / "airflow_db_password"

        def changed_read(descriptor, limit):
            chunk = read(descriptor, limit)
            path.write_bytes(b"p04-raced-different-value")
            return chunk

        with patch.object(module.os, "read", side_effect=changed_read):
            with self.assertRaises(module.ConnectionError):
                module.render("metadata", {}, secrets_dir=self.secrets)

    def test_atomic_replacement_during_read_is_rejected(self):
        module = load_helper()
        read = os.read
        path = self.secrets / "airflow_db_password"
        changed = False

        def replaced_read(descriptor, limit):
            nonlocal changed
            chunk = read(descriptor, limit)
            if not changed:
                changed = True
                replacement = self.write_secret("replacement", self.password.encode())
                replacement.replace(path)
            return chunk

        with patch.object(module.os, "read", side_effect=replaced_read):
            with self.assertRaises(module.ConnectionError):
                module.render("metadata", {}, secrets_dir=self.secrets)

    def test_cli_trusted_pipe_success_and_failure_have_no_extra_output(self):
        module = load_helper()
        output, errors = io.StringIO(), io.StringIO()
        status = module.main(
            ["broker"],
            environment={},
            secrets_dir=self.secrets,
            stdout=output,
            stderr=errors,
        )
        self.assertEqual(0, status)
        self.assertEqual(self.password, unquote(urlsplit(output.getvalue()).password))
        self.assertEqual("", errors.getvalue())
        self.assertNotIn("\n", output.getvalue())
        for arguments in ([], ["metadata", "p04-extra"], ["not-a-mode"]):
            output, errors = io.StringIO(), io.StringIO()
            self.assertEqual(
                1,
                module.main(
                    arguments,
                    environment={},
                    secrets_dir=self.secrets,
                    stdout=output,
                    stderr=errors,
                ),
            )
            self.assertEqual("", output.getvalue())
            self.assertEqual(module.ERROR + "\n", errors.getvalue())

    def test_cli_output_failure_and_cancellation_are_value_free(self):
        module = load_helper()

        class FailedPipe:
            def write(self, _value):
                raise BrokenPipeError("p04 synthetic private output detail")

        errors = io.StringIO()
        self.assertEqual(
            1,
            module.main(
                ["metadata"],
                environment={},
                secrets_dir=self.secrets,
                stdout=FailedPipe(),
                stderr=errors,
            ),
        )
        self.assertEqual(module.ERROR + "\n", errors.getvalue())
        with patch.object(module, "render", side_effect=KeyboardInterrupt):
            errors = io.StringIO()
            self.assertEqual(
                1, module.main(["metadata"], stdout=io.StringIO(), stderr=errors)
            )
            self.assertEqual(module.ERROR + "\n", errors.getvalue())
        self.assertEqual(1, module.main([], stdout=io.StringIO(), stderr=FailedPipe()))

    def test_cli_bad_arguments_in_a_fresh_process_are_redacted(self):
        result = subprocess.run(
            [sys.executable, str(HELPER), "metadata", "p04-private-looking-argument"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        self.assertEqual(1, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertEqual("Airflow connection: invalid input\n", result.stderr)

    def test_real_closed_stdout_pipe_has_fixed_error_and_exit_one(self):
        child = """import importlib.util, pathlib, sys
spec = importlib.util.spec_from_file_location('p04_uri_child', sys.argv[1])
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
raise SystemExit(helper.main(['metadata'], environment={}, secrets_dir=pathlib.Path(sys.argv[2])))
"""
        read_end, write_end = os.pipe()
        os.close(read_end)
        try:
            result = subprocess.run(
                [sys.executable, "-c", child, str(HELPER), str(self.secrets)],
                stdout=write_end,
                stderr=subprocess.PIPE,
                check=False,
                timeout=5,
            )
        finally:
            os.close(write_end)
        self.assertEqual(1, result.returncode)
        self.assertEqual(b"Airflow connection: invalid input\n", result.stderr)


if __name__ == "__main__":
    unittest.main()
