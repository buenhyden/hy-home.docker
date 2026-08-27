from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import unittest

import yaml

from scripts.lib.document_governance.suite_registry import SuiteRegistryError, load


MANIFEST = Path("scripts/manifest.yaml")


class SuiteRegistryTests(unittest.TestCase):
    def test_public_suites_and_atomic_ownership_are_exact(self) -> None:
        registry = load(MANIFEST)
        self.assertEqual(
            registry.public_names,
            (
                "agent-governance",
                "document-contract",
                "document-graph",
                "document-lifecycle",
                "operations",
                "repository-integrity",
            ),
        )
        self.assertTrue(all(len(item.public_suites) == 1 for item in registry.validators))
        self.assertTrue(all(item.has_mirrored_test for item in registry.production_modules))

    def test_rejects_duplicate_behavioral_consumers_and_suite_ownership(self) -> None:
        document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        validator = next(row for row in document["files"] if row["kind"] == "validator")
        validator["public_suites"] = ["document-contract", "document-graph"]
        with self.assertRaisesRegex(SuiteRegistryError, "exactly one"):
            self._load(document)

        document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        duplicate = copy.deepcopy(
            next(row for row in document["files"] if row["kind"] == "validator")
        )
        duplicate["path"] = "scripts/lib/document_governance/duplicate.py"
        duplicate["kind"] = "library"
        duplicate.pop("public_suites")
        duplicate["consumers"] = ["scripts/validation/ci_gate_contract.py"] * 2
        document["files"].append(duplicate)
        with self.assertRaisesRegex(SuiteRegistryError, "duplicates"):
            self._load(document)

    def test_rejects_missing_mirrored_tests_and_suite_logic_rows(self) -> None:
        document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        module = next(
            row
            for row in document["files"]
            if row["path"] == "scripts/lib/document_governance/suite_registry.py"
        )
        module["tests"] = ["tests/validation/test_script_manifest.py"]
        with self.assertRaisesRegex(SuiteRegistryError, "mirrored library test"):
            self._load(document)

        module["public_suites"] = ["repository-integrity"]
        with self.assertRaisesRegex(SuiteRegistryError, "only validators"):
            self._load(document)

    def _load(self, document: dict[str, object]):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "manifest.yaml"
            manifest.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
            return load(manifest)
