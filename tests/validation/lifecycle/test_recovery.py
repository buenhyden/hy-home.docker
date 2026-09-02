"""Minimal archive-recovery tests."""

from __future__ import annotations

import pathlib
import tempfile
import unittest

from scripts.lib.document_governance.git_provenance import HistoricalDocument
from scripts.lib.document_governance.lifecycle import recovery as recovery_module
from tests.validation.lifecycle._support import commit_all, init_repo


class HistoricalDocumentRecoveryTests(unittest.TestCase):
    def test_recovery_reads_only_the_committed_regular_blob(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            document = root / "docs/current.md"
            document.parent.mkdir(parents=True)
            document.write_text("current recovery body\n", encoding="utf-8")
            link = root / "docs/link.md"
            link.symlink_to("current.md")
            commit = commit_all(root, "recovery objects")
            document.unlink()
            link.unlink()

            recovered = HistoricalDocument(root, commit, "docs/current.md")
            self.assertEqual("current recovery body\n", recovered.read_text())

            for path in ("docs", "docs/missing.md", "docs/link.md"):
                with self.subTest(path=path), self.assertRaisesRegex(
                    ValueError,
                    "regular blob",
                ):
                    HistoricalDocument(root, commit, path).read_bytes()
