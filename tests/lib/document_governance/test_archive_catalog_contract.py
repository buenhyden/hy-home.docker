"""The capture parser consumes the Registry table binding."""

import types
import unittest
from unittest import mock

from scripts.lib.document_governance import archive


class ArchiveCatalogContractTests(unittest.TestCase):
    def test_capture_heading_and_columns_are_registry_owned(self):
        registry = types.SimpleNamespace(
            common={
                "archive_retention": {
                    "capture_section": "Capture Records",
                    "capture_columns": ["Unit", "Disposition", "Owner", "Origin"],
                }
            }
        )
        text = "## Capture Records\n\n| Unit | Disposition | Owner | Origin |\n| --- | --- | --- | --- |\n| `completed/item.md` | completed | REQ-0026 | `source` |\n"
        with mock.patch.object(archive, "_catalog_registry", return_value=registry):
            rows, findings = archive._catalog_rows(text)
        self.assertEqual([], findings)
        self.assertEqual(1, len(rows))


class ArchiveDispositionRegistryTests(unittest.TestCase):
    def test_invalid_disposition_mapping_is_rejected_before_execution(self):
        import copy
        import json
        from pathlib import Path

        from scripts.lib.document_governance.registry import validate_registry

        raw = json.loads(
            (
                Path(__file__).resolve().parents[3] / "docs/99.templates/registry.json"
            ).read_text()
        )
        for mutation in ("missing", "missing-task", "unknown-status", "citation-order"):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(raw)
                contract = changed["common"]["archive_retention"]
                if mutation == "missing":
                    del contract["disposition_entry_statuses"]
                elif mutation == "missing-task":
                    del contract["disposition_entry_statuses"]["task"]
                elif mutation == "citation-order":
                    contract["citation_order"] = ["integrity", "assessment"]
                else:
                    contract["disposition_entry_statuses"]["task"] = ["invented"]
                self.assertTrue(validate_registry(changed))

    def test_archive_contract_rejects_unsupported_shapes(self):
        import copy
        import json
        from pathlib import Path

        from scripts.lib.document_governance.registry import validate_registry

        raw = json.loads(
            (
                Path(__file__).resolve().parents[3] / "docs/99.templates/registry.json"
            ).read_text()
        )
        mutations = {
            "capture_columns": ["Unit"],
            "assessment_columns": ["Unit"],
            "catalog_path": "/etc/passwd",
            "default_assessment": "invented",
            "default_availability": "purged",
            "blocked_assessments": ["invented"],
            "history_only_availability": "purged",
            "legacy_transition_units": ["../../outside"],
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                changed = copy.deepcopy(raw)
                changed["common"]["archive_retention"][field] = value
                self.assertTrue(validate_registry(changed))
