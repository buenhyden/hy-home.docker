"""Tests for the retained promoted-evidence integrity check."""

from __future__ import annotations

import pathlib
import unittest
from unittest import mock

from scripts.lib.document_governance.lifecycle import promoted


ROOT = pathlib.Path(__file__).resolve().parents[4]


class HistoricalPromotedEvidenceTests(unittest.TestCase):
    def test_current_promoted_evidence_matches_its_recovery_blob(self) -> None:
        self.assertEqual([], promoted._historical_promoted_findings(ROOT))

    def test_missing_recovery_mapping_fails_closed(self) -> None:
        with mock.patch.object(
            promoted.archive_authority,
            "_migration_document",
            return_value={"rows": []},
        ):
            with self.assertRaises(promoted.ProfileError):
                promoted._historical_promoted_findings(ROOT)
