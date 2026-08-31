"""Lifecycle contract, provenance, and safety tests."""

from __future__ import annotations

import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

from scripts.lib.document_governance.lifecycle import contract as contract_module
from tests.validation.lifecycle._support import ROOT, SCRIPT, lifecycle, run


class SharedProvenanceTests(unittest.TestCase):
    def test_nested_cli_preserves_only_valid_same_root_descriptor(self) -> None:
        descriptor = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY)
        try:
            override = f"/proc/self/fd/{descriptor}"
            with mock.patch.dict(os.environ, {"HYHOME_CI_GATE_ROOT": override}):
                result = run(sys.executable, str(SCRIPT), "--help", cwd=ROOT)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("--mode", result.stdout)
                unrelated = run(
                    sys.executable,
                    "-c",
                    "import os; print(os.path.isdir(os.environ['HYHOME_CI_GATE_ROOT']))",
                    cwd=ROOT,
                )
                self.assertEqual("False\n", unrelated.stdout)
                self.assertEqual(override, os.environ["HYHOME_CI_GATE_ROOT"])
        finally:
            os.close(descriptor)

        with tempfile.TemporaryDirectory() as directory:
            other_root = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
            try:
                closed = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY)
                os.close(closed)
                for override in (
                    str(ROOT),
                    f"/proc/self/fd/{closed}",
                    f"/proc/self/fd/{other_root}",
                ):
                    with self.subTest(override=override), mock.patch.dict(
                        os.environ,
                        {"HYHOME_CI_GATE_ROOT": override},
                    ):
                        result = run(
                            sys.executable,
                            str(SCRIPT),
                            "--help",
                            cwd=ROOT,
                        )
                    self.assertEqual(1, result.returncode)
                    self.assertIn(
                        "FAIL: invalid HYHOME_CI_GATE_ROOT",
                        result.stderr,
                    )
            finally:
                os.close(other_root)

    def test_regular_reader_rejects_oversized_and_symlink_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "evidence.md"
            target.write_bytes(b"x" * (4 * 1024 * 1024 + 1))
            self.assertIsNone(
                lifecycle._read_regular_repo_bytes(
                    root,
                    "evidence.md",
                    require_tracked=False,
                )
            )
            link = root / "link.md"
            link.symlink_to(target)
            self.assertIsNone(
                lifecycle._read_regular_repo_bytes(
                    root,
                    "link.md",
                    require_tracked=False,
                )
            )

    def test_lifecycle_uses_shared_git_provenance(self) -> None:
        entrypoint = SCRIPT.read_text(encoding="utf-8")
        contract = (
            ROOT
            / "scripts/lib/document_governance/lifecycle/contract.py"
        ).read_text(encoding="utf-8")
        self.assertIn("scripts.lib.document_governance.git_provenance", contract)
        self.assertNotIn("METADATA_SCRIPT", entrypoint)
        self.assertNotIn(
            'spec_from_file_location(\n        "document_metadata',
            entrypoint,
        )
