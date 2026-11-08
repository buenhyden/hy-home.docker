"""Synthetic-only tests for the protected structure comparison CLI."""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.lib.ops import secret_structure as subject

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "scripts/operations/secret-structure.py"
PUBLIC_REGISTRY = (
    "# title\n\n"
    "| ID | Auto | Kind | Value | Env | Path | Date | Purpose |\n"
    "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
    "| **T-001** | X | PW | public | KEY | - | 2026 | test |\n"
    "\n| Retired ID | Canonical ID |\n| --- | --- |\n"
    "| COMM-003 | COMM-002 |\n"
)


def prepare(root):
    (root / "secrets").mkdir()
    (root / ".env.example").write_text(
        '# section\nKEY="example" # note\n', encoding="utf-8"
    )
    (root / ".env").write_text(
        '# section\nKEY="synthetic-private" # note\n', encoding="utf-8"
    )
    (root / ".env").chmod(0o600)
    (root / "secrets/SENSITIVE_ENV_VARS.md.example").write_text(
        PUBLIC_REGISTRY, encoding="utf-8"
    )
    registry = root / "secrets/SENSITIVE_ENV_VARS.md"
    registry.write_text(
        PUBLIC_REGISTRY.replace(" | public | ", " | synthetic-private | "),
        encoding="utf-8",
    )
    registry.chmod(0o600)


def invoke(root, command="check", *, read=True):
    args = [sys.executable, str(CLI), "--root", str(root), command]
    if read:
        args.append("--read-private")
    return subprocess.run(args, capture_output=True, text=True, check=False, timeout=10)


class StructureCliTests(unittest.TestCase):
    def test_explicit_private_read_compares_values_without_disclosing_them(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            completed = invoke(root)
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(json.loads(completed.stdout)["result"], "MATCH")
            self.assertNotIn("synthetic-private", completed.stdout + completed.stderr)

    def test_explicit_flag_is_required_before_any_private_read(self):
        with tempfile.TemporaryDirectory() as directory:
            completed = invoke(Path(directory), read=False)
            self.assertEqual(completed.returncode, 2)
            self.assertNotIn("MATCH", completed.stdout)

    def test_argparse_errors_never_reflect_untrusted_input_or_open_private(self):
        canary = "synthetic-private-canary"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            cases = (
                ["--root", str(root), "check", "--read-private", "--" + canary],
                ["--root", str(root), canary],
                ["--root", str(root), "check", canary],
                ["--root", canary],
                [canary],
            )
            for args in cases:
                with self.subTest(kind=len(args)):
                    result = subprocess.run(
                        [sys.executable, str(CLI), *args],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=10,
                    )
                    self.assertEqual(result.returncode, 2)
                    self.assertNotIn(canary, result.stdout + result.stderr)
                    self.assertNotIn("synthetic-private", result.stdout + result.stderr)
            with mock.patch.object(
                subject, "compare", side_effect=AssertionError("opened")
            ):
                with mock.patch("sys.stderr", io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        subject.main(["--root", str(root), "check", "--" + canary])
                    self.assertEqual(raised.exception.code, 2)

    def test_structure_drift_is_reported_without_private_text(self):
        mutations = (
            ("# section", "# private-canary"),
            ("KEY=", "OTHER="),
            ("# note", "# private-canary"),
        )
        for before, after in mutations:
            with self.subTest(kind=before), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                prepare(root)
                path = root / ".env"
                path.write_text(path.read_text().replace(before, after))
                completed = invoke(root)
                self.assertEqual(completed.returncode, 1)
                self.assertEqual(json.loads(completed.stdout)["env"], "DRIFT")
                self.assertNotIn("private-canary", completed.stdout + completed.stderr)
                self.assertNotIn(
                    "synthetic-private", completed.stdout + completed.stderr
                )

    def test_registry_layout_and_consumer_are_compared(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            path = root / "secrets/SENSITIVE_ENV_VARS.md"
            path.write_text(path.read_text().replace("| test |", "| private-canary |"))
            result = invoke(root)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["registry"], "DRIFT")
            self.assertNotIn("private-canary", result.stdout + result.stderr)

    def test_value_free_diagnostics_reference_only_public_structure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            env = root / ".env"
            env.write_text(
                '# section\nPRIVATE_KEY="synthetic-private" # private-comment\n'
            )
            registry = root / "secrets/SENSITIVE_ENV_VARS.md"
            registry.write_text(registry.read_text().replace("T-001", "PRIVATE-999"))
            result = invoke(root)
            self.assertEqual(result.returncode, 1)
            response = json.loads(result.stdout)
            self.assertEqual(
                response["details"]["env"],
                {"reason": "PUBLIC_ASSIGNMENT", "public_line": 2},
            )
            self.assertEqual(
                response["details"]["registry"],
                {"reason": "PUBLIC_ROW", "public_line": 5},
            )
            for canary in (
                "PRIVATE_KEY",
                "PRIVATE-999",
                "private-comment",
                "synthetic-private",
            ):
                self.assertNotIn(canary, result.stdout + result.stderr)

    def test_private_extra_diagnostic_has_no_private_position_or_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            env = root / ".env"
            with env.open("a") as stream:
                stream.write("PRIVATE_KEY=synthetic-private\n")
            result = invoke(root)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(
                json.loads(result.stdout)["details"]["env"], {"reason": "PRIVATE_EXTRA"}
            )
            self.assertNotIn("PRIVATE_KEY", result.stdout + result.stderr)
            self.assertNotIn("synthetic-private", result.stdout + result.stderr)

    def test_missing_private_and_bad_permissions_are_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            (root / ".env").unlink()
            self.assertEqual(invoke(root).returncode, 2)
            (root / ".env").write_text("KEY=x\n")
            (root / ".env").chmod(0o644)
            self.assertEqual(invoke(root).returncode, 2)

    def test_fifo_symlink_hardlink_and_oversize_are_blocked(self):
        for kind in ("fifo", "symlink", "hardlink", "oversize"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                prepare(root)
                target = root / ".env"
                if kind == "oversize":
                    target.write_bytes(b"x" * (subject.MAX_BYTES + 1))
                else:
                    target.unlink()
                    if kind == "fifo":
                        os.mkfifo(target, 0o600)
                    elif kind == "symlink":
                        target.symlink_to(root / ".env.example")
                    else:
                        os.link(root / ".env.example", target)
                self.assertEqual(invoke(root).returncode, 2)

    def test_smtp_equality_and_absent_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical = root / "secrets/communication/smtp/smtp_password.txt"
            canonical.parent.mkdir(parents=True)
            canonical.write_bytes(b"synthetic-secret")
            canonical.chmod(0o640)
            absent = invoke(root, "smtp-equality")
            self.assertEqual(absent.returncode, 2)
            self.assertEqual(
                json.loads(absent.stdout),
                {
                    "result": "OLD_ABSENT",
                    "comparison_performed": False,
                },
            )
            old = root / "secrets/communication/supabase/supabase_smtp_password.txt"
            old.parent.mkdir()
            old.write_bytes(b"synthetic-secret")
            old.chmod(0o600)
            equal = invoke(root, "smtp-equality")
            self.assertEqual(equal.returncode, 0)
            self.assertEqual(json.loads(equal.stdout)["result"], "EQUAL")
            old.write_bytes(b"synthetic-other")
            different = invoke(root, "smtp-equality")
            self.assertEqual(different.returncode, 1)
            self.assertEqual(json.loads(different.stdout)["result"], "DIFFERENT")
            old.write_bytes(b"")
            empty = invoke(root, "smtp-equality")
            self.assertEqual(empty.returncode, 2)
            self.assertEqual(json.loads(empty.stdout)["result"], "BLOCKED")
            self.assertNotIn(
                "synthetic-", absent.stdout + equal.stdout + different.stdout
            )


class ProjectionTests(unittest.TestCase):
    def test_repository_public_examples_parse(self):
        # The public registry lists every retired alias (LAB moves added five).
        subject.env_structure((ROOT / ".env.example").read_bytes())
        registry = (ROOT / "secrets/SENSITIVE_ENV_VARS.md.example").read_bytes()
        self.assertIn(b"| COMM-006 | LAB-036 |", registry)
        subject.registry_structure(registry)

    def test_alias_rows_need_two_identifiers_and_stay_unique(self):
        table = PUBLIC_REGISTRY.replace(
            "| COMM-003 | COMM-002 |\n",
            "| COMM-003 | COMM-002 |\n| AI-007 | LAB-034 |\n",
        )
        subject.registry_structure(table.encode())
        for bad in ("| AI-007 | lab |\n", "| AI-007 | LAB-034 |\n"):
            with self.subTest(row=bad), self.assertRaises(subject.UnsafeInput):
                subject.registry_structure((table + bad).encode())

    def test_unicode_special_characters_and_comments(self):
        one = 'A="한글 %40 # text" # note\nB=alpha#literal\nC=  # kept\n'
        two = 'A="다른 \\" quoted" # note\nB=beta#literal\nC=  # kept\n'
        self.assertEqual(
            subject.env_structure(one.encode()), subject.env_structure(two.encode())
        )
        changed = two.replace("# kept", "# changed")
        self.assertNotEqual(
            subject.env_structure(one.encode()), subject.env_structure(changed.encode())
        )
        self.assertEqual(
            subject.env_structure(b"KEY= # note\n"),
            subject.env_structure(b"KEY=synthetic # note\n"),
        )
        self.assertEqual(
            subject.env_structure(b"A=one\r\n"), subject.env_structure(b"A=two\r\n")
        )
        self.assertNotEqual(
            subject.env_structure(b"A=one\r\n"), subject.env_structure(b"A=two\n")
        )

    def test_values_only_registry_changes_do_not_change_structure(self):
        private = PUBLIC_REGISTRY.replace(" | public | ", " | private value | ")
        self.assertEqual(
            subject.registry_structure(PUBLIC_REGISTRY.encode()),
            subject.registry_structure(private.encode()),
        )

    def test_duplicate_and_ambiguous_inputs_are_rejected(self):
        invalid_env = (
            b"",
            b"# no assignments\n",
            b"A=1\nA=2\n",
            b'A="unterminated\n',
            b"A=x\\\n",
            b'A="x" unexpected\n',
            b"A=zero\x00\n",
            b"A=\xff\n",
            b"A=1\r",
        )
        for value in invalid_env:
            with (
                self.subTest(kind=repr(value)),
                self.assertRaises((subject.UnsafeInput, UnicodeError)),
            ):
                subject.env_structure(value)
        duplicate = PUBLIC_REGISTRY + "| **T-001** | X | PW | q | K | - | d | p |\n"
        invalid_tables = (
            "# no rows\n",
            duplicate,
            "| T-001 | x | malformed |\n",
            "| COMM-003 | INVALID |\n",
            "| bad | x | x | x | x | x | x | x |\n",
        )
        for value in invalid_tables:
            with self.subTest(kind=value), self.assertRaises(subject.UnsafeInput):
                subject.registry_structure(value.encode())

    def test_bad_root_is_closed_and_no_descriptors_leak(self):
        with self.assertRaises(subject.UnsafeInput):
            subject.HeldInputs("relative")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            link = root.parent / (root.name + "-link")
            link.symlink_to(root)
            try:
                with self.assertRaises(OSError):
                    subject.HeldInputs(link)
            finally:
                link.unlink()

    def test_changed_file_and_parent_are_rejected(self):
        for changed in ("file", "parent", "growth"):
            with self.subTest(kind=changed), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                prepare(root)
                with subject.HeldInputs(root) as inputs:
                    inputs.open("secrets/SENSITIVE_ENV_VARS.md", private=True)
                    if changed == "file":
                        path = root / "secrets/SENSITIVE_ENV_VARS.md"
                        path.rename(path.with_suffix(".old"))
                        path.write_text("new")
                    elif changed == "parent":
                        (root / "secrets").rename(root / "old-secrets")
                        (root / "secrets").mkdir()
                    else:
                        with (root / "secrets/SENSITIVE_ENV_VARS.md").open(
                            "a"
                        ) as stream:
                            stream.write("new")
                    with self.assertRaises(subject.UnsafeInput):
                        inputs.verify()

    def test_absent_history_reappearing_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "secrets").mkdir()
            with subject.HeldInputs(root) as inputs:
                self.assertIsNone(
                    inputs.open("secrets/missing/file", private=True, optional=True)
                )
                (root / "secrets/missing").mkdir()
                with self.assertRaises(subject.UnsafeInput):
                    inputs.verify()

    def test_absent_smtp_history_does_not_read_canonical_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical = root / "secrets/communication/smtp/smtp_password.txt"
            canonical.parent.mkdir(parents=True)
            canonical.write_bytes(b"synthetic-secret")
            canonical.chmod(0o640)
            with mock.patch.object(
                subject.os, "read", side_effect=AssertionError("unexpected read")
            ):
                code, result = subject.smtp_equality(root)
            self.assertEqual(code, 2)
            self.assertEqual(
                result, {"result": "OLD_ABSENT", "comparison_performed": False}
            )

    def test_size_growth_while_reading_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            original = os.read
            changed = False

            def read_then_change(fd, size):
                nonlocal changed
                data = original(fd, size)
                if not changed and data:
                    changed = True
                    with (root / ".env").open("ab") as stream:
                        stream.write(b"extra")
                return data

            with mock.patch.object(subject.os, "read", side_effect=read_then_change):
                with subject.HeldInputs(root) as inputs:
                    with self.assertRaises(subject.UnsafeInput):
                        inputs.open(".env", private=True)

    def test_in_process_comparison_and_closed_main_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            self.assertEqual(subject.compare(root)[0], 0)
            path = root / ".env"
            path.write_text(path.read_text().replace("# note", "# changed"))
            self.assertEqual(subject.compare(root)[0], 1)
            out = io.StringIO()
            with mock.patch("sys.stdout", out):
                self.assertEqual(
                    subject.main(["--root", str(root), "check", "--read-private"]), 1
                )
            self.assertNotIn("synthetic-private", out.getvalue())
            path.unlink()
            out = io.StringIO()
            with mock.patch("sys.stdout", out):
                self.assertEqual(
                    subject.main(["--root", str(root), "check", "--read-private"]), 2
                )
            self.assertEqual(json.loads(out.getvalue()), {"result": "BLOCKED"})

    def test_output_failure_cannot_report_success_or_modify_inputs(self):
        class UnwritableOutput:
            def write(self, _value):
                raise OSError("synthetic-output-failure")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            paths = (root / ".env", root / "secrets/SENSITIVE_ENV_VARS.md")
            before = [(path.read_bytes(), path.stat().st_mode) for path in paths]
            with mock.patch("sys.stdout", UnwritableOutput()):
                with self.assertRaises(OSError):
                    subject.main(["--root", str(root), "check", "--read-private"])
            self.assertEqual(
                before, [(path.read_bytes(), path.stat().st_mode) for path in paths]
            )

    def test_public_reference_kinds_and_missing_public_line(self):
        self.assertEqual(
            subject._first_difference("A=one\n# title\n", "A=one\n", "env"),
            {"reason": "PUBLIC_MISSING", "public_line": 2},
        )
        self.assertEqual(
            subject._first_difference("# title\n", "# other\n", "env"),
            {"reason": "PUBLIC_COMMENT", "public_line": 1},
        )
        self.assertEqual(
            subject._first_difference("\n", "# hidden\n", "env"),
            {"reason": "PUBLIC_LAYOUT", "public_line": 1},
        )
        self.assertEqual(
            subject._first_difference("| ID | Value |\n", "private\n", "registry"),
            {"reason": "PUBLIC_TABLE", "public_line": 1},
        )
        self.assertEqual(
            subject._first_difference("heading\n", "private\n", "registry"),
            {"reason": "PUBLIC_TEXT", "public_line": 1},
        )

    def test_in_process_smtp_equal_different_and_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            one = root / "secrets/communication/smtp/smtp_password.txt"
            two = root / "secrets/communication/supabase/supabase_smtp_password.txt"
            one.parent.mkdir(parents=True)
            two.parent.mkdir()
            one.write_bytes(b"synthetic-a")
            two.write_bytes(b"synthetic-a")
            one.chmod(0o640)
            two.chmod(0o600)
            self.assertEqual(subject.smtp_equality(root)[0], 0)
            two.write_bytes(b"synthetic-b")
            self.assertEqual(subject.smtp_equality(root)[0], 1)
            two.write_bytes(b"")
            with self.assertRaises(subject.UnsafeInput):
                subject.smtp_equality(root)
